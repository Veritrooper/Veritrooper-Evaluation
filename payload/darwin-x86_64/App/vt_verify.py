"""
VERITROOPER - Package checker (client-facing, standalone)

Double-click this (or the built vt_verify.exe) to check a VERITROOPER audit package.
It tells a non-technical recipient, in plain language:
  * whether anything in the package was changed since it was sealed,
  * whether it was sealed by the key whose fingerprint is shown, and
  * (if a trusted date-stamp is present) that it existed by that time.

TRUST: a checker that ships INSIDE the package is a convenience, not proof of origin.
The proof of origin is the SIGNER FINGERPRINT printed below - you must compare it to the
ID VERITROOPER gave you SEPARATELY (pilot agreement, a signed email, or veritrooper.com).
If it matches, the package genuinely came from that signer. You can also re-check with a
clean copy of this tool from veritrooper.com, or with standard OpenSSL (see Integrity/VERIFY.txt).

Dependencies: Python standard library + `cryptography` only (no OpenSSL required for the
core checks). Freeze to a no-install .exe with:  pyinstaller --onefile vt_verify.py
"""

import os
import sys
import json
import glob
import hashlib
import shutil
import subprocess
import unicodedata


def _pause():
    try:
        input("\nPress Enter to close...")
    except (EOFError, KeyboardInterrupt):
        pass


try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.exceptions import InvalidSignature
except ImportError:
    print("This checker needs the 'cryptography' library (pip install cryptography),")
    print("or use the built vt_verify.exe which has it bundled.")
    _pause()
    sys.exit(3)

ENVELOPE_DIR = "Integrity"
_NOISE = {"thumbs.db", ".ds_store", "desktop.ini"}
GREEN, RED, YEL, DIM, OFF = "", "", "", "", ""   # plain text (frozen consoles vary); keep glyph-free


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _norm(root, path):
    rel = os.path.relpath(path, root)
    if os.path.isabs(rel) or rel.startswith(".."):
        return None
    return unicodedata.normalize("NFC", rel.replace(os.sep, "/"))


def _validated_manifest_files(root, entries):
    if not isinstance(entries, list):
        raise ValueError("manifest files must be an array")
    root_real = os.path.realpath(os.path.abspath(root))
    listed, seen = {}, set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError("every manifest file entry requires a string path")
        digest = entry.get("sha256")
        if (not isinstance(digest, str) or len(digest) != 64
                or any(c not in "0123456789abcdefABCDEF" for c in digest)):
            raise ValueError("every manifest file entry requires a valid SHA-256 digest")
        rel = entry["path"]
        parts = rel.split("/")
        if (not rel or "\\" in rel or os.path.isabs(rel)
                or any(part in ("", ".", "..") for part in parts)
                or parts[0].casefold() == ENVELOPE_DIR.casefold()
                or ":" in parts[0]):
            raise ValueError("illegal manifest path: %r" % rel)
        folded = rel.casefold()
        if folded in seen:
            raise ValueError("case-folding duplicate manifest path: %s" % rel)
        seen.add(folded)
        target = os.path.realpath(os.path.join(root_real, *parts))
        if os.path.commonpath([root_real, target]) != root_real:
            raise ValueError("manifest path escapes package root: %s" % rel)
        listed[rel] = entry
    return listed


def _payload_files(pkg):
    env = os.path.join(pkg, ENVELOPE_DIR)
    out = []
    for base, dirs, names in os.walk(pkg):
        for dirname in list(dirs):
            dp = os.path.join(base, dirname)
            is_junction = getattr(os.path, "isjunction", lambda _p: False)(dp)
            if os.path.islink(dp) or is_junction:
                raise ValueError("symlink/junction directory not allowed: %s" % dp)
            if os.path.commonpath([os.path.realpath(pkg), os.path.realpath(dp)]) != os.path.realpath(pkg):
                raise ValueError("directory resolves outside package: %s" % dp)
        if os.path.abspath(base) == os.path.abspath(pkg):
            dirs[:] = [d for d in dirs if d != ENVELOPE_DIR]
        if os.path.commonpath([os.path.abspath(base), os.path.abspath(env)]) == os.path.abspath(env):
            continue
        for n in names:
            fp = os.path.join(base, n)
            if (os.path.islink(fp)
                    or getattr(os.path, "isjunction", lambda _p: False)(fp)):
                raise ValueError("symlink/junction file not allowed: %s" % fp)
            rel = _norm(pkg, fp)
            if rel:
                out.append(rel)
    return set(out)


def _find_package():
    """Where's the package? An explicit arg wins; else if this tool sits in an Integrity/
    folder, the package is its parent; else if the current folder has an Integrity/, use it."""
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        return os.path.abspath(sys.argv[1])
    here = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    if os.path.basename(here) == ENVELOPE_DIR and os.path.isdir(os.path.join(os.path.dirname(here), ENVELOPE_DIR)):
        return os.path.dirname(here)
    for cand in (here, os.getcwd()):
        if os.path.isdir(os.path.join(cand, ENVELOPE_DIR)):
            return cand
    return None


def _fingerprint(cert):
    h = cert.fingerprint(hashes.SHA256()).hex().upper()
    return ":".join(h[i:i + 2] for i in range(0, len(h), 2))


def _external_tsa_ca(pkg):
    """An explicitly supplied trust anchor must exist outside the package it vouches for."""
    candidate = os.environ.get("VT_TRUSTED_TSA_CA", "")
    if not candidate or not os.path.isfile(candidate):
        return None
    pkg_real = os.path.realpath(pkg)
    ca_real = os.path.realpath(candidate)
    try:
        if os.path.commonpath([pkg_real, ca_real]) == pkg_real:
            return None
    except ValueError:
        pass
    return ca_real


