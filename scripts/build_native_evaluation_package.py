"""Build a native macOS or Linux Evaluation distribution from a protected stage."""
from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import stat
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path


RELEASE = "RC36"
MODEL_NAME = "selene-1-mini-llama-3.1-8b-q4_k_m.gguf"
MODEL_SHA256 = "B8CE1F01DD99D03B75DD1BB7A69FA25D609EFF8C92AB118630C05A7A70829481"
ASSETS = {
    "linux.x86_64": {
        "python": "https://github.com/astral-sh/python-build-standalone/releases/download/20260901/cpython-3.14.7%2B20260901-x86_64-unknown-linux-gnu-install_only.tar.gz",
        "llama": "https://github.com/ggml-org/llama.cpp/releases/download/b8522/llama-b8522-bin-ubuntu-x64.tar.gz",
    },
    "darwin.arm64": {
        "python": "https://github.com/astral-sh/python-build-standalone/releases/download/20260901/cpython-3.14.7%2B20260901-aarch64-apple-darwin-install_only.tar.gz",
        "llama": "https://github.com/ggml-org/llama.cpp/releases/download/b8522/llama-b8522-bin-macos-arm64.tar.gz",
    },
    "darwin.x86_64": {
        "python": "https://github.com/astral-sh/python-build-standalone/releases/download/20260901/cpython-3.14.7%2B20260901-x86_64-apple-darwin-install_only.tar.gz",
        "llama": "https://github.com/ggml-org/llama.cpp/releases/download/b8522/llama-b8522-bin-macos-x64.tar.gz",
    },
}
ASSET_SHA256 = {
    "cpython-3.14.7%2B20260901-x86_64-unknown-linux-gnu-install_only.tar.gz": "0AB3305457051CD3E7C031857E005F1BDA17C218A1990567DACAAAC6DD1D14F0",
    "cpython-3.14.7%2B20260901-aarch64-apple-darwin-install_only.tar.gz": "30DAA970C7D223530120F1693CD3C6FA4C0C0D31EF158710B0DD77F286A5B23E",
    "cpython-3.14.7%2B20260901-x86_64-apple-darwin-install_only.tar.gz": "DD8841A2E8EF94BD1A02B52F92843120942140F112145D4E0199ABAB56F120B1",
    "llama-b8522-bin-ubuntu-x64.tar.gz": "47E78E1A710B1D666EB99055D44A93106B43289EDDBDD854946E485DE6EFBC7F",
    "llama-b8522-bin-macos-arm64.tar.gz": "7302C8832240D4B0FA2ECAD5C19ABAC8C74070EFD03F288E3493AFACA87C38C2",
    "llama-b8522-bin-macos-x64.tar.gz": "72FBEC3D801EB67A9EAB89D3B743E0DDDFEF2394D3D538C9F67708D7EAB9D733",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def download(url: str, destination: Path) -> None:
    if destination.is_file():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".partial")
    print(f"Downloading {url}", flush=True)
    urllib.request.urlretrieve(url, temporary)
    os.replace(temporary, destination)


def verify_download(path: Path) -> None:
    expected = ASSET_SHA256.get(path.name)
    if not expected or digest(path) != expected:
        raise SystemExit(f"Downloaded asset SHA-256 mismatch: {path.name}")


def extract_tar(archive_path: Path, destination: Path) -> None:
    root = destination.resolve()
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            candidate = (root / member.name).resolve()
            if candidate != root and root not in candidate.parents:
                raise SystemExit(f"Unsafe path in {archive_path.name}: {member.name}")
        archive.extractall(destination)


def native_target(target: str) -> bool:
    machine = platform.machine().lower()
    if target == "linux.x86_64":
        return platform.system() == "Linux" and machine in ("x86_64", "amd64")
    if target == "darwin.arm64":
        return platform.system() == "Darwin" and machine in ("arm64", "aarch64")
    return platform.system() == "Darwin" and machine in ("x86_64", "amd64")


