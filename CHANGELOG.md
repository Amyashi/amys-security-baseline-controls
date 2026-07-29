# Changelog

Material changes to the guide, workbook, accessible companion, control mapping, build process, and release policy are recorded here.

## Unreleased

### Added

- Separate ordered Windows 11 Home and Windows 11 Pro implementation guides.
- Edition-matched printable assessment workbooks.
- Edition-matched accessible Markdown implementation guides.
- Explicit commands, restart gates, verification, failure handling, rollback, and minimal-evidence instructions for every implementation step.
- Control-framework mapping.
- Controlled-author license and public contribution policy.
- Security reporting policy, issue forms, pull-request checklist, and code ownership.
- Public-release validator, least-privilege continuous integration, and dependency monitoring.
- Stable per-control source mappings and IEEE-style references with source-review dates.
- Deterministic PDF generation in the documented release environment and CI verification that committed artifacts match their source.
- Generated SHA-256 checksums validated against all four release PDFs.

### Changed

- Reframed the project as a general Windows 11 security baseline rather than a record for one device.
- Reorganized the reader experience around one linear implementation path per edition, with reference material moved after the action sequence.
- Kept unsupported Pro-only procedures out of the Home path and documented them in an edition-exclusion register.
- Separated dated observations from current verification requirements.
- Adopted versioned, edition-specific artifact filenames for the guides and workbooks.
- Updated pinned document-build and validation dependencies.
- Moved public support and vulnerability reporting to GitHub.

### Removed

- Community-specific contact information and branding.
- Publication-sensitive machine and diagnostic context.

## Release convention

Published releases use semantic version tags such as `v1.0.0`. A date is added to this file and `CITATION.cff` only when the corresponding release is published.
