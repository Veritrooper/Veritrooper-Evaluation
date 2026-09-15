"""Stream the approved Selene model from the public RC35 ZIP using HTTP ranges."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from remotezip import RemoteZip


MEMBER = "RC35 - Evaluation Offline Layout/Resources/Application/LocalEngine/models/selene-1-mini-llama-3.1-8b-q4_k_m.gguf"
EXPECTED = "B8CE1F01DD99D03B75DD1BB7A69FA25D609EFF8C92AB118630C05A7A70829481"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    h = hashlib.sha256()
    with RemoteZip(args.url) as archive, archive.open(MEMBER) as source, args.output.open("wb") as out:
        while True:
            block = source.read(8 * 1024 * 1024)
            if not block:
                break
            out.write(block)
            h.update(block)
    actual = h.hexdigest().upper()
    if actual != EXPECTED:
        args.output.unlink(missing_ok=True)
        raise SystemExit(f"Selene SHA-256 mismatch: {actual}")
    print(f"MODEL_OK {actual}")


if __name__ == "__main__":
    main()
