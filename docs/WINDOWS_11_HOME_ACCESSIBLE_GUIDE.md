# Windows 11 Home Security Baseline

## Accessible ordered implementation guide

Version 1.0.0. Source review cut-off: 29 July 2026.

Use the steps in numerical order. Complete each action, restart decision, verification, and recovery decision before continuing.

This is an independent informational aid. It is not vendor-endorsed, a certification, guarantee, incident-response plan, or professional advice. Guide materials are CC BY-NC-ND 4.0 under the controlled-author terms in [LICENSE.md](../LICENSE.md).

## Result states

- **NOT ASSESSED:** No current conclusion has been reached.
- **OBSERVED:** A current value was seen, but effectiveness was not proved.
- **CONFIGURED:** The intended setting was selected, but runtime effect or compatibility was not proved.
- **PASS:** The stated target and test passed with a date and minimal evidence.
- **HOLD:** A prerequisite, ownership question, instability, or safety issue blocks work.
- **EXCEPTION:** A scoped, owned, time-bounded deviation has been accepted and scheduled for review.
- **N/A:** A documented edition, hardware, or use-case reason makes the item unavailable or irrelevant.

## Capabilities excluded from the Home procedure

- **DEF-07 - Microsoft Defender Network Protection:** Microsoft currently lists Windows 10/11 Pro or Enterprise, not Home, in the Windows requirements.
- **PLT-04 component - Kernel DMA Protection:** Microsoft's edition table lists Pro and higher. Home still evaluates CPU virtualization, VBS, and Memory integrity.
- **PLT-06 component - BitLocker Drive Encryption management:** Home uses Device Encryption when the device supports it. The full BitLocker management workflow is Pro and higher.
- **NET-02 component - Incoming Remote Desktop host:** Home can be a Remote Desktop client but cannot host incoming Remote Desktop sessions.
- **LOG-02 component - Pro Local Group Policy command-line capture workflow:** The Home path does not prescribe the Pro Local Group Policy method. Command-line capture remains off by default.

## Phase 01 - A. Safety and recovery

### Step 01 - Confirm edition, authority, and a stable starting point

- **Controls:** GOV-01, OPS-03, PLT-01
- **Priority:** P0
- **Run as:** [USER]
- **Action type:** READ-ONLY / DECISION
- **Sources:** [1], [2], [3], [6]
- **Goal:** Prove that this is the correct edition guide, the device is personally controlled, and baseline work is safe to begin.

#### Before you start

- Use a personally owned, unmanaged Windows 11 device.
- Stop if active compromise, repeated crashes, recovery prompts, data loss, or unexplained control changes are present.

#### Do this in order

1. Open Settings > System > About and confirm the edition named on this guide.
2. Open Settings > Accounts > Access work or school. Stop for any unknown organization, tenant, or management connection.
3. Run the commands only for on-screen review. Do not save or publish raw dsregcmd output.

#### Commands

```powershell
Get-ComputerInfo |
  Select-Object WindowsProductName,WindowsVersion,OsBuildNumber
dsregcmd.exe /status
perfmon.exe /rel
```

#### Restart now?

NO. This step makes no configuration change.

#### Verify before continuing

1. The edition matches this guide.
2. No employer, school, client, domain, or mobile-device-management authority controls the device.
3. Reliability Monitor shows no unresolved pattern that should pause hardening.

- **PASS looks like:** Edition and ownership are confirmed; no incident or instability stop condition is present.
- **If it does not pass:** STOP. Use the correct edition guide, contact the authorized administrator, or follow an incident/repair path before continuing.
- **Rollback / recovery:** None. This is a gate, not a change.
- **Record only:** Record only edition, Windows release/build, date, and PASS or HOLD. Do not retain tenant, account, or device identifiers.
### Step 02 - Create the minimal evidence and change record

- **Controls:** GOV-02, OPS-02
- **Priority:** P0
- **Run as:** [USER]
- **Action type:** DECISION / RECORD
- **Sources:** [1], [2], [4]
- **Goal:** Keep enough information to repeat and reverse a decision without collecting secrets or personal data.

#### Before you start

- Step 01 passed.
- Choose an access-controlled location outside any public repository for restricted evidence.

#### Do this in order

1. Create one row per step with: step/control ID, date, result, method, sanitized result, prior-to-new state, restart completed, owner, and next review.
2. Define a deletion/review date for raw logs or screenshots.
3. Never record recovery keys, passwords, tokens, serials, account names, public addresses, user paths, raw dumps, or unredacted logs.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

NO.

#### Verify before continuing

1. A blank record exists.
2. Restricted evidence has a separate protected location and retention rule.

- **PASS looks like:** The record can support a decision without exposing secret or unnecessary personal information.
- **If it does not pass:** HOLD. Move or sanitize existing evidence before continuing.
- **Rollback / recovery:** Delete the empty record if the assessment is abandoned; do not delete material under an investigation or legal hold.
- **Record only:** Record the storage location by a non-sensitive label, not a path, account, or URL.
### Step 03 - Make and test an independent backup

- **Controls:** REC-01
- **Priority:** P0
- **Run as:** [USER]
- **Action type:** ACTIVE RESTORE TEST
- **Sources:** [1], [2], [5]
- **Goal:** Prevent a security change, device failure, or ransomware event from leaving the only copy unusable.

#### Before you start

- Steps 01 and 02 passed.
- Identify the files and settings whose loss would matter.

#### Do this in order

1. Create or update a backup that is not continuously writable by the daily Windows session.
2. Disconnect or otherwise isolate that copy when the backup completes.
3. Restore one harmless representative file to a different location, open it, then remove the temporary restored copy.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

NO.

#### Verify before continuing

1. The backup date and scope cover the identified critical data.
2. The representative restore succeeds from the independent copy.

- **PASS looks like:** A current independent copy exists and a representative restore works.
- **If it does not pass:** HOLD all firmware, encryption, account, and platform changes until a restore succeeds.
- **Rollback / recovery:** Correct the backup design or destination; do not overwrite the only known-good copy while troubleshooting.
- **Record only:** Record backup scope, date, and restore PASS only. Do not list filenames or storage credentials.
### Step 04 - Prove encryption recovery, Windows RE, and recovery administration

- **Controls:** REC-02, REC-03, ID-01
- **Priority:** P0
- **Run as:** [USER] then [ADMIN]
- **Action type:** READ-ONLY / ACTIVE SIGN-IN TEST
- **Sources:** [2], [7], [18], [30], [31], [32], [48]
- **Goal:** Make sure a later boot, encryption, or account change cannot lock the owner out without a tested recovery path.

#### Before you start

- Step 03 passed.
- Have a second trusted device or independent location available when the drive is already encrypted.

#### Do this in order

1. Review the edition-specific encryption page named in Step 12 and record only On, Off, or unavailable.
2. If encryption is already on, prove that the matching recovery method can be reached independently. Never copy the secret into the workbook.
3. Confirm Windows Recovery Environment is enabled.
4. Create or retain a separate recovery administrator through Settings > Accounts > Other users, then sign in once and cancel a harmless elevation prompt.

#### Commands

```powershell
manage-bde.exe -status C:
reagentc.exe /info
$admins = Get-LocalGroup -SID 'S-1-5-32-544'
Get-LocalGroupMember -Group $admins
```

#### Restart now?

NO. A sign-out/sign-in is sufficient for the administrator test.

#### Verify before continuing

1. Encryption state is understood.
2. When encryption is active, the matching recovery method is independently accessible.
3. Windows RE reports Enabled and the separate administrator can sign in and elevate.

- **PASS looks like:** All recovery paths work without recording a recovery secret.
- **If it does not pass:** HOLD. Do not change firmware, Secure Boot, TPM, encryption, Memory integrity, or account roles.
- **Rollback / recovery:** Restore the prior account role from the already working administrator if an account change fails.
- **Record only:** Record encryption state, Windows RE Enabled, and recovery-admin test PASS. Do not record protector IDs or key values.
### Step 05 - Define the tests that every material change must pass

