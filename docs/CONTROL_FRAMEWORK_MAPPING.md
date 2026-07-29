# Informative Control Framework Mapping

## Windows 11 Home and Pro Security Baseline

Version 1.0.0. Source review cut-off: 29 July 2026.

Copyright (c) 2026 Amyashi. This guide material is licensed under CC BY-NC-ND
4.0 under the controlled-author terms in [LICENSE.md](../LICENSE.md).

## Purpose

This document maps the public guide's major security areas to:

- the NIST Cybersecurity Framework (CSF) 2.0;
- CIS Controls v8.1, with emphasis on Implementation Group 1 (IG1); and
- Microsoft Windows security baseline concepts.

The mapping helps readers understand why a control area matters, identify coverage gaps, and plan future improvements. It also gives maintainers a stable structure for tracing guide content to authoritative sources.

## Important limits

This is an informative crosswalk. It is not:

- a claim of compliance, certification, conformance, or audit completion;
- a substitute for the complete text of any framework or benchmark;
- a legal, regulatory, contractual, or risk-acceptance opinion;
- a claim that Windows 11 Home can implement every enterprise control;
- a reproduction of the CIS Benchmarks or Microsoft baseline settings; or
- evidence that a particular computer is secure.

NIST CSF 2.0 describes cybersecurity outcomes. It is not a prescriptive product checklist. CIS Controls describe prioritized safeguards for organizations; IG1 is an enterprise-oriented minimum set, not a Windows-only configuration standard. Microsoft's downloadable security baselines are primarily designed for managed environments and often assume Group Policy, mobile device management, or enterprise licensing.

The public guide translates selected concepts into practical guidance for personally owned, unmanaged Windows 11 Home and Pro computers. A mapping means that a guide area supports an outcome or safeguard; it does not mean the outcome or safeguard is fully satisfied.

## Framework shorthand

### NIST CSF 2.0 functions and categories used here

- **GV** — Govern
  - **GV.OC** — Organizational Context
  - **GV.RM** — Risk Management Strategy
  - **GV.RR** — Roles, Responsibilities, and Authorities
  - **GV.PO** — Policy
  - **GV.OV** — Oversight
- **ID** — Identify
  - **ID.AM** — Asset Management
  - **ID.RA** — Risk Assessment
  - **ID.IM** — Improvement
- **PR** — Protect
  - **PR.AA** — Identity Management, Authentication, and Access Control
  - **PR.AT** — Awareness and Training
  - **PR.DS** — Data Security
  - **PR.PS** — Platform Security
  - **PR.IR** — Technology Infrastructure Resilience
- **DE** — Detect
  - **DE.CM** — Continuous Monitoring
  - **DE.AE** — Adverse Event Analysis
- **RS** — Respond
  - **RS.MA** — Incident Management
  - **RS.AN** — Incident Analysis
  - **RS.CO** — Incident Response Reporting and Communication
  - **RS.MI** — Incident Mitigation
- **RC** — Recover
  - **RC.RP** — Incident Recovery Plan Execution
  - **RC.CO** — Incident Recovery Communication

### CIS Controls v8.1 used here

1. Inventory and Control of Enterprise Assets
2. Inventory and Control of Software Assets
3. Data Protection
4. Secure Configuration of Enterprise Assets and Software
5. Account Management
6. Access Control Management
7. Continuous Vulnerability Management
8. Audit Log Management
9. Email and Web Browser Protections
10. Malware Defenses
11. Data Recovery
12. Network Infrastructure Management
13. Network Monitoring and Defense
14. Security Awareness and Skills Training
15. Service Provider Management
16. Application Software Security
17. Incident Response Management
18. Penetration Testing

IG1 applicability must be checked against the current CIS Controls Navigator and official CIS publications. A control number below identifies a related control family, not proof that every IG1 safeguard in that family is implemented.

### Microsoft concepts used here

The Microsoft column refers to public concepts such as:

- supported Windows versions and security updates;
- the Microsoft Security Compliance Toolkit and Windows security baselines;
- hardware-backed security, Secure Boot, TPM, virtualization-based security, and memory integrity;
- Microsoft Defender Antivirus, attack surface reduction, network protection, and Controlled Folder Access;
- Windows Firewall, local account controls, User Account Control, data encryption, recovery, and auditing; and
- testing, tailoring, documenting exceptions, and monitoring baseline changes.

