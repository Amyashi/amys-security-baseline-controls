# Amy's Security Baseline Controls

Amy's Security Baseline Controls is a general, evidence-driven Windows 11 security baseline for individual PC owners. It explains what to verify, what can differ between Windows 11 Home and Pro, which changes carry compatibility risk, and when to stop or roll back.

Version 1.0.0 is the initial public release. The materials are informational and do not certify a device, guarantee protection, replace incident response, or substitute for current vendor guidance or qualified professional advice.

## Choose your Windows edition

Start with the guide that matches **Settings > System > About > Windows specifications > Edition**. Each guide is an ordered implementation path: complete Step 01, use its PASS or HOLD rule, and continue only when directed.

### Windows 11 Home

- [Home implementation guide](docs/Amys_Windows_11_Home_Security_Baseline_v1.0.0.pdf) - ordered actions, commands, restart gates, verification, failure handling, rollback, and evidence guidance without Pro-only procedures.
- [Home printable workbook](docs/Amys_Windows_11_Home_Assessment_Workbook_v1.0.0.pdf) - a matching step-by-step assessment record.
- [Home accessible implementation guide](docs/WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md) - the same ordered path in a reflowable, searchable text format.

### Windows 11 Pro

- [Pro implementation guide](docs/Amys_Windows_11_Pro_Security_Baseline_v1.0.0.pdf) - the Home foundation plus supported Pro procedures for BitLocker, Network Protection, and carefully scoped optional capabilities.
- [Pro printable workbook](docs/Amys_Windows_11_Pro_Assessment_Workbook_v1.0.0.pdf) - a matching step-by-step assessment record.
- [Pro accessible implementation guide](docs/WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md) - the same ordered path in a reflowable, searchable text format.

For deeper study, use the [comprehensive accessible reference](docs/ACCESSIBLE_GUIDE.md) and [control framework mapping](docs/CONTROL_FRAMEWORK_MAPPING.md). They preserve the full stable-ID crosswalk and supplemental context, but are not the shortest implementation path.

The PDFs are generated artifacts. The Markdown companions remain the preferred accessible formats when a PDF reader does not expose the document structure adequately.

## What the baseline covers

- Recovery readiness and safe change gates
- Secure Boot, TPM, CPU virtualization, DMA remapping, VBS, HVCI, and vulnerable-driver protections
- Microsoft Defender, ransomware protections, browser security, DNS, firewall, and remote-access exposure
- Windows 11 Home and Pro availability indicators
- Vendor-neutral firmware guidance with exact-model verification requirements
- Gaming and application compatibility checks
- Explicit pass, hold, and rollback criteria
- Per-control citation traceability and IEEE-style references to primary Microsoft, NIST, and CISA sources
- Dated evidence rules and exact-model hardware-vendor source requirements

## Safe-use principles

1. Complete the recovery and evidence gate before changing firmware, TPM, Secure Boot, VBS, encryption, or other boot-critical controls.
2. Record the exact prior value and make one change at a time.
3. Use the current manual and support page for the exact device, motherboard, or OEM model.
4. Verify the effective Windows runtime state after each reboot; a configured value alone is not proof.
5. Run the named compatibility test before accepting a change.
6. Stop after an unexplained block, recovery prompt, crash, hardware error, lost save, or measurable regression.
7. Never publish recovery keys, logs, dumps, screenshots, account data, network identifiers, device identifiers, or other sensitive evidence.

Product behavior, subscriptions, servicing state, and documentation change. Treat every dated observation as historical context and recheck the current authoritative source before relying on it.

## Repository layout