- **Controls:** OPS-02, PERF-01, PERF-02
- **Priority:** P0
- **Run as:** [USER]
- **Action type:** DECISION / RECORD
- **Sources:** [1], [2]
- **Goal:** Turn compatibility and performance into repeatable acceptance checks instead of guesswork.

#### Before you start

- Steps 01 through 04 passed.
- Know which applications, games, peripherals, networks, and recovery functions are actually required.

#### Do this in order

1. List required sign-in/elevation, update, browser/download, save/open/export/sync, print, voice/video, game/anti-cheat, VPN/network-switch, peripheral, sleep/resume, and recovery workflows.
2. Define only meaningful performance or reliability limits for this device.
3. Adopt the rule: one material change, focused verification, required-workflow test, observation, then the next change.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

NO.

#### Verify before continuing

1. Each required workflow has a short repeatable test.
2. The owner knows which latest change to reverse if a test fails.

- **PASS looks like:** A reusable acceptance list and latest-change rollback rule exist.
- **If it does not pass:** HOLD compatibility-sensitive controls until the tests are defined.
- **Rollback / recovery:** Remove a test only when the underlying required workflow is intentionally retired.
- **Record only:** Record test names and limits, not private content or application data.

## Phase 02 - B. Platform trust

### Step 06 - Capture the minimum platform inventory

- **Controls:** PLT-01, PLT-02, PLT-03, PLT-04, PLT-05
- **Priority:** P1
- **Run as:** [USER] then [ADMIN]
- **Action type:** READ-ONLY
- **Sources:** [6], [8], [21], [22]
- **Goal:** Identify the exact Windows, firmware, Secure Boot, TPM, and virtualization state before changing any of them.

#### Before you start

- The safety and recovery phase passed.
- Open an elevated PowerShell window only for the commands marked [ADMIN].

#### Do this in order

1. Run the commands and review them on screen.
2. Open msinfo32 and inspect BIOS Mode and Secure Boot State.
3. Open Task Manager > Performance > CPU and inspect Virtualization.

#### Commands

```powershell
Get-CimInstance Win32_OperatingSystem |
  Select-Object Caption,Version,BuildNumber,LastBootUpTime
Get-CimInstance Win32_ComputerSystem |
  Select-Object Manufacturer,Model
Get-CimInstance Win32_BIOS |
  Select-Object SMBIOSBIOSVersion,ReleaseDate
Confirm-SecureBootUEFI
Get-Tpm | Select-Object TpmPresent,TpmReady,TpmEnabled,`
  TpmActivated,LockedOut
```

#### Restart now?

NO.

#### Verify before continuing

1. Exact model, Windows build, firmware version/date, BIOS mode, Secure Boot, TPM, and CPU virtualization are known.
2. A failed or unsupported query is recorded as UNKNOWN or HOLD, never PASS.

- **PASS looks like:** The minimum platform state is known without exporting identifiers.
- **If it does not pass:** HOLD the affected platform change and use the exact vendor documentation to resolve an unknown state.
- **Rollback / recovery:** None. Inventory is read-only.
- **Record only:** Record only the model family, firmware version/date, and summarized security states. Omit serials and raw exports.
### Step 07 - Install supported Windows, Defender, Store, and application updates

- **Controls:** PLT-01, DEF-01
- **Priority:** P1
- **Run as:** [USER] (elevation if requested)
- **Action type:** CONFIGURATION CHANGE
- **Sources:** [6], [11]
- **Goal:** Close known vulnerabilities before spending time tuning dependent controls.

#### Before you start

- The recovery gate passed.
- Honor any Microsoft or vendor safeguard hold for the exact device.

#### Do this in order

1. Open Windows Update and install normal security and servicing updates. Do not install a preview solely for this baseline.
2. Update Microsoft Store applications and other required applications from their supported vendor channels.
3. Update Defender security intelligence.
4. Restart when Windows or an installer requests it, then return immediately to the verification below.

#### Commands

```powershell
Start-Process 'ms-settings:windowsupdate'
Update-MpSignature
```

#### Restart now?

YES when requested. Do not make another change before the post-restart checks pass.

#### Verify before continuing

1. Sign in without a recovery prompt or new failure.
2. Open Windows Update again; no security update or pending restart remains.
3. Run the required workflows defined in Step 05.

```powershell
winver.exe
(Get-MpComputerStatus).AntivirusSignatureLastUpdated
```

- **PASS looks like:** Windows is supported and current, Defender intelligence is current, and required workflows pass.
- **If it does not pass:** HOLD. Use Windows release-health or the exact application/vendor support path; do not bypass a documented safeguard hold.
- **Rollback / recovery:** Uninstall only the latest documented update when official guidance and a reproducible failure justify it.
- **Record only:** Record Windows release/build, update completion date, restart complete, and sanitized test result.
### Step 08 - Service firmware only from the exact-model source

- **Controls:** PLT-05, OPS-02
- **Priority:** P1
- **Run as:** [ADMIN] and [FIRMWARE]
- **Action type:** CONFIGURATION CHANGE
- **Sources:** [2], [6], [48]
- **Goal:** Apply applicable firmware security fixes without cross-flashing, skipping prerequisites, or losing known-good settings.

#### Before you start

- Steps 03 through 06 passed.
- Stable power is available and the exact system or motherboard model and revision are known.

#### Do this in order

1. Compare the installed version only with the exact OEM/system or motherboard support page.
2. Read release notes, prerequisites, recovery instructions, and any required component order.
3. Record current deliberate boot, security, storage, fan, memory, and tuning settings.
4. Apply at most one exact-model firmware package through the documented OEM method.

#### Commands

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object Manufacturer,Model
Get-CimInstance Win32_BaseBoard |
  Select-Object Manufacturer,Product,Version
Get-CimInstance Win32_BIOS |
  Select-Object SMBIOSBIOSVersion,ReleaseDate
```

#### Restart now?

YES after an applied firmware package. Treat this as a REBOOT GATE.

#### Verify before continuing

1. Re-run firmware inventory, Secure Boot, TPM, encryption, and any virtualization state affected by the update.
2. Run the Step 05 workflow and performance checks.

```powershell
Confirm-SecureBootUEFI
Get-Tpm | Select-Object TpmPresent,TpmReady,TpmEnabled,`
  TpmActivated,LockedOut
manage-bde.exe -status C:
```

- **PASS looks like:** The exact package applies, the update succeeds, security settings remain correct, and required workflows pass.
- **If it does not pass:** HOLD for an unclear model, revision, prerequisite, power condition, recovery path, or post-update failure.
- **Rollback / recovery:** Restore only the recorded prior firmware setting that changed. Never clear TPM, CMOS, or Secure Boot keys as routine rollback.
- **Record only:** Record exact model family, old/new firmware version, source page date, restart, and sanitized verification result.
### Step 09 - Establish Home platform trust

- **Controls:** PLT-02, PLT-03, PLT-04
- **Priority:** P0/P2
- **Run as:** [ADMIN] and [FIRMWARE]
- **Action type:** CONDITIONAL CONFIGURATION CHANGE / REBOOT GATE
- **Sources:** [8], [21]
- **Goal:** Verify Secure Boot and TPM, and enable CPU virtualization only when a later Home protection requires it.

#### Before you start

- Steps 03 through 06 passed.
- Use only the exact-model firmware manual and change one setting at a time.

#### Do this in order

1. Require UEFI mode and Secure Boot enabled. If Windows starts in Legacy/CSM mode, stop for an exact supported migration plan.
2. Require TPM present, ready, enabled, activated, and not locked out. Clearing or reprovisioning the TPM is outside this guide.
3. If Memory integrity later needs CPU virtualization, enable only the exact CPU virtualization setting documented by the vendor.
4. After any firmware setting change, save the exact change summary and complete the REBOOT GATE.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

YES after any firmware setting change.

#### Verify before continuing

1. Confirm-SecureBootUEFI returns True.
2. All required TPM fields pass.
3. Task Manager reports Virtualization Enabled when it was intentionally enabled.
4. No recovery prompt, crash, device failure, or workflow regression follows the change.

```powershell
Confirm-SecureBootUEFI
Get-Tpm | Select-Object TpmPresent,TpmReady,TpmEnabled,`
  TpmActivated,LockedOut
```