Some concepts or management methods are edition-, hardware-, license-, or organization-dependent.

## Stable control families

The generated guide and printable workbook use the following stable control families. The detailed framework crosswalk below is broader and also covers supplemental text guidance, so a framework relationship must not be interpreted as a separate assessed control.

| Stable control family | Scope |
| --- | --- |
| GOV-01 through GOV-02 | Authority, scope, and evidence handling |
| REC-01 through REC-03 | Backups, encryption recovery, Windows RE, and recovery administration |
| PLT-01 through PLT-06 | Supported Windows, boot trust, TPM, virtualization, firmware, and data-at-rest protection |
| ID-01 through ID-03 | Daily-use least privilege, authentication recovery, and UAC |
| DEF-01 through DEF-07 | Antimalware foundation, tamper and cloud protection, PUA, ASR, CFA, and Network Protection |
| APP-01 through APP-02 | Application reputation, VBS/HVCI, and vulnerable-driver blocking |
| NET-01 through NET-04 | Firewall, remote exposure, SMB, DNS, and network failover |
| LOG-01 through LOG-03 | Audit scope, command-line privacy, and provider-scoped event review |
| OPS-01 through OPS-04 | Exceptions, staged change, incident stop, and scheduled review |
| PERF-01 through PERF-02 | Representative performance and workflow acceptance |

## Guide-to-framework crosswalk

