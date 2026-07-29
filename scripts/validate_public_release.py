from __future__ import annotations

from pathlib import Path
import hashlib
import re
import subprocess
import sys

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CHECKSUM_FILE = DOCS / "SHA256SUMS.txt"
sys.path.insert(0, str(ROOT / "src"))

from sbc_content import ASR_CANDIDATES

PDF_REQUIREMENTS = {
    DOCS / "Amys_Windows_11_Home_Security_Baseline_v1.0.0.pdf": {
        "edition": "Home",
        "kind": "guide",
        "title_fragment": "Windows 11 Home Security Baseline",
        "minimum_text": 50_000,
        "outline_required": True,
    },
    DOCS / "Amys_Windows_11_Home_Assessment_Workbook_v1.0.0.pdf": {
        "edition": "Home",
        "kind": "workbook",
        "title_fragment": "Windows 11 Home Assessment Workbook",
        "minimum_text": 10_000,
        "outline_required": True,
    },
    DOCS / "Amys_Windows_11_Pro_Security_Baseline_v1.0.0.pdf": {
        "edition": "Pro",
        "kind": "guide",
        "title_fragment": "Windows 11 Pro Security Baseline",
        "minimum_text": 55_000,
        "outline_required": True,
    },
    DOCS / "Amys_Windows_11_Pro_Assessment_Workbook_v1.0.0.pdf": {
        "edition": "Pro",
        "kind": "workbook",
        "title_fragment": "Windows 11 Pro Assessment Workbook",
        "minimum_text": 10_000,
        "outline_required": True,
    },
}

ACCESSIBLE_GUIDES = {
    "Home": DOCS / "WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md",
    "Pro": DOCS / "WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md",
}

REQUIRED_FILES = [
    ROOT / "LICENSE.md",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CHANGELOG.md",
    ROOT / "ACCESSIBILITY.md",
    ROOT / "THIRD_PARTY_NOTICES.md",
    ROOT / "CITATION.cff",
    *ACCESSIBLE_GUIDES.values(),
    DOCS / "ACCESSIBLE_GUIDE.md",
    DOCS / "CONTROL_FRAMEWORK_MAPPING.md",
    CHECKSUM_FILE,
]

FORBIDDEN_TEXT = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"discord(?:\.gg)?",
        r"support\s*@",
        r"private\s+work",
        r"chatgpt",
        r"codex",
        r"c:\\users\\",
        r"/users/",
        r"[a-z0-9._%+-]+@(?:gmail|me|outlook|hotmail|icloud)\.[a-z]{2,}",
        r"(?:api|access|auth|refresh)[_-]?token\s*[:=]\s*\S+",
        r"-----begin [a-z ]*private key-----",
        r"\b(?:host\s*name|serial\s*number|device\s*id|public\s*ip)\s*[:=]\s*\S+",
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    ]
]

TEXT_SUFFIXES = {".cff", ".md", ".py", ".txt", ".yaml", ".yml"}
ALLOWED_ACTIONS = {"/GoTo", "/URI"}
CONTROL_ID_PATTERN = re.compile(
    r"\b(?:GOV|REC|PLT|ID|DEF|APP|NET|LOG|OPS|PERF)-\d{2}\b"
)
STEP_ID_PATTERN = re.compile(r"(?m)^### Step (\d{2})\b")
PHASE_HEADING_PATTERN = re.compile(r"(?m)^## Phase (\d{2}) - (.+)$")


def fail(message: str) -> None:
    raise AssertionError(message)


def dereference(value):
    return value.get_object() if hasattr(value, "get_object") else value


def tracked_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths = []
    for raw_path in result.stdout.decode("utf-8").split("\0"):
        if not raw_path:
            continue
        path = ROOT / raw_path
        if path.suffix.lower() in TEXT_SUFFIXES:
            paths.append(path)
    return paths


def check_forbidden_text(label: str, text: str) -> None:
    for pattern in FORBIDDEN_TEXT:
        match = pattern.search(text)
        if match:
            fail(f"{label}: forbidden public-release text matched {pattern.pattern!r}")


def validate_repository_text() -> None:
    for path in tracked_text_files():
        relative = path.relative_to(ROOT)
        # Validation code intentionally contains red-flag strings as test
        # patterns. Public prose and the generator must not contain them.
        if relative.parts[0] in {"scripts", "tests"}:
            continue
        check_forbidden_text(
            str(path.relative_to(ROOT)),
            path.read_text(encoding="utf-8"),
        )


def validate_artifact_set() -> None:
    expected = {path.name for path in PDF_REQUIREMENTS}
    observed = {path.name for path in DOCS.glob("*.pdf")}
    if observed != expected:
        unexpected = sorted(observed - expected)
        missing = sorted(expected - observed)
        fail(
            "release PDF set is not exact; "
            f"missing={missing or 'none'}, unexpected={unexpected or 'none'}"
        )