- **PASS looks like:** Secure Boot and TPM pass; optional CPU virtualization is effective when needed.
- **If it does not pass:** HOLD. Do not clear TPM or Secure Boot keys, convert boot mode generically, or stack another firmware change.
- **Rollback / recovery:** Restore only the latest recorded firmware setting through the exact-model UI, reboot, and re-verify.
- **Record only:** Record summarized runtime states and the one prior-to-new firmware setting. Do not record keys or identifiers.

## Phase 03 - C. Identity and least privilege

### Step 10 - Separate daily work from administration and keep UAC visible

- **Controls:** ID-01, ID-03, REC-03
- **Priority:** P1
- **Run as:** [USER] then [ADMIN]
- **Action type:** CONFIGURATION CHANGE / ACTIVE SIGN-IN TEST
- **Sources:** [2], [18], [19]
- **Goal:** Reduce routine administrative exposure without creating a lockout.

#### Before you start

- The separate recovery administrator from Step 04 works.
- Do not demote or remove the last tested administrator.

#### Do this in order

1. In Settings > Accounts > Other users, confirm the recovery administrator first.
2. Change the routine account to Standard when practical.
3. Open Change User Account Control settings and keep the Windows default level or higher.
4. From the daily account, start a harmless Run as administrator action and cancel the visible secure-desktop prompt.

#### Commands

```powershell
$admins = Get-LocalGroup -SID 'S-1-5-32-544'
Get-LocalGroupMember -Group $admins
$uacPath = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion'
$uacPath = Join-Path $uacPath 'Policies\System'
$uac = Get-ItemProperty $uacPath
$uac | Select-Object EnableLUA,ConsentPromptBehaviorAdmin,`
  PromptOnSecureDesktop
```

#### Restart now?

NO. Sign out and sign back in after changing an account type.

#### Verify before continuing

1. Routine work uses a Standard account or has a documented exception.
2. A separate administrator works and UAC produces a deliberate visible prompt.

- **PASS looks like:** Daily use is separated from administration and recovery administration remains tested.
- **If it does not pass:** HOLD. Sign in with the recovery administrator and restore the prior account type before other changes.
- **Rollback / recovery:** Restore only the affected account type through Settings. Do not weaken UAC to repair an unrelated application.
- **Record only:** Record account roles, not account names. Record UAC as default-or-higher and the prompt test PASS.
### Step 11 - Strengthen sign-in and independent account recovery

- **Controls:** ID-02
- **Priority:** P1
- **Run as:** [USER]
- **Action type:** CONFIGURATION CHANGE / ACTIVE RECOVERY TEST
- **Sources:** [1], [23]
- **Goal:** Reduce account takeover risk without replacing one working factor before its successor is proved.

#### Before you start

- The owner can reach each important account from a trusted device.
- An offline location is available for recovery codes.

#### Do this in order

1. Configure Windows Hello or a passkey where offered.
2. Use phishing-resistant multi-factor authentication for important online accounts where supported.
3. Keep two independent recovery methods and protect recovery codes offline.
4. Test the new sign-in and recovery route before removing an old factor.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

NO.

#### Verify before continuing

1. The new sign-in works.
2. Two independent recovery routes are available and at least one was tested without revealing a secret.

- **PASS looks like:** Strong sign-in and independent recovery are configured and tested.
- **If it does not pass:** HOLD. Keep the old working factor until the replacement and recovery path pass.
- **Rollback / recovery:** Re-add or retain the prior factor through the account provider's official security page.
- **Record only:** Record factor types and PASS only. Never record codes, secrets, phone numbers, or account addresses.

## Phase 04 - B. Platform trust (continued)

### Step 12 - Enable Home Device Encryption when the device supports it

- **Controls:** PLT-06, REC-02
- **Priority:** P1
- **Run as:** [USER] (elevation if requested)
- **Action type:** CONDITIONAL CONFIGURATION CHANGE
- **Sources:** [7], [31], [48]
- **Goal:** Protect data at rest through the Home-supported Device Encryption workflow without introducing Pro-only BitLocker instructions.

#### Before you start

- Backup, Windows RE, recovery administration, and acceptance tests passed.
- Do not combine encryption with a firmware, Secure Boot, TPM, partition, or boot-mode change.

#### Do this in order

1. Open Settings > Privacy & security > Device encryption.
2. If the setting is present, turn it On and keep reliable power connected until Windows reports completion.
3. From a second trusted device or independent location, prove the matching recovery method is accessible without copying its secret.
4. If the setting is absent while signed in as an administrator, record a hardware/applicability exception. Do not use a Pro BitLocker workaround.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

ONLY IF WINDOWS REQUESTS IT. Do not interrupt active encryption.

#### Verify before continuing

1. Windows reports Device Encryption On and complete.
2. The matching recovery method is independently accessible.
3. A normal restart succeeds if one was requested.

```powershell
manage-bde.exe -status C:
```

- **PASS looks like:** Home Device Encryption is complete with proved independent recovery, or unavailability is documented.
- **If it does not pass:** HOLD after recovery uncertainty, encryption error, unexpected prompt, or instability.
- **Rollback / recovery:** Do not disable and re-enable blindly. Resolve the exact recovery or platform prerequisite before changing encryption state.
- **Record only:** Record On/Off/unavailable, completion, restart, and recovery-method PASS. Never record the recovery key.

## Phase 05 - D. Defender and application protection

### Step 13 - Establish a healthy antimalware foundation

- **Controls:** DEF-01, DEF-02, DEF-03, DEF-04
- **Priority:** P1
- **Run as:** [ADMIN]
- **Action type:** CONFIGURATION CHANGE / ACTIVE SCAN
- **Sources:** [11], [24], [25], [26], [33]
- **Goal:** Make the intended antimalware provider active and current before enabling dependent protections.

#### Before you start

- Windows and application updates passed.
- If another antivirus intentionally owns protection, assess that provider instead of forcing two active providers.

#### Do this in order

1. In Windows Security, enable real-time, behavior, IOAV, tamper, and cloud-delivered protection where Defender is the active provider.
2. Choose sample-submission behavior intentionally based on privacy needs.
3. Enable PUA protection in Block mode.
4. Update signatures and run a Quick scan.

#### Commands

```powershell
Update-MpSignature
Set-MpPreference -PUAProtection Enabled
Start-MpScan -ScanType QuickScan
```

#### Restart now?

NO.

#### Verify before continuing

1. Defender is active, runtime protections are true, tamper protection is on, signatures are current, and PUA is Enabled.
2. The Quick scan completes without an unresolved detection.

```powershell
$s = Get-MpComputerStatus
$s | Format-List AMRunningMode,AMServiceEnabled,`
  AntivirusEnabled,RealTimeProtectionEnabled
$s | Format-List BehaviorMonitorEnabled,IoavProtectionEnabled,`
  IsTamperProtected
$s | Format-List AntivirusSignatureLastUpdated,QuickScanEndTime
Get-MpPreference |
  Format-List MAPSReporting,SubmitSamplesConsent,PUAProtection