| Guide area | NIST CSF 2.0 relationship | CIS Controls v8.1 relationship | Microsoft baseline concept | Coverage note |
|---|---|---|---|---|
| Scope, audience, priorities, status, and exceptions | GV.OC, GV.RM, GV.PO, GV.OV, ID.IM | Primarily supports governance across Controls 1–18 | Define a baseline, tailor it, test it, record deviations, and reassess it | Partial. The guide gives personal-device governance, not an organizational risk program. |
| Windows edition, version, support, and update state | ID.AM, ID.RA, PR.PS | Controls 1, 2, and 7 | Run a supported release and install security and servicing updates | Strong for one computer; no enterprise inventory or centralized patch reporting. |
| UEFI, Secure Boot, certificate readiness, and firmware | ID.AM, PR.PS, PR.IR | Controls 4 and 7 | Hardware root of trust, Secure Boot, firmware servicing, and compatible recovery planning | Practical coverage only. Firmware configuration and update behavior are vendor-specific. |
| TPM, virtualization, DMA protection, VBS, HVCI, and memory integrity | ID.AM, PR.PS, PR.IR | Controls 4 and 7 | Hardware-backed isolation, TPM, virtualization-based security, and memory integrity | Hardware and edition dependent. Not every device can expose or support every feature. |
| LSA protection and credential hardening | PR.AA, PR.PS | Controls 5 and 6 | Protect authentication material and reduce credential theft paths | Partial. No domain credential policy, Windows Hello for Business deployment, or identity monitoring. |
| Standard user, administrator, UAC, and role separation | GV.RR, PR.AA | Controls 5 and 6 | Least privilege, separate administrative use, and elevation prompts | Strong for local accounts; no privileged access management or centralized role lifecycle. |
| Passwords, MFA, account recovery, and recovery codes | PR.AA, PR.AT, RC.RP | Controls 5, 6, and 14 | Strong authentication, protected recovery methods, and account recovery readiness | Partial. External account providers have separate policies and interfaces. |
| Device encryption, BitLocker, and recovery-key handling | PR.DS, PR.IR, RC.RP | Controls 3 and 11 | Protect data at rest and preserve authorized recovery | Strong conceptually; availability and management differ by edition, hardware, and account type. |
| Microsoft Defender Antivirus, cloud protection, PUA protection, and tamper protection | PR.PS, DE.CM | Controls 4 and 10 | Built-in anti-malware protection, cloud-delivered protection, and protection against configuration tampering | Good local coverage; no endpoint detection and response or central alert handling. |
| Defender Network Protection | PR.PS, PR.IR, DE.CM | Controls 9, 10, and 13 | Block or audit connections to known malicious or suspicious destinations | Edition and licensing dependent. The guide must permit N/A rather than unsafe substitutes. |
| Controlled Folder Access | PR.DS, PR.PS, DE.CM | Controls 3 and 10 | Reduce unauthorized changes to protected data folders | Compatibility-sensitive. Audit or limited deployment may be more appropriate than broad enforcement. |
| Defender exclusions | GV.RM, PR.PS, DE.CM | Controls 4 and 10 | Minimize exceptions, document business need, and review exclusions | Strong principle; the guide does not replace product-specific vendor validation. |
| Attack Surface Reduction rules | PR.PS, DE.CM | Controls 4 and 10 | Reduce common process, script, Office, credential, and driver abuse paths | Compatibility-sensitive. Some rules overlap with other protections or require audit-first rollout. |
| SmartScreen, Smart App Control, application reputation, and vulnerable-driver blocking | PR.PS, DE.CM | Controls 2, 4, and 10 | Application reputation, application control, and known-vulnerable driver defenses | Partial. Smart App Control availability and state depend on installation history and supported configuration. |
| Exploit Protection | PR.PS | Controls 4 and 10 | System and application exploit mitigations with minimal customization | Baseline-oriented. Per-application overrides require testing and a documented reason. |
| Edge, Firefox, downloads, extensions, and browser hardening | PR.PS, PR.AT, DE.CM | Controls 2, 9, 10, and 14 | Supported browsers, reputation checks, safe downloads, extension control, and patching | Practical local coverage; no central browser policy or web gateway. |
| DNS resolver selection and encrypted DNS | PR.IR, DE.CM | Controls 12 and 13 | Reliable name resolution and transport protection where supported | Limited. DNS filtering is not a complete content-control or malware-defense system. |
| Windows Firewall and network profiles | PR.PS, PR.IR, DE.CM | Controls 4, 12, and 13 | Host firewall enabled on all profiles, restrictive inbound behavior, and profile-aware rules | Strong local coverage; no network firewall, router, or centralized telemetry assessment. |
| Remote Desktop, Remote Assistance, Quick Assist, Remote Registry, and WinRM | PR.AA, PR.PS, PR.IR, DE.CM | Controls 4, 6, 12, and 13 | Disable unused remote services, restrict administrative access, and monitor allowed access | Strong local principle; legitimate support requirements can justify documented exceptions. |
| SMB and legacy protocol reduction | PR.PS, PR.IR, DE.CM | Controls 4, 7, 12, and 13 | Remove legacy protocols and limit lateral movement paths | Compatibility-sensitive. Network discovery, file sharing, and business applications require testing. |
| Custom firewall rules, SMB egress limits, and application ports | GV.RM, PR.IR, DE.CM | Controls 4, 12, and 13 | Apply narrowly scoped rules and verify required traffic | Advanced and environment-specific. Overly broad rules can break recovery, updates, or applications. |
| Ethernet, Wi-Fi, VPN, and failover behavior | ID.AM, PR.IR, DE.CM | Controls 1, 12, and 13 | Treat networks according to trust, test failover, and avoid unintended exposure | Partial. Router security, wireless infrastructure, and VPN-provider risk are outside the guide. |
| Windows Script Host and VBScript | PR.PS, DE.CM | Controls 2, 4, and 10 | Reduce or remove unused scripting engines while preserving required applications | Compatibility-sensitive. N/A or exception may be correct when a supported application depends on the feature. |
| PowerShell execution policy and script safety | PR.PS, PR.AT, DE.CM | Controls 2, 4, 8, 10, and 14 | Script governance, logging, least privilege, and safe administrative practices | Partial. Execution policy is not a security boundary; no enterprise application control or full PowerShell logging program is provided. |
| Audit policy, process creation, command-line logging, and Event 4688 | DE.CM, DE.AE, RS.AN | Control 8 and support for Control 17 | Generate useful local security events, protect logs, and review relevant activity | Partial. No central collection, retention service, correlation, alerting, or time-synchronization assessment. |
| Windows Recovery Environment, backups, cloud synchronization, and restore testing | PR.IR, RC.RP, RC.CO | Controls 3 and 11 | Recovery environment readiness, protected recovery keys, independent backups, and restore tests | Good local foundation. Synchronization alone is not backup, and cloud-provider recovery is outside scope. |
| Incident identification, containment, evidence, and escalation | DE.AE, RS.MA, RS.AN, RS.CO, RS.MI | Controls 8 and 17 | Preserve useful information, contain carefully, use trusted recovery paths, and seek help when needed | Basic only. No organizational incident response team, communications plan, forensic procedure, or legal workflow. |
| Reliability, crash investigation, and security-setting tuning | GV.RM, ID.IM, DE.AE, RS.MI | Controls 4, 7, 8, and 17 | Test changes, identify security-versus-compatibility causes, and roll back safely | Partial. Reliability troubleshooting is not a substitute for security monitoring or root-cause analysis. |
| Periodic review, source checks, and change history | GV.OV, ID.IM, DE.CM | Controls 4, 7, and 8 | Reassess settings after feature updates, hardware changes, incidents, and source revisions | Strong maintenance concept; no automatic monitoring or assigned organizational owner. |

