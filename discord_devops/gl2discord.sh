#!/bin/bash
# GitLens to Discord Integration
# Routes GitLens PR events to Discord channels
# Generated: 2025-12-06 | Operator: DOM_010101

# Usage: ./gl2discord.sh <channel_id> <title> <message>

CHANNEL_ID="$1"
TITLE="$2"
MESSAGE="$3"

if [ -z "$CHANNEL_ID" ] || [ -z "$TITLE" ]; then
    echo "Usage: ./gl2discord.sh <channel_id> <title> [message]"
    exit 1
fi

if [ -z "$DISCORD_WEBHOOK_URL" ]; then
    echo "⚠️  DISCORD_WEBHOOK_URL not set"
    echo "   Set with: export DISCORD_WEBHOOK_URL='your_webhook_url'"
    exit 1
fi

# Build JSON payload
PAYLOAD=$(cat <<EOF
{
    "embeds": [{
        "title": "$TITLE",
        "description": "$MESSAGE",
        "color": 16744448,
        "footer": {
            "text": "🔥 Strategickhaos Sovereignty"
        },
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    }]
}
EOF
)

# Send to Discord webhook
echo "📤 Sending to Discord channel: $CHANNEL_ID"
echo "   Title: $TITLE"

# NOTE: The curl command is commented out for safety during development/testing.
# To enable actual Discord integration:
# 1. Set DISCORD_WEBHOOK_URL environment variable
# 2. Uncomment the curl line below
# 3. Ensure webhook URL has proper channel permissions
#
# curl -H "Content-Type: application/json" -d "$PAYLOAD" "$DISCORD_WEBHOOK_URL"

echo "✅ Message prepared (dry-run mode - uncomment curl to send)"
