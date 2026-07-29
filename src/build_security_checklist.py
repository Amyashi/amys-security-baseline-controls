from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from sbc_content import (
    ASR_CANDIDATES,
    HOME_STEPS,
    HOME_UNAVAILABLE,
    PRO_STEPS,
    RESULT_STATES,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
HOME_GUIDE_OUT = DOCS / "Amys_Windows_11_Home_Security_Baseline_v1.0.0.pdf"
HOME_WORKBOOK_OUT = DOCS / "Amys_Windows_11_Home_Assessment_Workbook_v1.0.0.pdf"
PRO_GUIDE_OUT = DOCS / "Amys_Windows_11_Pro_Security_Baseline_v1.0.0.pdf"
PRO_WORKBOOK_OUT = DOCS / "Amys_Windows_11_Pro_Assessment_Workbook_v1.0.0.pdf"
HOME_ACCESSIBLE_OUT = DOCS / "WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md"
PRO_ACCESSIBLE_OUT = DOCS / "WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md"
CHECKSUM_OUT = DOCS / "SHA256SUMS.txt"
RELEASE_PDFS = (
    HOME_GUIDE_OUT,
    HOME_WORKBOOK_OUT,
    PRO_GUIDE_OUT,
    PRO_WORKBOOK_OUT,
)
VERSION = "1.0.0"
SOURCE_REVIEW_DATE = "29 July 2026"
SOURCE_ACCESS_DATE = "Jul. 29, 2026"
PDF_BUILD_EPOCH = "1785326400"  # 29 July 2026 12:00 UTC
AUTHOR = "Amyashi"

PAGE_W, PAGE_H = landscape(letter)
MARGIN_X = 28
TOP = 44
BOTTOM = 36
CONTENT_W = PAGE_W - 2 * MARGIN_X
CONTENT_H = PAGE_H - TOP - BOTTOM

NAVY = colors.HexColor("#132238")
BLUE = colors.HexColor("#2459A6")
TEAL = colors.HexColor("#0B756B")
INK = colors.HexColor("#172333")
MUTED = colors.HexColor("#4E5E70")
GRID = colors.HexColor("#AAB6C5")
PALE_BLUE = colors.HexColor("#EAF1FA")
PALE_TEAL = colors.HexColor("#E7F3F1")
PALE_AMBER = colors.HexColor("#FFF4D8")
PALE_GRAY = colors.HexColor("#F3F5F7")
WHITE = colors.white


def make_styles():
    styles = getSampleStyleSheet()
    definitions = [
        ("CoverTitle", "Helvetica-Bold", 26, 30, WHITE, 0),
        ("H1", "Helvetica-Bold", 18, 22, NAVY, 6),
        ("H2", "Helvetica-Bold", 12, 15, BLUE, 4),
        ("StepTitle", "Helvetica-Bold", 13.2, 16, NAVY, 4),
        ("Body", "Helvetica", 9.2, 12.2, INK, 6),
        ("BodySmall", "Helvetica", 8.6, 10.8, INK, 3),
        ("Cell", "Helvetica", 8.6, 10.8, INK, 0),
        ("CellBold", "Helvetica-Bold", 8.7, 10.8, INK, 0),
        ("CellHeader", "Helvetica-Bold", 8.5, 10, WHITE, 0),
        ("MatrixCell", "Helvetica", 7.9, 9.5, INK, 0),
        ("MatrixStatus", "Helvetica-Bold", 7.9, 9.5, NAVY, 0),
        ("SBCCode", "Courier", 8.1, 10.2, INK, 0),
        ("Reference", "Helvetica", 8.1, 9.6, INK, 0),
        ("WorkbookField", "Helvetica", 8.8, 11, INK, 0),
    ]
    for name, font, size, leading, color, after in definitions:
        styles.add(
            ParagraphStyle(
                name=name,
                fontName=font,
                fontSize=size,
                leading=leading,
                textColor=color,
                spaceAfter=after,
                keepWithNext=name in {"H1", "H2"},
            )
        )
    styles.add(
        ParagraphStyle(
            name="Status",
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=10.5,
            textColor=NAVY,
            alignment=TA_CENTER,
        )
    )
    return styles


STYLES = make_styles()


@dataclass(frozen=True)
class Control:
    control_id: str
    priority: str
    section: str
    title: str
    purpose: str
    target: str
    verify: str
    summary: str


CONTROLS = [
    Control(
        "GOV-01", "P0", "0. Read first: authority, scope, and recovery",
        "Managed-device authority stop",
        "Prevents a personal checklist from overriding an organization.",
        "<b>Target:</b> Confirm the device is personally owned and not governed by an employer, school, client, "
        "domain, or mobile-device-management policy. If management or an unknown work or school connection is present, "
        "<b>stop and contact the authorized administrator</b>. Do not disconnect management or bypass policy.",
        "<b>Verify:</b> Review Settings - Accounts - Access work or school and run "
        "<font name='Courier'>dsregcmd /status</font>. <b>Stop:</b> Any unknown tenant, domain, management URL, "
        "policy banner, or organization account is present.",
        "Authority is confirmed; managed devices are referred to the authorized administrator.",
    ),
    Control(
        "GOV-02", "P0", "0. Read first: authority, scope, and recovery",
        "Evidence minimization and handling",
        "Security evidence can expose identifiers, secrets, and personal data.",
        "<b>Target:</b> Record only the control ID, result, date, method, and minimum evidence needed. Never place "
        "recovery keys, passwords, tokens, serial numbers, public IPs, user paths, raw dumps, secret-bearing command "
        "lines, or unredacted logs in this workbook or repository.",
        "<b>Verify:</b> Review evidence before sharing; restrict sensitive material to people who need it. "
        "<b>Stop:</b> Move sensitive evidence to an access-controlled location and redact the shared copy.",
        "Evidence is minimal, redacted, access-controlled, and stored outside public repositories when sensitive.",
    ),
    Control(
        "REC-01", "P0", "0. Read first: authority, scope, and recovery",
        "Restorable backup",
        "A backup is useful only when required data can be restored.",
        "<b>Target:</b> Maintain a current copy that is not continuously writable from the normal user session. "
        "Define critical data and test a representative restore before firmware, encryption, identity, or policy changes.",
        "<b>Verify:</b> Restore a harmless sample to a separate location and open it. Record the date and scope, not "
        "the data. <b>Stop:</b> No independent copy exists, the restore fails, or the only copy mirrors deletion.",
        "A representative restore succeeds from a current copy isolated from routine write access.",
    ),
    Control(
        "REC-02", "P0", "0. Read first: authority, scope, and recovery",
        "Drive-recovery readiness",
        "Platform changes can trigger an encryption recovery prompt.",
        "<b>Target:</b> Determine whether Device Encryption or BitLocker is active. When active, prove the matching "
        "recovery key is accessible from an independent trusted location. Do not copy the key into assessment evidence.",
        "<b>Verify:</b> Use Windows encryption settings and, where available, "
        "<font name='Courier'>manage-bde -status</font>. Match only the key identifier. "
        "<b>Stop:</b> Encryption is active and the matching recovery method cannot be proved.",
        "Encryption state is known and its recovery method is accessible without recording the secret.",
    ),
    Control(
        "REC-03", "P0", "0. Read first: authority, scope, and recovery",
        "Recovery environment and administrator",
        "A tested recovery path prevents a hardening error from becoming an outage.",
        "<b>Target:</b> Windows Recovery Environment is enabled, recovery media is available when appropriate, and "
        "a separate recovery administrator can sign in. The recovery account is not used for routine work.",
        "<b>Verify:</b> Run <font name='Courier'>reagentc /info</font> and test a normal sign-in with the recovery "
        "administrator. <b>Stop:</b> Do not demote or remove an account until recovery access works.",
        "Windows RE and an independent administrator sign-in are tested.",
    ),
    Control(
        "PLT-01", "P1", "1. Platform trust and data protection",
        "Supported Windows and updates",
        "Supported, current software receives security fixes.",
        "<b>Target:</b> Run a supported Windows 11 edition and service release. Install normal security updates through "
        "Windows Update unless Microsoft or the device vendor documents a safeguard hold for the exact hardware.",
        "<b>Verify:</b> Run <font name='Courier'>winver</font>; review Windows Update; record edition, release, pending "
        "restart, and any hold. <b>Stop:</b> Do not force an update around a documented compatibility hold.",
        "Windows is supported, security updates are current, and any compatibility hold is documented.",
    ),
    Control(
        "PLT-02", "P0", "1. Platform trust and data protection",
        "UEFI boot and Secure Boot",
        "Secure Boot helps protect the pre-operating-system trust chain.",
        "<b>Target:</b> Use UEFI boot with Secure Boot enabled when supported. Pass REC-02 before changing keys, boot "
        "mode, or firmware.",
        "<b>Verify:</b> Run <font name='Courier'>Confirm-SecureBootUEFI</font> and review BIOS Mode plus Secure Boot "
        "State in <font name='Courier'>msinfo32</font>. <b>Stop:</b> Never clear or replace keys as an unplanned shortcut.",
        "Windows reports UEFI mode and Secure Boot enabled; recovery readiness passes first.",
    ),
    Control(
        "PLT-03", "P0", "1. Platform trust and data protection",
        "TPM health",
        "The TPM protects keys and platform measurements.",
        "<b>Target:</b> TPM is present, ready, enabled, activated, and not locked out. Clearing a TPM is outside this baseline.",
        "<b>Verify:</b> In elevated PowerShell run "
        "<font name='Courier'>Get-Tpm | Format-List TpmPresent,TpmReady,TpmEnabled,TpmActivated,LockedOut</font>. "
        "<b>Stop:</b> Do not clear the TPM; first identify encryption, sign-in, and management dependencies.",
        "TPM health fields pass without clearing, reprovisioning, or exposing key material.",
    ),
    Control(
        "PLT-04", "P2", "1. Platform trust and data protection",
        "Virtualization and DMA remapping",
        "Virtualization supports VBS; DMA remapping can isolate capable devices.",
        "<b>Target:</b> Enable CPU virtualization when VBS is intended. Treat Intel VT-d or AMD IOMMU as a separate "
        "firmware setting. Kernel DMA Protection depends on edition, hardware, firmware, and drivers.",
        "<b>Verify:</b> Review Task Manager - Performance - CPU and <font name='Courier'>msinfo32</font>. "
        "<b>Stop:</b> Do not treat one virtualization field as proof of every protection.",
        "CPU virtualization and supported DMA protections are separately inventoried and tested.",
    ),
    Control(
        "PLT-05", "P1", "1. Platform trust and data protection",
        "Exact-model firmware servicing",
        "Firmware may fix vulnerabilities but can reset security and stability settings.",
        "<b>Target:</b> Use only the support page, release notes, and updater for the exact system or motherboard model "
        "and revision. Record prerequisites, recovery, stable power, and prior settings before one update.",
        "<b>Verify:</b> Inventory with <font name='Courier'>Get-CimInstance Win32_BaseBoard</font> and "
        "<font name='Courier'>Get-CimInstance Win32_BIOS</font>. <b>Stop:</b> Wrong model, unclear prerequisite, "
        "unstable device, or unavailable recovery.",
        "Exact-model applicability, prerequisites, recovery, power, and post-update checks are documented.",
    ),
    Control(
        "PLT-06", "P1", "1. Platform trust and data protection",
        "Data-at-rest encryption",
        "Encryption limits disclosure from lost powered-off storage.",
        "<b>Target:</b> Use supported Device Encryption or BitLocker when compatible with the owner's recovery model. "
        "Protect recovery material separately and restrict access.",
        "<b>Verify:</b> Review Windows encryption settings and <font name='Courier'>manage-bde -status</font> where "
        "supported. <b>Stop:</b> Do not enable encryption until REC-02 and REC-03 pass.",
        "Supported encryption is intentional and its recovery path is proven.",
    ),
    Control(
        "ID-01", "P1", "2. Identity and least privilege",
        "Standard daily-use account",
        "Separating routine work from administration limits system-wide changes.",
        "<b>Target:</b> Use a standard account for routine work and a separate administrator only for deliberate elevation. "
        "Keep at least one tested recovery administrator.",
        "<b>Verify:</b> Run <font name='Courier'>Get-LocalGroupMember -Group Administrators</font> and review each "
        "enabled account. <b>Stop:</b> Do not remove or demote the last tested recovery administrator.",
        "Routine work uses a standard account and administration requires deliberate elevation.",
    ),
    Control(
        "ID-02", "P1", "2. Identity and least privilege",
        "Strong sign-in and recovery",
        "Strong authentication and independent recovery reduce takeover and lockout risk.",
        "<b>Target:</b> Use phishing-resistant authentication where supported, retain two independent recovery methods, "
        "and protect recovery codes offline. Avoid SMS as the only recovery factor.",
        "<b>Verify:</b> Review the account security page without capturing secrets or recovery codes. "
        "<b>Stop:</b> Do not remove an old factor until the replacement and recovery path are tested.",
        "Strong authentication and two independent recovery methods are configured and tested.",
    ),
    Control(
        "ID-03", "P1", "2. Identity and least privilege",
        "User Account Control",
        "UAC creates a visible boundary before administrative changes.",
        "<b>Target:</b> Keep UAC at the Windows default level or higher with secure-desktop prompts. An elevation prompt "
        "is authorization friction, not proof that software is trustworthy.",
        "<b>Verify:</b> Review UAC settings and perform a harmless Run as administrator prompt, then cancel. "
        "<b>Stop:</b> Never use Never notify as a performance workaround.",
        "UAC is default-or-higher and elevation is a deliberate, visible action.",
    ),
    Control(
        "DEF-01", "P1", "3. Malware, application, and exploit protection",
        "Active and current antimalware",
        "Dependent protections cannot be trusted when the provider is passive or stale.",
        "<b>Target:</b> Microsoft Defender Antivirus or another intentionally selected provider is active and current. "
        "Identify the controlling product or policy before troubleshooting.",
        "<b>Verify:</b> For Defender, inspect selected fields from <font name='Courier'>Get-MpComputerStatus</font>. "
        "<b>Stop:</b> Fix provider ownership and updates before tuning advanced controls.",
        "The intended antimalware provider is active, healthy, and current.",
    ),
    Control(
        "DEF-02", "P1", "3. Malware, application, and exploit protection",
        "Runtime and tamper protection",
        "Runtime scanning and tamper resistance prevent silent weakening.",
        "<b>Target:</b> Real-time, behavior, IOAV, and tamper protections are enabled unless an authorized policy "
        "documents an exception.",
        "<b>Verify:</b> Review Windows Security and selected <font name='Courier'>Get-MpComputerStatus</font> fields. "
        "<b>Stop:</b> Do not defeat tamper protection through unsupported registry or service changes.",
        "Runtime protections and tamper resistance are enabled or an authorized exception exists.",
    ),
    Control(
        "DEF-03", "P1", "3. Malware, application, and exploit protection",
        "Cloud and sample protection",
        "Cloud analysis improves detection; sample handling requires a privacy decision.",
        "<b>Target:</b> Enable cloud protection for this baseline and choose sample-submission behavior consistent with "
        "privacy requirements. Record an intentional exception rather than bypassing policy.",
        "<b>Verify:</b> Review Windows Security and MAPSReporting plus SubmitSamplesConsent from "
        "<font name='Courier'>Get-MpPreference</font>. <b>Stop:</b> Unknown policy ownership invokes GOV-01.",
        "Cloud protection is enabled and sample handling is an intentional privacy choice.",
    ),
    Control(
        "DEF-04", "P1", "3. Malware, application, and exploit protection",
        "Potentially unwanted application blocking",
        "PUA blocking reduces bundlers and deceptive software.",
        "<b>Target:</b> Use Block mode and review each detection before allowing software. Verify publisher, source, hash, and need.",
        "<b>Verify:</b> Run <font name='Courier'>Get-MpPreference | Select-Object PUAProtection</font> and review "
        "Protection History. <b>Stop:</b> Do not allow a detection solely because a workflow is interrupted.",
        "PUA protection is in Block mode and retained exceptions have a verified need and source.",
    ),
    Control(
        "DEF-05", "P2", "3. Malware, application, and exploit protection",
        "Attack Surface Reduction rules",
        "ASR can block common attack behaviors but requires staged compatibility testing.",
        "<b>Target:</b> Inventory exact GUID/action pairs, select rules by documented applicability, begin in Audit where "
        "appropriate, and move one rule at a time to Warn or Block after representative testing.",
        "<b>Verify:</b> Use Runbook 2, which handles empty or mismatched arrays and displays full GUIDs. "
        "<b>Stop:</b> Never bulk-enable a copied rule set or add a broad exclusion to hide an unexplained block.",
        "Applicable ASR rules have full GUIDs, explicit modes, owners, tests, and narrow exceptions.",
    ),
    Control(
        "DEF-06", "P2", "3. Malware, application, and exploit protection",
        "Controlled Folder Access",
        "CFA can limit ransomware writes but may block legitimate workflows.",
        "<b>Target:</b> Evaluate in Audit mode where practical, then enforce only after representative save, export, sync, "
        "and update workflows pass. Allow only a verified exact executable when evidence proves need.",
        "<b>Verify:</b> Review mode and allowed applications with <font name='Courier'>Get-MpPreference</font>; use "
        "Runbook 4 for a clearly labeled active local-write test. <b>Stop:</b> Investigate a blocked writer before allowance.",
        "CFA is intentional and required writes pass without broad allowances.",
    ),
    Control(
        "DEF-07", "P2", "3. Malware, application, and exploit protection",
        "Network Protection",
        "Network Protection extends reputation blocking when supported.",
        "<b>Target:</b> Use only when edition, antimalware mode, and cloud prerequisites support it. Unsupported systems "
        "record N/A rather than using undocumented workarounds.",
        "<b>Verify:</b> Review official prerequisites and "
        "<font name='Courier'>Get-MpPreference | Select-Object EnableNetworkProtection</font>; use only Microsoft's harmless "
        "evaluation. <b>Stop:</b> Never test with a live malicious site.",
        "Supported systems pass the official harmless test; unsupported systems record N/A.",
    ),
    Control(
        "APP-01", "P1", "3. Malware, application, and exploit protection",
        "Reputation-based application protection",
        "Reputation checks reduce risky downloads and launches.",
        "<b>Target:</b> Enable applicable reputation, phishing, and unwanted-app protection. Treat Smart App Control as "
        "availability-dependent and document compatibility limits.",
        "<b>Verify:</b> Review Windows Security - App and browser control. "
        "<b>Stop:</b> Do not disable broad protection to make one unverified application run.",
        "Applicable reputation controls are enabled and exceptions are specific and verified.",
    ),
    Control(
        "APP-02", "P2", "3. Malware, application, and exploit protection",
        "VBS, HVCI, and vulnerable-driver blocking",
        "Kernel protections can expose incompatible drivers or performance limits.",
        "<b>Target:</b> Keep the Microsoft vulnerable-driver blocklist enabled. Evaluate Memory Integrity after inventorying "
        "required drivers and defining limits. Make one reversible change and reboot.",
        "<b>Verify:</b> Use Runbook 3 and representative workloads. <b>Stop:</b> A boot failure, hardware error, required "
        "driver failure, or limit breach rolls back only the latest documented change.",
        "Driver blocking is enabled; VBS and HVCI are intentional and pass compatibility tests.",
    ),
    Control(
        "NET-01", "P1", "4. Network exposure and remote access",
        "Windows Firewall profiles",
        "Host firewall protection limits unsolicited inbound exposure.",
        "<b>Target:</b> Keep Domain, Private, and Public profiles enabled. Use the narrowest application, service, port, "
        "profile, and remote-address scope that meets a documented need.",
        "<b>Verify:</b> Run <font name='Courier'>Get-NetFirewallProfile -PolicyStore ActiveStore</font>. "
        "<b>Stop:</b> Never disable all profiles as a troubleshooting step.",
        "All profiles are enabled and custom inbound rules are narrowly scoped and justified.",
    ),
    Control(
        "NET-02", "P1", "4. Network exposure and remote access",
        "Remote services and listeners",
        "Unused remote-management paths increase attack surface.",
        "<b>Target:</b> Disable or restrict remote desktop, assistance, remote registry, remote management, and remote-control "
        "services when not required. Scope required access to trusted networks and strong authentication.",
        "<b>Verify:</b> Review services, listeners, firewall rules, and Settings. "
        "<b>Stop:</b> Do not disable an organization-managed service; invoke GOV-01.",
        "Only required remote services listen, with an owner, strong authentication, and narrow scope.",
    ),
    Control(
        "NET-03", "P1", "4. Network exposure and remote access",
        "SMB and legacy sharing",
        "Legacy SMB and guest access weaken authentication and integrity.",
        "<b>Target:</b> Remove SMB1, avoid insecure guest logons, require authenticated sharing, and use supported signing. "
        "Preserve only shares with an explicit need.",
        "<b>Verify:</b> Review Windows optional features, SMB configuration, and representative authenticated access. "
        "<b>Stop:</b> Do not expose file sharing directly to the public internet.",
        "SMB1 and insecure guest access are absent; required shares are authenticated and scoped.",
    ),
    Control(
        "NET-04", "P2", "4. Network exposure and remote access",
        "DNS and network failover",
        "Layered DNS or adapter changes can create privacy and reliability conflicts.",
        "<b>Target:</b> Select one documented DNS design, record trade-offs, and test required network paths. Change browser, "
        "operating-system, router, and VPN layers separately.",
        "<b>Verify:</b> Resolve a known domain and test planned adapter or VPN transitions within a predefined time. "
        "<b>Stop:</b> Repeated stable-link resolution failures or inconsistent policy ownership.",
        "Resolver and failover paths are documented and pass representative tests.",
    ),
    Control(
        "LOG-01", "P2", "5. Logging, exceptions, and operational assurance",
        "Security audit policy",
        "Useful events support diagnosis; excessive collection increases privacy risk.",
        "<b>Target:</b> Enable only audit categories needed for security decisions, define retention, and restrict deletion "
        "rights. Runbook 5 is read-only; Runbook 6 is an active local-write export test.",
        "<b>Verify:</b> Run <font name='Courier'>auditpol.exe /get /category:*</font>. "
        "<b>Stop:</b> Do not change managed policy or collect sensitive events without authority.",
        "Audit scope, retention, access, and deletion rights are proportionate and documented.",
    ),
    Control(
        "LOG-02", "P2", "5. Logging, exceptions, and operational assurance",
        "Command-line logging privacy",
        "Command-line events may capture tokens, paths, user data, and secrets.",
        "<b>Target:</b> Enable command-line capture only after documenting need, access, retention, and redaction. Never paste "
        "unredacted Event 4688 command lines into a public issue or workbook.",
        "<b>Verify:</b> Review policy and a synthetic command containing no secret. "
        "<b>Stop:</b> If secrets appear, restrict access, rotate exposed secrets, and revise collection.",
        "Command-line logging is justified, access-controlled, time-limited, and redacted before sharing.",
    ),
    Control(
        "LOG-03", "P2", "5. Logging, exceptions, and operational assurance",
        "Provider-scoped event review",
        "Provider and time scope prevent unrelated events from creating false conclusions.",
        "<b>Target:</b> Every event query specifies log, provider, event ID, and deliberate StartTime. Preserve only fields "
        "required for the decision.",
        "<b>Verify:</b> Run the executable examples in Runbook 5. "
        "<b>Stop:</b> An event number without provider and time context is not sufficient evidence.",
        "Event evidence is provider-scoped, time-scoped, minimal, and tied to a decision.",
    ),
    Control(
        "OPS-01", "P1", "5. Logging, exceptions, and operational assurance",
        "Narrow, expiring exceptions",
        "Broad or permanent exclusions silently weaken controls.",
        "<b>Target:</b> Every exclusion or allowance has an owner, exact scope, reason, approval date, test, and next review. "
        "Prefer supported configuration or contextual scope over broad folders and disabled protection.",
        "<b>Verify:</b> Review antimalware exclusions, CFA allowances, firewall rules, browser overrides, and remote access. "
        "<b>Stop:</b> Unknown owner or need requires investigation before renewal.",
        "Every exception is narrow, owned, tested, and scheduled for review or removal.",
    ),
    Control(
        "OPS-02", "P1", "5. Logging, exceptions, and operational assurance",
        "One-change staging and rollback",
        "One variable at a time preserves causal evidence and rollback.",
        "<b>Target:</b> Record prior state and limits; change one control; reboot when required; run focused security and "
        "usability tests; observe normal use before another material change.",
        "<b>Verify:</b> The record links control ID, owner, date, prior state, result, and rollback. "
        "<b>Stop:</b> Any unexplained block, crash, recovery prompt, data loss, or limit breach.",
        "Each material change is isolated, reversible, tested, and observed.",
    ),
    Control(
        "OPS-03", "P0", "5. Logging, exceptions, and operational assurance",
        "Incident and instability stop",
        "Hardening during compromise or instability can destroy evidence and worsen recovery.",
        "<b>Target:</b> Stop baseline work when compromise is suspected or the device has repeated crashes, hardware errors, "
        "unexpected recovery prompts, lost data, or unexplained control changes. Preserve evidence safely and escalate.",
        "<b>Verify:</b> The owner knows an authorized incident or repair path. "
        "<b>Stop:</b> Do not use this checklist as incident response, malware removal, or forensic guidance.",
        "Baseline work stops during suspected compromise or instability and follows an authorized path.",
    ),
    Control(
        "OPS-04", "P3", "5. Logging, exceptions, and operational assurance",
        "Scheduled review",
        "Posture drifts as software, firmware, risk, and required work change.",
        "<b>Target:</b> Review P0 and P1 after material platform changes and on a defined schedule. Review P2 by risk and "
        "compatibility; update P3 information when it affects decisions.",
        "<b>Verify:</b> The workbook has an owner and next-review date for each applicable control. "
        "<b>Stop:</b> A stale prior assessment is not current evidence.",
        "Every applicable control has an owner and review trigger or date.",
    ),
    Control(
        "PERF-01", "P2", "5. Logging, exceptions, and operational assurance",
        "Representative performance baseline",
        "Security changes should be tested against repeatable workloads.",
        "<b>Target:</b> Before changes affecting drivers, networking, storage, or virtualization, define representative "
        "workloads and applicable limits for latency, frame-time consistency, throughput, temperature, and reliability.",
        "<b>Verify:</b> Repeat the same workload, duration, and method before and after the isolated change. "
        "<b>Stop:</b> Investigate a limit breach before accepting a change or exception.",
        "Applicable performance and reliability limits are defined and tested consistently.",
    ),
    Control(
        "PERF-02", "P1", "5. Logging, exceptions, and operational assurance",
        "Representative workflow acceptance",
        "A secure configuration must support required authorized work.",
        "<b>Target:</b> Test normal sign-in, updates, save/open/export, synchronization, printing, communications, network "
        "access, peripherals, recovery, and other required workflows after material changes.",
        "<b>Verify:</b> Record only pass/fail, date, test name, and minimal sanitized evidence. "
        "<b>Stop:</b> Revert only the latest documented change when a required workflow fails.",
        "Required workflows pass after each material change without disabling broad protections.",
    ),
]


REFERENCES = [
    (
        "National Institute of Standards and Technology",
        "The NIST Cybersecurity Framework (CSF) 2.0",
        "NIST CSWP 29, Feb. 2024",
        "https://doi.org/10.6028/NIST.CSWP.29",
        "Govern, identify, protect, detect, respond, and recover outcomes.",
    ),
    (
        "National Institute of Standards and Technology",
        "Security and Privacy Controls for Information Systems and Organizations",
        "NIST SP 800-53 Rev. 5, Sept. 2020 (includes updates as of Dec. 10, 2020)",
        "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final",
        "Least privilege, configuration, logging, contingency planning, and recovery controls.",
    ),
    (
        "National Institute of Standards and Technology",
        "Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile",
        "NIST SP 800-61 Rev. 3, Apr. 2025",
        "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
        "Incident-response recommendations and CSF 2.0 integration.",
    ),
    (
        "National Institute of Standards and Technology",
        "Guide to Computer Security Log Management",
        "NIST SP 800-92, Sept. 2006",
        "https://csrc.nist.gov/pubs/sp/800/92/final",
        "Security-log planning, handling, retention, and operations.",
    ),
    (
        "Cybersecurity and Infrastructure Security Agency",
        "#StopRansomware Guide",
        "rev. Oct. 19, 2023",
        "https://www.cisa.gov/resources-tools/resources/stopransomware-guide",
        "Backups, recovery testing, access control, and preparation.",
    ),
    (
        "Microsoft",
        "Windows 11 release information",
        "",
        "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information",
        "Current servicing and release-health information.",
    ),
    (
        "Microsoft",
        "BitLocker Overview",
        "",
        "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/",
        "Encryption capabilities and recovery considerations.",
    ),
    (
        "Microsoft Support",
        "Windows 11 and Secure Boot",
        "",
        "https://support.microsoft.com/en-us/windows/security/devicesecurity/windows-11-and-secure-boot",
        "Secure Boot purpose, firmware guidance, and supported Windows behavior.",
    ),
    (
        "Microsoft",
        "Enable memory integrity",
        "",
        "https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity",
        "Memory Integrity and VBS enablement, compatibility, and rollback.",
    ),
    (
        "Microsoft",
        "Microsoft recommended driver block rules",
        "",
        "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules",
        "Vulnerable-driver blocklist behavior and compatibility.",
    ),
    (
        "Microsoft",
        "Microsoft Defender Antivirus security intelligence and product updates and support",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates",
        "Platform, engine, and security-intelligence servicing.",
    ),
    (
        "Microsoft",
        "ASR rules reference",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference",
        "Full ASR rule GUIDs, modes, prerequisites, and compatibility.",
    ),
    (
        "Microsoft",
        "Plan your attack surface reduction (ASR) rules deployment",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-deployment-plan",
        "Assessment, Audit mode, reporting, and staged enforcement.",
    ),
    (
        "Microsoft",
        "Controlled folder access (CFA) overview",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-overview",
        "Scope, modes, dependencies, and monitoring.",
    ),
    (
        "Microsoft",
        "Use network protection to help prevent connections to malicious or suspicious sites",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/network-protection",
        "Current prerequisites, modes, and safe evaluation.",
    ),
    (
        "Microsoft",
        "Windows Firewall Rules",
        "",
        "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/rules",
        "Narrow rule scope, precedence, and firewall design.",
    ),
    (
        "Microsoft",
        "SMB security hardening in Windows Server and Windows Client",
        "",
        "https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening",
        "Signing, guest access, SMB1, and current behavior.",
    ),
    (
        "Microsoft",
        "Local accounts",
        "",
        "https://learn.microsoft.com/en-us/windows/security/identity-protection/access-control/local-accounts",
        "Daily-use and administrative-account separation.",
    ),
    (
        "Microsoft Support",
        "User Account Control settings",
        "",
        "https://support.microsoft.com/en-us/windows/security/user-account-control-settings",
        "Supported UAC levels and prompt behavior.",
    ),
    (
        "Microsoft",
        "Command line process auditing",
        "",
        "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing",
        "Event 4688 configuration and plaintext-secret warning.",
    ),
    (
        "Microsoft",
        "TPM recommendations",
        "",
        "https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/tpm-recommendations",
        "TPM capabilities, Windows dependencies, and recommendations.",
    ),
    (
        "Microsoft",
        "Kernel DMA Protection",
        "",
        "https://learn.microsoft.com/en-us/windows/security/hardware-security/kernel-dma-protection-for-thunderbolt",
        "Hardware, firmware, driver, and edition dependencies.",
    ),
    (
        "Microsoft",
        "Passwordless sign-in",
        "",
        "https://learn.microsoft.com/en-us/windows/security/book/identity-protection-passwordless-sign-in",
        "Windows Hello, passkeys, FIDO2, and phishing-resistant sign-in.",
    ),
    (
        "Microsoft",
        "Protect security settings with tamper protection",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection",
        "Tamper-protection purpose, behavior, and management ownership.",
    ),
    (
        "Microsoft",
        "Configure behavioral, heuristic, and real-time protection",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/configure-protection-features-microsoft-defender-antivirus",
        "Real-time, behavior, IOAV, cloud, and related protection features.",
    ),
    (
        "Microsoft",
        "Detect and block potentially unwanted applications",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus",
        "PUA applicability, modes, configuration, and review.",
    ),
    (
        "Microsoft Support",
        "App & browser control in the Windows Security App",
        "",
        "https://support.microsoft.com/en-us/windows/security/windows-security/app-browser-control-in-the-windows-security-app",
        "Reputation-based protection and Smart App Control availability.",
    ),
    (
        "Microsoft",
        "Enable Remote Desktop on your PC",
        "",
        "https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access",
        "Remote Desktop exposure, trusted-network scope, authentication, and editions.",
    ),
    (
        "Microsoft",
        "DNS Queries and Lookups in Windows and Windows Server",
        "",
        "https://learn.microsoft.com/en-us/windows-server/networking/dns/queries-lookups",
        "Windows DNS client behavior and resolver redundancy.",
    ),
    (
        "Microsoft",
        "Push-button reset frequently-asked questions (FAQ)",
        "",
        "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/pbr-faq?view=windows-11",
        "Windows Recovery Environment and recovery-tool requirements.",
    ),
    (
        "Microsoft Support",
        "Device Encryption in Windows",
        "",
        "https://support.microsoft.com/en-us/windows/security/encryption/device-encryption-in-windows",
        "Home availability, prerequisites, recovery-account behavior, and supported UI.",
    ),
    (
        "Microsoft Support",
        "BitLocker Drive Encryption",
        "",
        "https://support.microsoft.com/en-us/windows/security/encryption/bitlocker-drive-encryption",
        "Pro-and-higher availability and the supported BitLocker management UI.",
    ),
    (
        "Microsoft",
        "Set-MpPreference",
        "",
        "https://learn.microsoft.com/en-us/powershell/module/defender/set-mppreference",
        "Elevated Defender configuration syntax and supported values.",
    ),
    (
        "Microsoft",
        "Evaluate network protection",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/evaluate-network-protection",
        "Official harmless test, audit and block workflow, and events 1125 and 1126.",
    ),
    (
        "Microsoft",
        "Attack surface reduction events in Windows Event Viewer",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-windows-events",
        "Provider-specific ASR, CFA, and Network Protection event identifiers.",
    ),
    (
        "Microsoft",
        "Monitor controlled folder access activity",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-monitor",
        "Controlled Folder Access audit and block events plus evaluation guidance.",
    ),
    (
        "Microsoft",
        "Set-NetFirewallProfile",
        "",
        "https://learn.microsoft.com/en-us/powershell/module/netsecurity/set-netfirewallprofile",
        "Supported Windows Firewall profile configuration syntax.",
    ),
    (
        "Microsoft",
        "Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows",
        "",
        "https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3",
        "SMB1 feature detection, removal, and restart behavior.",
    ),
    (
        "Microsoft",
        "Get-BitLockerVolume",
        "",
        "https://learn.microsoft.com/en-us/powershell/module/bitlocker/get-bitlockervolume",
        "BitLocker volume, protection, encryption, and protector status fields.",
    ),
    (
        "Microsoft",
        "BitLocker operations guide",
        "",
        "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/operations-guide",
        "Supported enablement, system-check, recovery, and operating procedures.",
    ),
    (
        "National Institute of Standards and Technology",
        "Guide to Storage Encryption Technologies for End User Devices",
        "NIST SP 800-111, Nov. 2007",
        "https://csrc.nist.gov/pubs/sp/800/111/final",
        "Technology-neutral endpoint storage-encryption and recovery considerations.",
    ),
    (
        "Microsoft",
        "auditpol set",
        "",
        "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol-set",
        "Supported audit-policy subcategory configuration syntax.",
    ),
    (
        "National Institute of Standards and Technology",
        "Guide to Enterprise Telework, Remote Access, and Bring Your Own Device (BYOD) Security",
        "NIST SP 800-46 Rev. 2, July 2016",
        "https://csrc.nist.gov/pubs/sp/800/46/r2/final",
        "Remote-access threat, authentication, and lifecycle considerations.",
    ),
    (
        "Microsoft",
        "Policy CSP - ADMX_AuditSettings",
        "",
        "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings",
        "Edition applicability and plaintext privacy warning for process command-line auditing.",
    ),
    (
        "Microsoft",
        "Attack surface reduction (ASR) rules overview",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-overview",
        "Any-edition availability with Microsoft Defender Antivirus, local PowerShell configuration, modes, and audit-first deployment.",
    ),
    (
        "Microsoft",
        "Configure controlled folder access (CFA)",
        "",
        "https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-configure",
        "Windows 10-or-later applicability, elevated PowerShell configuration, modes, and Windows Security workflow.",
    ),
    (
        "Microsoft",
        "How to enable insecure guest logons in SMB2 and SMB3",
        "",
        "https://learn.microsoft.com/en-us/windows-server/storage/file-server/enable-insecure-guest-logons-smb2-and-smb3",
        "Windows 11 applicability, administrator requirement, insecure-guest risk, defaults, and PowerShell configuration.",
    ),
    (
        "Microsoft",
        "manage-bde",
        "",
        "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde",
        "Windows 11 command-line encryption-status support for all drives, including unprotected drives.",
    ),
]


CONTROL_SOURCES = {
    "GOV-01": (1, 2),
    "GOV-02": (1, 2, 4),
    "REC-01": (1, 2, 5),
    "REC-02": (7,),
    "REC-03": (2, 30),
    "PLT-01": (6,),
    "PLT-02": (8,),
    "PLT-03": (21,),
    "PLT-04": (9, 22),
    "PLT-05": (2, 6),
    "PLT-06": (7,),
    "ID-01": (2, 18),
    "ID-02": (1, 23),
    "ID-03": (19,),
    "DEF-01": (11, 25),
    "DEF-02": (24, 25),
    "DEF-03": (25,),
    "DEF-04": (26,),
    "DEF-05": (12, 13),
    "DEF-06": (14,),
    "DEF-07": (15,),
    "APP-01": (27,),
    "APP-02": (9, 10),
    "NET-01": (16,),
    "NET-02": (2, 28),
    "NET-03": (17,),
    "NET-04": (29,),
    "LOG-01": (2, 4),
    "LOG-02": (4, 20),
    "LOG-03": (4, 20),
    "OPS-01": (1, 2),
    "OPS-02": (1, 2),
    "OPS-03": (3,),
    "OPS-04": (1,),
    "PERF-01": (1, 2),
    "PERF-02": (1, 2),
}

control_ids = {control.control_id for control in CONTROLS}
if set(CONTROL_SOURCES) != control_ids:
    raise ValueError("Every control must have exactly one source-mapping entry.")
if any(number < 1 or number > len(REFERENCES) for numbers in CONTROL_SOURCES.values() for number in numbers):
    raise ValueError("A control source number does not exist in REFERENCES.")

for edition_steps in (HOME_STEPS, PRO_STEPS):
    for step in edition_steps:
        for command_line in (*step.commands, *step.verify_commands):
            if len(command_line) > 64:
                raise ValueError(
                    f"Step {step.step_id} command line exceeds the copy/paste "
                    f"layout limit: {command_line!r}"
                )


PRIORITIES = [
    ("P0", "Safety gate", "A prerequisite or stop condition. P0 is not a severity score."),
    ("P1", "Core baseline", "A generally applicable foundational protection."),
    ("P2", "Enhanced control", "Risk- and compatibility-dependent hardening."),
    ("P3", "Informational", "Inventory, lifecycle, or review guidance."),
]


def para(text, style="Cell"):
    return Paragraph(text, STYLES[style])


def heading(text, key, level=0):
    result = Paragraph(text, STYLES["H1" if level == 0 else "H2"])
    result._bookmark_key = key
    result._bookmark_level = level
    return result


def configure_canvas(
    c: canvas.Canvas, title: str, subject: str, keywords: str
):
    c.setTitle(title)
    c.setAuthor(AUTHOR)
    c.setCreator(AUTHOR)
    c.setSubject(subject)
    c.setKeywords(keywords)
    c.setViewerPreference("DisplayDocTitle", "true")
    c._doc.Catalog.Lang = PDFString("en-US")


class OutlineDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        key = getattr(flowable, "_bookmark_key", None)
        if key:
            level = getattr(flowable, "_bookmark_level", 0)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(
                flowable.getPlainText(), key, level=level, closed=False
            )


class Cover(Flowable):
    def __init__(self, edition, workbook=False):
        super().__init__()
        self.edition = edition
        self.workbook = workbook
        self.width = CONTENT_W
        self.height = 300 if not workbook else 270

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.width, self.height, 14, fill=1, stroke=0)
        c.setFillColor(BLUE if self.workbook else TEAL)
        c.rect(0, self.height - 12, self.width, 12, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(
            36,
            self.height - 48,
            "PRINTABLE / BLANK ASSESSMENT RECORD"
            if self.workbook
            else "PUBLIC RELEASE / ORDERED IMPLEMENTATION GUIDE",
        )
        title = c.beginText(36, self.height - 94)
        title.setFont("Helvetica-Bold", 23 if self.workbook else 24)
        title.setLeading(28 if self.workbook else 29)
        title.textLine(f"Windows 11 {self.edition}")
        title.textLine("Assessment Workbook" if self.workbook else "Security Baseline")
        c.drawText(title)
        c.setFont("Helvetica", 10.5)
        c.setFillColor(colors.HexColor("#DCE6F2"))
        c.drawString(
            38,
            76,
            f"Use with the Windows 11 {self.edition} implementation guide"
            if self.workbook
            else "Action > restart gate > verify > recover > continue",
        )
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(WHITE)
        c.drawString(
            38,
            48,
            f"WINDOWS 11 {self.edition.upper()}   |   Version {VERSION}   |   Author: {AUTHOR}",
        )


def callout(title, body, accent=BLUE, background=PALE_BLUE):
    table = Table(
        [[para(f"<b>{escape(title)}</b>", "BodySmall"), para(body, "BodySmall")]],
        colWidths=[124, CONTENT_W - 124],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.8, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 5, accent),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def priority_table():
    data = [
        [
            para("PRIORITY", "CellHeader"),
            para("MEANING", "CellHeader"),
            para("HOW TO USE IT", "CellHeader"),
        ]
    ]
    for code, meaning, usage in PRIORITIES:
        data.append(
            [
                para(f"<b>{code}</b>", "Status"),
                para(f"<b>{meaning}</b>", "CellBold"),
                para(usage),
            ]
        )
    table = Table(data, colWidths=[82, 150, CONTENT_W - 232], repeatRows=1)
    table.setStyle(base_table_style(len(data)))
    return table


def base_table_style(row_count, header=True, pad=7):
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.55, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    for row_index in range(1 if header else 0, row_count):
        commands.append(
            (
                "BACKGROUND",
                (0, row_index),
                (-1, row_index),
                WHITE if row_index % 2 else PALE_GRAY,
            )
        )
    return TableStyle(commands)


def guide_control_table(items):
    data = [
        [
            para("ID / INITIAL STATUS", "CellHeader"),
            para("CONTROL / PURPOSE", "CellHeader"),
            para("PUBLIC BASELINE TARGET", "CellHeader"),
            para("VERIFY / STOP CONDITION", "CellHeader"),
        ]
    ]
    for item in items:
        source_labels = ", ".join(f"[{number}]" for number in CONTROL_SOURCES[item.control_id])
        data.append(
            [
                para(
                    f"<b>{item.control_id}</b><br/>{item.priority}<br/><br/>NOT ASSESSED",
                    "Status",
                ),
                para(
                    f"<b>{escape(item.title)}</b><br/>{escape(item.purpose)}"
                    f"<br/><font size='7.5' color='#4E5E70'><b>Sources:</b> {source_labels}</font>"
                ),
                para(item.target),
                para(item.verify),
            ]
        )
    table = Table(
        data,
        colWidths=[86, 155, 245, CONTENT_W - 486],
        repeatRows=1,
        splitByRow=1,
    )
    table.setStyle(base_table_style(len(data)))
    return table


def code_block(lines, width=CONTENT_W):
    long_lines = [line for line in lines if len(line) > 64]
    if long_lines:
        raise ValueError(
            "Displayed command line exceeds the copy/paste layout limit: "
            + repr(long_lines[0])
        )
    content = "<br/>".join(escape(line) for line in lines)
    table = Table([[para(content, "SBCCode")]], colWidths=[width])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F8FA")),
                ("BOX", (0, 0), (-1, -1), 0.65, GRID),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def runbook(title, classification, purpose, lines, result, caution):
    key = "runbook-" + "".join(character for character in title.lower() if character.isalnum())
    return [
        KeepTogether(
            [
                heading(title, key, level=1),
                callout(
                    classification,
                    f"<b>Purpose:</b> {purpose}<br/><b>Expected result:</b> {result}<br/><b>Caution:</b> {caution}",
                    TEAL if classification == "READ-ONLY" else BLUE,
                    PALE_TEAL if classification == "READ-ONLY" else PALE_BLUE,
                ),
                Spacer(1, 6),
                code_block(lines),
            ]
        ),
        Spacer(1, 8),
    ]


def workbook_card(control):
    line = "____________________________"
    fields = Table(
        [
            [
                para(f"<b>Assessment status:</b> {line}", "WorkbookField"),
                para(f"<b>Date:</b> {line}", "WorkbookField"),
            ],
            [
                para(f"<b>Owner:</b> {line}", "WorkbookField"),
                para(f"<b>Next review:</b> {line}", "WorkbookField"),
            ],
        ],
        colWidths=[CONTENT_W / 2, CONTENT_W / 2],
    )
    fields.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    evidence = Table(
        [
            [
                para("<b>Evidence reference:</b><br/><br/>", "WorkbookField"),
                para("<b>Exception / reason / approval:</b><br/><br/>", "WorkbookField"),
            ]
        ],
        colWidths=[CONTENT_W / 2, CONTENT_W / 2],
        rowHeights=[38],
    )
    evidence.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBEFORE", (1, 0), (1, -1), 0.45, GRID),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    table = Table(
        [
            [
                para(
                    f"<b>{control.control_id} - {escape(control.title)}</b> | "
                    f"{control.priority} | INITIAL STATUS: NOT ASSESSED",
                    "CellHeader",
                )
            ],
            [para(f"<b>Target:</b> {escape(control.summary)}", "WorkbookField")],
            [fields],
            [evidence],
        ],
        colWidths=[CONTENT_W],
        rowHeights=[22, 31, 47, 38],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, 1), PALE_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.75, NAVY),
                ("LINEBELOW", (0, 1), (-1, 2), 0.45, GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 7)])