| Path | Purpose |
| --- | --- |
| `docs/Amys_Windows_11_Home_Security_Baseline_v1.0.0.pdf` | Generated Home implementation guide |
| `docs/Amys_Windows_11_Home_Assessment_Workbook_v1.0.0.pdf` | Generated Home printable workbook |
| `docs/Amys_Windows_11_Pro_Security_Baseline_v1.0.0.pdf` | Generated Pro implementation guide |
| `docs/Amys_Windows_11_Pro_Assessment_Workbook_v1.0.0.pdf` | Generated Pro printable workbook |
| `docs/SHA256SUMS.txt` | SHA-256 release-artifact checksums |
| `docs/WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md` | Accessible Home implementation path |
| `docs/WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md` | Accessible Pro implementation path |
| `docs/ACCESSIBLE_GUIDE.md` | Comprehensive accessible reference |
| `docs/CONTROL_FRAMEWORK_MAPPING.md` | Control-framework crosswalk |
| `src/sbc_content.py` | Canonical ordered Home and Pro implementation content |
| `src/build_security_checklist.py` | Generated-document layout and build source |
| `tests/qa_security_checklist.py` | Document-specific quality checks |
| `scripts/validate_public_release.py` | Repository-wide public-release validation |
| `requirements.in` | Direct, intentionally selected build and validation dependencies |
| `requirements.txt` | Fully resolved, version- and hash-locked dependency graph |

## Rebuild and validate

Use Python 3.12.13. `requirements.in` records the direct project dependencies,
and `requirements.txt` locks the complete transitive graph with approved
distribution hashes. The supported install path accepts wheels only and fails
if a downloaded artifact does not match the lock. The operating system,
architecture, interpreter build, installer, and PDF-library behavior can still
affect results outside the documented environment, so the protected GitHub
Actions build remains the release gate. The generator is expected to use only
fonts and assets whose redistribution terms are documented in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

```powershell
python --version  # Must report Python 3.12.13
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --disable-pip-version-check --only-binary=:all: --require-hashes -r requirements.txt
python -m pip check
python src\build_security_checklist.py
python tests\qa_security_checklist.py
python scripts\validate_public_release.py
```

Automated checks do not replace visual review. Before a release, render every page and confirm that:

- no text, table, status marker, or link is clipped;
- continuation pages and repeated table headers are unambiguous;
- color is not the only way meaning is conveyed;
- reading order remains understandable;
- the workbook prints legibly in grayscale; and
- no sparse or accidental spill page was introduced.

See [ACCESSIBILITY.md](ACCESSIBILITY.md) for the accessibility policy and [CONTRIBUTING.md](CONTRIBUTING.md) for the review requirements.

## Reporting problems

- Use a GitHub issue for factual errors, broken references, accessibility problems, or improvement proposals.
- Use [GitHub private vulnerability reporting](https://github.com/Amyashi/amys-security-baseline-controls/security/advisories/new) for a vulnerability in this repository, its automation, or its generated artifacts.
- Do not attach unredacted diagnostics or other sensitive evidence to either channel.

## Release policy

A public release must:

1. pass the document-specific and repository-wide validators;
2. be rebuilt in the documented release environment from the declared dependency versions, with committed PDFs matching the generator;
3. receive a complete visual and print review;
4. contain no account, device, network, recovery, or diagnostic evidence;
5. keep both edition guides, both workbooks, accessible companions, mapping, citation metadata, and changelog synchronized; and
6. be published from a protected tag with the generated `docs/SHA256SUMS.txt` checksum file.

## License

The guide, generated PDFs, accessible companions, control mapping, and other prose are licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](LICENSE.md#guide-materials).

The build, validation, and automation code is not open source. It is all rights reserved, with a limited permission to download and execute unmodified copies for personal, noncommercial reproduction and validation of the unmodified guide materials. See [LICENSE.md](LICENSE.md) for the complete terms.

`src/sbc_content.py` is a mixed-content source file: its human-readable guide
content is guide material, while its Python and organizational elements remain
code. The license also provides a narrow permission to fork, modify, and share
repository material solely as needed to submit a contribution to the official
project. It does not authorize separate modified releases or broader
redistribution.

Third-party components remain subject to their own licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