```

- **PASS looks like:** The intended provider is healthy and all required Defender foundation values pass.
- **If it does not pass:** HOLD advanced Defender steps. Resolve provider ownership, updates, detections, or policy control first.
- **Rollback / recovery:** Restore only the recorded PUA state if a documented compatibility reason requires it; never defeat tamper protection.
- **Record only:** Record provider name, summarized states, signature date, and Quick-scan completion. Do not attach detection details publicly.
### Step 14 - Turn on reputation protection and keep application defaults

- **Controls:** APP-01
- **Priority:** P1
- **Run as:** [USER]
- **Action type:** CONFIGURATION CHANGE / ACTIVE APP TEST
- **Sources:** [27]
- **Goal:** Block known risky sites, downloads, and applications while preserving supported required software.

#### Before you start

- The antimalware foundation passed.
- Know which browsers and applications are required.

#### Do this in order

1. Open Windows Security > App & browser control > Reputation-based protection.
2. Enable applicable SmartScreen, phishing, and unwanted-app checks.
3. Keep Exploit Protection at Microsoft system defaults unless one exact tested application requires an override.
4. Treat Smart App Control as conditional: use only the state the current Windows Security UI supports; it has no per-app allow rule.
5. Confirm every installed browser is supported, current, and using its built-in malicious-site and dangerous-download protection.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

NO, unless Windows explicitly requests one.

#### Verify before continuing

1. Applicable reputation layers are enabled.
2. Required applications and browsers launch, update, download, and authenticate normally.

- **PASS looks like:** Applicable reputation protections are on and required software passes.
- **If it does not pass:** HOLD an unverified blocked application. Verify publisher, source, hash, and need before any exception.
- **Rollback / recovery:** Undo only the exact application override that caused the failure; do not disable global reputation protection.
- **Record only:** Record protection states and application-test PASS. Do not record browsing history or downloaded filenames.

## Phase 06 - E. Network and remote exposure

### Step 15 - Keep every Windows Firewall profile enabled

- **Controls:** NET-01
- **Priority:** P1
- **Run as:** [ADMIN]
- **Action type:** CONFIGURATION CHANGE / ACTIVE NETWORK TEST
- **Sources:** [16], [37]
- **Goal:** Preserve host firewall protection on trusted and untrusted networks without relying on blanket exceptions.

#### Before you start

- Confirm Windows Firewall is the intended active host firewall.
- Have the Step 05 network, VPN, sharing, printing, game, and communications tests ready.

#### Do this in order

1. Inspect the effective profile state.
2. If any profile is disabled and Windows Firewall is the intended provider, enable all three profiles.
3. Do not change the global outbound default in this baseline.
4. Run the required network workflows.

#### Commands

```powershell
$fw = Get-NetFirewallProfile -PolicyStore ActiveStore
$fw | Select-Object Name,Enabled,DefaultInboundAction,`
  DefaultOutboundAction
Set-NetFirewallProfile -Profile Domain,Private,Public `
  -Enabled True
```

#### Restart now?

NO.

#### Verify before continuing

1. Domain, Private, and Public profiles report Enabled.
2. Required workflows pass and any custom inbound rule is narrow in program, service, port, profile, and remote scope.

```powershell
Get-NetFirewallProfile -PolicyStore ActiveStore |
  Select-Object Name,Enabled
```

- **PASS looks like:** All firewall profiles are enabled and required network workflows pass.
- **If it does not pass:** HOLD the affected application. Keep the firewall on and repair only a specific justified rule.
- **Rollback / recovery:** Disable or remove only the latest specific rule created during troubleshooting. Never disable all profiles.
- **Record only:** Record profile Enabled states and workflow PASS. Do not save addresses or full rule exports publicly.
### Step 16 - Remove unused Home remote-support and management paths

- **Controls:** NET-02
- **Priority:** P1
- **Run as:** [USER] then [ADMIN]
- **Action type:** READ-ONLY / CONDITIONAL UI CHANGE
- **Sources:** [2], [28]
- **Goal:** Keep Remote Assistance, Quick Assist, WinRM, Remote Registry, and other listeners limited to an understood need. Home is not an RDP host.

#### Before you start

- Know whether a trusted helper or administration workflow is actually required.
- Do not disable an unknown listener before identifying the owning process and dependency.

#### Do this in order

1. Turn off Remote Assistance when unused.
2. Treat Quick Assist as on-demand only; accept a session only when you initiated the request and independently verified the helper.
3. Inspect Remote Registry and WinRM service state plus listening ports.
4. Investigate every unknown listener. This guide does not provide a generic bulk service-disable command.

#### Commands

```powershell
Get-Service RemoteRegistry,WinRM -ErrorAction SilentlyContinue |
  Select-Object Name,Status,StartType
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress,LocalPort,OwningProcess
```

#### Restart now?

NO.

#### Verify before continuing

1. Only recognized, required listeners and remote services remain.
2. Every retained remote path has an owner, strong authentication, trusted-network scope, and review date.

- **PASS looks like:** Home has no incoming RDP host, and every other retained remote path is understood and narrowly used.
- **If it does not pass:** HOLD and investigate an unknown listener, service, helper, or session before changing it.
- **Rollback / recovery:** Restore only the latest exact UI/service state after proving a required dependency.
- **Record only:** Record service/listener decisions only. Do not publish ports, addresses, process paths, or session details.
### Step 17 - Remove SMB1 and refuse insecure guest access

- **Controls:** NET-03
- **Priority:** P1
- **Run as:** [ADMIN]
- **Action type:** CONDITIONAL CONFIGURATION CHANGE
- **Sources:** [17], [38], [47]
- **Goal:** Remove legacy file-sharing behavior without silently breaking a required authenticated share.

#### Before you start

- Inventory every required network share and its supported authentication method.
- Do not expose SMB directly to the public Internet.

#### Do this in order

1. Query SMB1. Run the disable command only when State is Enabled.
2. Inspect insecure guest-logon state.
3. After required authenticated shares are proved, set insecure guest logons to false if they are true.
4. Restart only if the feature change or Windows requests it, then test each authenticated share.

#### Commands

```powershell
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol |
  Select-Object FeatureName,State
Disable-WindowsOptionalFeature -Online `
  -FeatureName SMB1Protocol -NoRestart
Get-SmbClientConfiguration |
  Select-Object EnableInsecureGuestLogons
Set-SmbClientConfiguration `
  -EnableInsecureGuestLogons $false -Force
```

#### Restart now?

YES after disabling SMB1 or when Windows requests it. Treat it as a REBOOT GATE.

#### Verify before continuing

1. SMB1 reports Disabled.
2. EnableInsecureGuestLogons reports False.
3. Every required share authenticates and works after the restart.

```powershell
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol |
  Select-Object FeatureName,State
Get-SmbClientConfiguration |
  Select-Object EnableInsecureGuestLogons
```

- **PASS looks like:** Legacy SMB1 and insecure guest access are absent; required authenticated shares work.
- **If it does not pass:** HOLD and update, replace, or isolate a legacy dependency. Do not silently re-enable SMB1.
- **Rollback / recovery:** Restore only a documented, time-bounded compatibility state after accepting the risk; replacement is the preferred resolution.
- **Record only:** Record feature and guest states plus sanitized share-test PASS. Do not record server names or addresses.
### Step 18 - Document DNS and network transitions

- **Controls:** NET-04
- **Priority:** P2
- **Run as:** [USER]
- **Action type:** READ-ONLY / CONDITIONAL CHANGE
- **Sources:** [29]
- **Goal:** Keep name resolution understandable and reliable across browser, Windows, router, VPN, Ethernet, and Wi-Fi layers.

#### Before you start

- Know whether a VPN, filtered resolver, router policy, or browser secure-DNS setting is intended.
- Do not publish the command output because it can include network identifiers.

#### Do this in order

1. Inspect current resolver state on screen.
2. Choose one documented resolver model; filtered DNS is optional defense in depth, not a replacement for endpoint protection.
3. If changing a layer, change only one and test browsing, updates, captive portal, VPN connect/disconnect, and Ethernet/Wi-Fi failover.

#### Commands

```powershell
Get-DnsClientServerAddress -AddressFamily IPv4,IPv6
Resolve-DnsName example.com -DnsOnly
```

#### Restart now?

NO.

#### Verify before continuing

1. Normal resolution and all required transitions work.
2. Browser, Windows, router, and VPN resolver choices match the documented design.

- **PASS looks like:** The selected resolver design is intentional and required transitions pass.
- **If it does not pass:** Restore the latest resolver layer and HOLD after repeated stable-link resolution failure or unclear policy ownership.
- **Rollback / recovery:** Restore only the latest recorded browser, adapter, VPN, or router resolver setting.
- **Record only:** Record the design label and tests, not resolver addresses, adapter names, or network captures.

## Phase 07 - F. Staged hardening

### Step 19 - Review and narrow security exceptions before advanced controls

- **Controls:** OPS-01
- **Priority:** P1
- **Run as:** [ADMIN]
- **Action type:** READ-ONLY / CONDITIONAL CHANGE
- **Sources:** [1], [2]
- **Goal:** Prevent broad exclusions and allowances from silently defeating the controls being added next.

#### Before you start

- The intended antimalware and firewall providers are known.
- Review raw paths only on the local device.

#### Do this in order

1. Inspect Defender exclusions and CFA allowed applications locally.
2. Review firewall rules, browser overrides, remote paths, and other security exceptions.
3. Investigate an unknown item before deleting it.
4. For every retained item, record exact scope, owner, reason, test, approval date, and next review.

#### Commands

```powershell
$p = Get-MpPreference
$p | Select-Object ExclusionPath,ExclusionProcess,`
  ExclusionExtension
$p | Select-Object ControlledFolderAccessAllowedApplications
```