def legacy_combined_guide_story():
    story = [
        Cover(),
        Spacer(1, 14),
        callout(
            "Independent guidance",
            "This independent informational aid is not endorsed by Microsoft or any hardware or security vendor. "
            "It is not a live audit, certification, guarantee, incident-response plan, or substitute for professional advice.",
            TEAL,
            PALE_TEAL,
        ),
        Spacer(1, 8),
        callout(
            "License and release notice",
            "Guide materials: CC BY-NC-ND 4.0. Controlled-author terms apply; see LICENSE.md. "
            f"Document version {VERSION}. Source review cut-off: {SOURCE_REVIEW_DATE}. "
            "Current authoritative vendor documentation takes precedence.",
        ),
        PageBreak(),
        heading("Start here", "start-here"),
        para(
            "This guide is a neutral starting baseline for personally owned Windows 11 Home and Pro devices. "
            "It begins with no claims about any device: every control is <b>NOT ASSESSED</b>. Use the separate printable "
            "workbook to record outcomes. Enterprise, regulated, incident-response, forensic, server, and managed environments "
            "require additional governance and professional review.",
            "Body",
        ),
        callout(
            "Mandatory stop condition",
            "If the device is owned, enrolled, monitored, or governed by an employer, school, client, or other organization, "
            "stop. Use the organization's authorized administrator and policy. Do not remove management or bypass controls.",
            colors.HexColor("#A24D00"),
            PALE_AMBER,
        ),
        Spacer(1, 8),
        heading("Priority model", "priority-model", level=1),
        para(
            "Priority describes implementation order and decision context, not vulnerability severity, exploitability, or risk.",
            "Body",
        ),
        priority_table(),
        Spacer(1, 8),
        heading("Assessment result states", "result-states", level=1),
        para(
            "<b>NOT ASSESSED:</b> no current conclusion. <b>OBSERVED:</b> a current value is recorded, but effectiveness "
            "is not proven. <b>CONFIGURED:</b> the intended setting is selected, but enforcement or compatibility is not "
            "yet proven. <b>PASS:</b> target and test pass with dated evidence. <b>HOLD:</b> a prerequisite or safety "
            "concern blocks work. <b>EXCEPTION:</b> an authorized, scoped, time-bounded deviation exists. <b>N/A:</b> the "
            "control is demonstrably not applicable. Unknown, observed, or merely configured is never PASS.",
            "Body",
        ),
        heading("Evidence rules", "evidence-rules", level=1),
        para(
            "Record the control ID, result, date, method, owner, and a minimal sanitized evidence reference. Store sensitive "
            "evidence outside the public repository with access restricted to people who need it. Do not record recovery keys, "
            "passwords, tokens, serial numbers, public addresses, user paths, raw dumps, secret-bearing command lines, or "
            "unredacted logs. Retention follows the owner's legal, privacy, operational, and investigation needs.",
            "Body",
        ),
        PageBreak(),
    ]

    sections = []
    for control in CONTROLS:
        if control.section not in sections:
            sections.append(control.section)
    for section_index, section in enumerate(sections):
        story.append(CondPageBreak(135))
        story.append(heading(section, "controls-" + section.split(".", 1)[0]))
        story.append(
            para(
                "Initial status for every control is NOT ASSESSED. Apply the stated stop conditions before making changes. "
                "Bracketed source numbers map each control to the IEEE-style references in Section 8.",
                "BodySmall",
            )
        )
        story.append(guide_control_table([item for item in CONTROLS if item.section == section]))
        if section_index != len(sections) - 1:
            story.append(Spacer(1, 12))

    story.extend(
        [
            PageBreak(),
            heading("6. Safe verification runbooks", "runbooks"),
            para(
                "Examples are for an authorized, personally owned Windows device. READ-ONLY commands query state. "
                "ACTIVE LOCAL-WRITE TEST commands create temporary evidence and therefore change local storage. "
                "Configuration changes are intentionally excluded.",
                "Body",
            ),
        ]
    )
    story.extend(
        runbook(
            "Runbook 1: platform inventory",
            "READ-ONLY",
            "Collect minimum platform and recovery state.",
            [
                "Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsBuildNumber,BiosFirmwareType",
                "Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer,Product,Version",
                "Get-CimInstance Win32_BIOS | Select-Object SMBIOSBIOSVersion,ReleaseDate",
                "Get-Tpm | Select-Object TpmPresent,TpmReady,TpmEnabled,TpmActivated,LockedOut",
                "reagentc.exe /info",
                "manage-bde.exe -status",
            ],
            "Applicable fields are recorded without serials, recovery keys, user paths, or raw full-object exports.",
            "If this is a managed device or recovery is unknown, stop before platform changes.",
        )
    )
    story.extend(
        runbook(
            "Runbook 2: Defender and ASR inventory",
            "READ-ONLY",
            "Display Defender health and exact ASR GUID/action pairs without failing on empty or mismatched arrays.",
            [
                "$status = Get-MpComputerStatus",
                "$status | Select-Object AMRunningMode,AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,IsTamperProtected,AntivirusSignatureLastUpdated",
                "$pref = Get-MpPreference",
                "$pref | Select-Object MAPSReporting,SubmitSamplesConsent,PUAProtection,EnableControlledFolderAccess,EnableNetworkProtection",
                "$ids = @($pref.AttackSurfaceReductionRules_Ids)",
                "$actions = @($pref.AttackSurfaceReductionRules_Actions)",
                "if ($ids.Count -eq 0) { 'No ASR rules returned by the active preference provider.' }",
                "else {",
                "  for ($i = 0; $i -lt $ids.Count; $i++) {",
                "    $action = if ($i -lt $actions.Count) { $actions[$i] } else { 'MISSING_ACTION' }",
                "    [pscustomobject]@{ RuleId = [string]$ids[$i]; Action = $action }",
                "  }",
                "}",
            ],
            "The command returns zero or more complete GUID/action pairs; a missing action is labeled.",
            "This inventory does not enable rules. Determine policy ownership before changing a mode.",
        )
    )
    asr_heading = heading("ASR GUID reference for review", "asr-guid-reference", level=1)
    asr_intro = para(
            "These full GUIDs identify commonly evaluated rules. The current Microsoft reference controls names, "
            "dependencies, applicability, and deployment. Do not infer a target mode from this list.",
            "Body",
    )
    asr_rows = [
        [para("FULL GUID", "CellHeader"), para("MICROSOFT RULE NAME", "CellHeader")],
        [para("56a863a9-875e-4185-98a7-b882c64b5ce5", "SBCCode"), para("Block abuse of exploited vulnerable signed drivers")],
        [para("9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2", "SBCCode"), para("Block credential stealing from LSASS")],
        [para("d4f940ab-401b-4efc-aadc-ad5f3c50688a", "SBCCode"), para("Block Office applications from creating child processes")],
        [para("3b576869-a4ec-4529-8536-b80a7769e899", "SBCCode"), para("Block Office applications from creating executable content")],
        [para("75668c1f-73b5-4cf0-bb93-3ecf5cb7cc84", "SBCCode"), para("Block Office applications from injecting code")],
        [para("92e97fa1-2edf-4476-bdd6-9dd0b4dddc7b", "SBCCode"), para("Block Win32 API calls from Office macros")],
        [para("be9ba2d9-53ea-4cdc-84e5-9b1eeee46550", "SBCCode"), para("Block executable content from email and webmail")],
        [para("d3e037e1-3eb8-44c8-a917-57927947596d", "SBCCode"), para("Block JavaScript or VBScript from launching downloaded executable content")],
        [para("c1db55ab-c21a-4637-bb3f-a12568109d35", "SBCCode"), para("Use advanced protection against ransomware")],
        [para("e6db77e5-3df2-4cf1-b95a-636979351e5b", "SBCCode"), para("Block persistence through WMI event subscription")],
    ]
    asr_table = Table(asr_rows, colWidths=[250, CONTENT_W - 250], repeatRows=1)
    asr_table.setStyle(base_table_style(len(asr_rows), pad=5))
    story.append(KeepTogether([asr_heading, asr_intro, asr_table]))
    story.extend(
        runbook(
            "Runbook 3: VBS, HVCI, and LSA runtime",
            "READ-ONLY",
            "Inspect runtime state instead of assuming a registry or firmware setting is effective.",
            [
                "$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime",
                "Get-CimInstance -Namespace root\\Microsoft\\Windows\\DeviceGuard -ClassName Win32_DeviceGuard | Select-Object VirtualizationBasedSecurityStatus,SecurityServicesConfigured,SecurityServicesRunning",
                "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Wininit';Id=12;StartTime=$boot} -ErrorAction SilentlyContinue | Select-Object -First 1 TimeCreated,Id,ProviderName,Message",
                "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-CodeIntegrity/Operational';ProviderName='Microsoft-Windows-CodeIntegrity';Id=3033,3063,3087;StartTime=$boot} -ErrorAction SilentlyContinue | Select-Object TimeCreated,Id,ProviderName,Message",
            ],
            "Runtime fields and current-boot provider events are reviewed against intent.",
            "Event messages may include paths and identifiers; sanitize them before sharing.",
        )
    )
    story.extend(
        runbook(
            "Runbook 4: temporary write acceptance",
            "ACTIVE LOCAL-WRITE TEST",
            "Create and remove a harmless temporary file to test an authorized write path. This is not read-only.",
            [
                "$testRoot = Join-Path $env:TEMP 'SBC-LocalWrite-Test'",
                "$testFile = Join-Path $testRoot 'audit-write-test.txt'",
                "New-Item -ItemType Directory -Path $testRoot -Force | Out-Null",
                "[System.IO.File]::WriteAllText($testFile, 'SBC active local-write test')",
                "Get-Item -LiteralPath $testFile | Select-Object Name,Length,LastWriteTime",
                "Remove-Item -LiteralPath $testRoot -Recurse -Force",
            ],
            "The file is created, inspected, and removed; events are evaluated from the recorded test start time.",
            "Use only this disposable path. Do not substitute a protected or irreplaceable file.",
        )
    )
    story.extend(
        runbook(
            "Runbook 5: provider-scoped event queries",
            "READ-ONLY",
            "Bind event IDs to the correct provider and current boot.",
            [
                "$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime",
                "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Hyper-V-Hypervisor';Id=41;StartTime=$boot} -ErrorAction SilentlyContinue | Select-Object TimeCreated,Id,ProviderName,Message",
                "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Kernel-Boot';Id=124;StartTime=$boot} -ErrorAction SilentlyContinue | Select-Object TimeCreated,Id,ProviderName,Message",
                "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Wininit';Id=12;StartTime=$boot} -ErrorAction SilentlyContinue | Select-Object TimeCreated,Id,ProviderName,Message",
                "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Windows Defender/Operational';ProviderName='Microsoft-Windows-Windows Defender';Id=1121,1122,1123,1124,1125,1126;StartTime=$boot} -ErrorAction SilentlyContinue | Select-Object TimeCreated,Id,ProviderName,Message",
            ],
            "Each result is tied to a log, provider, event ID, and deliberate start time.",
            "No result can be normal. Interpret an event only with feature state and test context.",
        )
    )
    story.extend(
        runbook(
            "Runbook 6: audit policy export",
            "ACTIVE LOCAL-WRITE TEST",
            "Exercise an audit-policy export to a disposable local file. This changes local storage.",
            [
                "$auditFile = Join-Path $env:TEMP 'SBC-AuditPolicy.csv'",
                "auditpol.exe /backup /file:$auditFile",
                "Get-Item -LiteralPath $auditFile | Select-Object Name,Length,LastWriteTime",
                "Remove-Item -LiteralPath $auditFile -Force",
            ],
            "The export is created, minimally inspected, and removed.",
            "Do not commit the export. Do not collect managed policy without authorization.",
        )
    )
    story.extend(
        [
            PageBreak(),
            heading("7. Assessment and change lifecycle", "lifecycle"),
            para(
                "<b>1. Establish authority and scope.</b> Apply GOV-01 and identify device and data classes.<br/>"
                "<b>2. Close the safety gate.</b> Pass GOV-02 and REC-01 through REC-03 before platform changes.<br/>"
                "<b>3. Capture a fresh baseline.</b> Untested controls remain NOT ASSESSED.<br/>"
                "<b>4. Prioritize.</b> Close applicable P1 controls, then evaluate P2 against risk and compatibility.<br/>"
                "<b>5. Stage one change.</b> Record prior state, limits, owner, rollback, and evidence handling.<br/>"
                "<b>6. Verify security and usability.</b> Run focused and representative tests.<br/>"
                "<b>7. Observe and review.</b> Set the next date; material updates trigger reassessment.",
                "Body",
            ),
            callout(
                "Owner decision",
                "A PASS records that the stated target and test passed at a point in time. It is not proof against every "
                "threat. Exceptions require an owner, reason, scope, approval date, compensating measure where useful, "
                "and next review.",
                TEAL,
                PALE_TEAL,
            ),
            PageBreak(),
            heading("8. References", "references"),
            para(
                f"Source review cut-off: {SOURCE_REVIEW_DATE}. Features, editions, and recommendations change. "
                "Use current authoritative documentation for implementation decisions. Reference numbers are stable "
                "within this document version and appear beside each control.",
                "Body",
            ),
        ]
    )
    reference_rows = [[para("IEEE-STYLE REFERENCE", "CellHeader"), para("USE IN THIS GUIDE", "CellHeader")]]
    for number, (author, title, publication, url, purpose) in enumerate(REFERENCES, 1):
        publication_text = f", {publication}" if publication else ""
        citation = (
            f"[{number}] {author}, \"{title}\"{publication_text}. "
            f"[Online]. Available: {url}. Accessed: {SOURCE_ACCESS_DATE}."
        )
        reference_rows.append(
            [
                para(
                    f"<link href='{escape(url)}' color='#2459A6'>{escape(citation)}</link>",
                    "Reference",
                ),
                para(escape(purpose), "Reference"),
            ]
        )
    reference_table = Table(
        reference_rows, colWidths=[410, CONTENT_W - 410], repeatRows=1, splitByRow=1
    )
    reference_table.setStyle(base_table_style(len(reference_rows), pad=6))
    story.append(reference_table)
    return story


