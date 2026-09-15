# VeriTrooper Evaluation Suite

VeriTrooper tests whether an AI workflow follows its source material and rules,
then produces an evidence record that a team or outside reviewer can inspect.

This repository is the official release page for the Windows Evaluation Suite.
The suite includes VeriTrooper Scout, SitRep, Watchtower, and the supporting
Governance Records workflow.

## Current release

The current evaluation release is **RC35**.

RC35 is distributed as one offline installation-layout folder. The folder
contains one installer EXE, installation instructions, checksum manifests, and
the complete protected application resources, including the local Selene model.
Keep the complete folder together and run only
`VERITROOPER Evaluation Setup.exe`.

Open the [latest release](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/latest)
for the official download location, published checksums, installation steps,
and signing status.

## Evaluation limits

- 14 days from the first real audit
- 5 total runs shared across Scout, SitRep, and Watchtower
- Up to 200 questions or evaluated interactions per run
- Opening the application, configuring it, and creating a Watchtower deployment
  do not consume a run

## Installation summary

1. Download the complete RC35 distribution from the official release page.
2. Verify the published SHA256 value.
3. Extract the complete folder to a local NTFS drive.
4. Keep `VERITROOPER Evaluation Setup.exe` and the `Resources` directory
   together.
5. Run `VERITROOPER Evaluation Setup.exe` and accept the displayed licence.

The installer verifies the size and SHA256 of every application resource while
installing. Installation stops if any required file is missing, incomplete, or
altered. No internet connection is required for installation or the local audit
path.

RC35 is currently unsigned while Microsoft public-trust validation is pending.
Windows may display **Unknown publisher**. Use only the official download and
confirm its published SHA256 value before installation.

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
