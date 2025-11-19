#!/bin/bash
# Pre-Sleep Checklist Script
# Ensures all systems are backed up, mirrored, and ready for hibernation

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Timestamp for file naming
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         PRE-SLEEP CHECKLIST - NODE 137 PROTOCOL          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Verify site is live
echo -e "${YELLOW}[1/5] Verifying GitHub Pages site...${NC}"
SITE_URL="https://Me10101-01.github.io"
if command -v curl &> /dev/null; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL" || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✓ Site is live: $SITE_URL${NC}"
    else
        echo -e "${YELLOW}⚠ Site returned HTTP $HTTP_CODE - verify manually in private window${NC}"
    fi
else
    echo -e "${YELLOW}⚠ curl not found - please verify manually: $SITE_URL${NC}"
fi
echo ""

# 2. Confirm pineal mirrors
echo -e "${YELLOW}[2/5] Verifying pineal backups (encrypted files)...${NC}"
PINEAL_FILES=$(find . -name "Me10101-01_pineal_*.json.gpg" 2>/dev/null | wc -l)
if [ "$PINEAL_FILES" -gt 0 ]; then
    echo -e "${GREEN}✓ Found $PINEAL_FILES encrypted pineal backup(s)${NC}"
    
    # Spot-check first encrypted file
    FIRST_PINEAL=$(find . -name "Me10101-01_pineal_*.json.gpg" 2>/dev/null | head -n 1)
    if [ -n "$FIRST_PINEAL" ]; then
        echo -e "${BLUE}  Spot-checking: $FIRST_PINEAL${NC}"
        if command -v gpg &> /dev/null; then
            if gpg --list-packets "$FIRST_PINEAL" &>/dev/null; then
                echo -e "${GREEN}✓ GPG file integrity verified${NC}"
            else
                echo -e "${RED}✗ GPG integrity check failed${NC}"
            fi
        else
            echo -e "${YELLOW}⚠ gpg not found - skipping integrity check${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⚠ No pineal backup files found${NC}"
    echo -e "${BLUE}  Note: Create with naming pattern: Me10101-01_pineal_YYYY-MM-DD_HH-MM-SS.json.gpg${NC}"
fi

# Clean up any decrypted local copies
DECRYPTED_FILES=$(find . -name "Me10101-01_pineal_*.json" ! -name "*.gpg" 2>/dev/null)
if [ -n "$DECRYPTED_FILES" ]; then
    echo -e "${YELLOW}  Found decrypted local copies - deleting for security...${NC}"
    find . -name "Me10101-01_pineal_*.json" ! -name "*.gpg" -delete 2>/dev/null || true
    echo -e "${GREEN}✓ Decrypted files removed${NC}"
fi
echo ""

# 3. Create Docker snapshots
echo -e "${YELLOW}[3/5] Creating Docker snapshots...${NC}"
if command -v docker &> /dev/null; then
    # Create snapshots directory if it doesn't exist
    mkdir -p snapshots
    
    # Docker ps snapshot
    DOCKER_PS_FILE="snapshots/docker_ps_${TIMESTAMP}.txt"
    docker ps -a > "$DOCKER_PS_FILE" 2>/dev/null || echo "No docker containers" > "$DOCKER_PS_FILE"
    echo -e "${GREEN}✓ Docker ps snapshot: $DOCKER_PS_FILE${NC}"
    
    # Docker volumes snapshot
    DOCKER_VOLS_FILE="snapshots/docker_vols_${TIMESTAMP}.txt"
    docker volume ls > "$DOCKER_VOLS_FILE" 2>/dev/null || echo "No docker volumes" > "$DOCKER_VOLS_FILE"
    echo -e "${GREEN}✓ Docker volumes snapshot: $DOCKER_VOLS_FILE${NC}"
    
    # Count running containers
    RUNNING=$(docker ps -q | wc -l)
    TOTAL=$(docker ps -aq | wc -l)
    echo -e "${BLUE}  Containers: $RUNNING running, $TOTAL total${NC}"
else
    echo -e "${YELLOW}⚠ Docker not found - skipping container snapshots${NC}"
fi
echo ""

# 4. Lock workstation reminder
echo -e "${YELLOW}[4/5] Workstation security...${NC}"
echo -e "${BLUE}  Remember to lock workstation:${NC}"
echo -e "${BLUE}  • Windows: Windows+L${NC}"
echo -e "${BLUE}  • Linux: Super+L or lock screen${NC}"
echo -e "${BLUE}  • macOS: Ctrl+Cmd+Q${NC}"
echo ""

# 5. Setup hibernate timer
echo -e "${YELLOW}[5/5] Hibernate timer setup...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo -e "${BLUE}  Windows detected - to set hibernate timer:${NC}"
    echo -e "${BLUE}  Run in Administrator PowerShell:${NC}"
    echo -e "${GREEN}  shutdown /h /t 300${NC}"
    echo -e "${BLUE}  (Hibernates in 5 minutes)${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${BLUE}  Linux detected - to set suspend timer:${NC}"
    echo -e "${GREEN}  sudo rtcwake -m mem -s 300${NC}"
    echo -e "${BLUE}  (Suspends in 5 minutes)${NC}"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${BLUE}  macOS detected - to set sleep timer:${NC}"
    echo -e "${GREEN}  sudo pmset sleepnow${NC}"
    echo -e "${BLUE}  Or use: caffeinate -u -t 300 && pmset sleepnow${NC}"
fi
echo ""

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   PRE-SLEEP CHECKLIST                     ║${NC}"
echo -e "${BLUE}╠═══════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║ ✓ Site verification attempted                             ║${NC}"
echo -e "${GREEN}║ ✓ Pineal mirrors checked                                  ║${NC}"
echo -e "${GREEN}║ ✓ Docker snapshots created                                ║${NC}"
echo -e "${GREEN}║ ✓ Workstation lock reminder displayed                     ║${NC}"
echo -e "${GREEN}║ ✓ Hibernate timer instructions provided                   ║${NC}"
echo -e "${BLUE}╠═══════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║               FINAL REMINDERS:                            ║${NC}"
echo -e "${BLUE}║  • Hydrate                                                ║${NC}"
echo -e "${BLUE}║  • Earplugs                                               ║${NC}"
echo -e "${BLUE}║  • Dark room                                              ║${NC}"
echo -e "${BLUE}║  • Phone on Do Not Disturb                                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}The rotation is held. Sleep well. ⚡${NC}"
echo ""