def legacy_combined_workbook_story():
    story = [
        Cover(workbook=True),
        Spacer(1, 14),
        callout(
            "How to use this workbook",
            "Read the companion guide before assessing a control. Each control begins NOT ASSESSED. Use OBSERVED or "
            "CONFIGURED as interim states; write PASS, HOLD, EXCEPTION, or N/A only after applying the target and "
            "verification method. Keep sensitive evidence in an access-controlled location and record only a sanitized reference.",
        ),
        Spacer(1, 8),
        callout(
            "Release notice",
            "Independent informational aid; not vendor-endorsed, a certification, guarantee, incident-response guide, "
            f"or professional advice. Version {VERSION}. Source review cut-off: {SOURCE_REVIEW_DATE}. "
            "Guide materials: CC BY-NC-ND 4.0. Controlled-author terms apply; see LICENSE.md.",
            TEAL,
            PALE_TEAL,
        ),
        PageBreak(),
        heading("Assessment instructions", "workbook-instructions"),
        para(
            "Device or assessment label: ________________________________________________<br/>"
            "Assessment owner: ________________________________   Start date: __________________<br/>"
            "Scope and exclusions: ___________________________________________________________________________________<br/><br/>"
            "<b>Do not write:</b> recovery keys, passwords, tokens, secret-bearing commands, serial numbers, public IPs, "
            "user paths, raw dumps, or unredacted logs. If organization-managed, stop and contact the authorized administrator.",
            "Body",
        ),
        priority_table(),
        Spacer(1, 8),
        para(
            "<b>Result states:</b> NOT ASSESSED means no current conclusion. OBSERVED records current state without proving "
            "effectiveness. CONFIGURED records intent without proving enforcement or compatibility. PASS means the target "
            "and test passed with dated evidence. HOLD means a prerequisite or safety concern blocks work. EXCEPTION is an "
            "authorized, scoped, time-bounded deviation. N/A requires a documented applicability reason.",
            "Body",
        ),
        PageBreak(),
    ]
    sections = []
    for control in CONTROLS:
        if control.section not in sections:
            sections.append(control.section)
    for section_index, section in enumerate(sections):
        section_controls = [item for item in CONTROLS if item.section == section]
        title = heading(section, "workbook-" + section.split(".", 1)[0])
        intro = para(
                "Use one card per control. Preserve sensitive supporting evidence outside this printable record.",
                "BodySmall",
        )
        story.append(CondPageBreak(190))
        story.append(title)
        story.append(intro)
        story.append(workbook_card(section_controls[0]))
        for control in section_controls[1:]:
            story.append(workbook_card(control))
        if section_index != len(sections) - 1:
            story.append(Spacer(1, 12))
    return story


