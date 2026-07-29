from pathlib import Path
import re
import sys

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "src"))

from sbc_content import ASR_CANDIDATES

HOME_GUIDE = DOCS / "Amys_Windows_11_Home_Security_Baseline_v1.0.0.pdf"
HOME_WORKBOOK = DOCS / "Amys_Windows_11_Home_Assessment_Workbook_v1.0.0.pdf"
PRO_GUIDE = DOCS / "Amys_Windows_11_Pro_Security_Baseline_v1.0.0.pdf"
PRO_WORKBOOK = DOCS / "Amys_Windows_11_Pro_Assessment_Workbook_v1.0.0.pdf"

EXPECTED = {
    HOME_GUIDE: {
        "title": "Amy's Windows 11 Home Security Baseline",
        "subject": (
            "Ordered Windows 11 Home security implementation guide with commands, "
            "restart gates, verification, rollback, and evidence controls"
        ),
        "artifact_keyword": "implementation guide",
        "pages": (30, 45),
        "outlines": 8,
        "links": 90,
        "required": [
            "Windows 11 Home",
            "Quick implementation path",
            "Step 01",
            "RESTART NOW?",
            "PASS LOOKS LIKE",
            "IF IT DOES NOT PASS",
            "ROLLBACK / RECOVERY",
            "Pro-only capabilities excluded from Home",
            "ASR candidate appendix",
            "Microsoft Defender Network Protection",
            "Home can be a Remote Desktop client",
            "IEEE-style references",
            "CC BY-NC-ND 4.0",
        ],
        "forbidden": [
            "Set-MpPreference -EnableNetworkProtection",
            "Turn Remote Desktop on and confirm",
            "Enable command-line content in Event 4688",
        ],
    },
    HOME_WORKBOOK: {
        "title": "Amy's Windows 11 Home Assessment Workbook",
        "subject": (
            "Printable ordered assessment workbook for the Windows 11 Home "
            "Security Baseline"
        ),
        "artifact_keyword": "assessment workbook",
        "pages": (8, 18),
        "outlines": 3,
        "links": 0,
        "required": [
            "Windows 11 Home",
            "PRINTABLE / BLANK ASSESSMENT RECORD",
            "STEP 01",
            "Result:",
            "Restart completed:",
            "Sanitized result / evidence reference:",
            "HOLD / exception / rollback:",
            "INITIAL STATUS: NOT ASSESSED",
            "Final sign-off summary",
            "Overall disposition",
            "Home edition-excluded register",
            "CC BY-NC-ND 4.0",
        ],
        "forbidden": [],
    },
    PRO_GUIDE: {
        "title": "Amy's Windows 11 Pro Security Baseline",
        "subject": (
            "Ordered Windows 11 Pro security implementation guide with commands, "
            "restart gates, verification, rollback, and evidence controls"
        ),
        "artifact_keyword": "implementation guide",
        "pages": (32, 47),
        "outlines": 9,
        "links": 90,
        "required": [
            "Windows 11 Pro",
            "Quick implementation path",
            "Step 01",
            "RESTART NOW?",
            "PASS LOOKS LIKE",
            "IF IT DOES NOT PASS",
            "ROLLBACK / RECOVERY",
            "Get-BitLockerVolume",
            "Set-MpPreference -EnableNetworkProtection AuditMode",
            "If required, use Appendix D",
            "Only for a defined investigative need, use Appendix E",
            "Pro baseline path",
            "Optional Pro Remote Desktop host",
            "Optional Pro Event 4688",
            "IEEE-style references",
            "CC BY-NC-ND 4.0",
        ],
        "forbidden": [
            "FULL-GUID-FROM-APPENDIX-B",
            "off by default on the Home path",
        ],
    },
    PRO_WORKBOOK: {
        "title": "Amy's Windows 11 Pro Assessment Workbook",
        "subject": (
            "Printable ordered assessment workbook for the Windows 11 Pro "
            "Security Baseline"
        ),
        "artifact_keyword": "assessment workbook",
        "pages": (8, 18),
        "outlines": 3,
        "links": 0,
        "required": [
            "Windows 11 Pro",
            "PRINTABLE / BLANK ASSESSMENT RECORD",
            "STEP 01",
            "Result:",
            "Restart completed:",
            "Sanitized result / evidence reference:",
            "HOLD / exception / rollback:",
            "INITIAL STATUS: NOT ASSESSED",
            "Final sign-off summary",
            "Overall disposition",
            "CC BY-NC-ND 4.0",
        ],
        "forbidden": [],
    },
}