def validate_checksums() -> None:
    expected = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in PDF_REQUIREMENTS
    }

    observed = {}
    lines = CHECKSUM_FILE.read_text(encoding="utf-8").splitlines()
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        if not match:
            fail(f"{CHECKSUM_FILE.name}: malformed checksum line {line!r}")
        digest, filename = match.groups()
        if filename in observed:
            fail(f"{CHECKSUM_FILE.name}: duplicate entry for {filename}")
        observed[filename] = digest

    if list(observed) != sorted(observed):
        fail(f"{CHECKSUM_FILE.name}: entries must be alphabetically sorted")
    if observed != expected:
        fail(f"{CHECKSUM_FILE.name}: entries do not match the current release PDFs")


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_control_ids(text: str) -> set[str]:
    return set(CONTROL_ID_PATTERN.findall(text))


def validate_accessible_phase_outline(edition: str, text: str) -> None:
    phases = PHASE_HEADING_PATTERN.findall(text)
    if not phases:
        fail(f"{edition} accessible guide has no ordered phase headings")
    expected_numbers = [
        f"{number:02d}" for number in range(1, len(phases) + 1)
    ]
    observed_numbers = [number for number, _ in phases]
    if observed_numbers != expected_numbers:
        fail(
            f"{edition} accessible guide phase order is wrong: "
            f"{observed_numbers}"
        )
    if len(phases) != len(set(phases)):
        fail(f"{edition} accessible guide has duplicate phase headings")

    seen = set()
    for _, label in phases:
        base_label = re.sub(r" \(continued(?: \d+)?\)$", "", label)
        is_continuation = bool(
            re.search(r" \(continued(?: \d+)?\)$", label)
        )
        if base_label in seen and not is_continuation:
            fail(
                f"{edition} accessible guide ambiguously repeats phase "
                f"{base_label!r}"
            )
        if base_label not in seen and is_continuation:
            fail(
                f"{edition} accessible guide labels first phase occurrence "
                f"as a continuation: {label!r}"
            )
        seen.add(base_label)


def validate_edition_sync() -> None:
    for edition in ("Home", "Pro"):
        guide = next(
            path
            for path, settings in PDF_REQUIREMENTS.items()
            if settings["edition"] == edition and settings["kind"] == "guide"
        )
        workbook = next(
            path
            for path, settings in PDF_REQUIREMENTS.items()
            if settings["edition"] == edition and settings["kind"] == "workbook"
        )
        accessible = ACCESSIBLE_GUIDES[edition]

        guide_ids = extract_control_ids(extract_pdf_text(guide))
        workbook_ids = extract_control_ids(extract_pdf_text(workbook))
        accessible_text = accessible.read_text(encoding="utf-8")
        accessible_ids = extract_control_ids(accessible_text)

        if len(guide_ids) < 30:
            fail(f"{edition} guide contains too few stable control IDs")
        if workbook_ids != guide_ids:
            fail(f"{edition} guide and workbook stable control IDs do not match")
        missing = guide_ids - accessible_ids
        if missing:
            fail(
                f"{edition} accessible guide is missing stable control IDs: "
                + ", ".join(sorted(missing))
            )

        expected_step_count = 24 if edition == "Home" else 25
        expected_steps = [
            f"{step:02d}" for step in range(1, expected_step_count + 1)
        ]
        observed_steps = STEP_ID_PATTERN.findall(accessible_text)
        if observed_steps != expected_steps:
            fail(
                f"{edition} accessible guide step order is wrong: "
                f"{observed_steps}"
            )
        if "[LICENSE.md](../LICENSE.md)" not in accessible_text:
            fail(f"{edition} accessible guide license reference is not linked")
        if "## ASR candidate appendix" not in accessible_text:
            fail(f"{edition} accessible guide is missing the ASR appendix")
        if (
            "This is a candidate reference, not a recommendation to enable every rule."
            not in accessible_text
        ):
            fail(f"{edition} accessible guide is missing ASR safety guidance")
        for guid, title, note in ASR_CANDIDATES:
            expected_row = f"| `{guid}` | {title} | {note} |"
            if expected_row not in accessible_text:
                fail(
                    f"{edition} accessible guide is missing the complete "
                    f"ASR candidate row for {guid}"
                )
        validate_accessible_phase_outline(edition, accessible_text)

    home_accessible = ACCESSIBLE_GUIDES["Home"].read_text(encoding="utf-8")
    if "Set-MpPreference -EnableNetworkProtection" in home_accessible:
        fail("Home implementation path contains a Pro-only Network Protection command")
    pro_accessible = ACCESSIBLE_GUIDES["Pro"].read_text(encoding="utf-8")
    if "Set-MpPreference -EnableNetworkProtection AuditMode" not in pro_accessible:
        fail("Pro implementation path is missing Network Protection audit mode")