def bullet_flowables(items, numbered=False, style="BodySmall"):
    result = []
    for index, item in enumerate(items, 1):
        marker = f"{index}." if numbered else "-"
        result.append(para(f"<b>{marker}</b> {escape(item)}", style))
    return result


def compact_label_table(items):
    data = []
    for label, value in items:
        data.append(
            [
                para(f"<b>{escape(label)}</b>", "BodySmall"),
                para(escape(value), "BodySmall"),
            ]
        )
    table = Table(data, colWidths=[104, CONTENT_W - 104])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.45, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def step_meta_table(step):
    rows = [
        [
            para(
                f"<b>PHASE</b> {escape(step.phase)}<br/><b>CONTROLS</b> {escape(', '.join(step.controls))}",
                "BodySmall",
            ),
            para(f"<b>PRIORITY</b><br/>{escape(step.priority)}", "BodySmall"),
            para(f"<b>RUN AS</b><br/>{escape(step.access)}", "BodySmall"),
            para(f"<b>ACTION TYPE</b><br/>{escape(step.classification)}", "BodySmall"),
            para(
                f"<b>SOURCES</b><br/>{escape(', '.join(f'[{n}]' for n in step.sources))}",
                "BodySmall",
            ),
        ]
    ]
    widths = [166, 76, 128, 230, CONTENT_W - 600]
    table = Table(rows, colWidths=widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.45, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def mini_box(title, body, width, accent=BLUE, background=PALE_BLUE):
    table = Table(
        [[para(f"<b>{escape(title)}</b><br/>{escape(body)}", "BodySmall")]],
        colWidths=[width],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.6, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def result_state_table():
    rows = [[para("STATE", "CellHeader"), para("USE IT ONLY WHEN", "CellHeader")]]
    for state, meaning in RESULT_STATES:
        rows.append([para(f"<b>{escape(state)}</b>", "Status"), para(escape(meaning))])
    table = Table(rows, colWidths=[116, CONTENT_W - 116], repeatRows=1)
    table.setStyle(base_table_style(len(rows), pad=5))
    return table


def quick_path_table(steps):
    half_w = (CONTENT_W - 10) / 2

    def half_table(items):
        rows = [
            [
                para("STEP", "CellHeader"),
                para("DO THIS IN ORDER", "CellHeader"),
                para("RESTART", "CellHeader"),
            ]
        ]
        for step in items:
            restart_short = "NO" if step.restart.upper().startswith("NO") else "READ STEP"
            rows.append(
                [
                    para(f"<b>{step.step_id}</b>", "Status"),
                    para(
                        f"<b>{escape(step.title)}</b><br/>"
                        f"<font size='7.5'>{escape(step.access)} | {escape(', '.join(step.controls))}</font>",
                        "BodySmall",
                    ),
                    para(escape(restart_short), "Status"),
                ]
            )
        table = Table(
            rows,
            colWidths=[38, half_w - 106, 68],
            repeatRows=1,
        )
        table.setStyle(base_table_style(len(rows), pad=4))
        return table

    split = (len(steps) + 1) // 2
    outer = Table(
        [[half_table(steps[:split]), half_table(steps[split:])]],
        colWidths=[half_w, half_w],
    )
    outer.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("LINEBEFORE", (1, 0), (1, -1), 10, WHITE),
            ]
        )
    )
    return outer


