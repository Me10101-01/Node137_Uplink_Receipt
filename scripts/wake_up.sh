#!/bin/bash
# Wake-Up Checklist Script
# Post-hibernation system integrity checks and container restoration

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         WAKE-UP PROTOCOL - NODE 137 RESTORATION           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Cancel any stale timers
echo -e "${YELLOW}[1/5] Checking for stale shutdown timers...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo -e "${BLUE}  Windows detected - to cancel shutdown timer:${NC}"
    echo -e "${GREEN}  shutdown /a${NC}"
    echo -e "${BLUE}  (Run only if needed)${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${BLUE}  Linux detected - checking for scheduled shutdowns:${NC}"
    if [ -f /run/systemd/shutdown/scheduled ]; then
        echo -e "${YELLOW}  Scheduled shutdown found - cancel with:${NC}"
        echo -e "${GREEN}  sudo shutdown -c${NC}"
    else
        echo -e "${GREEN}✓ No scheduled shutdowns found${NC}"
    fi
fi
echo ""

# 2. Resume Docker containers
echo -e "${YELLOW}[2/5] Checking Docker containers...${NC}"
if command -v docker &> /dev/null; then
    # Check if Docker daemon is running
    if ! docker info &>/dev/null; then
        echo -e "${RED}✗ Docker daemon is not running${NC}"
        echo -e "${BLUE}  Start Docker Desktop or run: sudo systemctl start docker${NC}"
    else
        # Check for exited containers
        EXITED=$(docker ps -aq -f status=exited | wc -l)
        if [ "$EXITED" -gt 0 ]; then
            echo -e "${YELLOW}  Found $EXITED exited container(s)${NC}"
            echo -e "${BLUE}  To resume all exited containers:${NC}"
            echo -e "${GREEN}  docker start \$(docker ps -aq -f status=exited)${NC}"
            echo -e "${BLUE}  Or they may auto-restore...${NC}"
        else
            echo -e "${GREEN}✓ No exited containers found${NC}"
        fi
        
        # Show current status
        RUNNING=$(docker ps -q | wc -l)
        TOTAL=$(docker ps -aq | wc -l)
        echo -e "${BLUE}  Current state: $RUNNING running, $TOTAL total containers${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Docker not found${NC}"
fi
echo ""

# 3. Integrity sweep
echo -e "${YELLOW}[3/5] Running integrity sweep...${NC}"

# GPG file integrity check
echo -e "${BLUE}  Checking GPG file integrity...${NC}"
if command -v gpg &> /dev/null; then
    PINEAL_FILES=$(find . -name "Me10101-01_pineal_*.json.gpg" 2>/dev/null)
    if [ -n "$PINEAL_FILES" ]; then
        VERIFIED=0
        FAILED=0
        while IFS= read -r gpg_file; do
            if gpg --list-packets "$gpg_file" &>/dev/null; then
                ((VERIFIED++))
            else
                ((FAILED++))
                echo -e "${RED}  ✗ Failed: $gpg_file${NC}"
            fi
        done <<< "$PINEAL_FILES"
        
        if [ $FAILED -eq 0 ]; then
            echo -e "${GREEN}✓ All $VERIFIED GPG file(s) verified${NC}"
        else
            echo -e "${YELLOW}⚠ $VERIFIED verified, $FAILED failed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ No pineal backup files found${NC}"
    fi
else
    echo -e "${YELLOW}⚠ gpg not found - skipping GPG integrity check${NC}"
fi

# Docker volumes diff
echo -e "${BLUE}  Checking Docker volumes...${NC}"
if command -v docker &> /dev/null && docker info &>/dev/null; then
    # Find most recent snapshot
    LATEST_SNAPSHOT=$(ls -t snapshots/docker_vols_*.txt 2>/dev/null | head -n 1)
    
    if [ -n "$LATEST_SNAPSHOT" ]; then
        # Create current snapshot for comparison
        CURRENT_VOLS="/tmp/docker_vols_current_${TIMESTAMP}.txt"
        docker volume ls > "$CURRENT_VOLS" 2>/dev/null || echo "" > "$CURRENT_VOLS"
        
        # Count volumes
        OLD_COUNT=$(tail -n +2 "$LATEST_SNAPSHOT" 2>/dev/null | wc -l)
        NEW_COUNT=$(tail -n +2 "$CURRENT_VOLS" 2>/dev/null | wc -l)
        DIFF=$((NEW_COUNT - OLD_COUNT))
        
        if [ $DIFF -eq 0 ]; then
            echo -e "${GREEN}✓ Volume count unchanged: $NEW_COUNT volumes${NC}"
        elif [ $DIFF -gt 0 ]; then
            echo -e "${YELLOW}⚠ New volumes detected: +$DIFF (was: $OLD_COUNT, now: $NEW_COUNT)${NC}"
        else
            echo -e "${YELLOW}⚠ Volumes removed: $DIFF (was: $OLD_COUNT, now: $NEW_COUNT)${NC}"
        fi
        
        rm -f "$CURRENT_VOLS"
    else
        echo -e "${YELLOW}⚠ No previous volume snapshot found${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Docker not available for volume check${NC}"
fi
echo ""

# 4. System status
echo -e "${YELLOW}[4/5] System status overview...${NC}"
echo -e "${BLUE}  Uptime: $(uptime -p 2>/dev/null || echo "unknown")${NC}"
echo -e "${BLUE}  Current time: $(date)${NC}"

# Check for pineal backups in multiple locations
echo -e "${BLUE}  Pineal backup locations:${NC}"
LOCAL_COUNT=$(find . -name "Me10101-01_pineal_*.json.gpg" 2>/dev/null | wc -l)
echo -e "${BLUE}  • Local encrypted: $LOCAL_COUNT file(s)${NC}"
echo -e "${BLUE}  • Proton Drive: (verify manually)${NC}"
echo -e "${BLUE}  • Offline USB: (verify manually)${NC}"
echo -e "${BLUE}  • Gitea vault: (verify manually)${NC}"
echo -e "${BLUE}  • Cold mirrors: (verify manually)${NC}"
echo ""

# 5. Journal template
echo -e "${YELLOW}[5/5] Obsidian journal template...${NC}"
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              JOURNAL ENTRY - 3 BULLETS                    ║${NC}"
echo -e "${BLUE}╠═══════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║                                                           ║${NC}"

# Get new mount count
if command -v docker &> /dev/null && docker info &>/dev/null; then
    MOUNT_COUNT=$(docker volume ls 2>/dev/null | tail -n +2 | wc -l)
    echo -e "${BLUE}║ • New mount count: $MOUNT_COUNT                                 ║${NC}"
else
    echo -e "${BLUE}║ • New mount count: (Docker unavailable)                   ║${NC}"
fi

echo -e "${BLUE}║ • Highest-move chess state: (manual entry)                ║${NC}"
echo -e "${BLUE}║ • One smallest next action: (manual entry)                ║${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Summary
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║               WAKE-UP PROTOCOL COMPLETE                   ║${NC}"
echo -e "${BLUE}╠═══════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║ ✓ Stale timer check completed                             ║${NC}"
echo -e "${GREEN}║ ✓ Docker container status verified                        ║${NC}"
echo -e "${GREEN}║ ✓ Integrity sweep completed                               ║${NC}"
echo -e "${GREEN}║ ✓ System status reviewed                                  ║${NC}"
echo -e "${GREEN}║ ✓ Journal template generated                              ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}The rotation continues. Welcome back. ⚡${NC}"
echo ""