def write_text(path: Path, value: str, executable: bool = False) -> None:
    path.write_text(value, encoding="utf-8", newline="\n")
    if executable:
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def installer_script(target: str) -> str:
    mac = target.startswith("darwin")
    default_root = '${HOME}/Library/Application Support/Veritrooper Evaluation/RC36' if mac else '${XDG_DATA_HOME:-${HOME}/.local/share}/veritrooper-evaluation/RC36'
    shortcut_root = '${HOME}/Applications' if mac else '${HOME}/.local/bin'
    return f'''#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE="$HERE/Resources/Application"
DEST="${{VT_INSTALL_ROOT:-{default_root}}}"
if [ ! -d "$SOURCE" ]; then printf '%s\n' "Resources/Application is missing." >&2; exit 2; fi
EXPECTED=$(awk '$2 == "Resources/Application/LocalEngine/models/{MODEL_NAME}" {{print $1}}' "$HERE/SHA256SUMS.txt")
if command -v shasum >/dev/null 2>&1; then
  ACTUAL=$(shasum -a 256 "$SOURCE/LocalEngine/models/{MODEL_NAME}" | awk '{{print $1}}')
else
  ACTUAL=$(sha256sum "$SOURCE/LocalEngine/models/{MODEL_NAME}" | awk '{{print $1}}')
fi
if [ -z "$EXPECTED" ] || [ "$ACTUAL" != "$EXPECTED" ]; then printf '%s\n' "Model integrity check failed." >&2; exit 3; fi
mkdir -p "$(dirname "$DEST")"
STAGE="$DEST.installing.$$"
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -R "$SOURCE/." "$STAGE/"
rm -rf "$DEST.previous"
if [ -d "$DEST" ]; then mv "$DEST" "$DEST.previous"; fi
mv "$STAGE" "$DEST"
mkdir -p "{shortcut_root}"
'''+ ('''APP="$HOME/Applications/VERITROOPER Evaluation.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cat > "$APP/Contents/MacOS/veritrooper-evaluation" <<'LAUNCH'
#!/bin/sh
set -eu
ROOT="${VT_INSTALL_ROOT:-${HOME}/Library/Application Support/Veritrooper Evaluation/RC36}"
export VT_LOCAL_ENGINE_DIR="$ROOT/LocalEngine"
export PYTHONPATH="$ROOT"
LOG="$HOME/Library/Logs/Veritrooper Evaluation.log"
"$ROOT/python/bin/python3" -m _webui.server --port 8300 --log "$LOG" &
PID=$!
i=0
while [ $i -lt 30 ]; do curl -fsS http://127.0.0.1:8300/api/server/status >/dev/null 2>&1 && break; sleep 1; i=$((i+1)); done
open http://127.0.0.1:8300/
wait $PID
LAUNCH
chmod 755 "$APP/Contents/MacOS/veritrooper-evaluation"
cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict><key>CFBundleExecutable</key><string>veritrooper-evaluation</string><key>CFBundleIdentifier</key><string>com.veritrooper.evaluation</string><key>CFBundleName</key><string>VERITROOPER Evaluation</string><key>CFBundlePackageType</key><string>APPL</string><key>CFBundleShortVersionString</key><string>RC36</string></dict></plist>
PLIST
printf '%s\n' "Installed. Open VERITROOPER Evaluation from your Applications folder."
''' if mac else '''LAUNCH="$HOME/.local/bin/veritrooper-evaluation"
cat > "$LAUNCH" <<'LAUNCHER'
#!/bin/sh
set -eu
ROOT="${VT_INSTALL_ROOT:-${XDG_DATA_HOME:-${HOME}/.local/share}/veritrooper-evaluation/RC36}"
export VT_LOCAL_ENGINE_DIR="$ROOT/LocalEngine"
export PYTHONPATH="$ROOT"
LOG="${XDG_STATE_HOME:-${HOME}/.local/state}/veritrooper/console.log"
mkdir -p "$(dirname "$LOG")"
"$ROOT/python/bin/python3" -m _webui.server --port 8300 --log "$LOG" &
PID=$!
i=0
while [ $i -lt 30 ]; do curl -fsS http://127.0.0.1:8300/api/server/status >/dev/null 2>&1 && break; sleep 1; i=$((i+1)); done
if command -v xdg-open >/dev/null 2>&1; then xdg-open http://127.0.0.1:8300/ >/dev/null 2>&1 || true; fi
wait $PID
LAUNCHER
chmod 755 "$LAUNCH"
DESKTOP="${XDG_DATA_HOME:-${HOME}/.local/share}/applications/veritrooper-evaluation.desktop"
mkdir -p "$(dirname "$DESKTOP")"
cat > "$DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Name=VERITROOPER Evaluation
Exec=$LAUNCH
Terminal=false
Categories=Utility;
EOF
printf '%s\n' "Installed. Run $LAUNCH or open VERITROOPER Evaluation from your application menu."
''')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=ASSETS)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--requirements-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--skip-archive", action="store_true")
    args = parser.parse_args(argv)
    if not native_target(args.target):
        raise SystemExit(f"{args.target} packages must be built on their native operating system and architecture")
    if digest(args.model) != MODEL_SHA256:
        raise SystemExit("The supplied model does not match the approved Selene SHA-256")
    package_name = f"VERITROOPER-Evaluation-{RELEASE}-{args.target.replace('.', '-')}"
    package = args.output.resolve() / package_name
    if package.exists():
        raise SystemExit(f"Refusing to overwrite {package}")
    app = package / "Resources" / "Application"
    shutil.copytree(args.stage / "App", app)
    if args.target.startswith("darwin"):
        for runtime in app.glob("pyarmor_runtime_*/*.so"):
            subprocess.run(["codesign", "--force", "--sign", "-", str(runtime)], check=True)

    runtime_archive = args.cache / Path(ASSETS[args.target]["python"]).name
    llama_archive = args.cache / Path(ASSETS[args.target]["llama"]).name
    download(ASSETS[args.target]["python"], runtime_archive)
    download(ASSETS[args.target]["llama"], llama_archive)
    verify_download(runtime_archive)
    verify_download(llama_archive)
    extract_tar(runtime_archive, app)
    python = app / "python" / "bin" / "python3"
    if not python.is_file():
        raise SystemExit("Python standalone archive did not contain python/bin/python3")
    command = [str(python), "-m", "pip", "install", "--disable-pip-version-check",
               "--no-compile", "-r", str(args.requirements_root / "requirements" / "all.in")]
    subprocess.run(command, check=True)

    with tempfile.TemporaryDirectory(prefix="vt-llama-") as temporary:
        temporary_path = Path(temporary)
        extract_tar(llama_archive, temporary_path)
        candidates = list(temporary_path.rglob("llama-server"))
        if len(candidates) != 1:
            raise SystemExit(f"Expected one llama-server, found {len(candidates)}")
        source_root = candidates[0].parent
        shutil.copytree(source_root, app / "LocalEngine" / "llama-server")
    server = app / "LocalEngine" / "llama-server" / "llama-server"
    server.chmod(server.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    if args.target.startswith("darwin"):
        for binary in sorted(app.joinpath("LocalEngine", "llama-server").rglob("*")):
            if binary.is_file() and (binary.suffix in (".dylib", ".so") or binary.name == "llama-server"):
                subprocess.run(["codesign", "--force", "--sign", "-", str(binary)], check=True)
    models = app / "LocalEngine" / "models"
    models.mkdir(parents=True)
    try:
        os.link(args.model, models / MODEL_NAME)
    except OSError:
        shutil.copy2(args.model, models / MODEL_NAME)

    sums = []
    for path in sorted(p for p in (package / "Resources").rglob("*") if p.is_file()):
        rel = path.relative_to(package).as_posix()
        sums.append(f"{digest(path).lower()}  {rel}")
    write_text(package / "SHA256SUMS.txt", "\n".join(sums) + "\n")
    installer_name = "Install VERITROOPER Evaluation.command" if args.target.startswith("darwin") else "Install VERITROOPER Evaluation.run"
    write_text(package / installer_name, installer_script(args.target), executable=True)
    platform_name = "macOS" if args.target.startswith("darwin") else "Linux"
    write_text(package / "INSTALLATION README.txt", f"""VERITROOPER Evaluation {RELEASE} for {platform_name}
================================================================

This is a complete offline Evaluation installation. Keep the installer and Resources folder together.

INSTALL
  1. Extract the entire downloaded ZIP.
  2. Open or run \"{installer_name}\".
  3. Start VERITROOPER Evaluation from your Applications folder or application menu.

INTEGRITY
  SHA256SUMS.txt records a SHA-256 fingerprint for every shipped resource. The installer verifies the 4.9 GB Selene model before copying it. Advanced users can verify everything with:

    shasum -a 256 -c SHA256SUMS.txt

This preview is not yet signed or notarized. Your operating system may require you to approve opening it through its security settings.

Evaluation limits: 14 days, 5 shared audit runs, and 200 items per run.
""")
    if not args.skip_archive:
        archive_path = args.output.resolve() / (package_name + ".zip")
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=1, allowZip64=True) as archive:
            for path in sorted(package.rglob("*")):
                if path.is_file():
                    archive.write(path, (Path(package_name) / path.relative_to(package)).as_posix())
        print(f"Archive: {archive_path}")
    print(f"Package: {package}")


if __name__ == "__main__":
    main()