def step_story(step, edition):
    key = f"{edition.lower()}-step-{step.step_id}"
    column_w = (CONTENT_W - 12) / 2
    inner_w = column_w - 14
    left = [
        para("<b>BEFORE YOU START</b>", "BodySmall"),
        *bullet_flowables(step.prerequisites),
        Spacer(1, 4),
        para("<b>DO THIS IN ORDER</b>", "BodySmall"),
        *bullet_flowables(step.actions, numbered=True),
    ]
    if step.commands:
        left.extend(
            [
                Spacer(1, 4),
                para("<b>COPY / PASTE COMMANDS</b>", "BodySmall"),
                para(
                    "Run only after reading the numbered actions. State-changing lines are conditional.",
                    "BodySmall",
                ),
                code_block(step.commands, inner_w),
            ]
        )
    else:
        left.extend(
            [
                Spacer(1, 4),
                para(
                    "<b>COMMANDS:</b> None. Use the supported interface named above.",
                    "BodySmall",
                ),
            ]
        )
    restart_accent = (
        colors.HexColor("#A24D00")
        if not step.restart.upper().startswith("NO")
        else BLUE
    )
    restart_background = (
        PALE_AMBER if not step.restart.upper().startswith("NO") else PALE_BLUE
    )
    right = [
        mini_box(
                "RESTART NOW?",
            step.restart,
            inner_w,
            restart_accent,
            restart_background,
        ),
        Spacer(1, 6),
        para("<b>VERIFY BEFORE CONTINUING</b>", "BodySmall"),
        *bullet_flowables(step.verification, numbered=True),
    ]
    if step.verify_commands:
        right.extend(
            [
                Spacer(1, 4),
                para("<b>VERIFICATION COMMANDS</b>", "BodySmall"),
                code_block(step.verify_commands, inner_w),
            ]
        )
    right.extend(
        [
            Spacer(1, 5),
            mini_box("PASS LOOKS LIKE", step.pass_text, inner_w, TEAL, PALE_TEAL),
            Spacer(1, 5),
            mini_box(
                "IF IT DOES NOT PASS",
                step.if_not,
                inner_w,
                colors.HexColor("#A24D00"),
                PALE_AMBER,
            ),
            Spacer(1, 5),
            mini_box("ROLLBACK / RECOVERY", step.rollback, inner_w, BLUE, PALE_BLUE),
            Spacer(1, 5),
            mini_box("RECORD ONLY", step.evidence, inner_w, MUTED, PALE_GRAY),
        ]
    )
    columns = Table([[left, right]], colWidths=[column_w, column_w])
    columns.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.65, GRID),
                ("LINEBEFORE", (1, 0), (1, -1), 0.65, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    _, columns_h = columns.wrap(CONTENT_W, CONTENT_H)
    required = min(CONTENT_H - 6, columns_h + 105)
    return [
        CondPageBreak(required),
        heading(f"Step {step.step_id} - {step.title}", key, level=1),
        step_meta_table(step),
        Spacer(1, 5),
        callout("Goal", escape(step.goal), TEAL, PALE_TEAL),
        Spacer(1, 5),
        columns,
        Spacer(1, 12),
    ]


HOME_MATRIX_OVERRIDES = {
    "PLT-04": "Home: inventory CPU virtualization and test VBS/Memory integrity. Kernel DMA Protection is not a Home capability.",
    "PLT-06": "Home: use Device Encryption only when the device and Windows UI support it; prove independent recovery.",
    "DEF-07": "Not part of the Home procedure. See the edition-excluded capability register.",
    "NET-02": "Home: minimize Remote Assistance, Quick Assist, WinRM, Remote Registry, and unknown listeners. Home cannot host RDP.",
    "LOG-02": "Home: leave plaintext command-line capture off by default; collect only proportionate local audit data.",
}


PRO_MATRIX_OVERRIDES = {
    "PLT-04": "Pro: separately inventory CPU virtualization, IOMMU, Kernel DMA Protection, VBS, and Memory integrity.",
    "PLT-06": "Pro: use the supported BitLocker wizard, system-check restart, full status verification, and independent recovery.",
    "DEF-07": "Pro: audit Network Protection, run Microsoft's harmless test, then enforce and repeat the test.",
    "NET-02": "Pro: leave RDP hosting off unless required; if enabled, require NLA and trusted-network firewall scope.",
    "LOG-02": "Pro: command-line capture is optional, privacy-gated, and off by default.",
}


def control_matrix(edition, steps):
    overrides = HOME_MATRIX_OVERRIDES if edition == "Home" else PRO_MATRIX_OVERRIDES
    step_map = {}
    for step in steps:
        for control_id in step.controls:
            step_map.setdefault(control_id, []).append(step.step_id)
    rows = [
        [
            para("ID / PRIORITY", "CellHeader"),
            para(f"{edition.upper()} OUTCOME", "CellHeader"),
            para("PROCEDURE STEP", "CellHeader"),
            para("SOURCES", "CellHeader"),
        ]
    ]
    for control in CONTROLS:
        if edition == "Home" and control.control_id == "DEF-07":
            continue
        outcome = overrides.get(control.control_id, control.summary)
        steps_text = ", ".join(step_map.get(control.control_id, ("Reference only",)))
        source_labels = ", ".join(f"[{n}]" for n in CONTROL_SOURCES[control.control_id])
        rows.append(
            [
                para(f"{control.control_id}<br/>{control.priority}", "MatrixStatus"),
                para(escape(outcome), "MatrixCell"),
                para(escape(steps_text), "MatrixStatus"),
                para(escape(source_labels), "MatrixStatus"),
            ]
        )
    table = Table(
        rows,
        colWidths=[72, 480, 100, CONTENT_W - 652],
        repeatRows=1,
        splitByRow=1,
    )
    table.setStyle(base_table_style(len(rows), pad=3))
    return table


def home_unavailable_table(large=False):
    cell_style = "Body" if large else "Cell"
    rows = [
        [
            para("CONTROL / COMPONENT", "CellHeader"),
            para("NOT IN THE HOME PROCEDURE", "CellHeader"),
            para("WHY", "CellHeader"),
        ]
    ]
    for control_id, capability, reason in HOME_UNAVAILABLE:
        rows.append(
            [
                para(f"<b>{escape(control_id)}</b>", cell_style),
                para(escape(capability), cell_style),
                para(escape(reason), cell_style),
            ]
        )
    table = Table(rows, colWidths=[132, 205, CONTENT_W - 337], repeatRows=1)
    table.setStyle(base_table_style(len(rows), pad=8 if large else 6))
    return table


def asr_candidate_table():
    rows = [
        [
            para("FULL GUID", "CellHeader"),
            para("MICROSOFT RULE NAME", "CellHeader"),
            para("APPLICABILITY NOTE", "CellHeader"),
        ]
    ]
    for guid, title, note in ASR_CANDIDATES:
        rows.append(
            [
                para(escape(guid), "SBCCode"),
                para(escape(title)),
                para(escape(note)),
            ]
        )
    table = Table(
        rows,
        colWidths=[240, 225, CONTENT_W - 465],
        repeatRows=1,
        splitByRow=1,
    )
    table.setStyle(base_table_style(len(rows), pad=5))
    return table


def reference_table():
    rows = [[para("IEEE-STYLE REFERENCE", "CellHeader"), para("USE", "CellHeader")]]
    for number, (author, title, publication, url, purpose) in enumerate(REFERENCES, 1):
        publication_text = f", {publication}" if publication else ""
        citation = (
            f"[{number}] {author}, \"{title}\"{publication_text}. "
            f"[Online]. Available: {url}. Accessed: {SOURCE_ACCESS_DATE}."
        )
        rows.append(
            [
                para(
                    f"<link href='{escape(url)}' color='#2459A6'>{escape(citation)}</link>",
                    "Reference",
                ),
                para(escape(purpose), "Reference"),
            ]
        )
    table = Table(rows, colWidths=[476, CONTENT_W - 476], repeatRows=1)
    table.setStyle(base_table_style(len(rows), pad=3))
    return table


def reboot_gate_story():
    return [
        heading("Appendix A - Reboot gate", "reboot-gate"),
        para(
            "Use this gate after every firmware, Secure Boot, SMB1, Memory integrity, BitLocker system-check, or other restart-dependent change. "
            "Do not start the next material change until every applicable item passes.",
            "Body",
        ),
        compact_label_table(
            [
                ("1. SIGN IN", "Normal sign-in succeeds without an unexpected recovery prompt."),
                ("2. STABILITY", "No new crash, repeated hardware error, missing device, or unexplained restart appears."),
                ("3. FOCUSED CHECK", "The one feature just changed is effective in Windows runtime state."),
                ("4. WORKFLOWS", "Every affected Step 05 test passes."),
                ("5. LIMITS", "Applicable reliability and performance limits remain acceptable."),
                ("6. DECISION", "Record PASS and observe normal use, or HOLD and reverse only the latest change."),
            ]
        ),
        Spacer(1, 8),
        callout(
            "If Windows cannot boot",
            "Use the already proved Windows RE path. Restore only the latest documented reversible setting. "
            "Do not clear TPM, CMOS, or Secure Boot keys and do not stack another change.",
            colors.HexColor("#A24D00"),
            PALE_AMBER,
        ),
    ]


def pro_rdp_appendix():
    return [
        PageBreak(),
        heading("Appendix D - Optional Pro Remote Desktop host", "pro-rdp"),
        callout(
            "Default decision: OFF",
            "Skip this appendix when incoming Remote Desktop is not required. Never forward TCP 3389 directly from the Internet; use a trusted VPN for outside-network access.",
            TEAL,
            PALE_TEAL,
        ),
        para(
            "<b>Preconditions:</b> trusted Private network; strong unique password; NLA-capable client; intended account; "
            "documented need; no unknown management policy.",
            "Body",
        ),
        para("<b>Do this in order</b>", "BodySmall"),
        *bullet_flowables(
            (
                "Settings > System > Remote Desktop > On.",
                "Keep Require devices to use Network Level Authentication enabled.",
                "Under Remote Desktop users, add only the intended account; avoid routine remote administrator use.",
                "In Windows Firewall with Advanced Security, keep Remote Desktop inbound rules off on Public.",
                "Limit the allowed remote addresses to Local subnet or a narrower trusted range.",
                "From a second trusted device, test the intended account and confirm no other account can sign in.",
            ),
            numbered=True,
        ),
        code_block(
            (
                "$path = 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server'",
                "Get-ItemPropertyValue -Path $path -Name fDenyTSConnections",
                "$nlaPath = \"$path\\WinStations\\RDP-Tcp\"",
                "Get-ItemPropertyValue -Path $nlaPath -Name UserAuthentication",
                "Get-NetTCPConnection -LocalPort 3389 -State Listen `",
                "  -ErrorAction SilentlyContinue",
            )
        ),
        Spacer(1, 6),
        callout(
            "PASS",
            "fDenyTSConnections is 0, UserAuthentication is 1, only intended accounts connect, rules exclude Public, "
            "remote scope is LocalSubnet or narrower, and no direct Internet exposure exists.",
            TEAL,
            PALE_TEAL,
        ),
        callout(
            "Rollback",
            "Settings > System > Remote Desktop > Off. Verify fDenyTSConnections is 1 and no TCP 3389 listener remains.",
            BLUE,
            PALE_BLUE,
        ),
    ]


def pro_command_line_appendix():
    return [
        PageBreak(),
        heading("Appendix E - Optional Pro Event 4688 command-line content", "pro-4688"),
        callout(
            "Default decision: OFF",
            "Command-line arguments are stored in plaintext and can contain passwords, tokens, private paths, and personal data. "
            "Enable this only for a defined investigative use with restricted access, retention, and review.",
            colors.HexColor("#A24D00"),
            PALE_AMBER,
        ),
        para("<b>Do this in order only after accepting the privacy cost</b>", "BodySmall"),
        *bullet_flowables(
            (
                "Open secpol.msc > Advanced Audit Policy Configuration > Detailed Tracking > Audit Process Creation and enable Success.",
                "Open gpedit.msc > Computer Configuration > Administrative Templates > System > Audit Process Creation.",
                "Set Include command line in process creation events to Enabled.",
                "Apply policy, generate the harmless Notepad test below, and inspect only the recent matching Security event.",
                "Define who can read the Security log, how long it is kept, and when this optional setting will be reviewed.",
            ),
            numbered=True,
        ),
        code_block(
            (
                "gpupdate.exe /target:computer /force",
                "$start = Get-Date",
                "$notepad = Join-Path $env:WINDIR 'System32\\notepad.exe'",
                "Start-Process $notepad -ArgumentList 'SBC-4688-test.txt'",
                "$f = @{",
                "  LogName='Security'",
                "  ProviderName='Microsoft-Windows-Security-Auditing'",
                "  Id=4688",
                "  StartTime=$start",
                "}",
                "Get-WinEvent -FilterHashtable $f -MaxEvents 50 |",
                "  Select-Object -First 1 TimeCreated,Id,ProviderName",
            )
        ),
        Spacer(1, 6),
        callout(
            "PASS",
            "A new provider-scoped 4688 event appears for the harmless test, access and retention are controlled, and the owner accepts the privacy cost.",
            TEAL,
            PALE_TEAL,
        ),
        callout(
            "Rollback",
            "Return both policy settings to their recorded prior states and run gpupdate again. Do not clear the Security log. "
            "If a real secret was logged, treat it as exposed and rotate it.",
            BLUE,
            PALE_BLUE,
        ),
    ]


def implementation_guide_story(edition, steps):
    story = [
        Cover(edition),
        Spacer(1, 14),
        callout(
            "Use this edition only",
            f"This document contains one ordered path for Windows 11 {edition}. Complete each step, its restart decision, "
            "and its verification before moving to the next step.",
            TEAL,
            PALE_TEAL,
        ),
        Spacer(1, 8),
        callout(
            "Independent guidance",
            "This independent informational aid is not endorsed by Microsoft or any hardware or security vendor. "
            "It is not a live audit, certification, guarantee, incident-response plan, or substitute for professional advice.",
        ),
        Spacer(1, 8),
        callout(
            "License and release notice",
            "Guide materials: CC BY-NC-ND 4.0. Controlled-author terms apply; see LICENSE.md. "
            f"Version {VERSION}. Source review cut-off: {SOURCE_REVIEW_DATE}. Current authoritative documentation takes precedence.",
        ),
        PageBreak(),
        heading("Start here", f"{edition.lower()}-start"),
        para(
            "This is the implementation path. The full control matrix, source traceability, evidence rules, and optional advanced "
            "material follow in appendices so they do not interrupt the work.",
            "Body",
        ),
        callout(
            "Mandatory stop",
            "Stop for an organization-managed device, suspected compromise, repeated instability, unavailable recovery, "
            "or an unexplained recovery prompt. Do not remove management, clear security keys, or keep hardening during an incident.",
            colors.HexColor("#A24D00"),
            PALE_AMBER,
        ),
        Spacer(1, 8),
        heading("Four labels used throughout", f"{edition.lower()}-labels", level=1),
        compact_label_table(
            [
                ("[USER]", "Run from the normal Windows account; no elevation is expected."),
                ("[ADMIN]", "Open PowerShell or Windows Terminal with Run as administrator."),
                ("[FIRMWARE]", "Use only the exact-model OEM UEFI/firmware interface and documentation."),
                ("REBOOT GATE", "Restart now, verify the one change, run required workflows, and stop on failure."),
            ]
        ),
        Spacer(1, 8),
        heading("Result states", f"{edition.lower()}-states", level=1),
        result_state_table(),
        PageBreak(),
        heading("Quick implementation path", f"{edition.lower()}-quick-path"),
        para(
            "Follow the step numbers in order. A conditional restart means the full step contains the exact trigger. "
            "Do not interpret CONFIGURED as PASS; the verification column in the step must pass.",
            "Body",
        ),
        quick_path_table(steps),
    ]
    for step in steps:
        story.extend(step_story(step, edition))
    story.extend([PageBreak(), *reboot_gate_story()])
    if edition == "Home":
        story.extend(
            [
                PageBreak(),
                heading("Appendix B - Pro-only capabilities excluded from Home", "home-unavailable"),
                para(
                    "These items are listed once for clarity. They do not appear as implementation steps in the Home path.",
                    "Body",
                ),
                home_unavailable_table(),
                PageBreak(),
                heading("Appendix C - Home control matrix", "home-matrix"),
                para(
                    "The matrix is a reference and traceability appendix. Use the numbered procedure above to do the work.",
                    "Body",
                ),
                control_matrix(edition, steps),
                PageBreak(),
                heading("Appendix D - ASR candidate reference", "home-asr-candidates"),
                para(
                    "This list identifies candidates; it does not prescribe a bulk preset. Use current Microsoft applicability "
                    "and deploy one full GUID at a time through Step 21.",
                    "Body",
                ),
                asr_candidate_table(),
            ]
        )
    else:
        story.extend(
            [
                PageBreak(),
                heading("Appendix B - Pro control matrix", "pro-matrix"),
                para(
                    "The matrix is a reference and traceability appendix. Use the numbered procedure above to do the work.",
                    "Body",
                ),
                control_matrix(edition, steps),
                PageBreak(),
                heading("Appendix C - ASR candidate reference", "pro-asr-candidates"),
                para(
                    "This list identifies candidates; it does not prescribe a bulk preset. Use current Microsoft applicability "
                    "and deploy one full GUID at a time through Step 21.",
                    "Body",
                ),
                asr_candidate_table(),
                *pro_rdp_appendix(),
                *pro_command_line_appendix(),
            ]
        )
    story.extend(
        [
            PageBreak(),
            heading(
                f"Appendix {'E' if edition == 'Home' else 'F'} - IEEE-style references",
                f"{edition.lower()}-references",
            ),
            para(
                f"Source review cut-off: {SOURCE_REVIEW_DATE}. Reference numbers remain stable within version {VERSION}. "
                "Product behavior, licensing, interfaces, and recommendations can change.",
                "Body",
            ),
            reference_table(),
        ]
    )
    return story


def workbook_step_card(step, edition):
    blank = "____________________________"
    header = para(
        f"<b>STEP {step.step_id} - {escape(step.title)}</b><br/>"
        f"{escape(', '.join(step.controls))} | {escape(step.priority)} | INITIAL STATUS: NOT ASSESSED",
        "CellHeader",
    )
    rows = [
        [header, ""],
        [
            para(f"<b>Result:</b> {blank}", "WorkbookField"),
            para(f"<b>Date:</b> {blank}", "WorkbookField"),
        ],
        [
            para(f"<b>Prior state:</b> {blank}", "WorkbookField"),
            para(f"<b>New state:</b> {blank}", "WorkbookField"),
        ],
        [
            para(f"<b>Restart completed:</b> {blank}", "WorkbookField"),
            para(f"<b>Owner:</b> {blank}", "WorkbookField"),
        ],
        [
            para("<b>Sanitized result / evidence reference:</b><br/><br/>", "WorkbookField"),
            para("<b>HOLD / exception / rollback:</b><br/><br/>", "WorkbookField"),
        ],
        [
            para(f"<b>Required workflows:</b> {blank}", "WorkbookField"),
            para(f"<b>Next review:</b> {blank}", "WorkbookField"),
        ],
    ]
    table = Table(
        rows,
        colWidths=[CONTENT_W / 2, CONTENT_W / 2],
        rowHeights=[28, 24, 24, 24, 42, 24],
    )
    table.setStyle(
        TableStyle(
            [
                ("SPAN", (0, 0), (-1, 0)),
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, 3), PALE_BLUE),
                ("BACKGROUND", (0, 5), (-1, 5), PALE_GRAY),
                ("GRID", (0, 0), (-1, -1), 0.5, GRID),
                ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 7)])


