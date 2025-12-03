# SovereignGuard Security Architecture
## Version 1.0 | Node 137 | Strategickhaos Swarm Security Subsystem

---

## Overview

SovereignGuard is the security subsystem of the Strategickhaos Swarm, providing a comprehensive framework for secrets management, identity verification, and secure communication across the empire infrastructure.

The architecture is designed to integrate with:
- **GitHub Enterprise** + Queen App + self-hosted runners
- **Podman** sovereign stack (registry, cAdvisor, monitoring)
- **Swarm-core** repository + Sovereignty-Architecture-Elevator-Pitch
- Real legal entities + empire YAML configurations

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        STRATEGICKHAOS EMPIRE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐         ┌──────────────────────────────────────┐  │
│  │  GitHub Enterprise│         │           HashiCorp Vault            │  │
│  │    + Queen App    │────────▶│   (Central Secret Store)             │  │
│  │                   │         │                                      │  │
│  │   - App ID        │         │  KV Secrets Engine                   │  │
│  │   - Private Key   │◀────────│  ├── kv/queen-app/config             │  │
│  │   - Webhook Secret│         │  │   ├── github_app_private_key      │  │
│  │   - OAuth Client  │         │  │   ├── github_webhook_secret       │  │
│  │                   │         │  │   └── github_client_secret        │  │
│  └──────────────────┘         │  ├── kv/swarm-runners/                │  │
│           │                    │  │   └── runner_tokens               │  │
│           │                    │  └── kv/registry/                    │  │
│           ▼                    │      └── credentials                 │  │
│  ┌──────────────────┐         │                                      │  │
│  │  Swarm Runners    │         │  SSH Secrets Engine                  │  │
│  │  (swarm-node-01)  │────────▶│  └── Signed SSH Certificates         │  │
│  │                   │         │                                      │  │
│  └──────────────────┘         │  PKI Secrets Engine                  │  │
│           │                    │  └── TLS Certificates                │  │
│           │                    │                                      │  │
│           ▼                    │  Database Secrets Engine             │  │
│  ┌──────────────────┐         │  └── Dynamic DB Credentials          │  │
│  │  Podman Stack     │         └──────────────────────────────────────┘  │
│  │  - Registry       │                         │                         │
│  │  - cAdvisor       │                         │                         │
│  │  - Monitoring     │◀────────────────────────┘                         │
│  └──────────────────┘                                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Vault Foundation (Immediate)
**Status:** Planned  
**Target:** Primary Swarm GKE Autopilot Cluster

1. **Vault Installation**
   - Deploy via Helm chart to `vault` namespace
   - Configure HA mode with integrated storage
   - Set up audit logging

2. **Secret Engines Configuration**
   - KV v2 (key-value secrets)
   - SSH (signed certificates)
   - PKI (TLS certificates)
   - Database (dynamic credentials)

3. **Initial Policies**
   - Queen App read access to designated paths
   - Swarm runner limited access
   - Admin policies for management

### Phase 2: Mesh Security (Month 2-3)
- Service mesh integration
- mTLS between services
- Zero-trust networking

### Phase 3: Enclave Protection (Month 4-6)
- Secure enclaves for sensitive operations
- Hardware security module (HSM) integration
- Key ceremony procedures

### Phase 4: Air-Gap Capabilities (Month 7-9)
- Offline operation modes
- Air-gapped secret distribution
- Disaster recovery procedures

### Phase 5: Audit & Compliance (Month 10-12)
- Comprehensive audit trails
- Compliance reporting
- Security attestations

### Phase 6: Chaos Engineering (Ongoing)
- Security chaos testing
- Incident response drills
- Continuous hardening

---

## Kubernetes Integration

### Target Cluster
- **Type:** GKE Autopilot
- **Context:** `primary_swarm_gke_autopilot`
- **Vault Namespace:** `vault`

### Namespace Configuration
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: vault
  labels:
    app.kubernetes.io/name: vault
    app.kubernetes.io/part-of: sovereignguard
```

### Service Endpoints
- **Vault API:** `https://vault.vault.svc.cluster.local:8200`
- **External:** `https://vault.strategickhaos.ai` (when configured)

---

## Secret Paths

### Queen App Secrets
```
kv/queen-app/config/
├── github_app_id
├── github_app_private_key
├── github_webhook_secret
├── github_client_id
└── github_client_secret
```

### Swarm Runner Secrets
```
kv/swarm-runners/
├── runner_registration_token
├── runner_auth_token
└── runner_labels
```

### Registry Credentials
```
kv/registry/
├── username
├── password
└── server
```

---

## Vault Policies

### Queen App Policy
```hcl
# queen-app-policy.hcl
path "kv/data/queen-app/*" {
  capabilities = ["read", "list"]
}

path "kv/metadata/queen-app/*" {
  capabilities = ["read", "list"]
}
```

### Swarm Runner Policy
```hcl
# swarm-runner-policy.hcl
path "kv/data/swarm-runners/*" {
  capabilities = ["read"]
}

path "ssh/sign/runner-role" {
  capabilities = ["create", "update"]
}
```

---

## Health Checks

### Vault Health Endpoint
```bash
curl -s http://vault.vault.svc:8200/v1/sys/health
```

### Workflow Integration
```yaml
- name: Check Vault health
  run: |
    curl -s http://vault.vault.svc:8200/v1/sys/health || echo "Vault not reachable"
```

---

## Security Considerations

1. **Access Control**
   - All secrets require authentication
   - Least privilege principle enforced
   - Token TTL management

2. **Encryption**
   - Transit encryption for data in motion
   - Seal/unseal with shamir keys or auto-unseal
   - Audit log encryption

3. **Compliance**
   - GDPR considerations
   - SOC2 alignment
   - Security attestations

---

## Prerequisites

Before running Phase 1 setup:

1. **Cluster Access**
   ```bash
   kubectl config current-context
   kubectl get nodes
   ```

2. **Helm Installed**
   ```bash
   helm version
   ```

3. **Network Access**
   - Port 8200 (Vault API)
   - Port 8201 (Vault cluster)

---

## References

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [Vault Helm Chart](https://github.com/hashicorp/vault-helm)
- [Kubernetes Auth Method](https://www.vaultproject.io/docs/auth/kubernetes)

---

**Node 137 | Strategickhaos | SovereignGuard v1.0**