## Coverage by NIST CSF 2.0 function

### Govern — partial

The guide defines scope, priorities, statuses, evidence expectations, exceptions, and review triggers. It does not establish an organizational governance structure, risk appetite, supply-chain program, workforce roles, policy approval process, or executive oversight.

### Identify — partial

The guide identifies the Windows edition, version, hardware security capabilities, recovery state, and important software or network dependencies. It does not provide a complete hardware, software, data, service-provider, or business-process inventory.

### Protect — strongest coverage

Most guide content concerns secure configuration, least privilege, data protection, malware defenses, network restrictions, browser safety, and platform security. Coverage remains device-specific and does not equal the complete Microsoft Security Baseline, CIS Benchmark, or all IG1 safeguards.

### Detect — partial

The guide includes Defender state, selected protection events, local audit configuration, and Event Viewer checks. It does not implement continuous centralized monitoring, log aggregation, alert triage, behavioral analytics, or a security operations function.

### Respond — basic

The guide provides introductory containment, evidence, and escalation guidance. It does not provide a full incident response plan, predefined communications, authority assignments, forensic acquisition procedures, or exercise program.

### Recover — useful local foundation

The guide covers Windows Recovery Environment, recovery keys, backups, restore testing, and basic recovery sequencing. It does not establish organization-wide recovery objectives, alternate infrastructure, crisis communications, or disaster recovery exercises.

## Material gaps and out-of-scope areas

Readers and maintainers should not infer coverage where the guide is silent. Important limitations include:

1. **Unmanaged personal devices only.** The guide does not cover Active Directory, Microsoft Entra ID administration, Intune, Group Policy at scale, mobile device management, or enterprise change control.
2. **No complete benchmark implementation.** It is not a line-by-line implementation of the CIS Microsoft Windows Benchmark, the Microsoft Security Baseline, NIST SP 800-53, or any regulatory standard.
3. **No compliance claim.** There is no independent assessment, control testing program, sample method, evidence standard, or auditor attestation.
4. **No centralized detection.** The guide does not deploy endpoint detection and response, security information and event management, managed detection and response, or a staffed monitoring function.
5. **Limited inventory and vulnerability management.** It does not yet provide a complete software inventory, application owner, end-of-life tracking, third-party patch schedule, or formal vulnerability prioritization process.
6. **Limited application control.** Smart App Control, reputation checks, and ASR rules do not constitute a general allowlisting program.
7. **Network perimeter outside scope.** Routers, wireless access points, firewalls outside Windows, guest networks, IoT devices, and internet-service-provider equipment are not assessed.
8. **Other platforms outside scope.** Mobile devices, macOS, Linux, game consoles, hypervisors, cloud workloads, and network appliances require separate baselines.
9. **Physical security outside scope.** Theft deterrence, secure storage, tamper evidence, disposal, and facility access need separate consideration.
10. **Service-provider governance is limited.** Cloud account, backup provider, VPN provider, browser synchronization, and support-vendor risks are not fully assessed.
11. **Security awareness is introductory.** The guide includes safe-use cues but not a formal awareness, phishing, or role-based training program.
12. **Software development is outside scope.** Secure development, source control, dependency review, signing pipelines, and application security testing are separate concerns.
13. **No penetration-testing program.** Validation is limited to safe local observation and functional testing.
14. **No regulated-data design.** The guide is not designed to make a personal computer suitable for regulated, financial, health, legal, government, or other high-impact data.
15. **Edition and hardware constraints remain.** Home and Pro expose different controls, and security hardware capabilities vary by manufacturer and model.
16. **Product behavior changes.** Windows features, licensing, interfaces, defaults, and documentation can change after publication.

## How to use this mapping

### For a reader

