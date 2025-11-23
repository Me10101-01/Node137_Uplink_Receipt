# Safe fixer: writes the YAML, backs up your profile, and performs a targeted fix
# Usage: run in PowerShell as the same user: .\fix_recon_and_write_progress.ps1

# 1) Write YAML progress file (overwrites if exists)
$yaml = @'
progress:
  - item: Set up 7% royalty lock legally (irrevocable charitable assignment documents signed)
    status: in_progress
    notes: Manifest written and locally committed (a3d26bd); GPG signing failed (gpg not found); push failed (no upstream/remote not found); OpenTimestamps failed (ots not found, DNS resolve failed); CRT not created
  - item: Document the PLAN for 7% lock as proof of intent
    status: complete
    notes: SOVEREIGN_MANIFEST_v1.0.md created multiple times; includes irrevocable assignment under 26 U.S.C. § 170 & § 664
  - item: Confirm Strategickhaos DAO LLC (Wyoming) existence
    status: complete
    notes: Verified with Certificate of Good Standing (ID 2025-001708194) and EIN 39-2923503
  - item: Identify or create other operational legal entities (charitable arms/nonprofit recipients)
    status: in_progress
    notes: ValorYield Engine Nonprofit Corporation confirmed (ID 2025-001708312); beneficiaries identified (St. Jude, MSF, etc.); no new creations
  - item: Prepare evidence for investors/partners (business proof)
    status: pending
    notes: Not primary focus
  - item: Prepare evidence for legal defense (courtroom-grade documentation)
    status: in_progress
    notes: Certificates, EIN, manifest provide base; GPG/OTS/Arweave failed; needs full chain
  - item: Prepare evidence for academic submission (SNHU capstone)
    status: in_progress
    notes: Framed as academic; GitHub vault aligns but not pushed
  - item: Prepare evidence for public transparency (X platform, GitHub)
    status: in_progress
    notes: Bio updates suggested; repo create/push failed; manifest ready
  - item: File Charitable Remainder Unitrust (CRT)
    status: pending
    notes: Not executed
  - item: Record Copyright Royalty Assignment with county recorder
    status: pending
    notes: Not done
  - item: Amend DAO LLC operating agreement to reference manifest + timestamps
    status: pending
    notes: Not executed
  - item: Publish full proof chain on IPFS + Arweave + GitHub
    status: pending
    notes: Git push failed; Arweave install/deploy failed (npm not found)
  - item: File micro-entity declaration (Form SB/15A)
    status: in_progress
    notes: Start-Process opened URL; form not submitted in dump
  - item: File provisional patent application
    status: pending
    notes: EFS-Web opened; pandoc failed (not installed); PDF not generated; upload not done
  - item: Update X bio with legal-safe version
    status: in_progress
    notes: Versions provided; not pasted in dump
  - item: Pin post with proofs (receipts, timestamps)
    status: pending
    notes: Content ready; no patent receipt yet
  - item: Fix GPG signing for Git commits
    status: pending
    notes: gpg not found/installed; import failed; commit -S failed
  - item: Install and run OpenTimestamps for manifest
    status: pending
    notes: winget failed (no package); ots not found; iwr aborted; DNS resolve failed
  - item: Upload to Arweave
    status: pending
    notes: npm not found; install failed
  - item: Provide Wyoming Articles of Organization PDF
    status: complete
    notes: CertOfGoodStanding provided (two versions)
  - item: Provide EIN Confirmation Letter
    status: complete
    notes: CP 575 E provided
  - item: Provide UIDP Smart Contract Code Snippet or Tx Hash
    status: pending
    notes: Not provided
  - item: Provide Donation-Triggered Mint Script
    status: pending
    notes: Not provided
  - item: Provide Notarization Proof (Git SHA or .ots)
    status: in_progress
    notes: Local commit a3d26bd; no push/stamp
  - item: Keep personal assets under $5k forever
    status: N/A
    notes: Ongoing policy
  - item: Publish annual transparency report on IPFS + GitHub
    status: pending
    notes: Not created
  - item: Fix PowerShell profile syntax error
    status: pending
    notes: Errors persist in dump (missing expression/Unexpected token)
  - item: Install GPG
    status: pending
    notes: winget GnuPG.Gpg4win not run in dump
  - item: Install Node.js/npm
    status: pending
    notes: Not installed; npm commands fail
  - item: Install Pandoc
    status: pending
    notes: pandoc not found
  - item: Install Claude Code
    status: complete
    notes: irm | iex succeeded; version 2.0.50; PATH note given
  - item: Add .local\bin to PATH
    status: pending
    notes: Not added in dump
  - item: WSL path fixes
    status: N/A
    notes: Multiple translation errors; ignore for core tasks
  - item: Git init repo
    status: pending
    notes: gh create fails (not git repo)
  - item: Git commit with GPG
    status: in_progress
    notes: Unsigned commit succeeded (a3d26bd)
  - item: Git push to GitHub
    status: pending
    notes: Fails (remote not found)
  - item: Download ots.exe
    status: pending
    notes: iwr aborted
  - item: Stamp manifest with OpenTimestamps
    status: pending
    notes: ots not found; iwr DNS failed
  - item: Convert MD to PDF for patent
    status: pending
    notes: pandoc not found
  - item: Add patent files to git
    status: pending
    notes: git add failed (files not exist)
  - item: gh agent-task view
    status: N/A
    notes: Unknown command; not needed
