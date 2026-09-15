# RC36 cross-platform build

This branch contains protected macOS application payloads and the reproducible
native packaging workflow for Apple Silicon and Intel Macs. It does not contain
readable VeriTrooper product source or the licensed Selene model.

The workflow retrieves the already-published RC35 model through HTTP range
requests, verifies its approved SHA-256, downloads pinned native Python and
llama.cpp assets, verifies their publisher-provided SHA-256 values, builds the
distribution on the matching Mac architecture, runs a real local inference,
and retains only the package that passed those checks.

The public release remains RC35 until the RC36 macOS artifacts finish and the
release page is updated.
