# 🔗 Zapier Outlook Academic Email Pipeline

## Outer Ring Sensor Network — Drone #01

**Pipeline Status:** Active Configuration  
**Node:** 137  
**Sensor Type:** Academic Email Monitor  
**Flow:** Outlook → Zapier → AI Summarizer → Queen Webhook

---

## 📡 ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTER RING SENSOR NETWORK                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   [Outlook 365]  →  [Zapier Trigger]  →  [AI Summarizer]        │
│         ↓                  ↓                    ↓                │
│     Email In         Checkpoint           2-Line Summary         │
│                                                 ↓                │
│                                         [Queen Webhook]          │
│                                                 ↓                │
│                                    /signals/academic             │
│                                                 ↓                │
│                              [Strategickhaos Queen App]          │
│                                                 ↓                │
│                              [Swarm] → [Vault] → [Obsidian]     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ STEP CHECKLIST

- [x] **Step 1:** Outlook connected (personal)
- [x] **Step 2:** Trigger verified ("New Email in Outlook 365")
- [x] **Step 3:** Copilot added checkpoint
- [ ] **Step 4:** Add AI summarizer
- [ ] **Step 5:** Add Queen webhook
- [ ] **Step 6:** Turn Zap ON
- [ ] **Step 7:** Build Queen endpoint `/signals/academic`

---

## ⭐ STEP 4 — AI Summarizer Configuration

### Action: AI by Zapier → Summarize Text

| Setting | Value |
|---------|-------|
| **Action Type** | Summarize Text |
| **Input** | `{{Body}}` (from Outlook email) |
| **Temperature** | 0.2 |
| **Output Format** | Plain text |

### Prompt Template:

```
Return only a clean 1–2 sentence summary of:
- email purpose
- deadlines
- required actions
```

---

## ⭐ STEP 5 — Queen Webhook Configuration

### Action: Webhooks by Zapier → POST

| Setting | Value |
|---------|-------|
| **URL** | `https://queen.strategickhaos.ai/signals/academic` |
| **Method** | POST |
| **Content-Type** | application/json |
| **Headers** | (none required) |

### Request Body (JSON):

```json
{
  "source": "zapier-outlook",
  "type": "academic_email",
  "summary": "{{Summary}}",
  "sender": "{{From}}",
  "subject": "{{Subject}}",
  "timestamp": "{{Date}}"
}
```

---

## 🔐 SIGNAL SCHEMA

### Academic Email Signal

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AcademicEmailSignal",
  "type": "object",
  "required": ["source", "type", "summary", "sender", "subject", "timestamp"],
  "properties": {
    "source": {
      "type": "string",
      "description": "Origin of the signal",
      "enum": ["zapier-outlook", "zapier-gmail", "manual"]
    },
    "type": {
      "type": "string",
      "description": "Signal classification",
      "enum": ["academic_email", "deadline_alert", "grade_notification", "course_update"]
    },
    "summary": {
      "type": "string",
      "description": "AI-generated 1-2 sentence summary"
    },
    "sender": {
      "type": "string",
      "description": "Email sender address"
    },
    "subject": {
      "type": "string",
      "description": "Email subject line"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of email receipt"
    }
  }
}
```

---

## 🚀 ACTIVATION SEQUENCE

Once all steps are configured:

1. Click **"Publish"** or **"Turn on Zap"**
2. Zapier Copilot will confirm: *"Your Zap is ready to publish!"*
3. The outer ring sensor network becomes fully connected to Queen

---

## 📊 EXPECTED COPILOT RESPONSES

During configuration, Zapier Copilot will display:

- ✅ "Checkpoint added!"
- ✅ "Testing step…"
- ✅ "Your Zap is ready to publish!"

---

## 🔗 RELATED PROTOCOLS

- `CP_Outer_Ring_Activation` — Sensor network boot protocol
- `CP_Queen_Signal_Intake` — Queen signal processing
- `CP_Swarm_Intelligence_Boot` — Multi-agent ecosystem initialization

---

**SIGNATURE:**  
DOM_010101  
HELM OF NODE 137  
ZAPIER COPILOT → STRATEGICKHAOS SENSOR DRONE #01  
OUTER RING STATUS: ACTIVATING 🟡