'@

$yamlPath = Join-Path -Path (Get-Location) -ChildPath 'SOVEREIGN_PROGRESS.yaml'
Set-Content -Path $yamlPath -Value $yaml -Encoding UTF8
Write-Host "Wrote YAML to $yamlPath"

# 2) Backup profile
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}
$bak = "$PROFILE.bak.$((Get-Date).ToString('yyyyMMddHHmmss'))"
Copy-Item -Path $PROFILE -Destination $bak -Recurse -Force
Write-Host "Backed up existing profile to $bak"

# 3) Targeted replacement for the exact malformed line you reported:
#    param([Parameter(Mandatory=\True)][string]\)
# Replace with:
#    param([Parameter(Mandatory=$true)][string]$target)
$content = Get-Content -Path $PROFILE -Raw -ErrorAction SilentlyContinue
if ($null -eq $content) { $content = '' }

$malformedPattern = 'param\(\[Parameter\(Mandatory=\\True\)\]\[string\]\\\)'
$correctReplacement = 'param([Parameter(Mandatory=$true)][string]$target)'

if ($content -match $malformedPattern) {
    $newContent = $content -replace $malformedPattern, [System.Text.RegularExpressions.Regex]::Escape($correctReplacement)
    # The -replace above will escape replacement, so convert escape sequences back:
    $newContent = $newContent -replace [System.Text.RegularExpressions.Regex]::Escape($correctReplacement), $correctReplacement
    Set-Content -Path $PROFILE -Value $newContent -Encoding UTF8
    Write-Host "Replaced malformed recon param line in $PROFILE"
} else {
    Write-Host "Malformed recon param line with that exact backslashes not found. No replace done."
    Write-Host "If your profile still errors, paste the first 30 lines with: Get-Content $PROFILE -TotalCount 30"
}

# 4) Try sourcing the profile to show errors (will display the same parse error if still present)
try {
    . $PROFILE
    Write-Host "Profile sourced OK."
} catch {
    Write-Host "Error sourcing profile: $($_.Exception.Message)"
    if ($_.InvocationInfo) { Write-Host $_.InvocationInfo.PositionMessage }
}

# 5) Try to locate gpg.exe and add its directory to PATH (only if found)
$gpgPaths = @()
$probeDirs = @('C:\Program Files','C:\Program Files (x86)')
foreach ($d in $probeDirs) {
    if (Test-Path $d) {
        $gpgPaths += Get-ChildItem -Path $d -Filter 'gpg.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName -ErrorAction SilentlyContinue
    }
}
$gpgPaths = $gpgPaths | Select-Object -Unique
if ($gpgPaths.Count -gt 0) {
    Write-Host "Found gpg.exe at:"
    $gpgPaths | ForEach-Object { Write-Host "  $_" }
    $gpgDir = Split-Path $gpgPaths[0]
    Write-Host "Adding $gpgDir to user PATH (setx). You will need to restart PowerShell to pick it up."
    setx PATH "$env:PATH;$gpgDir" | Out-Null
} else {
    Write-Host "gpg.exe not found under Program Files. If you just installed Gpg4win, restart PowerShell or reboot. To install: winget install GnuPG.Gpg4win"
}

# 6) Check for the AE551957... key blob in .gnupg
$keyPath = Join-Path -Path $env:USERPROFILE -ChildPath '.gnupg\private-keys-v1.d\AE5519579584DEF5.key'
if (Test-Path $keyPath) {
    Write-Host "Found key blob at $keyPath"
    Write-Host "If this is an exported OpenPGP secret (ASCII-armored), import with: gpg --import `"$keyPath`""
    Write-Host "If this is a GnuPG internal blob, do NOT use --import. Instead copy to $env:USERPROFILE\.gnupg\private-keys-v1.d (it's already there) and ensure proper permissions."
} else {
    Write-Host "$keyPath not found. Search for potential key files with:"
    Write-Host "  Get-ChildItem -Path $env:USERPROFILE -Recurse -Force -ErrorAction SilentlyContinue -Filter '*AE5519579584DEF5*' | Select-Object FullName"
}

Write-Host "Done. Inspect the profile backup if anything looks wrong. If you want I can produce a version of the recon function to insert (with more of the original body preserved) — paste the first 30 lines of $PROFILE and I'll prepare it."