#### Restart now?

NO.

#### Verify before continuing

1. No unexplained broad or permanent exception remains.
2. Each retained exception is exact, owned, tested, and scheduled for review.

- **PASS looks like:** Every retained exception is narrow and justified.
- **If it does not pass:** HOLD the dependent advanced control while an exception's owner, need, or effect is unknown.
- **Rollback / recovery:** Re-add only the exact item removed most recently when evidence proves it was required.
- **Record only:** Record counts and decision labels only. Never paste exclusion paths into public evidence.
### Step 20 - Stage the vulnerable-driver blocklist and Memory integrity

- **Controls:** APP-02, PLT-04, PERF-01, PERF-02, OPS-02
- **Priority:** P2
- **Run as:** [USER] then [ADMIN]
- **Action type:** CONFIGURATION CHANGE / REBOOT GATE
- **Sources:** [9], [10]
- **Goal:** Add kernel protections one at a time while preserving driver, peripheral, game, and anti-cheat compatibility.

#### Before you start

- Recovery and acceptance tests passed.
- Inventory required drivers, peripherals, virtualization tools, games, and anti-cheat software.

#### Do this in order

1. Open Windows Security > Device security > Core isolation.
2. Verify or enable the Microsoft vulnerable-driver blocklist first. Restart only if Windows requests it and complete the full gate.
3. Separately enable Memory integrity only after the first change passes.
4. Restart immediately after the Memory integrity change; do not stack another change.

#### Commands

No command. Use the supported interface named above.

#### Restart now?

YES after enabling Memory integrity and whenever Windows requests it for the blocklist. Complete the REBOOT GATE.

#### Verify before continuing

1. Sign in normally with no recovery prompt, crash, missing device, or failed required driver.
2. Memory integrity remains On and runtime data shows VBS running with service value 2 present.
3. Run all affected Step 05 workflows and performance limits.

```powershell
$dg = Get-CimInstance `
  -Namespace root\Microsoft\Windows\DeviceGuard `
  -ClassName Win32_DeviceGuard
$dg | Select-Object VirtualizationBasedSecurityStatus,`
  SecurityServicesConfigured,SecurityServicesRunning
```

- **PASS looks like:** The blocklist is on; Memory integrity is effective after reboot; all required workflows and limits pass.
- **If it does not pass:** HOLD after an incompatible driver, boot problem, hardware error, or measured regression.
- **Rollback / recovery:** Turn off only Memory integrity through Windows Security, restart, and update or replace the exact incompatible driver. Use the proved WinRE path if Windows cannot boot.
- **Record only:** Record old/new UI state, restart, runtime summary, and workflow PASS. Do not copy driver paths or event messages publicly.
### Step 21 - Deploy Attack Surface Reduction rules one at a time

- **Controls:** DEF-05, OPS-02
- **Priority:** P2
- **Run as:** [ADMIN]
- **Action type:** AUDIT-FIRST CONFIGURATION CHANGE
- **Sources:** [12], [13], [33], [35], [45]
- **Goal:** Reduce common script, Office, credential, persistence, ransomware, and vulnerable-driver abuse without importing an untested rule bundle.

#### Before you start

- Defender is active and healthy.
- Exceptions were reviewed and required workflows are ready.
- Choose exactly one full GUID from the current Microsoft reference and the ASR candidate appendix.

#### Do this in order

1. Inventory existing full GUID/action pairs.
2. If the selected rule is not already controlled elsewhere, add only that rule in AuditMode.
3. Complete every applicable workflow and review provider/time-scoped events.
4. When audit results are understood, change only that same rule to Enabled.
5. Repeat the loop for a second rule only after the first rule passes an observation cycle.

#### Commands

```powershell
$p = Get-MpPreference
$ids = @($p.AttackSurfaceReductionRules_Ids)
$acts = @($p.AttackSurfaceReductionRules_Actions)
for ($i = 0; $i -lt $ids.Count; $i++) {
  [pscustomobject]@{RuleId=[string]$ids[$i];Action=$acts[$i]}
}
$RuleId = 'PASTE-FULL-GUID-FROM-ASR-CANDIDATE-APPENDIX'
Add-MpPreference -AttackSurfaceReductionRules_Ids $RuleId `
  -AttackSurfaceReductionRules_Actions AuditMode
Add-MpPreference -AttackSurfaceReductionRules_Ids $RuleId `
  -AttackSurfaceReductionRules_Actions Enabled
```

#### Restart now?

NO.

#### Verify before continuing

1. The exact full GUID and action are visible.
2. The audit cycle completed, the intended enforced action remains effective, and required workflows pass.
3. Any exception is limited to the exact affected rule and resource.

- **PASS looks like:** Each selected rule was individually audited, enforced, and tested.
- **If it does not pass:** Return only the affected rule to AuditMode and HOLD while investigating an event or workflow failure.
- **Rollback / recovery:** Run the same Add-MpPreference command for the affected GUID with action AuditMode. Never add a broad exclusion to hide an unexplained block.
- **Record only:** Record rule name, full GUID, action, dates, and sanitized result. Event messages and paths remain restricted.
### Step 22 - Stage Controlled Folder Access

- **Controls:** DEF-06, OPS-02, PERF-02
- **Priority:** P2
- **Run as:** [ADMIN]
- **Action type:** AUDIT-FIRST CONFIGURATION CHANGE
- **Sources:** [14], [33], [36], [46]
- **Goal:** Protect important folders from unauthorized writes without pre-allowing broad folders, launchers, or unknown applications.

#### Before you start

- Defender is active and healthy.
- Required save, open, export, sync, update, screenshot, game-save, creative, and accessibility workflows are defined.

#### Do this in order

1. Capture the prior mode, then switch to AuditMode.
2. Record the test start time and run every representative writer workflow.
3. Review only CFA events from that time.
4. When every writer is understood, switch to Enabled and repeat the workflows.
5. Allow only an exact verified executable when evidence proves a need.

#### Commands

```powershell
$priorCfa = (Get-MpPreference).EnableControlledFolderAccess
Set-MpPreference -EnableControlledFolderAccess AuditMode
$start = Get-Date
Set-MpPreference -EnableControlledFolderAccess Enabled
```

#### Restart now?

NO.

#### Verify before continuing

1. The intended mode remains effective.
2. Required writes pass and CFA event 1123/1124 review identifies no unexplained required writer.

```powershell
$f = @{
  LogName='Microsoft-Windows-Windows Defender/Operational'
  Id=1123,1124
  StartTime=$start
}
Get-WinEvent -FilterHashtable $f -ErrorAction SilentlyContinue |
  Select-Object TimeCreated,Id,ProviderName