Use the mapping to answer three questions:

1. Which security outcome does this guide area support?
2. Which nearby areas are not covered?
3. Does the device need a stronger organizational or managed-device baseline?

Do not convert a PASS in the guide into a statement such as “NIST compliant,” “CIS compliant,” or “Microsoft baseline compliant.”

### For a maintainer

When adding or changing a control:

1. assign a stable control identifier;
2. state the desired outcome in plain language;
3. document Home, Pro, hardware, and licensing applicability;
4. set the priority and allowed result states;
5. provide a UI-first verification method;
6. describe compatibility and recovery risks;
7. cite the primary source and record the source-check date;
8. map only the most directly related framework categories;
9. identify what the control does not cover; and
10. update the change history and next review date.

Recommended traceability fields are:

- control identifier;
- title and intended outcome;
- applicability;
- priority;
- allowed status values;
- expected state;
- verification method;
- evidence type and handling;
- owner or maintainer;
- exception reason and expiry date;
- primary source;
- source-check date;
- guide version introduced or changed; and
- next review date.

## Future maturity priorities

The following additions would close the most significant gaps without turning the personal-device guide into an enterprise standard:

1. a basic asset and software inventory worksheet;
2. a third-party application update and end-of-life review;
3. a data classification and backup coverage worksheet;
4. a short account and recovery inventory;
5. a local log review schedule with retention cautions;
6. an incident contact and decision card that contains no public personal information;
7. a restore-test record;
8. an exception register with review dates;
9. a hardware and edition applicability table; and
10. release-level regression testing for all instructions.

## Primary references

[1] National Institute of Standards and Technology, “The NIST Cybersecurity Framework (CSF) 2.0,” CSWP 29, Feb. 2024. [Online]. Available: <https://doi.org/10.6028/NIST.CSWP.29>. Accessed: Jul. 29, 2026.

[2] National Institute of Standards and Technology, “Guide to Enterprise Patch Management Planning: Preventive Maintenance for Technology,” NIST SP 800-40 Rev. 4, Apr. 2022. [Online]. Available: <https://csrc.nist.gov/pubs/sp/800/40/r4/final>. Accessed: Jul. 29, 2026.

[3] National Institute of Standards and Technology, “Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile,” NIST SP 800-61 Rev. 3, Apr. 2025. [Online]. Available: <https://csrc.nist.gov/pubs/sp/800/61/r3/final>. Accessed: Jul. 29, 2026.

[4] National Institute of Standards and Technology, “Digital Identity Guidelines: Authentication and Authenticator Management,” NIST SP 800-63B-4, Jul. 2025. [Online]. Available: <https://csrc.nist.gov/pubs/sp/800/63/b/4/final>. Accessed: Jul. 29, 2026.

[5] National Institute of Standards and Technology, “BIOS Protection Guidelines,” NIST SP 800-147, Apr. 2011. [Online]. Available: <https://csrc.nist.gov/pubs/sp/800/147/final>. Accessed: Jul. 29, 2026.

[6] Center for Internet Security, “CIS Critical Security Controls Version 8.1.” [Online]. Available: <https://www.cisecurity.org/controls/v8-1>. Accessed: Jul. 29, 2026.

[7] Center for Internet Security, “CIS Controls Implementation Group 1.” [Online]. Available: <https://www.cisecurity.org/controls/implementation-groups/ig1>. Accessed: Jul. 29, 2026.

[8] Center for Internet Security, “CIS Critical Security Controls Navigator.” [Online]. Available: <https://www.cisecurity.org/controls/cis-controls-list>. Accessed: Jul. 29, 2026.

[9] Microsoft, “Security baselines.” [Online]. Available: <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines>. Accessed: Jul. 29, 2026.

[10] Microsoft, “Security Compliance Toolkit and Baselines.” [Online]. Available: <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10>. Accessed: Jul. 29, 2026.

[11] Microsoft, “Download Microsoft Security Compliance Toolkit 1.0.” [Online]. Available: <https://www.microsoft.com/en-us/download/details.aspx?id=55319>. Accessed: Jul. 29, 2026.

[12] Microsoft, “Windows 11 Release Information.” [Online]. Available: <https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information>. Accessed: Jul. 29, 2026.

Current official publications take precedence if framework names, mappings, safeguards, baseline packages, licensing, or product behavior change.
