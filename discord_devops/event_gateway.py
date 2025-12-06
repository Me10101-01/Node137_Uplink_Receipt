#!/usr/bin/env python3
"""
Discord DevOps Event Gateway
Routes GitHub webhooks to Discord channels with FlameLang glyph integration.

Generated: 2025-12-06 | Operator: DOM_010101 | EIN: 39-2923503
"""

import hmac
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class WebhookEvent:
    """Represents a GitHub webhook event."""
    event_type: str
    action: str
    repository: str
    sender: str
    payload: dict


@dataclass
class DiscordMessage:
    """Represents a Discord message to be sent."""
    channel: str
    title: str
    description: str
    color: int
    glyph_code: str


class EventGateway:
    """
    Event Gateway for Discord DevOps
    
    Routes GitHub webhook events to Discord channels
    with FlameLang glyph context.
    """
    
    # Event type to channel mapping
    EVENT_CHANNEL_MAP = {
        "pull_request": "#prs",
        "push": "#deployments",
        "workflow_run": "#cluster-status",
        "security_alert": "#alerts",
        "issue_comment": "#dev-feed",
        "issues": "#dev-feed",
    }
    
    # Event type to glyph mapping
    EVENT_GLYPH_MAP = {
        "pull_request": ("RS1", "[200]"),
        "push": ("FL1", "[100]"),
        "workflow_run": ("ND1", "[900]"),
        "security_alert": ("FB1", "[137]"),
        "issue_comment": ("RC3", "[952]"),
        "issues": ("RC3", "[952]"),
    }
    
    # Embed colors
    COLORS = {
        "success": 0x00FF00,  # Green
        "warning": 0xFFFF00,  # Yellow
        "error": 0xFF0000,    # Red
        "info": 0xFF6600,     # Orange (Flame)
    }
    
    def __init__(self, webhook_secret: Optional[str] = None):
        """Initialize the event gateway."""
        self.webhook_secret = webhook_secret or os.environ.get("GITHUB_WEBHOOK_SECRET", "")
        
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify GitHub webhook signature using HMAC.
        
        Args:
            payload: Raw webhook payload bytes
            signature: X-Hub-Signature-256 header value
            
        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            return False
        
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected}", signature)
    
    def parse_event(self, event_type: str, payload: dict) -> WebhookEvent:
        """
        Parse a GitHub webhook event.
        
        Args:
            event_type: The X-GitHub-Event header value
            payload: Parsed JSON payload
            
        Returns:
            WebhookEvent object
        """
        action = payload.get("action", "")
        repository = payload.get("repository", {}).get("full_name", "unknown")
        sender = payload.get("sender", {}).get("login", "unknown")
        
        return WebhookEvent(
            event_type=event_type,
            action=action,
            repository=repository,
            sender=sender,
            payload=payload
        )
    
    def route_event(self, event: WebhookEvent) -> DiscordMessage:
        """
        Route an event to the appropriate Discord channel.
        
        Args:
            event: The parsed webhook event
            
        Returns:
            DiscordMessage to be sent
        """
        channel = self.EVENT_CHANNEL_MAP.get(event.event_type, "#dev-feed")
        glyph_code, binding = self.EVENT_GLYPH_MAP.get(event.event_type, ("RC3", "[952]"))
        
        # Build message based on event type
        if event.event_type == "pull_request":
            title = f"🔀 PR {event.action.title()}: {event.payload.get('pull_request', {}).get('title', 'Unknown')}"
            description = f"Repository: {event.repository}\nBy: {event.sender}"
            color = self.COLORS["info"]
        elif event.event_type == "push":
            title = f"🚀 Push to {event.repository}"
            commits = event.payload.get("commits", [])
            description = f"Commits: {len(commits)}\nBy: {event.sender}"
            color = self.COLORS["success"]
        elif event.event_type == "workflow_run":
            conclusion = event.payload.get("workflow_run", {}).get("conclusion", "unknown")
            title = f"⚙️ Workflow {conclusion.title()}"
            description = f"Repository: {event.repository}"
            color = self.COLORS["success"] if conclusion == "success" else self.COLORS["error"]
        elif event.event_type == "security_alert":
            title = f"🛡️ Security Alert"
            description = f"Repository: {event.repository}\nAction: {event.action}"
            color = self.COLORS["warning"]
        else:
            title = f"📢 {event.event_type.replace('_', ' ').title()}"
            description = f"Repository: {event.repository}\nBy: {event.sender}"
            color = self.COLORS["info"]
        
        return DiscordMessage(
            channel=channel,
            title=title,
            description=description,
            color=color,
            glyph_code=glyph_code
        )
    
    def format_discord_embed(self, message: DiscordMessage) -> dict:
        """
        Format a Discord message as an embed.
        
        Args:
            message: The DiscordMessage to format
            
        Returns:
            Dictionary suitable for Discord webhook
        """
        return {
            "embeds": [{
                "title": message.title,
                "description": message.description,
                "color": message.color,
                "footer": {
                    "text": f"🔥 Glyph: {message.glyph_code} | Strategickhaos Sovereignty"
                }
            }]
        }
    
    def process_webhook(self, event_type: str, payload: dict, signature: str = "") -> dict:
        """
        Process a complete webhook request.
        
        Args:
            event_type: The X-GitHub-Event header
            payload: Parsed JSON payload
            signature: Optional X-Hub-Signature-256 header
            
        Returns:
            Result dictionary with Discord message
        """
        # Parse event
        event = self.parse_event(event_type, payload)
        
        # Route to Discord
        message = self.route_event(event)
        
        # Format as embed
        embed = self.format_discord_embed(message)
        
        return {
            "success": True,
            "channel": message.channel,
            "glyph": message.glyph_code,
            "embed": embed
        }


def main():
    """Demonstrate Event Gateway functionality."""
    gateway = EventGateway()
    
    print("🌐 Discord DevOps - Event Gateway")
    print("=" * 60)
    
    # Simulate webhook events
    test_events = [
        ("pull_request", {"action": "opened", "pull_request": {"title": "Add FlameLang support"}, 
                          "repository": {"full_name": "strategickhaos/sovereignty"}, 
                          "sender": {"login": "dom010101"}}),
        ("push", {"commits": [1, 2, 3], "repository": {"full_name": "strategickhaos/sovereignty"},
                  "sender": {"login": "dom010101"}}),
        ("workflow_run", {"workflow_run": {"conclusion": "success"},
                          "repository": {"full_name": "strategickhaos/sovereignty"},
                          "sender": {"login": "github-actions"}}),
    ]
    
    print("\n📥 Processing Webhook Events:")
    print("-" * 60)
    
    for event_type, payload in test_events:
        result = gateway.process_webhook(event_type, payload)
        print(f"\n  Event: {event_type}")
        print(f"  Channel: {result['channel']}")
        print(f"  Glyph: {result['glyph']}")
        print(f"  Title: {result['embed']['embeds'][0]['title']}")
    
    print("\n✨ Event Gateway processing complete.")


if __name__ == "__main__":
    main()
