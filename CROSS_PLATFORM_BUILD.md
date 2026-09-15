# RC36 cross-platform build

This repository contains protected macOS application payloads and the
reproducible native packaging workflow for Apple Silicon and Intel Macs. It
does not contain readable VeriTrooper product source or the licensed Selene
model.

The workflow retrieves the already-published RC35 model through HTTP range
requests, verifies its approved SHA-256, downloads pinned native Python and
llama.cpp assets, verifies their publisher-provided SHA-256 values, builds the
distribution on the matching Mac architecture, runs a real local inference,
and retains only the package that passed those checks. The native test also
verifies protected imports, the PyArmor runtime signature, the llama binary,
model startup, an actual completion, and process shutdown.

The Linux x86_64 package is built and tested in Ubuntu 24.04. The RC36 macOS
packages are built on GitHub's native Apple Silicon and Intel runners. RC36 is
published as a prerelease until Apple Developer ID signing and notarization are
available.
