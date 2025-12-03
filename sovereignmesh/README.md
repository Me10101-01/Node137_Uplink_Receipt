# SovereignMesh

## GitHub Codespaces as Free Kubernetes Alternative

SovereignMesh is an architecture that leverages GitHub Codespaces as sovereign compute nodes, providing Kubernetes-like orchestration at $0/month within free tier limits.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SOVEREIGNMESH CLUSTER                                │
│                   (GitHub Codespaces as Compute Nodes)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  EXTERNAL SIGNALS                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  Zapier  │  │  SNHU    │  │  Thread  │  │ Discord  │                   │
│  │  Zaps    │  │  Email   │  │  Bank    │  │ Webhooks │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       │             │             │             │                          │
│       └─────────────┴──────┬──────┴─────────────┘                          │
│                            ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  CODESPACE 1: QUEEN (Orchestrator)                                  │  │
│  │  ├── queen.js (signal router)                                       │  │
│  │  ├── /signals/academic → routes to Knowledge Node                   │  │
│  │  ├── /signals/financial → routes to SwarmGate                       │  │
│  │  ├── /signals/security → routes to SovereignGuard                   │  │
│  │  └── Port 3000 → https://queen-abc123.github.dev                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                            │                                               │
│       ┌────────────────────┼────────────────────┐                         │
│       ▼                    ▼                    ▼                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                   │
│  │ CODESPACE 2 │    │ CODESPACE 3 │    │ CODESPACE 4 │                   │
│  │ SwarmGate   │    │ Knowledge   │    │ Dashboard   │                   │
│  │ (Financial) │    │ (Academic)  │    │ (Interface) │                   │
│  │ Port 3001   │    │ Port 3002   │    │ Port 3003   │                   │
│  └─────────────┘    └─────────────┘    └─────────────┘                   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  CODESPACE 5: AI COUNCIL (Legion of Minds)                          │  │
│  │  Claude │ GPT │ Grok │ Local Proxy │ Consensus Engine               │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  LOCAL NODES: Nova (Ollama) │ Lyra (Ollama) │ Athena (K8s) │ iPower      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Codespaces ↔ Kubernetes Mapping

| Codespaces Feature    | K8s Equivalent       |
|-----------------------|----------------------|
| Public HTTPS URL      | Ingress/LoadBalancer |
| Port forwarding       | NodePort/Service     |
| Persistent filesystem | PersistentVolume     |
| Container tooling     | Pod runtime          |
| GitHub auth           | ServiceAccount       |
| Isolated environment  | Namespace            |

## Quick Start

### 1. Install Dependencies

```bash
cd sovereignmesh
npm install
```

### 2. Configure Environment

Create a `.env` file:

```env
# GitHub App Configuration
GITHUB_APP_ID=1884781
GITHUB_CLIENT_ID=Iv23liTGwnOOha2UYNuf
GITHUB_PRIVATE_KEY_PATH=./github-app.pem
GITHUB_WEBHOOK_SECRET=your-webhook-secret

# Queen Node Configuration
QUEEN_PORT=3000
NODE_ENV=development

# Optional: Mesh Node URLs (Codespace URLs)
QUEEN_URL=https://your-queen-codespace.github.dev
SWARMGATE_URL=https://your-swarmgate-codespace.github.dev
KNOWLEDGE_URL=https://your-knowledge-codespace.github.dev
DASHBOARD_URL=https://your-dashboard-codespace.github.dev

# Optional: API Keys
ZAPIER_WEBHOOK_TOKEN=your-zapier-token
SOVEREIGN_API_KEY=your-api-key
```

### 3. Start Queen Node

```bash
npm start
```

### 4. Configure GitHub App Webhook

Set your GitHub App webhook URL to:
```
https://[YOUR-QUEEN-CODESPACE].github.dev/webhooks/github
```

## API Endpoints

### Signals

| Endpoint                 | Method | Description                          |
|--------------------------|--------|--------------------------------------|
| `/signals/academic`      | POST   | Route to Knowledge Node              |
| `/signals/financial`     | POST   | Route to SwarmGate                   |
| `/signals/security`      | POST   | Route to SovereignGuard              |
| `/signals/intelligence`  | POST   | Route to AI Council                  |
| `/signals/broadcast`     | POST   | Broadcast to all nodes               |
| `/signals/routes`        | GET    | List available routes                |

### Webhooks

| Endpoint                 | Method | Description                          |
|--------------------------|--------|--------------------------------------|
| `/webhooks/github`       | POST   | GitHub App webhooks                  |
| `/webhooks/zapier`       | POST   | Zapier automation signals            |
| `/webhooks/discord`      | POST   | Discord bot webhooks                 |
| `/webhooks/snhu`         | POST   | SNHU email notifications             |
| `/webhooks/thread`       | POST   | Thread Bank notifications            |
| `/webhooks/status`       | GET    | Webhook endpoints status             |

### Health

| Endpoint                 | Method | Description                          |
|--------------------------|--------|--------------------------------------|
| `/health`                | GET    | Basic health check                   |
| `/health/detailed`       | GET    | Detailed system information          |
| `/health/nodes`          | GET    | Status of all mesh nodes             |
| `/health/ready`          | GET    | Kubernetes readiness probe           |
| `/health/live`           | GET    | Kubernetes liveness probe            |

## Signal Routing

Signals are automatically classified and routed based on type:

| Signal Type    | Target Node      | Priority  | Sources                    |
|----------------|------------------|-----------|----------------------------|
| `academic`     | Knowledge Node   | Normal    | SNHU, Obsidian, Research   |
| `financial`    | SwarmGate        | High      | Thread Bank, Trading       |
| `security`     | SovereignGuard   | Critical  | Audit, Alerts, Breaches    |
| `intelligence` | AI Council       | Normal    | Queries, Consensus         |

## GitHub App Integration

### Required Permissions

Configure your GitHub App (ID: `1884781`) with these permissions:

- **Repository**: Contents (Read), Issues (Read/Write), Pull Requests (Read/Write)
- **Organization**: Members (Read)
- **Account**: Email (Read)

### Webhook Events

Subscribe to these events:
- Push, Pull Request, Issues, Security Advisory, Code Scanning Alert

## Audit Trail

All operations are logged to:
- `logs/audit.log` - General audit trail
- `logs/signals.log` - Signal routing events
- `logs/access.log` - HTTP access logs

## Owner

**Node 137 - Strategickhaos**

Part of the SovereignGuard security model and Estrategi-Khaos ecosystem.
