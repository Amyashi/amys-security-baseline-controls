# Windows 11 Home and Pro Security Baseline

## Accessible, screen-reader-friendly companion

Version 1.0.0. Source review cut-off: 29 July 2026.

Copyright (c) 2026 Amyashi. This guide material is licensed under CC BY-NC-ND
4.0 under the controlled-author terms in [LICENSE.md](../LICENSE.md).

This guide explains a compatibility-aware security baseline for a personally owned Windows 11 Home or Pro computer. It is written in a linear format for screen readers, text enlargement, keyboard navigation, printing, and readers who prefer plain language.

This companion describes the intended public baseline. It does not report the condition of any particular computer.

If your goal is to implement the baseline from start to finish, use the edition-specific ordered path:

- [Windows 11 Home accessible implementation guide](WINDOWS_11_HOME_ACCESSIBLE_GUIDE.md)
- [Windows 11 Pro accessible implementation guide](WINDOWS_11_PRO_ACCESSIBLE_GUIDE.md)

This comprehensive companion remains the deeper control-by-control reference and stable-ID crosswalk.

## Start here

Follow this decision path before changing a setting.

1. If you suspect ransomware, account takeover, unauthorized remote access, or another active compromise, stop normal use and go to [Incident basics](#incident-basics). Do not try to harden through an active incident.
2. If the computer is managed by an employer, school, family organizer, or device-management service, stop. Ask the responsible administrator before changing security, audit, networking, encryption, firmware, or account settings.
3. Confirm that Windows 11 and the installed edition are still supported. Install normal security updates through Windows Update, but do not bypass a documented safeguard hold.
4. Prove that recovery is possible. Confirm Windows Recovery Environment, a working administrator account, accessible drive-encryption recovery information when encryption is on, and a tested backup restore.
5. Record the current state before changing anything. Do not rely on an old screenshot or another computer's result.
6. Complete P0 safety gates first, then P1 core controls. Treat P2 and P3 items as enhanced or optional work.
7. Change one setting at a time. Restart when required, verify the runtime state, and test the programs and devices you actually use.
8. Stop after an unexplained block, lost save, crash, recovery prompt, boot problem, or repeatable performance regression. Preserve the evidence and reverse only the latest documented change.

If you are not sure whether a step applies, mark it **HOLD**. An honest HOLD is safer than forcing a setting.

## Audience and scope

This guide is intended for:

- A personally owned, general-purpose Windows 11 Home or Pro computer.
- A reader who wants stronger protection without unnecessarily breaking games, accessibility tools, creative software, peripherals, or ordinary home-network use.
- A system that uses Microsoft Defender Antivirus as its active antivirus.
- Routine hardening and verification, not live incident response.

This guide assumes that the reader can sign in, obtain administrator help when required, and use current Microsoft and hardware-vendor documentation.

This guide does not provide:

- A certification, guarantee, or complete implementation of a NIST, CIS, Microsoft, regulatory, or contractual baseline.
- Enterprise device management, domain, Microsoft Intune, Microsoft Defender for Endpoint, security information and event management, or centralized monitoring instructions.
- A substitute for the current manual and support page for the exact computer or motherboard model.
- A substitute for qualified incident-response, legal, privacy, or digital-forensics advice.
- A complete router, wireless-network, mobile-device, cloud-service, or physical-security baseline.

Windows editions, hardware, firmware, subscriptions, and management rights affect what is available. Never install an unofficial Group Policy editor or force an undocumented registry workaround to imitate a feature that the installed edition does not support.

## Threats considered

The baseline is designed primarily to reduce risk from:

- Commodity malware and ransomware.
- Malicious or compromised downloads, installers, scripts, mods, browser content, and drivers.
- Credential theft and account takeover.
- Unnecessary local administrator use.
- Unwanted inbound network access and unused remote-management features.
- Unsafe security exclusions and overly broad firewall rules.
- Failed recovery after a firmware, encryption, or boot-security change.

The baseline does not assume that every user faces the same risk. A high-profile person, journalist, activist, developer handling production credentials, or person facing a targeted adversary needs a separate threat assessment and stronger controls.

## Priority definitions

Priority is a workflow aid. It is not a CVSS score, a Microsoft severity, or a prediction that compromise will occur.

### P0 - safety gate or stop condition

Complete or resolve P0 before a related high-impact change. Examples include recovery readiness, active security protection, known administrator access, and unresolved boot or stability problems.

If a P0 fails, use **HOLD**. Do not work around it.

### P1 - core baseline

P1 controls provide the normal security foundation for an applicable system. Complete them after P0 gates pass. A P1 can be **N/A** when the edition, hardware, or use case does not support it.

### P2 - enhanced or higher-friction protection

P2 controls can improve protection or investigation capability but may add privacy, performance, administration, or compatibility cost. Test and document them before enforcement.

### P3 - optional or informational

P3 controls are useful only for a particular workflow, threat, or diagnostic need. They are not required for the general baseline.

## Status definitions

Use words, not color alone, to record status.

### NOT ASSESSED

No current evidence exists. This is the default for a new reader and a new computer.

### OBSERVED

A current command, screen, or log shows a value. Observation does not prove that a configured protection is effective.

### CONFIGURED

A setting was applied or is intentionally selected. Runtime enforcement and compatibility are not yet proven.

### PASS

Current evidence matches the requirement and any required representative-use test succeeds.

### HOLD

Do not proceed. A prerequisite is missing, the result is unclear, the device is unstable, or a potentially unsafe condition exists.

### EXCEPTION

The recommended state is not used because a documented requirement or compatibility issue remains. Record:

- The exact control and affected scope.
- The reason.
- The evidence supporting the exception.
- The compensating protection, if any.
- The person who accepted it.
- The acceptance date and next review date.

An exception is not the same as ignoring a failed control.

### N/A

The control does not apply because of edition, hardware, service, or use-case limits. Record the reason. Do not count N/A as PASS.

## Glossary

### ASR

Attack Surface Reduction rules. Microsoft Defender Antivirus rules that block or audit behaviors commonly used by malware.

### CFA

Controlled Folder Access. A Microsoft Defender feature that restricts untrusted applications from changing files in protected folders.

### DMA and IOMMU

Direct Memory Access allows devices to access memory efficiently. An Input-Output Memory Management Unit can isolate device access. Intel commonly calls the firmware feature VT-d; AMD commonly calls it IOMMU.

### HVCI or Memory integrity

Hypervisor-protected Code Integrity. Windows Security displays the consumer setting as Memory integrity. It uses virtualization-based protection to restrict kernel code and drivers.

### IOAV

Internet-origin file scanning by Microsoft Defender Antivirus.

### LSA and LSASS

The Local Security Authority and its process. LSA protection can run LSASS as a protected process to make credential theft more difficult.

### MAPS or cloud-delivered protection

Microsoft's cloud protection service used by Defender Antivirus for rapid analysis and reputation decisions.

### PUA

Potentially unwanted application. Software that might bundle unwanted programs, show unexpected advertising, or behave in ways the user did not intend.

### Secure Boot

A UEFI feature that verifies trusted pre-boot software before Windows starts.

### TPM

Trusted Platform Module. Hardware or firmware-backed security used by features such as Windows Hello, drive encryption, and boot integrity.

### UEFI

The modern firmware interface that starts the computer before Windows loads. Menu names vary by exact model and firmware version.

### VBS

Virtualization-based security. Windows uses hardware virtualization to isolate selected security functions.

### WHEA

Windows Hardware Error Architecture. WHEA events can indicate hardware, firmware, power, memory, or stability problems.

### Windows RE

Windows Recovery Environment. Recovery tools used when Windows cannot start normally.

## How to record a control

For each control, record:

- Control name or ID.
- Priority and applicability.
- Date and time.
- Windows edition and version.
- Current value.
- Evidence location without copying secrets.
- Status.
- Any change made.
- Restart completed, when required.
- Representative-use test and result.
- Exception reason and review date, when applicable.

Do not mark PASS based only on a toggle when the control requires a restart, runtime check, or workflow test.

## Safe sequence

### Step 1 - rule out an active incident

Review Windows Security Protection History, recent account activity, enabled administrators, unexpected remote access, and Reliability Monitor.

**PASS:** There is no unexplained security detection, administrator, remote session, recurring crash, or ordinary-use failure.

**HOLD:** Compromise is plausible, the device is actively encrypting files, an unknown administrator exists, or remote access is unexplained.

### Step 2 - prove recovery readiness

Confirm that:

- Windows RE is enabled.
- At least one administrator account works.
- Drive-encryption state is known.
- The matching recovery key is accessible from another trusted location when encryption is on.
- Critical files are covered by backup.
- A sampled restore from each critical data set opens correctly.
- At least one encrypted backup copy is not continuously writable from the daily account.

**PASS:** Every applicable recovery item is proven.

**HOLD:** Do not change firmware, TPM, Secure Boot, VBS, Memory integrity, or encryption.

### Step 3 - capture a current baseline

Record Windows, firmware, driver, Defender, firewall, encryption, network, and reliability state. Define acceptable limits for performance, failover time, crashes, and compatibility before changing anything.

### Step 4 - update from official sources

Use Windows Update and the current support page for the exact device or motherboard. Respect compatibility holds. For firmware, confirm the exact model and revision, prerequisites, supported update method, and package hash when the vendor supplies one.

### Step 5 - remove broad exceptions carefully

Inventory Defender exclusions, CFA allowed applications, browser mitigation overrides, and custom firewall rules. Change one exact item, test it, and restore only that item if a legitimate failure returns.

### Step 6 - verify the protection foundation

Verify active and current Defender Antivirus, real-time and behavior monitoring, intentional cloud and sample settings, Tamper Protection, and enabled firewall profiles before relying on dependent controls.

### Step 7 - stage compatibility-impacting controls

Use Audit mode where supported. Change one ASR, CFA, HVCI, scripting, firewall, or boot-security setting. Restart when required. Test required programs, games, accessibility features, devices, storage, and network functions.

### Step 8 - observe and freeze

After a material change, use the computer normally without stacking more changes. A major Windows, firmware, or driver update ends the observation period and requires a fresh baseline.

## PDF and workbook control-ID crosswalk

The edition-specific visual guides and printable workbooks use stable control IDs. This text companion organizes the same core material into longer plain-language sections and also contains a few clearly identified supplemental topics. Use this crosswalk when transferring a result to the matching workbook.

| PDF/workbook control ID | Accessible section or topic |
| --- | --- |
| GOV-01 | Start here; Audience and scope; managed-device stop in Safe sequence |
| GOV-02 | How to record a control; Evidence handling |
| REC-01 | 26. Windows RE, OneDrive recovery, and independent backup |
| REC-02 | 8. Drive encryption and recovery; 26. Windows RE, OneDrive recovery, and independent backup |
| REC-03 | 6. Standard daily account, administrator recovery, and UAC; 26. Windows RE, OneDrive recovery, and independent backup |
| PLT-01 | 1. Windows edition, support, and updates |
| PLT-02 | 2. UEFI, Secure Boot, and Secure Boot certificates |
| PLT-03 | 3. TPM health |
| PLT-04 | 4. CPU virtualization, DMA remapping, VBS, and Memory integrity |
| PLT-05 | 27. Firmware currency and exact-model servicing |
| PLT-06 | 8. Drive encryption and recovery |
| ID-01 and ID-03 | 6. Standard daily account, administrator recovery, and UAC |
| ID-02 | 7. Online accounts, passwords, MFA, and recovery |
| DEF-01, DEF-02, DEF-03, and DEF-04 | 9. Microsoft Defender foundation |
| DEF-05 | 13. ASR rules |
| DEF-06 | 11. Controlled Folder Access and ransomware recovery |
| DEF-07 | 10. Network Protection |
| APP-01 | 14. SmartScreen, Smart App Control, and application reputation |
| APP-02 | 4. CPU virtualization, DMA remapping, VBS, and Memory integrity |
| NET-01 | 18. Windows Firewall and network profiles |
| NET-02 | 19. RDP, Remote Assistance, Quick Assist, Remote Registry, and WinRM |
| NET-03 | 20. Legacy features and SMB; 21. Custom firewall rules, SMB egress, and application ports |
| NET-04 | 17. Filtered DNS and resolver layering; 22. Ethernet, Wi-Fi, VPN, and failover |
| LOG-01, LOG-02, and LOG-03 | 25. Audit policy and Event 4688 command lines |
| OPS-01 | 12. Defender exclusions; 21. Custom firewall rules, SMB egress, and application ports; Evidence handling |
| OPS-02 | Safe sequence |
| OPS-03 | Incident basics; 28. Reliability, crashes, WHEA, and platform tuning |
| OPS-04 | Review triggers |
| PERF-01 and PERF-02 | Safe sequence; 28. Reliability, crashes, WHEA, and platform tuning |

The LSA, Exploit Protection, browser, Windows Script Host, and PowerShell sections are supplemental detail in v1.0.0. They do not create additional workbook controls and should not be counted as separate PASS results.

## Accessible control guide

### 1. Windows edition, support, and updates

**Priority:** P1<br>
**Applies to:** Home and Pro

Open **Settings > System > About** and **Settings > Windows Update**. Use `winver` if you need the full build number. Compare the installed release with Microsoft's Windows 11 release information and lifecycle pages.

**PASS:** The edition, version, build, update state, restart state, and any safeguard hold are dated and understood. Supported security updates are installed through normal servicing.

**HOLD:** A restart is pending, the release is unsupported, or Microsoft or the device vendor has placed a compatibility hold.

**EXCEPTION:** A documented temporary deferral identifies the reason, affected update, mitigation, and review date.

### 2. UEFI, Secure Boot, and Secure Boot certificates

**Priority:** P0 for recovery readiness; P1 for verified boot state<br>
**Applies to:** Supported Home and Pro hardware

Open **System Information** and record **BIOS Mode** and **Secure Boot State**. In **Windows Security > Device security > Secure Boot**, read the full certificate-status text, not only the icon.

Do not clear Secure Boot keys, force DB or DBX changes, switch boot modes, or disable Compatibility Support Module merely to make a menu appear.

**PASS:** BIOS Mode is UEFI, Secure Boot is On, and Windows says required certificate updates are applied or current Microsoft guidance confirms the equivalent completed state.

**HOLD:** Recovery access is unproven; Windows reports a paused, incomplete, unsupported, or action-required certificate state; or the exact-model vendor procedure is unclear.

**N/A:** The hardware or installed Windows configuration does not support Secure Boot. Record the limitation and do not invent a workaround.

### 3. TPM health

**Priority:** P0 before TPM, boot, or encryption changes<br>
**Applies to:** Windows 11 systems

Open **Windows Security > Device security > Security processor details**. An administrator may use `Get-Tpm` for additional read-only status.

**PASS:** The TPM is present, ready, enabled, activated, and not locked out.

**HOLD:** Do not clear or replace the TPM while drive encryption, Windows Hello, or account-recovery effects are unknown.

### 4. CPU virtualization, DMA remapping, VBS, and Memory integrity

**Priority:** P1 for inventory; P2 for a compatibility-impacting change<br>
**Applies to:** Hardware and edition dependent

Use **Task Manager > Performance > CPU** to record virtualization. Use the exact-model firmware manual to distinguish CPU virtualization from VT-d or IOMMU. Use **System Information** and **Windows Security > Device security > Core isolation details** to record VBS, Kernel DMA Protection, Memory integrity, incompatible drivers, and the vulnerable-driver blocklist.

Kernel DMA Protection requires supported hardware and a supported Windows edition. Do not score an unsupported edition as failed.

**PASS:** Applicable firmware and Windows runtime states match the chosen protection; the vulnerable-driver blocklist is on; required drivers, games, anti-cheat, accessibility tools, and peripherals pass testing.

**HOLD:** An incompatible driver, blue screen, boot failure, WHEA event, or unacceptable repeatable regression appears.

**EXCEPTION:** Memory integrity may remain off when a required component cannot yet be replaced. Document the exact component, update plan, compensating controls, and review date.

### 5. LSA protection (supplemental in v1.0.0)

**Priority:** P1<br>
**Applies to:** Home and Pro

Verify LSA protection after a restart using current Microsoft guidance and the Windows event that confirms LSASS started as a protected process. Registry presence alone is not PASS.

**PASS:** Current-boot evidence confirms the protected-process state.

**HOLD:** A required authentication plug-in or driver is incompatible. Investigate the named component before adding stronger lock settings.

### 6. Standard daily account, administrator recovery, and UAC

**Priority:** P0 before changing account membership; P1 as the normal state<br>
**Applies to:** Home and Pro

Use **Settings > Accounts > Other users** and the User Accounts tools to inventory enabled accounts. Use a standard account for ordinary browsing, email, chat, gaming, and productivity. Keep a separate tested administrator for elevation and recovery.

Open **Change User Account Control settings**. Use the default level or higher. Never use **Never notify** as the baseline.

**PASS:** Every enabled account is recognized; the daily account is standard; a separate administrator works; and elevation displays the expected secure prompt.

**HOLD:** Do not demote or remove the only working administrator.

### 7. Online accounts, passwords, MFA, and recovery

**Priority:** P1<br>
**Applies to:** Every important online account

Use each provider's official security page. Prefer passkeys or security keys when supported. Otherwise use MFA. Store unique passwords in a reputable password manager. Keep at least two independent recovery methods and store recovery codes away from the protected device.

Review recent activity, signed-in devices, application access, forwarding, mailbox rules, and recovery addresses.

**PASS:** Important accounts use phishing-resistant authentication where available, unique passwords, independent recovery, and recognized sessions.

**HOLD:** Unknown activity, forwarding, recovery details, or application access exists. Secure the account from a clean device.

**EXCEPTION:** If only weaker MFA is available, record that limitation and retain MFA rather than reverting to password-only access.

### 8. Drive encryption and recovery

**Priority:** P0 before firmware or boot-security changes; P1 for the protection decision<br>
**Applies to:** Device and edition dependent

On Home, open **Settings > Privacy & security > Device encryption**. On Pro, also use **Manage BitLocker**. Decide whether encryption should be enabled based on device mobility, physical-access risk, performance, and recovery capability.

Never copy a recovery password into this guide, a public issue, a screenshot collection, or a source repository.

**PASS:** Encryption availability and state are known. When protection is on, the matching recovery key is accessible off-device and an administrator account works.

**HOLD:** Recovery-key access is unknown or the only copy is on the protected computer.

**N/A:** Device encryption is not available on the hardware or edition. Record the reason.

### 9. Microsoft Defender foundation

**Priority:** P0<br>
**Applies to:** Systems using Microsoft Defender Antivirus as the active antivirus

Open **Windows Security > Virus & threat protection**. Confirm:

- Defender Antivirus is the active provider.
- Real-time, behavior, and internet-origin file protection are active.
- Security intelligence and the Defender engine and platform are current.
- Cloud-delivered protection is on.
- Automatic sample submission uses an intentional privacy choice. **Send safe samples automatically** is the normal profile; other choices require a documented reason.
- Tamper Protection is on.
- Potentially unwanted application blocking is on.

**PASS:** The active provider and runtime values are current and healthy, with no unexplained management conflict.

**HOLD:** Defender is passive, disabled, stale, or policy-conflicted. Fix the foundation before ASR, CFA, or Network Protection.

**EXCEPTION:** A privacy requirement may select a different sample-submission mode. Record the security effect and review date.

### 10. Network Protection

**Priority:** P2<br>
**Applies to:** Supported Pro systems; Home is N/A

Confirm active Defender, real-time protection, behavior monitoring, and cloud protection first. Use only Microsoft's harmless Network Protection demonstration.

**PASS:** On a supported Pro system, Network Protection is in the chosen mode and the official harmless test produces the expected current event.

**HOLD:** Prerequisites are unhealthy or a legitimate site is blocked without an understood policy owner.

**N/A:** Windows 11 Home. Keep browser reputation protection enabled, but do not call it Network Protection.

### 11. Controlled Folder Access and ransomware recovery

**Priority:** P2<br>
**Applies to:** Home and Pro with active Defender Antivirus

CFA is enhanced protection, not a universal requirement. Inventory protected folders and allowed applications. Use Audit mode when a supported management method is available, or perform careful representative tests before relying on Block mode.

Test harmless writes in protected data folders and the exact workflows used for document saving, screenshots, game saves, sync, accessibility tools, and creative applications.

**PASS:** CFA is in the chosen mode, required writes succeed, and every allowed application is an exact trusted writer supported by evidence.

**HOLD:** Multiple unexplained blocks occur or the blocked executable is unknown.

**EXCEPTION:** Allow only the exact verified executable needed for a reproducible legitimate write. Do not pre-allow a launcher or an entire folder.

### 12. Defender exclusions

**Priority:** P1<br>
**Applies to:** Systems using Defender Antivirus

Open **Windows Security > Virus & threat protection > Manage settings > Exclusions**. Review file, folder, process, and extension exclusions.

**PASS:** No broad drive, profile, download, application-data, or executable-content location is excluded without measured need.

**HOLD:** An exclusion is unexplained or points to a writable location that can contain executable content.

**EXCEPTION:** Keep only the narrowest measured exception, with owner, reason, date, evidence, and review date.

### 13. ASR rules

**Priority:** P2<br>
**Applies to:** Home and Pro with active Defender Antivirus; management methods vary

Inventory every ASR rule by full name and GUID. Do not assume a rule is active because a policy value exists. Start compatibility-impacting rules in Audit mode when supported, inspect current events, and test required Office, scripting, installer, driver, and game workflows.

Treat each ASR rule as an individual control. LSA credential-theft protection is redundant when LSA protection is proven. The vulnerable signed-driver ASR rule prevents writing a vulnerable driver to disk; it does not stop an already-installed driver from loading.

**PASS:** The exact rule and mode match the decision, dependencies are healthy, and required workflows pass.

**HOLD:** Events identify an unexplained or required blocked process.

**EXCEPTION:** Keep only the affected rule in Audit or Disabled while replacing the exact incompatible component.

### 14. SmartScreen, Smart App Control, and application reputation

**Priority:** P1 for reputation protection; P2 for Smart App Control<br>
**Applies to:** Availability dependent

Open **Windows Security > App & browser control**. Keep reputation-based checks and PUA protection enabled. Record Smart App Control as On, Evaluation, Off, or unavailable.

Enable or re-enable Smart App Control only when the Windows Security interface offers the option. It has no per-application allow rule and can block unsigned or low-reputation tools.

**PASS:** Reputation protections are on. Smart App Control is on only when supported and all required software passes testing.

**EXCEPTION:** Smart App Control may remain off for documented application compatibility while SmartScreen, PUA protection, Defender, and careful software sourcing remain active.

### 15. Exploit Protection and browser-specific overrides (supplemental in v1.0.0)

**Priority:** P1 for system defaults; P2 for custom overrides<br>
**Applies to:** Home and Pro

Open **Windows Security > App & browser control > Exploit protection settings**. Prefer Windows system defaults. Export current settings before removing an override.

**PASS:** System settings use supported defaults, and no browser-specific override exists without a documented reason and compatibility test.

**HOLD:** A custom browser mitigation is unexplained or causes sign-in, extension, update, video, digital-rights-management, or accessibility failures.

### 16. Edge and Firefox security (supplemental in v1.0.0)

**Priority:** P1<br>
**Applies to:** Installed browsers

For each installed browser:

- Keep automatic updates active.
- Enable phishing, malicious-site, and dangerous-download protection.
- Review extensions and remove those no longer needed.
- Use HTTPS upgrading or HTTPS-only behavior where supported.
- Record whether browser encrypted DNS follows the operating-system policy or intentionally uses a separate provider.
- Test sign-in, extensions, downloads, media, protected video, and accessibility tools.

**PASS:** The browser is supported and current; reputation protection is active; extensions are justified; resolver behavior is intentional; and required sites work.

**EXCEPTION:** Use a narrow site exception only after confirming the site is legitimate. Do not disable global reputation protection to fix one site.

### 17. Filtered DNS and resolver layering

**Priority:** P3<br>
**Applies to:** Optional

Filtered DNS is defense in depth. It does not replace Defender, browser protection, safe account practices, or software updates.

Choose one understandable model:

- A central router or Windows resolver that browsers follow; or
- The same intended filtering policy at each browser and network layer.

Record router, Windows adapter, and browser settings. Test normal name resolution, the provider's harmless block test, and Ethernet-to-Wi-Fi failover.

**PASS:** The chosen model has no unintended browser bypass and resolution remains reliable.

**HOLD:** Ownership is unclear or encrypted DNS repeatedly fails after the connection stabilizes.

**EXCEPTION:** Plain DNS fallback or a different provider may be accepted for a documented network requirement and reviewed later.

### 18. Windows Firewall and network profiles

**Priority:** P1<br>
**Applies to:** Home and Pro

Open **Windows Security > Firewall & network protection**. Keep Domain, Private, and Public profiles enabled. The normal inbound posture is block unless a specific permitted rule applies.

Use **Public** for hotels, guest Wi-Fi, public hotspots, and any network whose other devices you do not trust. Use **Private** only for a controlled network when discovery or sharing is needed.

**PASS:** All profiles are enabled; the active network profile matches trust and sharing needs; and required applications work through specific rules.

**HOLD:** A third-party firewall, management policy, or unexplained custom rule controls the effective state.

### 19. RDP, Remote Assistance, Quick Assist, Remote Registry, and WinRM

**Priority:** P1<br>
**Applies to:** Edition and use-case dependent

Treat these as separate controls.

- Remote Desktop hosting is unavailable on Home. On Pro, keep it off unless required.
- Keep Remote Assistance off when unused.
- Remove or restrict Quick Assist when unused. If retained, accept a session only when you initiated the request and independently verified the helper.
- When remote administration is unused, no WinRM listener or inbound rule should expose it.
- Keep Remote Registry stopped unless a documented management requirement exists.

**PASS:** Each feature is off, absent, or narrowly justified with authentication, network scope, owner, and review date.

**HOLD:** An unknown listener, inbound rule, helper, or remote session exists.

**N/A:** Record edition-specific limits rather than forcing a feature.

### 20. Legacy features and SMB

**Priority:** P1<br>
**Applies to:** Home and Pro

Remove or disable SMB1, Telnet Client, and TFTP Client when unused. Do not permit insecure SMB guest access. Record SMB signing state and test every required authenticated share.

**PASS:** Legacy features are absent or disabled, insecure guest access is off, signing state is understood, and required authenticated shares work.

**HOLD:** A storage device requires SMB1, guest fallback, or disabled signing. Update or replace the device before weakening the computer.

### 21. Custom firewall rules, SMB egress, and application ports

**Priority:** P2 or P3<br>
**Applies to:** Only when a documented requirement exists

Default inbound blocking makes many blanket custom inbound rules redundant. Inspect a rule's direction, protocol, local and remote ports, local and remote addresses, program, service, and profile.

An outbound TCP 445 block can reduce internet SMB exposure but can also break trusted local or VPN shares if it is not scoped. Port-only blocks for an application protocol provide limited protection and can break legitimate use.

**PASS:** Every custom rule has a purpose, exact scope, owner, test, and review date.

**HOLD:** A blanket rule affects all programs, addresses, or profiles without a documented need.

**EXCEPTION:** Disable, rather than delete, one conflicting rule during a test. Re-enable that exact rule to roll back.

### 22. Ethernet, Wi-Fi, VPN, and failover

**Priority:** P2<br>
**Applies to:** Multi-network systems

Record interface metrics, default routes, DNS behavior, and VPN routes. Start a harmless continuous connection test, disconnect Ethernet, verify Wi-Fi and DNS, reconnect Ethernet, and confirm that the intended route returns.

**PASS:** Both transitions recover within a predefined time and required applications still work.

**HOLD:** Do not disable adapters or networking services as a first troubleshooting step. Restore one recorded metric or resolver layer at a time.

### 23. Windows Script Host and VBScript (supplemental in v1.0.0)

**Priority:** P3<br>
**Applies to:** Use-case dependent

First determine whether Windows Script Host and the VBScript capability exist and whether a required installer, scheduled task, or administration script depends on them.

Creating and running a test script is an **active test**, not read-only work.

**PASS:** An absent capability is N/A, or the selected state is proven and required workflows pass.

**EXCEPTION:** Keep required scripting capability only with a documented dependency, supported software, and review date.

### 24. PowerShell execution policy (supplemental in v1.0.0)

**Priority:** P3<br>
**Applies to:** Home and Pro

Execution policy is a workflow safety feature, not a security boundary. Record all scopes and the effective value.

**PASS:** The effective policy matches the scripting need, no unexpected higher-priority override exists, and broader settings such as Bypass or Unrestricted have a time-bounded reason.

**HOLD:** Do not override an organizational policy or change several scopes at once.

### 25. Audit policy and Event 4688 command lines

**Priority:** P2 for selected auditing; P3 for command-line capture<br>
**Applies to:** Edition and management method dependent

Logging has value only when someone reviews it and retention is sufficient. Record the selected audit subcategories, Security log size, retention behavior, review owner, and review cadence.

Process-creation command-line capture can expose passwords, tokens, private paths, and other sensitive arguments in plaintext. It is an advanced investigative control, not the default consumer baseline.

**PASS:** Selected events are generated by a harmless test; volume is manageable; review and retention are defined; and the privacy cost is accepted.

**HOLD:** The Security log is filling unexpectedly, sensitive arguments are exposed, or no review use case exists.

**N/A:** Edition or management method does not support the setting.

### 26. Windows RE, OneDrive recovery, and independent backup

**Priority:** P0 for recovery readiness; P1 for ongoing recovery<br>
**Applies to:** Service dependent

Windows RE is repair media, not a personal-file backup. OneDrive version history protects only synchronized data and can also synchronize unwanted changes.

Inventory every critical data set. Record its backup destination, last successful date, retention, encryption, and next restore test. Restore a harmless historical sample from each data set into a new folder and verify it.

**PASS:** Windows RE is enabled; critical data coverage is complete; sampled restores work; and at least one encrypted copy is offline or separately credentialed.

**HOLD:** Do not call ransomware recovery ready when a critical data set is missing or a restore has not been tested.

### 27. Firmware currency and exact-model servicing

**Priority:** P0 gates before change; P1 for inventory<br>
**Applies to:** All systems

Record the exact computer or motherboard manufacturer, model, revision, installed UEFI version, and release date. Use only that exact support page. Read prerequisites for management-engine, security-processor, microcode, and firmware layers.

Before updating, prove recovery, record firmware settings, verify the package or hash when available, provide stable power, and use the documented built-in or OEM update method.

**PASS:** Applicability and prerequisite order are confirmed, and all affected boot, encryption, virtualization, thermal, device, and application checks pass afterward.

**HOLD:** Model, revision, package, prerequisite, recovery, power, or compatibility-hold information is unclear.

### 28. Reliability, crashes, WHEA, and platform tuning

**Priority:** P0 when instability is unresolved; otherwise outside the core security baseline<br>
**Applies to:** Systems with crash or tuning history

Use Reliability Monitor and current WHEA and bugcheck evidence. A memory dump can contain sensitive data.

CPU undervolting, overclocking, power limits, boost presets, and memory tuning are stability topics. Do not copy values from another processor or motherboard. Do not mix tuning changes with security-control changes.

**PASS:** There is no unexplained recurring crash, WHEA error, freeze, or restart during representative use.

**HOLD:** Freeze firmware, HVCI, driver, and tuning changes after a new crash. Preserve restricted evidence and reverse only the latest documented reversible change.

## Safe UEFI method

Use firmware menus only when a control above requires a specific setting.

1. Complete recovery gates.
2. Record the exact system or motherboard model, revision, and firmware version.
3. Photograph or export the current page and all deliberate boot, TPM, virtualization, DMA, encryption, fan, memory, and tuning settings.
4. Use the exact-model manual or built-in search. Stop if the label is absent or only similar.
5. Change one exact setting.
6. Read the full save summary before confirming.
7. Restart and verify the Windows runtime state.
8. Do not import an old firmware profile across firmware generations unless the vendor explicitly supports it.
9. Never clear TPM, CMOS, or Secure Boot keys as routine enablement or troubleshooting.

## Evidence handling

### Never record or share

- Passwords.
- Recovery-key values.
- Authentication tokens or session cookies.
- Private keys or certificates with private material.
- One-time recovery codes.
- Full payment, identity, or account records.

### Record only when needed

- Control name and status.
- Date, Windows edition, version, and firmware version.
- A redacted screenshot of the relevant setting.
- Event provider, event ID, time, and a redacted summary.
- A hash or publisher identity for a file under review.
- The result of a harmless representative test.

### Restricted evidence

Treat memory dumps, full event exports, command-line logs, browser profiles, account-activity exports, network captures, and unredacted screenshots as sensitive. Store them in an access-controlled, encrypted location. Do not put them in a source repository or public issue.

### Retention and deletion

Choose a review or deletion date when collecting evidence. Keep only what supports a control, exception, incident, or required investigation. Delete temporary test files and unneeded sensitive evidence securely when the purpose ends, subject to any legal or investigation hold.

### Sharing

Create a redacted copy rather than editing the only original. Review filenames, paths, account names, email addresses, IP addresses, device names, serial numbers, license details, and document metadata before sharing.

## Incident basics

These steps are for immediate safety, not a complete forensic procedure.

1. If ransomware, unauthorized remote control, or active compromise is plausible, disconnect Ethernet and Wi-Fi.
2. If network isolation is impossible and harm is continuing, power down.
3. Stop normal use. Do not sign into more accounts or restore backups to the affected device.
4. From a separate trusted device, secure important accounts, review sessions, and contact qualified help.
5. Record the time, symptoms, visible messages, and actions taken without copying secrets.
6. Preserve logs or dumps only when safe and necessary. Restrict access because they can contain sensitive data.
7. Do not reconnect or restore files until the device and accounts are considered clean.

For a suspected account compromise, use the provider's official recovery page typed directly into the browser. Rotate exposed credentials and invalidate unknown sessions. Deleting a log that contained a secret does not make the secret safe; rotate it.

## Recovery basics

A recovery plan should answer:

- What data is critical?
- Where is each data set stored?
- How recent must a restored copy be?
- How long can the computer be unavailable?
- Which backup cannot be modified by the daily account?
- Where are drive-recovery and account-recovery methods stored?
- How will Windows be reinstalled if local recovery fails?
- When was each restore path last tested?

Test recovery with harmless sample files. Do not use the only copy of important data as the test.

## Review triggers

Reassess affected controls after:

- A major Windows update.
- A firmware update or reset.
- A chipset, graphics, storage, network, anti-cheat, or security-driver update.
- A new antivirus or management product.
- A new browser, extension, remote-access tool, VPN, network share, or backup service.
- A crash, recovery prompt, unexplained security block, account alert, or suspected compromise.
- A change from Home to Pro or a change in subscription or management.

Also schedule a periodic review even when nothing obvious changes. Record the source-review date and next review date for time-sensitive guidance.

## Primary source starting points

- Windows 11 release information: <https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information>
- Microsoft Security Compliance Toolkit: <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10>
- Microsoft Defender Antivirus and Windows security guidance: <https://learn.microsoft.com/en-us/windows/security/book/operating-system-security-virus-and-threat-protection>
- Microsoft network protection: <https://learn.microsoft.com/en-us/defender-endpoint/network-protection>
- Microsoft ASR rule reference: <https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference>
- Microsoft Controlled Folder Access: <https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-configure>
- Microsoft vulnerable-driver block rules: <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules>
- Microsoft Kernel DMA Protection: <https://learn.microsoft.com/en-us/windows/security/hardware-security/kernel-dma-protection-for-thunderbolt>
- Microsoft Secure Boot certificate status: <https://support.microsoft.com/en-us/servicing/os/secure-boot/2026/03/secure-boot-certificate-update-status-in-the-windows-security-app>
- NIST Cybersecurity Framework 2.0: <https://doi.org/10.6028/NIST.CSWP.29>
- CIS Controls v8.1: <https://www.cisecurity.org/controls/v8-1>

Current authoritative documentation takes precedence over this companion when product behavior, licensing, or support changes.
