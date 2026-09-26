# VeriTrooper Evaluation Suite

VeriTrooper tests whether an AI workflow follows its source material and rules,
then produces an evidence record that a team or outside reviewer can inspect.

This repository is the official release page for the VeriTrooper Evaluation
Suite on Windows, macOS, and Linux. The suite includes VeriTrooper Scout,
SitRep, Watchtower, and the supporting Governance Records workflow.

## Current release

The current Windows evaluation is **RC39, an unsigned prerelease**. Microsoft
public-trust validation remains **In Progress**, so Windows may show **Unknown
publisher**. The protected application passed source provenance, full resource
integrity, local Selene inference, web-console, and saved-run output checks.
An exact elevated install, upgrade, and uninstall run on a separate clean
Windows host remains pending.

A separate unsigned **RC39 Linux x86_64 preview** is available for Ubuntu 24.04.
It passed isolated missing/corrupt-resource, offline and repeat installation,
protected inference, console, and evidence-preservation acceptance. Mac RC39
packages are not available; the existing **RC36 macOS previews** remain available.

Each platform is distributed as one complete ZIP64 archive. The extracted
folder contains one root installer, installation instructions, checksum
manifests, and the complete protected application resources, including the
local Selene model. Keep the root installer and `Resources` folder together.

Open the [RC39 release](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/tag/rc39-evaluation)
for the complete download, published checksum, changes, installation steps,
and acceptance limitations.

- [Download Windows RC39](https://pub-9cb04876f6974621af1364971fc6efc4.r2.dev/evaluation/rc39/VERITROOPER-Evaluation-RC39.zip)
- [Windows RC39 SHA256 checksum](https://pub-9cb04876f6974621af1364971fc6efc4.r2.dev/evaluation/rc39/VERITROOPER-Evaluation-RC39.zip.sha256.txt)
- [Download the Linux RC39 preview](https://pub-9cb04876f6974621af1364971fc6efc4.r2.dev/evaluation/rc39/linux/VERITROOPER-Evaluation-RC39-linux-x86_64.zip)
- [Linux RC39 preview SHA256 checksum](https://pub-9cb04876f6974621af1364971fc6efc4.r2.dev/evaluation/rc39/linux/VERITROOPER-Evaluation-RC39-linux-x86_64.zip.sha256.txt)
- [Existing RC36 macOS and Linux previews](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/tag/rc36-cross-platform)
- [Earlier Windows RC35 release](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/tag/rc35-evaluation)

RC39 contains the repaired certifier, Doctor, and deterministic verifier used in
the final three 50-question validation cohorts. The full source suite passed 707
tests, and protected saved-run review produced 30 valid proof PDFs. These checks
validate product behavior; they do not establish new benchmark scores.

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

Windows RC39, earlier Windows releases, and the Linux previews are unsigned. The
RC36 macOS packages are ad hoc signed for build integrity but are not Apple
Developer ID signed or notarized. Use only the official downloads and confirm
the published SHA256 before installation. A matching checksum identifies the
published package; it does not provide a trusted publisher signature. Scanned
image-only OCR requires a native Tesseract installation in the macOS and Linux
previews.

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
