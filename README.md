# VeriTrooper Evaluation Suite

VeriTrooper tests whether an AI workflow follows its source material and rules,
then produces an evidence record that a team or outside reviewer can inspect.

This repository is the official release page for the VeriTrooper Evaluation
Suite on Windows, macOS, and Linux. The suite includes VeriTrooper Scout,
SitRep, Watchtower, and the supporting Governance Records workflow.

## Current release

The current Windows evaluation release is **RC35**. Native Linux and macOS
evaluation previews are available as **RC36**.

Each platform is distributed as one complete ZIP64 archive. The extracted
folder contains one root installer, installation instructions, checksum
manifests, and the complete protected application resources, including the
local Selene model. Keep the root installer and `Resources` folder together.

Open the [RC36 cross-platform release](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/tag/rc36-cross-platform)
for all official download locations, published checksums, installation steps,
and signing status. The existing [RC35 Windows release](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/tag/rc35-evaluation)
remains available and unchanged.

## Evaluation limits

- 14 days from the first real audit
- 5 total runs shared across Scout, SitRep, and Watchtower
- Up to 200 questions or evaluated interactions per run
- Opening the application, configuring it, and creating a Watchtower deployment
  do not consume a run

## Installation summary

1. Download the complete distribution for your operating system and processor.
2. Verify the published SHA256 value.
3. Extract the complete folder to a local drive.
4. Keep the root installer and `Resources` directory together.
5. Run `VERITROOPER Evaluation Setup.exe` on Windows,
   `Install VERITROOPER Evaluation.run` on Linux, or
   `Install VERITROOPER Evaluation.command` on macOS.

The installer verifies the size and SHA256 of every application resource while
installing. Installation stops if any required file is missing, incomplete, or
altered. No internet connection is required for installation or the local audit
path.

Windows RC35 and Linux RC36 are currently unsigned. The macOS packages are ad
hoc signed for build integrity but are not Apple Developer ID signed or
notarized. Use only the official downloads and confirm the published SHA256
before installation. Scanned image-only OCR requires a native Tesseract
installation in the macOS and Linux preview.

## What to try

Bring one real AI workflow and the source material it should follow. VeriTrooper
will test the workflow, show what holds up or falls short, and produce evidence
you can use in a review.

## Important boundaries

VeriTrooper supplies testing and governance evidence. It does not provide legal
advice, perform a conformity assessment, certify compliance, prove the absence
of every error, or replace accountable human review. A qualified person remains
responsible for interpreting findings and approving decisions.

Questions or evaluation feedback: brianb@veritrooper.com

[Learn more at veritrooper.com](https://veritrooper.com/)
