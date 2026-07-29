# Accessibility

The project provides the same core guidance in multiple formats so readers can choose the format that works best for them.

## Available formats

- `docs/WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md` is the ordered, reflowable implementation path for Windows 11 Home.
- `docs/WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md` is the ordered, reflowable implementation path for Windows 11 Pro.
- `docs/ACCESSIBLE_GUIDE.md` is the comprehensive reference companion. It supports reflow, search, browser zoom, custom styles, and common screen-reader navigation. A stable-ID crosswalk connects its plain-language sections to the generated artifacts; clearly labeled supplemental topics do not create extra assessment results.
- `docs/Amys_Windows_11_Home_Security_Baseline_v1.0.0.pdf` and `docs/Amys_Windows_11_Pro_Security_Baseline_v1.0.0.pdf` are the designed visual implementation guides.
- `docs/Amys_Windows_11_Home_Assessment_Workbook_v1.0.0.pdf` and `docs/Amys_Windows_11_Pro_Assessment_Workbook_v1.0.0.pdf` are designed for printing and handwritten or local note-taking.
- `docs/CONTROL_FRAMEWORK_MAPPING.md` provides a text-based control crosswalk.

## Design requirements

Release review checks that:

- headings and sections follow a logical hierarchy;
- tables repeat headers and remain understandable without color alone;
- text and meaningful graphics have sufficient contrast;
- links use descriptive text;
- instructions do not rely only on position, shape, or color;
- fonts remain legible at the intended print size;
- every PDF page is reviewed for clipping, overlap, and ambiguous continuation; and
- each ordered accessible guide remains synchronized with its matching PDF and workbook;
- the comprehensive accessible reference's stable-ID crosswalk remains synchronized with the full control catalog.

## PDF limitation

PDF support varies by viewer and assistive technology. A visually correct PDF may still expose an incomplete structure tree or inconvenient reading order. The matching Home or Pro Markdown implementation guide is therefore the preferred accessible edition when the PDF does not work well with a reader's tools.

The printable workbook is not a secure evidence store. Readers should avoid writing sensitive recovery, credential, account, device, or network data in a copy that may be shared.

## Reporting an accessibility problem

Use the **Guide problem** issue form and select accessibility as the affected area. Describe the format, page or section, viewer or assistive technology, and the barrier encountered. Do not include sensitive device or account information.
