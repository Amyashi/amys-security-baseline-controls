# Third-party notices

This project uses third-party software to build and validate its documents. Those components are not relicensed by this repository.

| Component | Version | Purpose | License |
| --- | ---: | --- | --- |
| [ReportLab](https://pypi.org/project/reportlab/) | 5.0.0 | PDF generation | BSD-style license |
| [pypdf](https://pypi.org/project/pypdf/) | 6.15.0 | PDF structure and metadata validation | BSD-3-Clause |
| [pdfplumber](https://pypi.org/project/pdfplumber/) | 0.11.10 | PDF text and geometry validation | MIT |
| [Pillow](https://pypi.org/project/pillow/) | 12.3.0 | Image and font support used by the PDF toolchain | MIT-CMU |

The authoritative license text for each installed package is included in its distribution and source repository. Transitive dependencies retain their own license terms.

## Security automation

Repository automation uses pip-audit 2.10.1 under the Apache License 2.0 and
GitHub's Dependency Review Action 5.0.0 under the MIT License. Both are
isolated from the PDF build environment:

- pip-audit: <https://github.com/pypa/pip-audit/blob/v2.10.1/LICENSE>
- Dependency Review Action:
  <https://github.com/actions/dependency-review-action/blob/v5.0.0/LICENSE>

## Fonts

Generated artifacts must use only fonts whose embedding and redistribution terms permit the intended release. If Bitstream Vera fonts supplied with ReportLab are used, they remain subject to the Bitstream Vera Fonts Copyright and license included with the ReportLab distribution. The font names must not be used to promote or advertise a modified font without permission.

No proprietary operating-system font file may be copied into this repository.

## External documentation and standards

The guide links to documentation and standards from Microsoft, NIST, CISA, hardware vendors, and other publishers. Links and short factual citations do not transfer ownership of those materials or imply endorsement. Readers must follow the publisher's current terms and documentation.

Microsoft, Windows, product names, company names, and trademarks belong to their respective owners. This is an independent informational project and is not affiliated with, sponsored by, or endorsed by any cited organization.
