# Contributing

Thank you for helping improve Amy's Security Baseline Controls. This is a controlled-author project: issues and well-supported proposals are welcome, but changes are accepted at the author's discretion.

## Before contributing

Please search existing issues before opening a new one. Use:

- **Guide problem** for a factual error, broken reference, unclear instruction, accessibility problem, or unsafe ambiguity.
- **Improvement proposal** for a new control, structural change, or usability enhancement.
- **GitHub private vulnerability reporting** for a vulnerability in the repository, automation, or generated artifacts.

Do not use this repository for device-specific technical support.

## Evidence and privacy

Use current primary sources whenever possible. A claim about Windows, firmware, hardware, licensing, product behavior, or framework guidance should include:

- the authoritative source URL;
- the date it was checked;
- the affected edition, version, or hardware prerequisite; and
- a clear distinction between documented behavior, observation, and inference.

Never submit recovery keys, credentials, tokens, certificates, full logs, dumps, registry exports, screenshots with account or device data, serial numbers, hostnames, network identifiers, public IP addresses, or other sensitive evidence. Replace necessary examples with neutral placeholders.

## Limited permission to prepare a contribution

The [contribution-only permission in LICENSE.md](LICENSE.md#contribution-only-permission)
allows you to fork, modify, and share repository material only as reasonably
necessary to prepare, discuss, review, and submit a contribution to the
official
[`Amyashi/amys-security-baseline-controls`](https://github.com/Amyashi/amys-security-baseline-controls)
repository through GitHub.

That permission does not authorize a separate release, a general-purpose
modified fork, commercial use, or redistribution outside the contribution
process. Preserve existing copyright and license notices, identify your
changes, and do not include third-party material unless you have the right to
submit it under the grant below.

## Pull requests

An issue is preferred before a substantial pull request. A pull request should:

1. address one coherent problem;
2. preserve the general, system- and device-neutral scope;
3. update the matching edition-accessible guide, comprehensive reference, and control mapping when relevant;
4. rebuild all four edition-specific PDFs;
5. pass all automated checks;
6. include a complete visual and print review; and
7. explain source dates, compatibility risks, and rollback implications.

Opening a pull request makes a proposal; it does not incorporate the change
into the project. Only the author accepts a contribution by merging or
otherwise expressly incorporating it. The author may edit, combine, defer,
decline, remove, or decline to maintain a contribution.

## Contribution grant

By opening a pull request, posting proposed material in an issue, or otherwise
submitting material through the official repository, you represent that you
have the right to submit it and grant Amyashi a perpetual, worldwide,
non-exclusive, royalty-free, irrevocable license to use, reproduce, modify,
prepare derivative works from, distribute, publicly display, publicly perform,
sublicense, and relicense the contribution as part of this project or related
editions.

The grant covers the material you contribute and revisions you submit during
review; it does not transfer ownership of pre-existing repository material.
If accepted, the author may incorporate and distribute the contribution under
the project terms applicable to the resulting material.

You retain any copyright you hold in your original contribution. The grant
remains effective whether the submission is accepted, edited, declined, or
later removed. Submission does not grant contributors a license to other
repository content beyond the contribution-only permission and does not
otherwise change the terms in [LICENSE.md](LICENSE.md).

## Local validation

Use Python 3.12.13 and the complete hash-locked dependency graph:

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

Automated validation is necessary but not sufficient. Render and inspect every PDF page before marking a change ready for release.

For an intentional dependency update, edit `requirements.in`, then regenerate
the lock with pip-tools 7.6.0 under Python 3.12.13:

```powershell
python -m pip install pip-tools==7.6.0
python -m piptools compile --generate-hashes --resolver=backtracking --strip-extras requirements.in
```

Review all resolved-version and hash changes before committing them. Dependency
updates must pass the same document validation and visual-review gates as source
changes.