CONTROL_IDS = [
    "GOV-01", "GOV-02",
    "REC-01", "REC-02", "REC-03",
    "PLT-01", "PLT-02", "PLT-03", "PLT-04", "PLT-05", "PLT-06",
    "ID-01", "ID-02", "ID-03",
    "DEF-01", "DEF-02", "DEF-03", "DEF-04", "DEF-05", "DEF-06", "DEF-07",
    "APP-01", "APP-02",
    "NET-01", "NET-02", "NET-03", "NET-04",
    "LOG-01", "LOG-02", "LOG-03",
    "OPS-01", "OPS-02", "OPS-03", "OPS-04",
    "PERF-01", "PERF-02",
]

FORBIDDEN_PUBLIC_TEXT = [
    "discord.gg",
    "support@",
    "@gmail",
    "@me.com",
    "prior conversation",
    "prior chat",
    "ChatGPT",
    "Codex",
    "C:\\Users\\",
    "/Users/",
    "CURRENT DEVICE STATE",
    "PRIOR DEVICE EVIDENCE",
    "VERIFIED DEVICE STATE",
    "HOST NAME:",
    "SERIAL NUMBER:",
    "DEVICE ID:",
    "PUBLIC IP:",
]

ACCESSIBLE_GUIDES = {
    "Home": DOCS / "WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md",
    "Pro": DOCS / "WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md",
}


def count_outlines(items):
    total = 0
    for item in items:
        total += count_outlines(item) if isinstance(item, list) else 1
    return total


def inspect_uri_annotations(reader):
    uris = []
    for page_number, page in enumerate(reader.pages, 1):
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            assert annotation.get("/Subtype") == "/Link", (page_number, annotation)
            action = annotation.get("/A")
            assert action and action.get("/S") == "/URI", (page_number, action)
            uri = action.get("/URI")
            assert isinstance(uri, str) and uri.startswith("https://"), (
                page_number,
                uri,
            )
            uris.append(uri)
    return uris


def assert_no_active_content(reader):
    root = reader.trailer["/Root"]
    assert "/AcroForm" not in root
    assert "/OpenAction" not in root
    assert "/AA" not in root
    assert not (reader.get_fields() or {})
    names = root.get("/Names")
    if names:
        names = names.get_object()
        assert "/JavaScript" not in names
        assert "/EmbeddedFiles" not in names
    for page_number, page in enumerate(reader.pages, 1):
        assert "/AA" not in page, page_number
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            assert annotation.get("/Subtype") != "/Widget", page_number
            assert "/AA" not in annotation, page_number


def assert_bounds_and_fonts(path):
    allowed_base14_fonts = {"Helvetica", "Helvetica-Bold", "Courier"}
    with pdfplumber.open(path) as document:
        for page_number, page in enumerate(document.pages, 1):
            assert round(page.width, 1) == 792.0
            assert round(page.height, 1) == 612.0
            for char in page.chars:
                assert -0.5 <= char["x0"] <= page.width + 0.5, (
                    page_number,
                    char["text"],
                    char["x0"],
                )
                assert -0.5 <= char["x1"] <= page.width + 0.5, (
                    page_number,
                    char["text"],
                    char["x1"],
                )
                assert -0.5 <= char["top"] <= page.height + 0.5, (
                    page_number,
                    char["text"],
                    char["top"],
                )
                assert -0.5 <= char["bottom"] <= page.height + 0.5, (
                    page_number,
                    char["text"],
                    char["bottom"],
                )
                assert char["size"] >= 7.0, (
                    page_number,
                    char["text"],
                    char["size"],
                )
                assert char["fontname"] in allowed_base14_fonts, (
                    page_number,
                    char["text"],
                    char["fontname"],
                )