def check(pkg):
    env = os.path.join(pkg, ENVELOPE_DIR)
    rows, ok = [], True

    def row(label, good, detail):
        nonlocal ok
        mark = "[ OK ]" if good else "[FAIL]"
        if good is None:
            mark = "[ -- ]"
        elif not good:
            ok = False
        rows.append(f"  {mark}  {label:<32} {detail}")

    mpath = os.path.join(env, "manifest.json")
    if not os.path.exists(mpath):
        return False, None, [f"  [FAIL]  Not a sealed VERITROOPER package (no {ENVELOPE_DIR}/manifest.json)."]
    with open(mpath, "rb") as f:
        mbytes = f.read()
    try:
        manifest = json.loads(mbytes)
        if not isinstance(manifest, dict):
            raise ValueError("manifest root must be an object")
    except (ValueError, TypeError) as e:
        row("Manifest validity", False, str(e))
        return False, None, rows
    try:
        listed = _validated_manifest_files(pkg, manifest.get("files"))
    except ValueError as e:
        row("Manifest validity", False, str(e))
        return False, None, rows
    row("Manifest validity", True, "valid JSON object and file schema")

    # 1) signer certificate + signature (raw ECDSA over the manifest bytes)
    fp = None
    cpath, spath = os.path.join(env, "signer_cert.pem"), os.path.join(env, "manifest.sig")
    if os.path.exists(cpath) and os.path.exists(spath):
        with open(cpath, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())
        fp = _fingerprint(cert)
        with open(spath, "rb") as f:
            sig = f.read()
        try:
            cert.public_key().verify(sig, mbytes, ec.ECDSA(hashes.SHA256()))
            row("Digital signature", True, "valid (manifest is authentic and unaltered)")
        except InvalidSignature:
            row("Digital signature", False, "INVALID - the seal does not match the contents")
    else:
        row("Digital signature", False, "missing signature or signer certificate")

    # 2) every listed file unchanged
    changed = [p for p, e in listed.items()
               if not os.path.exists(os.path.join(pkg, p.replace("/", os.sep)))
               or _sha256(os.path.join(pkg, p.replace("/", os.sep))) != e["sha256"]]
    row("Nothing was changed", not changed,
        f"all {len(listed)} files match the seal" if not changed
        else f"{len(changed)} file(s) altered or missing: {', '.join(changed[:4])}")

    # 3) no unexpected extra files
    try:
        extra = sorted(_payload_files(pkg) - set(listed))
    except ValueError as e:
        row("No unexpected files added", False, str(e))
        return False, fp, rows
    extra = [e for e in extra if os.path.basename(e).lower() not in _NOISE]
    row("No unexpected files added", not extra, "none" if not extra
        else f"{len(extra)} unlisted file(s): {', '.join(extra[:4])}")

    # 4) trusted date-stamp (optional; full check needs OpenSSL)
    tsr = os.path.join(env, "timestamp.tsr")
    if os.path.exists(tsr):
        external_ca = _external_tsa_ca(pkg)
        bundled_ca = next((os.path.join(env, n) for n in ("tsa_chain.pem",)
                           if os.path.exists(os.path.join(env, n))), None)
        ca = external_ca or bundled_ca
        if shutil.which("openssl") and ca:
            p = subprocess.run(["openssl", "ts", "-verify", "-data", mpath, "-in", tsr, "-CAfile", ca],
                               capture_output=True, text=True)
            if external_ca:
                row("Trusted date-stamp", p.returncode == 0,
                    "verified against the externally supplied trust anchor" if p.returncode == 0
                    else "present but did not verify against the external trust anchor")
            else:
                row("Date-stamp token", None if p.returncode == 0 else False,
                    "cryptographically consistent with the package-bundled chain, but NOT "
                    "independently trusted" if p.returncode == 0 else "present but did not verify")
        else:
            row("Trusted date-stamp", None, "present - for full date proof, verify with OpenSSL (see VERIFY.txt)")
    else:
        row("Trusted date-stamp", None, "none attached")

    return ok, fp, rows


def main():
    print("=" * 64)
    print("  VERITROOPER - Package Checker")
    print("=" * 64)
    pkg = _find_package()
    if not pkg:
        print("\n  Could not find a package to check.")
        print("  Put this tool inside the audit package's Integrity folder and run it,")
        print("  or drag the audit folder onto it.")
        _pause()
        return 2
    print(f"  Checking: {pkg}\n")
    ok, fp, rows = check(pkg)
    print("\n".join(rows))
    print("-" * 64)
    if ok:
        print("  RESULT: the package is INTACT - nothing was changed since it was sealed.")
    else:
        print("  RESULT: this package DID NOT pass - do not rely on it. See the lines marked FAIL.")
    if fp:
        print("\n  Sealed by signer fingerprint:")
        print(f"    {fp}")
        # a bundled reference copy (convenience only - compare to the ID given out-of-band)
        ref = os.path.join(pkg, ENVELOPE_DIR, "trusted_fingerprint.txt")
        if os.path.exists(ref):
            want = open(ref, encoding="utf-8").read().strip()
            same = want.replace(":", "").upper() == fp.replace(":", "").upper()
            print(f"    (matches the fingerprint bundled with this package: {'yes' if same else 'NO'})")
        print("\n  IMPORTANT: confirm this fingerprint matches the ID VERITROOPER gave you")
        print("  SEPARATELY (your agreement, a signed email, or veritrooper.com). Only then")
        print("  does a valid signature prove the package genuinely came from VERITROOPER.")
    _pause()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