def workbook_signoff_summary():
    rows = [
        [
            para("<b>Overall disposition</b>", "WorkbookField"),
            para(
                "PASS / HOLD / EXCEPTION: ________________________________",
                "WorkbookField",
            ),
        ],
        [
            para(
                "<b>Unresolved steps, controls, or exception references</b>",
                "WorkbookField",
            ),
            para("<br/><br/>", "WorkbookField"),
        ],
        [
            para("<b>Reviewed / approved by</b>", "WorkbookField"),
            para(
                "_______________________________   Date: __________________",
                "WorkbookField",
            ),
        ],
        [
            para("<b>Next reassessment</b>", "WorkbookField"),
            para(
                "Date or event trigger: ____________________________________",
                "WorkbookField",
            ),
        ],
    ]
    table = Table(
        rows,
        colWidths=[245, CONTENT_W - 245],
        rowHeights=[30, 46, 30, 30],
    )
    table.setStyle(base_table_style(len(rows), pad=6, header=False))
    return table


def edition_workbook_story(edition, steps):
    story = [
        Cover(edition, workbook=True),
        Spacer(1, 14),
        callout(
            "Use with the matching guide",
            f"This workbook follows the Windows 11 {edition} guide in the same order. Do not use it with the other edition.",
            TEAL,
            PALE_TEAL,
        ),
        Spacer(1, 8),
        callout(
            "Never write secrets",
            "Do not record recovery keys, passwords, tokens, raw logs, unredacted paths, account names, serials, addresses, or device identifiers.",
        ),
        PageBreak(),
        heading("Assessment instructions", f"{edition.lower()}-workbook-instructions"),
        para(
            "Device label: ______________________________________   Assessment owner: ________________________________<br/>"
            "Start date: __________________   Scope/exclusions: ___________________________________________________________<br/><br/>"
            "Complete cards in numerical order. A configured value is not PASS until the matching guide verification and required workflows pass.",
            "Body",
        ),
        result_state_table(),
        Spacer(1, 8),
        callout(
            "Restart record",
            "For every restart-dependent change, stop at the reboot gate, verify the one change, run affected workflows, and record the result before continuing.",
            BLUE,
            PALE_BLUE,
        ),
        PageBreak(),
        heading("Ordered step record", f"{edition.lower()}-workbook-steps"),
        para(
            "Use one card per guide step. Preserve sensitive supporting evidence outside this printable record.",
            "BodySmall",
        ),
    ]
    for step in steps:
        story.append(CondPageBreak(180))
        story.append(workbook_step_card(step, edition))
    story.extend(
        [
            CondPageBreak(166),
            Spacer(1, 10),
            para("<b>Final sign-off summary</b>", "H2"),
            para(
                "Complete this only after the final guide acceptance step. Keep sensitive supporting evidence outside this workbook.",
                "BodySmall",
            ),
            workbook_signoff_summary(),
        ]
    )
    if edition == "Home":
        story.extend(
            [
                PageBreak(),
                heading("Home edition-excluded register", "home-workbook-unavailable"),
                para(
                    "These capabilities are preclassified as outside the Home procedure. Do not spend assessment time trying to enable them.",
                    "Body",
                ),
                home_unavailable_table(large=True),
            ]
        )
    story.extend(
        [
            PageBreak(),
            heading("Exception and review register", f"{edition.lower()}-workbook-exceptions"),
            para(
                "Every retained exception needs an exact scope, owner, reason, compensating measure where useful, approval date, and next review.",
                "Body",
            ),
        ]
    )
    exception_rows = [
        [
            para("STEP / CONTROL", "CellHeader"),
            para("EXACT SCOPE AND REASON", "CellHeader"),
            para("OWNER / APPROVAL", "CellHeader"),
            para("NEXT REVIEW", "CellHeader"),
        ]
    ]
    for _ in range(10):
        exception_rows.append(["", "", "", ""])
    exception_table = Table(
        exception_rows,
        colWidths=[110, 350, 160, CONTENT_W - 620],
        rowHeights=[24] + [39] * 10,
        repeatRows=1,
    )
    exception_table.setStyle(base_table_style(len(exception_rows), pad=5))
    story.append(exception_table)
    return story


