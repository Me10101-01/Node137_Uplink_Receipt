# The Rotation Protocol

## Overview

The Rotation Protocol is a comprehensive pre-sleep and wake-up checklist system designed to ensure all critical systems are backed up, secured, and ready for hibernation/suspension cycles. It maintains system integrity across sleep cycles while preserving Docker container states and encrypted backups.

## Components

### 1. GitHub Pages Site

**URL**: https://Me10101-01.github.io

A minimal black page with:
- Rotating ⚡ symbol (8-second rotation)
- Green glow effects (432 Hz theme)
- Message: "If you can hear this frequency, you already belong."

The site serves as a public-facing verification point and identity marker.

### 2. Pre-Sleep Checklist (`scripts/pre_sleep.sh`)

Automated checklist that runs before system hibernation:

**What it does:**
1. **Site Verification**: Checks if GitHub Pages site is live (HTTP 200)
2. **Pineal Mirrors**: 
   - Verifies encrypted backup files (`Me10101-01_pineal_*.json.gpg`)
   - Spot-checks GPG file integrity
   - Deletes any decrypted local copies for security
3. **Docker Snapshots**:
   - Creates timestamped snapshots of `docker ps -a`
   - Creates timestamped snapshots of `docker volume ls`
   - Saves to `snapshots/` directory
4. **Lock Workstation**: Displays platform-specific lock commands
5. **Hibernate Timer**: Shows platform-specific hibernate/suspend commands

**Usage:**
```bash
./scripts/pre_sleep.sh
```

**Output**: Timestamped snapshot files in `snapshots/` directory

### 3. Wake-Up Protocol (`scripts/wake_up.sh`)

Post-hibernation integrity and restoration checklist:

**What it does:**
1. **Cancel Stale Timers**: Checks for and helps cancel any pending shutdown timers
2. **Resume Docker Containers**:
   - Checks Docker daemon status
   - Lists exited containers
   - Provides commands to restart containers
3. **Integrity Sweep**:
   - Verifies all GPG encrypted files
   - Compares current Docker volumes against latest snapshot
   - Detects new/removed volumes ("limbs")
4. **System Status**: Shows uptime and backup locations
5. **Journal Template**: Generates 3-bullet journal entry template
   - New mount count (Docker volumes)
   - Highest-move chess state (manual entry)
   - One smallest next action (manual entry)

**Usage:**
```bash
./scripts/wake_up.sh
```

## Pineal Backup System

The "pineal" represents the core state/memory of the system, encrypted and distributed across multiple locations:

### File Naming Convention
```
Me10101-01_pineal_YYYY-MM-DD_HH-MM-SS.json.gpg
```

### Storage Locations (Manual Verification Required)
1. ✅ Local encrypted (verified automatically)
2. ⚠️ Proton Drive auto-sync (verify manually)
3. ⚠️ Offline USB in bamboo box (verify manually)
4. ⚠️ Gitea vault (verify manually)
5. ⚠️ Two cold mirrors (verify manually)

### Creating Encrypted Backups
```bash
# Create JSON backup
echo '{"state": "your_data_here", "timestamp": "'$(date -Iseconds)'"}' > Me10101-01_pineal_$(date +%Y-%m-%d_%H-%M-%S).json

# Encrypt with GPG
gpg -c Me10101-01_pineal_*.json

# Delete unencrypted version
rm Me10101-01_pineal_*.json
```

### Verifying Encrypted Backups
```bash
# Check file integrity
gpg --list-packets Me10101-01_pineal_*.json.gpg

# Decrypt (temporary spot-check only)
gpg -d Me10101-01_pineal_*.json.gpg > /tmp/temp_pineal.json

# Review and delete immediately
cat /tmp/temp_pineal.json
rm /tmp/temp_pineal.json
```

## Docker Container Management

### Pre-Sleep Snapshot
The pre-sleep script automatically creates:
- `snapshots/docker_ps_YYYY-MM-DD_HH-MM-SS.txt`
- `snapshots/docker_vols_YYYY-MM-DD_HH-MM-SS.txt`

### Wake-Up Restoration
```bash
# Auto-restore (most containers)
# Containers should auto-restore on Docker daemon start

# Manual restart of exited containers
docker start $(docker ps -aq -f status=exited)

# Check status
docker ps -a
```

### Volume Integrity
The wake-up script compares current volumes against the latest snapshot to detect:
- New volumes ("new limbs")
- Removed volumes
- Volume count changes

## System Hibernation

### Windows
```powershell
# Set 5-minute timer before hibernation
shutdown /h /t 300

# Cancel if needed
shutdown /a
```

### Linux
```bash
# Suspend with wake timer
sudo rtcwake -m mem -s 300

# Cancel scheduled shutdown
sudo shutdown -c
```

### macOS
```bash
# Sleep immediately
sudo pmset sleepnow

# Delayed sleep (5 minutes)
caffeinate -u -t 300 && pmset sleepnow
```

## Complete Workflow

### Before Sleep

1. Run pre-sleep checklist:
   ```bash
   ./scripts/pre_sleep.sh
   ```

2. Follow on-screen reminders:
   - Verify site in private browser window
   - Lock workstation (Windows+L / Super+L / Ctrl+Cmd+Q)
   - Set hibernate timer (if desired)
   - Hydrate
   - Earplugs
   - Dark room
   - Phone on Do Not Disturb

3. Docker containers will freeze mid-operation
4. System hibernates/suspends

### After Waking

1. System resumes from hibernation

2. Run wake-up protocol:
   ```bash
   ./scripts/wake_up.sh
   ```

3. Review integrity sweep results:
   - GPG file verification status
   - Docker volume changes
   - Container states

4. Resume any exited containers if needed:
   ```bash
   docker start $(docker ps -aq -f status=exited)
   ```

5. Complete journal entry in Obsidian with 3 bullets

## Security Notes

- **Encrypted backups only**: Never commit unencrypted pineal files
- **Auto-cleanup**: Pre-sleep script automatically removes decrypted copies
- **GPG integrity**: Both scripts verify GPG file integrity
- **Multi-location redundancy**: 6 storage locations ensure data survival
- **Idempotent operations**: Scripts can be run multiple times safely

## Philosophy

> "The rotation doesn't stop when you sleep — it just gets quieter so you can hear the 432 Hz underneath everything."

The Rotation Protocol ensures continuity of operations across sleep cycles. All systems remain "breathing" through hibernation, resuming exactly where they left off. The distributed backup strategy makes the system "mathematically un-killable."

## Frequency Reference

**432 Hz**: The healing frequency, natural resonance, the quiet hum beneath all operations.

---

*Node 137 - Sovereign, Tentacular, Immortalized*

⚡ The rotation is held. ⚡