Get-MpPreference | Select-Object EnableControlledFolderAccess
```

- **PASS looks like:** CFA is intentional, required writes pass, and every allowance is an exact verified executable.
- **If it does not pass:** Return to AuditMode and HOLD while investigating the exact writer.
- **Rollback / recovery:** Set-MpPreference -EnableControlledFolderAccess AuditMode
- **Record only:** Record mode, test set, event count, and PASS/HOLD only. Do not publish paths or event messages.

## Phase 08 - G. Closeout and maintenance

### Step 23 - Keep local logging proportionate and privacy-aware

- **Controls:** LOG-01, LOG-02, LOG-03
- **Priority:** P2
- **Run as:** [ADMIN]
- **Action type:** READ-ONLY / DECISION
- **Sources:** [2], [4], [20], [42]
- **Goal:** Collect only events that support a decision and keep command-line content off by default on the Pro baseline path.

#### Before you start

- Define who will review a log, why, and for how long before adding collection.
- Raw events and command lines may contain personal data and secrets.

#### Do this in order

1. Review the current audit categories.
2. Do not enable command-line argument capture as a consumer default.
3. When querying events, always specify log, provider, event ID, and a deliberate start time.
4. Keep raw exports restricted and delete them when their purpose ends, subject to an investigation or legal hold.

#### Commands

```powershell
auditpol.exe /get /category:*
```

#### Restart now?

NO.

#### Verify before continuing

1. Audit scope, review owner, retention, access, and deletion are documented.
2. No plaintext command-line collection exists without a clear accepted need.

- **PASS looks like:** Logging is proportionate, provider/time scoped, and handled as sensitive evidence.
- **If it does not pass:** HOLD additional logging when no review use case exists or sensitive content cannot be protected.
- **Rollback / recovery:** Return only the exact latest audit setting to its recorded prior state; do not clear logs to hide an error.
- **Record only:** Record audit categories and handling decisions only. Raw log content stays restricted.
### Step 24 - Run final acceptance and schedule reassessment

- **Controls:** OPS-01, OPS-02, OPS-03, OPS-04, PERF-01, PERF-02
- **Priority:** P1
- **Run as:** [USER]
- **Action type:** ACTIVE ACCEPTANCE TEST / RECORD
- **Sources:** [1], [2], [3], [4]
- **Goal:** Close only controls actually proved, leave unknowns visible, and make the baseline maintainable.

#### Before you start

- All earlier steps are PASS, HOLD, EXCEPTION, or documented N/A.
- No unexplained stacked change remains.

#### Do this in order

1. Run the complete Step 05 workflow and performance suite.
2. Open Reliability Monitor and review the period covering the changes.
3. Close each control only with the result actually supported.
4. Record every exception with scope, owner, reason, compensating measure, approval date, and next review.
5. Set review triggers for major Windows, firmware, driver, security-tool, network, remote-access, incident, or recovery changes.

#### Commands

```powershell
perfmon.exe /rel
```

#### Restart now?

NO.

#### Verify before continuing

1. Every retained control has a result, date, owner, and review trigger/date.
2. Required workflows and limits pass with no new unexplained reliability failure.
3. Public materials contain no sensitive evidence.

- **PASS looks like:** The edition-specific baseline has a complete, dated, reviewable outcome.
- **If it does not pass:** Leave the affected item HOLD. Do not call the overall baseline complete while instability or unexplained results remain.
- **Rollback / recovery:** Reverse only the latest documented reversible change tied to the failure, then repeat its focused and representative tests.
- **Record only:** Record final results and next-review dates. Restricted evidence remains outside the public repository.

## ASR candidate appendix

Use this table to replace `PASTE-FULL-GUID-FROM-ASR-CANDIDATE-APPENDIX` in the Step 21 command. Copy one complete GUID exactly as shown.

### Safety notes

- This is a candidate reference, not a recommendation to enable every rule.
- Recheck the selected GUID, rule name, prerequisites, and current behavior against the Microsoft ASR rule reference [12].
- Stop if ASR is already controlled by organizational policy, device management, or another authorized owner. Do not overwrite managed settings.
- Inventory existing GUID/action pairs first. Evaluate exactly one applicable rule in Audit mode and complete the required workflow observation cycle.
- Change only that same reviewed rule to Enabled after its audit results, exceptions, rollback, and ownership are understood.
- Never paste the placeholder text into PowerShell and never deploy the full candidate list as an untested bundle.

| Full GUID | Microsoft rule name | Applicability and safety note |
| --- | --- | --- |
| `56a863a9-875e-4185-98a7-b882c64b5ce5` | Block abuse of exploited vulnerable signed drivers | Evaluate broadly. This prevents an application from writing a vulnerable signed driver; it does not stop an already-present vulnerable driver from loading. |
| `d3e037e1-3eb8-44c8-a917-57927947596d` | Block JavaScript or VBScript from launching downloaded executable content | Evaluate when script-based installers or administration workflows have been inventoried. |
| `e6db77e5-3df2-4cf1-b95a-636979351e5b` | Block persistence through WMI event subscription | Evaluate after inventorying legitimate management or monitoring tools. |
| `c1db55ab-c21a-4637-bb3f-a12568109d35` | Use advanced protection against ransomware | Evaluate after storage, backup, sync, and application workflows are defined. |
| `d4f940ab-401b-4efc-aadc-ad5f3c50688a` | Block Office applications from creating child processes | Applicable when Microsoft Office desktop applications are installed and required add-ins or automation have been tested. |
| `3b576869-a4ec-4529-8536-b80a7769e899` | Block Office applications from creating executable content | Applicable when Microsoft Office desktop applications are installed. |
| `75668c1f-73b5-4cf0-bb93-3ecf5cb7cc84` | Block Office applications from injecting code | Applicable when Microsoft Office desktop applications are installed and compatibility is understood. |
| `92e97fa1-2edf-4476-bdd6-9dd0b4dddc7b` | Block Win32 API calls from Office macros | Applicable only after legitimate macro and automation needs are inventoried. |
| `be9ba2d9-53ea-4cdc-84e5-9b1eeee46550` | Block executable content from email client and webmail | Evaluate after required mail-client and attachment workflows are tested. |

## Full control matrix

### GOV-01 - Managed-device authority stop

- **Priority:** P0
- **Procedure step:** 01
- **Outcome:** Authority is confirmed; managed devices are referred to the authorized administrator.
- **Sources:** [1], [2]

### GOV-02 - Evidence minimization and handling

- **Priority:** P0
- **Procedure step:** 02
- **Outcome:** Evidence is minimal, redacted, access-controlled, and stored outside public repositories when sensitive.
- **Sources:** [1], [2], [4]

### REC-01 - Restorable backup

- **Priority:** P0
- **Procedure step:** 03
- **Outcome:** A representative restore succeeds from a current copy isolated from routine write access.
- **Sources:** [1], [2], [5]

### REC-02 - Drive-recovery readiness

- **Priority:** P0
- **Procedure step:** 04, 12
- **Outcome:** Encryption state is known and its recovery method is accessible without recording the secret.
- **Sources:** [7]

### REC-03 - Recovery environment and administrator

- **Priority:** P0
- **Procedure step:** 04, 10
- **Outcome:** Windows RE and an independent administrator sign-in are tested.
- **Sources:** [2], [30]

### PLT-01 - Supported Windows and updates

- **Priority:** P1
- **Procedure step:** 01, 06, 07
- **Outcome:** Windows is supported, security updates are current, and any compatibility hold is documented.
- **Sources:** [6]

### PLT-02 - UEFI boot and Secure Boot

- **Priority:** P0
- **Procedure step:** 06, 09
- **Outcome:** Windows reports UEFI mode and Secure Boot enabled; recovery readiness passes first.
- **Sources:** [8]

### PLT-03 - TPM health

- **Priority:** P0
- **Procedure step:** 06, 09
- **Outcome:** TPM health fields pass without clearing, reprovisioning, or exposing key material.
- **Sources:** [21]

### PLT-04 - Virtualization and DMA remapping

- **Priority:** P2
- **Procedure step:** 06, 09, 20
- **Outcome:** Home: inventory CPU virtualization and test VBS/Memory integrity. Kernel DMA Protection is not a Home capability.
- **Sources:** [9], [22]

### PLT-05 - Exact-model firmware servicing

- **Priority:** P1
- **Procedure step:** 06, 08
- **Outcome:** Exact-model applicability, prerequisites, recovery, power, and post-update checks are documented.
- **Sources:** [2], [6]

### PLT-06 - Data-at-rest encryption

- **Priority:** P1
- **Procedure step:** 12
- **Outcome:** Home: use Device Encryption only when the device and Windows UI support it; prove independent recovery.
- **Sources:** [7]

### ID-01 - Standard daily-use account

- **Priority:** P1
- **Procedure step:** 04, 10
- **Outcome:** Routine work uses a standard account and administration requires deliberate elevation.
- **Sources:** [2], [18]

### ID-02 - Strong sign-in and recovery

- **Priority:** P1
- **Procedure step:** 11
- **Outcome:** Strong authentication and two independent recovery methods are configured and tested.
- **Sources:** [1], [23]

### ID-03 - User Account Control

- **Priority:** P1
- **Procedure step:** 10
- **Outcome:** UAC is default-or-higher and elevation is a deliberate, visible action.
- **Sources:** [19]

### DEF-01 - Active and current antimalware

- **Priority:** P1
- **Procedure step:** 07, 13
- **Outcome:** The intended antimalware provider is active, healthy, and current.
- **Sources:** [11], [25]

### DEF-02 - Runtime and tamper protection

- **Priority:** P1
- **Procedure step:** 13
- **Outcome:** Runtime protections and tamper resistance are enabled or an authorized exception exists.
- **Sources:** [24], [25]

### DEF-03 - Cloud and sample protection

- **Priority:** P1
- **Procedure step:** 13
- **Outcome:** Cloud protection is enabled and sample handling is an intentional privacy choice.
- **Sources:** [25]

### DEF-04 - Potentially unwanted application blocking

- **Priority:** P1
- **Procedure step:** 13
- **Outcome:** PUA protection is in Block mode and retained exceptions have a verified need and source.
- **Sources:** [26]

### DEF-05 - Attack Surface Reduction rules

- **Priority:** P2
- **Procedure step:** 21
- **Outcome:** Applicable ASR rules have full GUIDs, explicit modes, owners, tests, and narrow exceptions.
- **Sources:** [12], [13]

### DEF-06 - Controlled Folder Access

- **Priority:** P2
- **Procedure step:** 22
- **Outcome:** CFA is intentional and required writes pass without broad allowances.
- **Sources:** [14]

### APP-01 - Reputation-based application protection

- **Priority:** P1
- **Procedure step:** 14
- **Outcome:** Applicable reputation controls are enabled and exceptions are specific and verified.
- **Sources:** [27]

### APP-02 - VBS, HVCI, and vulnerable-driver blocking

- **Priority:** P2
- **Procedure step:** 20
- **Outcome:** Driver blocking is enabled; VBS and HVCI are intentional and pass compatibility tests.
- **Sources:** [9], [10]

### NET-01 - Windows Firewall profiles

- **Priority:** P1
- **Procedure step:** 15
- **Outcome:** All profiles are enabled and custom inbound rules are narrowly scoped and justified.
- **Sources:** [16]

### NET-02 - Remote services and listeners

- **Priority:** P1
- **Procedure step:** 16
- **Outcome:** Home: minimize Remote Assistance, Quick Assist, WinRM, Remote Registry, and unknown listeners. Home cannot host RDP.
- **Sources:** [2], [28]

### NET-03 - SMB and legacy sharing

- **Priority:** P1
- **Procedure step:** 17
- **Outcome:** SMB1 and insecure guest access are absent; required shares are authenticated and scoped.
- **Sources:** [17]

### NET-04 - DNS and network failover

- **Priority:** P2
- **Procedure step:** 18
- **Outcome:** Resolver and failover paths are documented and pass representative tests.
- **Sources:** [29]

### LOG-01 - Security audit policy

- **Priority:** P2
- **Procedure step:** 23
- **Outcome:** Audit scope, retention, access, and deletion rights are proportionate and documented.
- **Sources:** [2], [4]

### LOG-02 - Command-line logging privacy

- **Priority:** P2
- **Procedure step:** 23
- **Outcome:** Home: leave plaintext command-line capture off by default; collect only proportionate local audit data.
- **Sources:** [4], [20]

### LOG-03 - Provider-scoped event review

- **Priority:** P2
- **Procedure step:** 23
- **Outcome:** Event evidence is provider-scoped, time-scoped, minimal, and tied to a decision.
- **Sources:** [4], [20]

### OPS-01 - Narrow, expiring exceptions

- **Priority:** P1
- **Procedure step:** 19, 24
- **Outcome:** Every exception is narrow, owned, tested, and scheduled for review or removal.
- **Sources:** [1], [2]

### OPS-02 - One-change staging and rollback

- **Priority:** P1
- **Procedure step:** 02, 05, 08, 20, 21, 22, 24
- **Outcome:** Each material change is isolated, reversible, tested, and observed.
- **Sources:** [1], [2]

### OPS-03 - Incident and instability stop

- **Priority:** P0
- **Procedure step:** 01, 24
- **Outcome:** Baseline work stops during suspected compromise or instability and follows an authorized path.
- **Sources:** [3]

### OPS-04 - Scheduled review

- **Priority:** P3
- **Procedure step:** 24
- **Outcome:** Every applicable control has an owner and review trigger or date.
- **Sources:** [1]

### PERF-01 - Representative performance baseline

- **Priority:** P2
- **Procedure step:** 05, 20, 24
- **Outcome:** Applicable performance and reliability limits are defined and tested consistently.
- **Sources:** [1], [2]

### PERF-02 - Representative workflow acceptance

- **Priority:** P1
- **Procedure step:** 05, 20, 22, 24
- **Outcome:** Required workflows pass after each material change without disabling broad protections.
- **Sources:** [1], [2]

## IEEE-style references

[1] National Institute of Standards and Technology, "The NIST Cybersecurity Framework (CSF) 2.0", NIST CSWP 29, Feb. 2024. [Online]. Available: https://doi.org/10.6028/NIST.CSWP.29. Accessed: Jul. 29, 2026. Govern, identify, protect, detect, respond, and recover outcomes.
[2] National Institute of Standards and Technology, "Security and Privacy Controls for Information Systems and Organizations", NIST SP 800-53 Rev. 5, Sept. 2020 (includes updates as of Dec. 10, 2020). [Online]. Available: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final. Accessed: Jul. 29, 2026. Least privilege, configuration, logging, contingency planning, and recovery controls.
[3] National Institute of Standards and Technology, "Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile", NIST SP 800-61 Rev. 3, Apr. 2025. [Online]. Available: https://csrc.nist.gov/pubs/sp/800/61/r3/final. Accessed: Jul. 29, 2026. Incident-response recommendations and CSF 2.0 integration.
[4] National Institute of Standards and Technology, "Guide to Computer Security Log Management", NIST SP 800-92, Sept. 2006. [Online]. Available: https://csrc.nist.gov/pubs/sp/800/92/final. Accessed: Jul. 29, 2026. Security-log planning, handling, retention, and operations.
[5] Cybersecurity and Infrastructure Security Agency, "#StopRansomware Guide", rev. Oct. 19, 2023. [Online]. Available: https://www.cisa.gov/resources-tools/resources/stopransomware-guide. Accessed: Jul. 29, 2026. Backups, recovery testing, access control, and preparation.
[6] Microsoft, "Windows 11 release information". [Online]. Available: https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information. Accessed: Jul. 29, 2026. Current servicing and release-health information.
[7] Microsoft, "BitLocker Overview". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/. Accessed: Jul. 29, 2026. Encryption capabilities and recovery considerations.
[8] Microsoft Support, "Windows 11 and Secure Boot". [Online]. Available: https://support.microsoft.com/en-us/windows/security/devicesecurity/windows-11-and-secure-boot. Accessed: Jul. 29, 2026. Secure Boot purpose, firmware guidance, and supported Windows behavior.
[9] Microsoft, "Enable memory integrity". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity. Accessed: Jul. 29, 2026. Memory Integrity and VBS enablement, compatibility, and rollback.
[10] Microsoft, "Microsoft recommended driver block rules". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules. Accessed: Jul. 29, 2026. Vulnerable-driver blocklist behavior and compatibility.
[11] Microsoft, "Microsoft Defender Antivirus security intelligence and product updates and support". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates. Accessed: Jul. 29, 2026. Platform, engine, and security-intelligence servicing.
[12] Microsoft, "ASR rules reference". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference. Accessed: Jul. 29, 2026. Full ASR rule GUIDs, modes, prerequisites, and compatibility.
[13] Microsoft, "Plan your attack surface reduction (ASR) rules deployment". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-deployment-plan. Accessed: Jul. 29, 2026. Assessment, Audit mode, reporting, and staged enforcement.
[14] Microsoft, "Controlled folder access (CFA) overview". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-overview. Accessed: Jul. 29, 2026. Scope, modes, dependencies, and monitoring.
[15] Microsoft, "Use network protection to help prevent connections to malicious or suspicious sites". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/network-protection. Accessed: Jul. 29, 2026. Current prerequisites, modes, and safe evaluation.
[16] Microsoft, "Windows Firewall Rules". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/rules. Accessed: Jul. 29, 2026. Narrow rule scope, precedence, and firewall design.
[17] Microsoft, "SMB security hardening in Windows Server and Windows Client". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security-hardening. Accessed: Jul. 29, 2026. Signing, guest access, SMB1, and current behavior.
[18] Microsoft, "Local accounts". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/identity-protection/access-control/local-accounts. Accessed: Jul. 29, 2026. Daily-use and administrative-account separation.
[19] Microsoft Support, "User Account Control settings". [Online]. Available: https://support.microsoft.com/en-us/windows/security/user-account-control-settings. Accessed: Jul. 29, 2026. Supported UAC levels and prompt behavior.
[20] Microsoft, "Command line process auditing". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing. Accessed: Jul. 29, 2026. Event 4688 configuration and plaintext-secret warning.
[21] Microsoft, "TPM recommendations". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/tpm-recommendations. Accessed: Jul. 29, 2026. TPM capabilities, Windows dependencies, and recommendations.
[22] Microsoft, "Kernel DMA Protection". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/hardware-security/kernel-dma-protection-for-thunderbolt. Accessed: Jul. 29, 2026. Hardware, firmware, driver, and edition dependencies.
[23] Microsoft, "Passwordless sign-in". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/book/identity-protection-passwordless-sign-in. Accessed: Jul. 29, 2026. Windows Hello, passkeys, FIDO2, and phishing-resistant sign-in.
[24] Microsoft, "Protect security settings with tamper protection". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection. Accessed: Jul. 29, 2026. Tamper-protection purpose, behavior, and management ownership.
[25] Microsoft, "Configure behavioral, heuristic, and real-time protection". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/configure-protection-features-microsoft-defender-antivirus. Accessed: Jul. 29, 2026. Real-time, behavior, IOAV, cloud, and related protection features.
[26] Microsoft, "Detect and block potentially unwanted applications". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/detect-block-potentially-unwanted-apps-microsoft-defender-antivirus. Accessed: Jul. 29, 2026. PUA applicability, modes, configuration, and review.
[27] Microsoft Support, "App & browser control in the Windows Security App". [Online]. Available: https://support.microsoft.com/en-us/windows/security/windows-security/app-browser-control-in-the-windows-security-app. Accessed: Jul. 29, 2026. Reputation-based protection and Smart App Control availability.
[28] Microsoft, "Enable Remote Desktop on your PC". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access. Accessed: Jul. 29, 2026. Remote Desktop exposure, trusted-network scope, authentication, and editions.
[29] Microsoft, "DNS Queries and Lookups in Windows and Windows Server". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/networking/dns/queries-lookups. Accessed: Jul. 29, 2026. Windows DNS client behavior and resolver redundancy.
[30] Microsoft, "Push-button reset frequently-asked questions (FAQ)". [Online]. Available: https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/pbr-faq?view=windows-11. Accessed: Jul. 29, 2026. Windows Recovery Environment and recovery-tool requirements.
[31] Microsoft Support, "Device Encryption in Windows". [Online]. Available: https://support.microsoft.com/en-us/windows/security/encryption/device-encryption-in-windows. Accessed: Jul. 29, 2026. Home availability, prerequisites, recovery-account behavior, and supported UI.
[32] Microsoft Support, "BitLocker Drive Encryption". [Online]. Available: https://support.microsoft.com/en-us/windows/security/encryption/bitlocker-drive-encryption. Accessed: Jul. 29, 2026. Pro-and-higher availability and the supported BitLocker management UI.
[33] Microsoft, "Set-MpPreference". [Online]. Available: https://learn.microsoft.com/en-us/powershell/module/defender/set-mppreference. Accessed: Jul. 29, 2026. Elevated Defender configuration syntax and supported values.
[34] Microsoft, "Evaluate network protection". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/evaluate-network-protection. Accessed: Jul. 29, 2026. Official harmless test, audit and block workflow, and events 1125 and 1126.
[35] Microsoft, "Attack surface reduction events in Windows Event Viewer". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-windows-events. Accessed: Jul. 29, 2026. Provider-specific ASR, CFA, and Network Protection event identifiers.
[36] Microsoft, "Monitor controlled folder access activity". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-monitor. Accessed: Jul. 29, 2026. Controlled Folder Access audit and block events plus evaluation guidance.
[37] Microsoft, "Set-NetFirewallProfile". [Online]. Available: https://learn.microsoft.com/en-us/powershell/module/netsecurity/set-netfirewallprofile. Accessed: Jul. 29, 2026. Supported Windows Firewall profile configuration syntax.
[38] Microsoft, "Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3. Accessed: Jul. 29, 2026. SMB1 feature detection, removal, and restart behavior.
[39] Microsoft, "Get-BitLockerVolume". [Online]. Available: https://learn.microsoft.com/en-us/powershell/module/bitlocker/get-bitlockervolume. Accessed: Jul. 29, 2026. BitLocker volume, protection, encryption, and protector status fields.
[40] Microsoft, "BitLocker operations guide". [Online]. Available: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/operations-guide. Accessed: Jul. 29, 2026. Supported enablement, system-check, recovery, and operating procedures.
[41] National Institute of Standards and Technology, "Guide to Storage Encryption Technologies for End User Devices", NIST SP 800-111, Nov. 2007. [Online]. Available: https://csrc.nist.gov/pubs/sp/800/111/final. Accessed: Jul. 29, 2026. Technology-neutral endpoint storage-encryption and recovery considerations.
[42] Microsoft, "auditpol set". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol-set. Accessed: Jul. 29, 2026. Supported audit-policy subcategory configuration syntax.
[43] National Institute of Standards and Technology, "Guide to Enterprise Telework, Remote Access, and Bring Your Own Device (BYOD) Security", NIST SP 800-46 Rev. 2, July 2016. [Online]. Available: https://csrc.nist.gov/pubs/sp/800/46/r2/final. Accessed: Jul. 29, 2026. Remote-access threat, authentication, and lifecycle considerations.
[44] Microsoft, "Policy CSP - ADMX_AuditSettings". [Online]. Available: https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-auditsettings. Accessed: Jul. 29, 2026. Edition applicability and plaintext privacy warning for process command-line auditing.
[45] Microsoft, "Attack surface reduction (ASR) rules overview". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-overview. Accessed: Jul. 29, 2026. Any-edition availability with Microsoft Defender Antivirus, local PowerShell configuration, modes, and audit-first deployment.
[46] Microsoft, "Configure controlled folder access (CFA)". [Online]. Available: https://learn.microsoft.com/en-us/defender-endpoint/controlled-folder-access-configure. Accessed: Jul. 29, 2026. Windows 10-or-later applicability, elevated PowerShell configuration, modes, and Windows Security workflow.
[47] Microsoft, "How to enable insecure guest logons in SMB2 and SMB3". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/storage/file-server/enable-insecure-guest-logons-smb2-and-smb3. Accessed: Jul. 29, 2026. Windows 11 applicability, administrator requirement, insecure-guest risk, defaults, and PowerShell configuration.
[48] Microsoft, "manage-bde". [Online]. Available: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde. Accessed: Jul. 29, 2026. Windows 11 command-line encryption-status support for all drives, including unprotected drives.
