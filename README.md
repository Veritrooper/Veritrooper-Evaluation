# VeriTrooper Scout

**AI answer assurance for systems that must be right about your source material.**

VeriTrooper Scout tests an AI model or assistant against approved source material, identifies unsupported or incorrect answers, and produces a portable evidence package that engineers, reviewers, auditors, and accountable decision-makers can inspect.

> **No trial software is distributed from this repository.** This is an informational entry point only. It contains no source code, installer, executable, activation file, or downloadable evaluation package. Controlled evaluations are arranged directly with VeriTrooper.

## Explore VeriTrooper

- [Run the interactive Scout demonstration](https://veritrooper.com/demo/)
- [Inspect a real, sanitized evidence package](https://veritrooper.com/evidence/)
- [Review the assurance methodology](https://veritrooper.com/methodology/)
- [Read the security and deployment overview](https://veritrooper.com/security/)
- [Browse product documentation](https://veritrooper.com/docs/)
- [Plan a guided enterprise pilot](https://veritrooper.com/pilot/)
- [Contact VeriTrooper](https://veritrooper.com/contact/)

## What Scout does

Scout evaluates whether an AI answers correctly from the material it is supposed to use.

1. **Establish ground truth** from approved documents, policies, records, tables, or other supported sources.
2. **Test the AI under review** with a bounded, traceable question set.
3. **Settle clear cases deterministically** where reproducible rules can reach a reliable verdict.
4. **Route contested cases for independent review** rather than allowing the model under test to confirm itself.
5. **Preserve every verdict and source** in a reviewable evidence package with integrity verification and human signoff.

Scout is the pre-deployment checkpoint in the VeriTrooper assurance system:

- **SitRep** examines whether source material is sound before an AI relies on it.
- **Scout** tests whether an AI answers correctly before it ships.
- **Watchtower** checks whether production answers remain reliable after deployment.

## Evidence, not a dashboard score

A completed Scout engagement can produce role-specific reports, per-finding records, source references, machine-readable results, run configuration, integrity material, and reviewer disposition. The public evidence page contains a sanitized report set from a real 1,000-question audit so prospective evaluators can inspect the form of the output before sharing private material.

## Deployment and data boundary

VeriTrooper is designed to run on customer-controlled infrastructure, including offline and air-gapped environments. Local operation does not require customer documents or audit results to be uploaded to VeriTrooper.

If an operator deliberately selects a cloud model or remote endpoint, the data required for that call is sent directly to the selected provider under that provider's terms and using the operator's credentials. VeriTrooper does not operate an intermediary service that receives the customer's audit corpus.

## Controlled evaluation

Evaluations are provided through a guided, bounded process so that the system under review, approved sources, deployment boundary, success criteria, and responsible reviewers are defined before a run begins. Trial software and activation material are delivered only through an approved channel; they are not published on GitHub.

[Request a guided pilot](https://veritrooper.com/pilot/) or email [contact@veritrooper.com](mailto:contact@veritrooper.com).

## Important boundaries

VeriTrooper supplies testing and governance evidence. It does not provide legal advice, perform a conformity assessment, certify compliance, prove the absence of every error, or replace accountable human review. A qualified person remains responsible for interpreting findings and approving decisions.

Copyright 2026 VeriTrooper LLC. All rights reserved. Patent pending, including U.S. patent application 19/685,794.