def validate_pdf(path, rules):
    assert path.exists() and path.stat().st_size > 20_000, path
    reader = PdfReader(path)
    low, high = rules["pages"]
    assert low <= len(reader.pages) <= high, (path.name, len(reader.pages))

    metadata = reader.metadata
    assert metadata.title == rules["title"], (path.name, metadata.title)
    assert metadata.author == "Amyashi", (path.name, metadata.author)
    assert metadata.subject == rules["subject"], (path.name, metadata.subject)
    assert metadata.creator == "Amyashi", (path.name, metadata.creator)
    keywords = (metadata.get("/Keywords") or "").lower()
    assert "least privilege" in keywords
    assert rules["artifact_keyword"] in keywords
    if rules["artifact_keyword"] == "implementation guide":
        assert "assessment workbook" not in keywords

    root = reader.trailer["/Root"]
    assert root.get("/Lang") == "en-US"
    viewer = root.get("/ViewerPreferences")
    assert viewer and bool(viewer.get_object().get("/DisplayDocTitle")) is True
    outlines = count_outlines(reader.outline)
    assert outlines >= rules["outlines"], (path.name, outlines)

    page_text = [page.extract_text() or "" for page in reader.pages]
    normalized = re.sub(r"\s+", " ", "\n".join(page_text))
    for required in rules["required"]:
        assert required in normalized, (path.name, required)
    for forbidden in FORBIDDEN_PUBLIC_TEXT + rules["forbidden"]:
        assert forbidden.lower() not in normalized.lower(), (path.name, forbidden)
    for control_id in CONTROL_IDS:
        assert control_id in normalized, (path.name, control_id)
    for page_number, text in enumerate(page_text, 1):
        assert len(text.strip()) >= 150, (path.name, page_number, len(text.strip()))

    assert_no_active_content(reader)
    uris = inspect_uri_annotations(reader)
    assert len(uris) >= rules["links"], (path.name, len(uris))
    assert_bounds_and_fonts(path)
    return len(reader.pages), len(uris), outlines


def step_ids(text):
    return re.findall(r"(?m)^### Step (\d{2})\b", text)


def validate_accessible_phase_outline(path, text):
    phases = re.findall(r"(?m)^## Phase (\d{2}) - (.+)$", text)
    assert phases, (path.name, "missing ordered phase headings")
    assert [number for number, _ in phases] == [
        f"{number:02d}" for number in range(1, len(phases) + 1)
    ], (path.name, phases)
    assert len(phases) == len(set(phases)), (path.name, phases)

    seen = set()
    for _, label in phases:
        base_label = re.sub(r" \(continued(?: \d+)?\)$", "", label)
        if base_label in seen:
            assert re.search(r" \(continued(?: \d+)?\)$", label), (
                path.name,
                label,
            )
        else:
            assert "(continued" not in label, (path.name, label)
            seen.add(base_label)


def validate_accessible_sync():
    for edition, path in ACCESSIBLE_GUIDES.items():
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert f"# Windows 11 {edition} Security Baseline" in text
        assert "[LICENSE.md](../LICENSE.md)" in text
        assert "#### Restart now?" in text
        assert "**PASS looks like:**" in text
        assert "**If it does not pass:**" in text
        assert "**Rollback / recovery:**" in text
        assert "**Record only:**" in text
        assert "## ASR candidate appendix" in text
        assert (
            "This is a candidate reference, not a recommendation to enable every rule."
            in text
        )
        for guid, title, note in ASR_CANDIDATES:
            assert f"| `{guid}` | {title} | {note} |" in text, (
                path.name,
                guid,
            )
        validate_accessible_phase_outline(path, text)
        assert step_ids(text) == [f"{number:02d}" for number in range(1, 25 + (edition == "Pro"))]
        for forbidden in FORBIDDEN_PUBLIC_TEXT:
            assert forbidden.lower() not in text.lower(), (path.name, forbidden)
    home_text = ACCESSIBLE_GUIDES["Home"].read_text(encoding="utf-8")
    assert "Set-MpPreference -EnableNetworkProtection" not in home_text
    pro_text = ACCESSIBLE_GUIDES["Pro"].read_text(encoding="utf-8")
    assert "Set-MpPreference -EnableNetworkProtection AuditMode" in pro_text


results = {path.name: validate_pdf(path, rules) for path, rules in EXPECTED.items()}
validate_accessible_sync()
for name, (pages, links, outlines) in results.items():
    print(
        f"PASS: {name}: {pages} pages, {links} HTTPS links, "
        f"{outlines} outline entries, valid bounds and no active content"
    )