def validate_action(action, label: str) -> int:
    action = dereference(action)
    action_type = str(action.get("/S", ""))
    if action_type not in ALLOWED_ACTIONS:
        fail(f"{label}: unsupported PDF action {action_type or '<missing>'}")
    if action_type == "/URI":
        uri = str(action.get("/URI", ""))
        if not uri.startswith("https://"):
            fail(f"{label}: URI must use HTTPS: {uri!r}")
        return 1
    return 0


def validate_pdf(path: Path, settings: dict[str, object]) -> tuple[int, int, int]:
    if not path.is_file():
        fail(f"missing release artifact: {path.relative_to(ROOT)}")

    reader = PdfReader(path)
    if not reader.pages:
        fail(f"{path.name}: PDF has no pages")
    if reader.is_encrypted:
        fail(f"{path.name}: release PDF must not be encrypted")

    metadata = reader.metadata
    title = str(getattr(metadata, "title", "") or "")
    author = str(getattr(metadata, "author", "") or "")
    if settings["title_fragment"] not in title:
        fail(f"{path.name}: unexpected title metadata {title!r}")
    if author != "Amyashi":
        fail(f"{path.name}: unexpected author metadata {author!r}")

    catalog = dereference(reader.trailer["/Root"])
    language = str(catalog.get("/Lang", ""))
    if not language.lower().startswith("en"):
        fail(f"{path.name}: missing English document-language metadata")

    for key in ["/OpenAction", "/AA", "/AcroForm"]:
        if catalog.get(key) is not None:
            fail(f"{path.name}: unsupported catalog entry {key}")

    names = dereference(catalog.get("/Names", {})) or {}
    for key in ["/JavaScript", "/EmbeddedFiles"]:
        if names.get(key) is not None:
            fail(f"{path.name}: unsupported active or embedded content {key}")

    if settings["outline_required"]:
        try:
            if not reader.outline:
                fail(f"{path.name}: PDF must contain navigation bookmarks")
        except Exception as exc:
            fail(f"{path.name}: could not read outline: {exc}")

    page_text = []
    uri_count = 0
    for page_number, page in enumerate(reader.pages, 1):
        if page.get("/AA") is not None:
            fail(f"{path.name}, page {page_number}: additional actions are not allowed")
        page_text.append(page.extract_text() or "")
        for annotation_ref in page.get("/Annots", []):
            annotation = dereference(annotation_ref)
            if annotation.get("/AA") is not None:
                fail(
                    f"{path.name}, page {page_number}: annotation additional "
                    "actions are not allowed"
                )
            action = annotation.get("/A")
            if action is not None:
                uri_count += validate_action(
                    action,
                    f"{path.name}, page {page_number}",
                )

    text = "\n".join(page_text)
    if len(text) < int(settings["minimum_text"]):
        fail(f"{path.name}: extracted text is unexpectedly short ({len(text)} characters)")
    check_forbidden_text(path.name, text)

    if not re.search(r"CC\s+BY-NC-ND\s+4\.0", text, re.IGNORECASE):
        fail(f"{path.name}: missing controlled-author license notice")
    if not re.search(
        r"informational|not\s+(?:a\s+)?certification",
        text,
        re.IGNORECASE,
    ):
        fail(f"{path.name}: missing informational-use limitation")

    edition = str(settings["edition"])
    if f"Windows 11 {edition}" not in text:
        fail(f"{path.name}: edition label is missing")

    return len(reader.pages), uri_count, len(text)


def main() -> int:
    missing = [
        str(path.relative_to(ROOT))
        for path in REQUIRED_FILES
        if not path.is_file()
    ]
    if missing:
        fail("missing required public-release files: " + ", ".join(missing))

    for path in [
        *ACCESSIBLE_GUIDES.values(),
        DOCS / "ACCESSIBLE_GUIDE.md",
        DOCS / "CONTROL_FRAMEWORK_MAPPING.md",
    ]:
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 1_000:
            fail(f"{path.relative_to(ROOT)} is unexpectedly short")
        check_forbidden_text(str(path.relative_to(ROOT)), text)

    validate_repository_text()
    validate_artifact_set()
    validate_checksums()
    validate_edition_sync()

    summaries = []
    for path, settings in PDF_REQUIREMENTS.items():
        pages, links, characters = validate_pdf(path, settings)
        summaries.append(
            f"{path.name}: {pages} pages, {links} HTTPS links, "
            f"{characters} extracted characters"
        )

    print("PASS: public-release repository and artifact checks")
    for summary in summaries:
        print(f"  {summary}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