def accessible_asr_appendix_lines():
    lines = [
        "",
        "## ASR candidate appendix",
        "",
        "Use this table to replace `PASTE-FULL-GUID-FROM-ASR-CANDIDATE-APPENDIX` "
        "in the Step 21 command. Copy one complete GUID exactly as shown.",
        "",
        "### Safety notes",
        "",
        "- This is a candidate reference, not a recommendation to enable every rule.",
        "- Recheck the selected GUID, rule name, prerequisites, and current behavior "
        "against the Microsoft ASR rule reference [12].",
        "- Stop if ASR is already controlled by organizational policy, device "
        "management, or another authorized owner. Do not overwrite managed settings.",
        "- Inventory existing GUID/action pairs first. Evaluate exactly one applicable "
        "rule in Audit mode and complete the required workflow observation cycle.",
        "- Change only that same reviewed rule to Enabled after its audit results, "
        "exceptions, rollback, and ownership are understood.",
        "- Never paste the placeholder text into PowerShell and never deploy the full "
        "candidate list as an untested bundle.",
        "",
        "| Full GUID | Microsoft rule name | Applicability and safety note |",
        "| --- | --- | --- |",
    ]
    for guid, title, note in ASR_CANDIDATES:
        lines.append(f"| `{guid}` | {title} | {note} |")
    return lines


