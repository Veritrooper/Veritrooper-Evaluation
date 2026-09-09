# VeriTrooper Evaluation Suite

VeriTrooper tests whether an AI workflow follows the source material and rules it was given, then produces a record a team or outside reviewer can inspect.

This repository is the official download page for the Windows Evaluation Suite. It includes VeriTrooper Scout, SitRep, and Watchtower, plus the supporting Governance Records workflow.

## Evaluation limits

- 14 days from the first real audit
- 5 total runs shared across Scout, SitRep, and Watchtower
- Up to 200 questions or evaluated interactions per run
- Opening the application, configuring it, and creating a Watchtower deployment do not consume a run

## Install

Open the [latest release](https://github.com/Veritrooper/Veritrooper-Evaluation/releases/latest) and download the .exe, all three numbered .bin files, SHA256SUMS.txt, and the installation instructions. Keep them together in one folder.

GitHub changes spaces in uploaded asset names to periods. Before running setup, rename the four installer files as follows:

1. `VERITROOPER.Evaluation.Suite.Setup.exe` to `VERITROOPER Evaluation Suite Setup.exe`
2. `VERITROOPER.Evaluation.Suite.Setup-1.bin` to `VERITROOPER Evaluation Suite Setup-1.bin`
3. `VERITROOPER.Evaluation.Suite.Setup-2.bin` to `VERITROOPER Evaluation Suite Setup-2.bin`
4. `VERITROOPER.Evaluation.Suite.Setup-3.bin` to `VERITROOPER Evaluation Suite Setup-3.bin`

Then verify the SHA-256 hashes and run `VERITROOPER Evaluation Suite Setup.exe`.

This release candidate is not yet code-signed, so Windows may show **Unknown publisher**. Continue only when the downloaded hashes match `SHA256SUMS.txt`.

## What to try

Bring one real AI workflow and the source material it should follow. VeriTrooper will test the workflow, show what holds up or falls short, and produce evidence you can use in a review.

## Important boundaries

VeriTrooper supplies testing and governance evidence. It does not provide legal advice, perform a conformity assessment, certify compliance, prove the absence of every error, or replace accountable human review. A qualified person remains responsible for interpreting findings and approving decisions.

Questions or evaluation feedback: brianb@veritrooper.com

[Learn more at veritrooper.com](https://veritrooper.com/)
