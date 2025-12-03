# SovereignGuard v1.0

**Security Subsystem for Strategickhaos Swarm**

Node: 137 | Version: 1.0 | Status: Phase 1 Planned

---

## Overview

SovereignGuard is the security framework for the Strategickhaos empire, providing:

- **Vault Integration** - Central secret store using HashiCorp Vault
- **Policy Management** - Role-based access control for secrets
- **Secure Communication** - PKI and SSH certificate management
- **Audit Logging** - Comprehensive security audit trails

## Directory Structure

```
sovereignguard/
├── README.md           # This file
├── config/
│   └── sovereignguard.yaml    # Framework configuration
├── docs/
│   └── ARCHITECTURE.md        # Security architecture documentation
└── scripts/
    └── phase1-vault-setup.sh  # Vault installation script
```

## Quick Start

### Prerequisites

1. **Kubernetes cluster** with kubectl access
2. **Helm v3** installed
3. **Cluster admin** permissions

### Phase 1: Vault Setup

```bash
# Verify cluster connection
kubectl config current-context
kubectl get nodes

# Review the script (recommended)
less scripts/phase1-vault-setup.sh

# Dry run to see what will happen
./scripts/phase1-vault-setup.sh --dry-run

# Run the setup
./scripts/phase1-vault-setup.sh
```

### Verify Installation

```bash
# Check Vault pods
kubectl get pods -n vault

# Check Vault services
kubectl get svc -n vault

# Test Vault health
kubectl exec -n vault vault-0 -- vault status
```

## Configuration

See `config/sovereignguard.yaml` for full configuration options including:

- Vault server settings
- Secret engine configuration
- Policy definitions
- Monitoring integration
- Backup settings

## Integration Points

### Queen App
- Store GitHub App credentials in Vault
- Retrieve secrets at runtime via Vault API

### Swarm Runners
- Fetch runner tokens from Vault
- Use SSH certificates for secure access

### Workflows
- Health check steps for Vault availability
- Secret injection via Vault CSI provider

## Implementation Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Vault Foundation | Planned |
| 2 | Mesh Security | Future |
| 3 | Enclave Protection | Future |
| 4 | Air-Gap Capabilities | Future |
| 5 | Audit & Compliance | Future |
| 6 | Chaos Engineering | Ongoing |

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Full security architecture
- [Configuration Reference](config/sovereignguard.yaml) - All configuration options

## Security Considerations

- All secrets require authentication
- Least privilege principle enforced
- Token TTL management
- Audit logging enabled by default
- Network policies for pod isolation

## Related Files

- `/config/sovereign_security.yaml` - Empire-level security integration config

---

**Node 137 | Strategickhaos | SovereignGuard v1.0**
