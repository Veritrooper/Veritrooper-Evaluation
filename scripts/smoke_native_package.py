"""Run an actual native llama.cpp completion through a packaged protected app."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, required=True)
    parser.add_argument("--port", type=int, default=18081)
    parser.add_argument("--ctx", type=int, default=2048)
    args = parser.parse_args(argv)
    app = args.app.resolve()
    os.environ["VT_LOCAL_ENGINE_DIR"] = str(app / "LocalEngine")
    os.environ.setdefault("VT_STATE_DIR", str(app.parent / "smoke-state"))
    sys.path.insert(0, str(app))
    from engine import local_validator

    result = local_validator.ensure_running(port=args.port, ctx=args.ctx, timeout=180)
    print(json.dumps(result, sort_keys=True), flush=True)
    if not result.get("ok"):
        return 2
    payload = json.dumps({
        "model": "local",
        "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
        "temperature": 0,
        "max_tokens": 4,
    }).encode("utf-8")
    request = urllib.request.Request(
        local_validator.local_url(args.port), data=payload,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            body = json.loads(response.read())
        completion = str(body["choices"][0]["message"]["content"] or "").strip()
        if not completion:
            print("Native inference returned an empty completion", file=sys.stderr)
            return 4
        print(completion, flush=True)
    finally:
        stopped = local_validator.stop()
        print(f"STOPPED={stopped}", flush=True)
    if local_validator.is_healthy(args.port, timeout=1):
        print("Server remained healthy after stop", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