def write_accessible_guide(path, edition, steps):
    lines = [
        f"# Windows 11 {edition} Security Baseline",
        "",
        "## Accessible ordered implementation guide",
        "",
        f"Version {VERSION}. Source review cut-off: {SOURCE_REVIEW_DATE}.",
        "",
        "Use the steps in numerical order. Complete each action, restart decision, verification, and recovery decision before continuing.",
        "",
        "This is an independent informational aid. It is not vendor-endorsed, a certification, guarantee, incident-response plan, or professional advice. Guide materials are CC BY-NC-ND 4.0 under the controlled-author terms in [LICENSE.md](../LICENSE.md).",
        "",
        "## Result states",
        "",
    ]
    for state, meaning in RESULT_STATES:
        lines.append(f"- **{state}:** {meaning}")
    if edition == "Home":
        lines.extend(["", "## Capabilities excluded from the Home procedure", ""])
        for control_id, capability, reason in HOME_UNAVAILABLE:
            lines.append(f"- **{control_id} - {capability}:** {reason}")
    current_phase = None
    phase_segment = 0
    phase_occurrences = {}
    for step in steps:
        if step.phase != current_phase:
            phase_segment += 1
            phase_occurrences[step.phase] = phase_occurrences.get(step.phase, 0) + 1
            occurrence = phase_occurrences[step.phase]
            continuation = (
                ""
                if occurrence == 1
                else " (continued)"
                if occurrence == 2
                else f" (continued {occurrence - 1})"
            )
            lines.extend(
                [
                    "",
                    f"## Phase {phase_segment:02d} - {step.phase}{continuation}",
                    "",
                ]
            )
            current_phase = step.phase
        lines.extend(
            [
                f"### Step {step.step_id} - {step.title}",
                "",
                f"- **Controls:** {', '.join(step.controls)}",
                f"- **Priority:** {step.priority}",
                f"- **Run as:** {step.access}",
                f"- **Action type:** {step.classification}",
                f"- **Sources:** {', '.join(f'[{n}]' for n in step.sources)}",
                f"- **Goal:** {step.goal}",
                "",
                "#### Before you start",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in step.prerequisites)
        lines.extend(["", "#### Do this in order", ""])
        lines.extend(f"{index}. {item}" for index, item in enumerate(step.actions, 1))
        lines.extend(["", "#### Commands", ""])
        if step.commands:
            lines.extend(["```powershell", *step.commands, "```"])
        else:
            lines.append("No command. Use the supported interface named above.")
        lines.extend(["", f"#### Restart now?", "", step.restart, "", "#### Verify before continuing", ""])
        lines.extend(f"{index}. {item}" for index, item in enumerate(step.verification, 1))
        if step.verify_commands:
            lines.extend(["", "```powershell", *step.verify_commands, "```"])
        lines.extend(
            [
                "",
                f"- **PASS looks like:** {step.pass_text}",
                f"- **If it does not pass:** {step.if_not}",
                f"- **Rollback / recovery:** {step.rollback}",
                f"- **Record only:** {step.evidence}",
            ]
        )
    lines.extend(accessible_asr_appendix_lines())
    lines.extend(["", "## Full control matrix", ""])
    step_map = {}
    for step in steps:
        for control_id in step.controls:
            step_map.setdefault(control_id, []).append(step.step_id)
    overrides = HOME_MATRIX_OVERRIDES if edition == "Home" else PRO_MATRIX_OVERRIDES
    for control in CONTROLS:
        if edition == "Home" and control.control_id == "DEF-07":
            continue
        outcome = overrides.get(control.control_id, control.summary)
        step_text = ", ".join(step_map.get(control.control_id, ("Reference only",)))
        source_text = ", ".join(f"[{n}]" for n in CONTROL_SOURCES[control.control_id])
        lines.extend(
            [
                f"### {control.control_id} - {control.title}",
                "",
                f"- **Priority:** {control.priority}",
                f"- **Procedure step:** {step_text}",
                f"- **Outcome:** {outcome}",
                f"- **Sources:** {source_text}",
                "",
            ]
        )
    lines.extend(["## IEEE-style references", ""])
    for number, (author, title, publication, url, purpose) in enumerate(REFERENCES, 1):
        publication_text = f", {publication}" if publication else ""
        lines.append(
            f"[{number}] {author}, \"{title}\"{publication_text}. "
            f"[Online]. Available: {url}. Accessed: {SOURCE_ACCESS_DATE}. {purpose}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def page_decorator(title, short_title, subject, keywords):
    def decorate(c, doc):
        configure_canvas(c, title, subject, keywords)
        if c.getPageNumber() == 1:
            return
        c.saveState()
        c.setStrokeColor(GRID)
        c.line(MARGIN_X, PAGE_H - 29, PAGE_W - MARGIN_X, PAGE_H - 29)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(MARGIN_X, PAGE_H - 19, short_title)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.3)
        c.drawRightString(
            PAGE_W - MARGIN_X,
            PAGE_H - 19,
            f"Version {VERSION} | Source review cut-off: {SOURCE_REVIEW_DATE}",
        )
        c.line(MARGIN_X, 24, PAGE_W - MARGIN_X, 24)
        c.setFont("Helvetica", 7.1)
        c.drawString(
            MARGIN_X,
            12,
            "Independent informational aid | CC BY-NC-ND 4.0 controlled-author terms in LICENSE.md | Do not record secrets",
        )
        c.setFont("Helvetica-Bold", 7.2)
        c.drawRightString(PAGE_W - MARGIN_X, 12, f"PAGE {c.getPageNumber()}")
        c.restoreState()

    return decorate


def build_pdf(output_path, title, subject, story, short_title, keywords):
    doc = OutlineDocTemplate(
        str(output_path),
        pagesize=landscape(letter),
        invariant=1,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title=title,
        author=AUTHOR,
        subject=subject,
        creator=AUTHOR,
        keywords=keywords,
    )
    frame = Frame(
        MARGIN_X,
        BOTTOM,
        CONTENT_W,
        CONTENT_H,
        id="main",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    template = PageTemplate(
        id="all-pages",
        frames=[frame],
        onPage=page_decorator(title, short_title, subject, keywords),
    )
    doc.addPageTemplates([template])
    doc.build(story)


def write_checksums(paths):
    lines = []
    for path in sorted(paths, key=lambda item: item.name):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}")
    CHECKSUM_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    # ReportLab reads this standard variable when invariant mode is enabled.
    # Pinning it to the documented source-review date keeps metadata meaningful
    # while allowing committed artifacts to be reproduced byte for byte.
    os.environ["SOURCE_DATE_EPOCH"] = PDF_BUILD_EPOCH
    DOCS.mkdir(parents=True, exist_ok=True)
    build_pdf(
        HOME_GUIDE_OUT,
        "Amy's Windows 11 Home Security Baseline",
        "Ordered Windows 11 Home security implementation guide with commands, restart gates, verification, rollback, and evidence controls",
        implementation_guide_story("Home", HOME_STEPS),
        "WINDOWS 11 HOME SECURITY BASELINE",
        "Windows 11, security baseline, least privilege, recovery, Microsoft Defender, implementation guide",
    )
    build_pdf(
        HOME_WORKBOOK_OUT,
        "Amy's Windows 11 Home Assessment Workbook",
        "Printable ordered assessment workbook for the Windows 11 Home Security Baseline",
        edition_workbook_story("Home", HOME_STEPS),
        "WINDOWS 11 HOME ASSESSMENT WORKBOOK",
        "Windows 11, security baseline, least privilege, recovery, Microsoft Defender, assessment workbook, printable checklist",
    )
    build_pdf(
        PRO_GUIDE_OUT,
        "Amy's Windows 11 Pro Security Baseline",
        "Ordered Windows 11 Pro security implementation guide with commands, restart gates, verification, rollback, and evidence controls",
        implementation_guide_story("Pro", PRO_STEPS),
        "WINDOWS 11 PRO SECURITY BASELINE",
        "Windows 11, security baseline, least privilege, recovery, Microsoft Defender, implementation guide",
    )
    build_pdf(
        PRO_WORKBOOK_OUT,
        "Amy's Windows 11 Pro Assessment Workbook",
        "Printable ordered assessment workbook for the Windows 11 Pro Security Baseline",
        edition_workbook_story("Pro", PRO_STEPS),
        "WINDOWS 11 PRO ASSESSMENT WORKBOOK",
        "Windows 11, security baseline, least privilege, recovery, Microsoft Defender, assessment workbook, printable checklist",
    )
    write_accessible_guide(HOME_ACCESSIBLE_OUT, "Home", HOME_STEPS)
    write_accessible_guide(PRO_ACCESSIBLE_OUT, "Pro", PRO_STEPS)
    write_checksums(RELEASE_PDFS)
    for path in RELEASE_PDFS:
        print(path)
    print(HOME_ACCESSIBLE_OUT)
    print(PRO_ACCESSIBLE_OUT)
    print(CHECKSUM_OUT)


if __name__ == "__main__":
    main()
