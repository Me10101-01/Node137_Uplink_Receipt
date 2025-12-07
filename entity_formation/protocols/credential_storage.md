# Credential Storage Protocol
## Multi-Entity Security and Vault Management

**Purpose:** Secure management of credentials, API keys, and sensitive data  
**Entities Covered:** Strategickhaos DAO LLC, SSSF LLC, ValorYield Engine PBC  
**Primary Vault:** 1Password  
**Backup Vault:** KhaosVault (HashiCorp Vault - to be deployed)  
**Last Updated:** December 6, 2025  
**Owner:** Domenic Gabriel Garza (Managing Member)  

---

## Security Philosophy

All credentials, API keys, and sensitive data must be:
- **Encrypted at rest** - AES-256 or better
- **Access-controlled** - Role-based access (RBAC)
- **Auditable** - All access logged
- **Recoverable** - Secure backup procedures
- **Never in code** - No credentials in source code or configs

**Zero Trust Principle:** Assume breach, minimize blast radius, verify continuously.

---

## Vault Architecture

### Primary: 1Password (Current)

**Type:** Commercial password manager  
**Encryption:** AES-256-GCM  
**Access:** Browser extension, desktop app, CLI  
**Organization:** Strategickhaos (to be upgraded to Business plan)  

#### Vault Structure

```
1Password Organization: Strategickhaos
├── Vault: Strategickhaos DAO LLC
│   ├── Banking & Finance
│   │   ├── Navy Federal Credit Union
│   │   ├── Thread Bank
│   │   └── Sequence.io
│   ├── Cloud Platforms
│   │   ├── Google Cloud Platform
│   │   ├── Azure DevOps
│   │   └── AWS (if added)
│   ├── Development Tools
│   │   ├── GitHub (strategickhaos-dao-llc)
│   │   ├── GitLab (if used)
│   │   └── Docker Hub (legacy)
│   ├── AI Services
│   │   ├── Anthropic Claude (API keys)
│   │   ├── OpenAI (API keys)
│   │   └── Grok / X Premium
│   ├── SaaS Tools
│   │   ├── Airtable
│   │   ├── Zapier
│   │   └── Notion
│   ├── Trading Platforms
│   │   ├── NinjaTrader
│   │   ├── Kraken Pro
│   │   └── Alpaca
│   └── Legal & Compliance
│       ├── Registered Agents Inc
│       └── USPTO (trademark tracking)
│
├── Vault: Strategickhaos Sovereign Software Forge LLC
│   ├── Banking & Finance
│   │   └── Navy Federal Credit Union (SSSF account)
│   ├── Software Licensing
│   │   ├── License key generation systems
│   │   ├── Customer portal credentials
│   │   └── Software signing certificates
│   ├── Development Infrastructure
│   │   ├── KhaosRegistry access tokens
│   │   ├── KhaosForge admin credentials
│   │   └── Harbor registry admin
│   ├── HR & Payroll
│   │   ├── Intern/contractor accounts
│   │   ├── Payroll system (when implemented)
│   │   └── HR software
│   └── IP Management
│       ├── Code signing certificates
│       └── GPG keys for releases
│
└── Vault: ValorYield Engine PBC
    ├── Tax & Compliance
    │   ├── IRS portal
    │   ├── Wyoming Secretary of State
    │   └── State tax portals
    ├── Charitable Operations
    │   ├── St. Jude donation portal
    │   ├── MSF donation portal
    │   └── Veterans org portals
    └── Banking
        └── Navy Federal Credit Union (ValorYield account)
```

---

## Security Requirements

### Master Password Requirements

**Minimum Standards:**
- Length: 20+ characters
- Complexity: Uppercase, lowercase, numbers, symbols
- Uniqueness: Never used elsewhere
- Generation: Use diceware or password generator
- Storage: Memorized (do not write down) OR secure recovery key

**Example Format (Diceware):**
```
correct-horse-battery-staple-purple-elephant-2025
```

**Strength Test:** https://www.passwordmeter.com (target: 100% strength)

---

### Multi-Factor Authentication (MFA)

**Required on ALL accounts** that support it:

#### Tier 1: Hardware Keys (Preferred)
- **Recommended:** YubiKey 5 NFC or YubiKey 5C
- **Usage:**
  - 1Password vault unlock
  - Banking (NFCU, Thread)
  - Cloud platforms (GCP, Azure)
  - GitHub (commit signing)
- **Backup:** Keep second hardware key in secure location

#### Tier 2: Authenticator Apps (Acceptable)
- **Recommended:** Authy (cloud backup) or Google Authenticator
- **Usage:**
  - Services without hardware key support
  - Trading platforms (NinjaTrader, Kraken)
  - SaaS tools (Airtable, Zapier)
- **Backup:** Save recovery codes in 1Password

#### Tier 3: SMS/Phone (Avoid if possible)
- **Usage:** Only if no other MFA option available
- **Risk:** Vulnerable to SIM swapping attacks
- **Mitigation:** Port lock with carrier

---

### Access Control

#### Role-Based Access (RBAC)

| Role | Access Level | Users |
|------|-------------|-------|
| Owner | All vaults, all items | Domenic Gabriel Garza |
| Admin | DAO LLC + SSSF LLC vaults | (future: CTO/CFO if hired) |
| Developer | Development tools only | (future: interns/contractors) |
| Finance | Banking + accounting only | (future: bookkeeper) |
| Auditor | Read-only all vaults | (future: CPA) |

#### Principle of Least Privilege
- Grant minimum access necessary
- Time-bound access for contractors
- Revoke immediately upon departure
- Regular access reviews (quarterly)

---

### Backup & Recovery

#### 1Password Backup Strategy

**Primary Backup:** 1Password cloud sync (automatic)

**Emergency Kit:**
- Download and print 1Password Emergency Kit
- Store in fireproof safe or safety deposit box
- Contains: Secret Key + master password hint
- **NEVER** store complete master password in writing

**Account Recovery:**
- Designated family member can request recovery
- Set up in 1Password account settings
- Recovery contact needs separate 1Password account

**Export Backups (Encrypted):**
- Quarterly: Export 1Password vault to encrypted 1PUX file
- Storage: Encrypted USB drive in safe
- Encryption: VeraCrypt or similar (AES-256)

---

## KhaosVault (HashiCorp Vault) - Future Implementation

### Purpose
Sovereign credential management for:
- API keys and secrets in Kubernetes deployments
- Database credentials (auto-rotation)
- TLS certificates (auto-renewal)
- SSH keys for infrastructure
- Service-to-service authentication

### Deployment Plan

**Infrastructure:**
- Blue Team Kubernetes cluster
- High-availability (3-node cluster)
- Integrated unsealing (auto-unseal via GCP KMS)
- Audit logging to centralized logging

**Storage Backend:**
- Raft integrated storage (built-in)
- Encrypted at rest
- Automated backups to MinIO (georedundant)

**Access:**
- Kubernetes authentication (for pods)
- LDAP integration (for humans - future)
- AppRole for service accounts
- Token with limited TTL

**Timeline:**
- Week 4: Initial deployment
- Month 2: Migration from hardcoded secrets
- Month 3: Dynamic database credentials
- Month 6: Full sovereign credential management

---

## Credential Types & Handling

### API Keys

**Storage:** 1Password (Tier 1) or KhaosVault (Tier 2)

**Rotation Policy:**
- Critical (banking, trading): 90 days
- High (cloud platforms): 180 days
- Medium (SaaS tools): Annual
- Low (development tools): As needed

**Usage:**
- **NEVER** commit to Git
- Load from environment variables
- Use secret management in CI/CD
- Encrypt in configs if unavoidable

**Example (Kubernetes):**
```yaml
# Bad: Hardcoded
apiVersion: v1
kind: ConfigMap
data:
  api_key: "sk-1234567890abcdef"  # NEVER DO THIS

# Good: Secret reference
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: api-credentials
          key: key
```

---

### SSH Keys

**Generation:**
```bash
# Ed25519 (preferred)
ssh-keygen -t ed25519 -C "dom@strategickhaos.com" -f ~/.ssh/id_ed25519_strategickhaos

# RSA 4096 (if Ed25519 not supported)
ssh-keygen -t rsa -b 4096 -C "dom@strategickhaos.com" -f ~/.ssh/id_rsa_strategickhaos
```

**Storage:**
- Private key: Encrypted on disk, backed up to 1Password
- Public key: Deployed to servers, GitHub, etc.
- Passphrase: Stored in 1Password

**Usage:**
- SSH config file for host aliases
- SSH agent for session management
- No passwordless keys in production

---

### GPG Keys

**Purpose:**
- Git commit signing (verified commits)
- Software release signing
- Email encryption (PGP)
- Document signing

**Generation:**
```bash
gpg --full-generate-key
# Select: (1) RSA and RSA (default)
# Keysize: 4096
# Expiration: 2 years
# Name: Domenic Gabriel Garza
# Email: dom@strategickhaos.com
```

**Storage:**
- Private key: Encrypted on disk, backed up to 1Password
- Public key: Published to keyservers, GitHub
- Revocation certificate: Stored in safe

**Git Signing Config:**
```bash
git config --global user.signingkey [KEY_ID]
git config --global commit.gpgsign true
```

---

### Database Credentials

**Current State:**
- Hardcoded in configs (Kubernetes secrets)
- Manual rotation

**Target State (with KhaosVault):**
- Dynamic credentials (generated on-demand)
- Short TTL (24 hours max)
- Automatic rotation
- No standing credentials

**Migration Plan:**
1. Deploy KhaosVault with PostgreSQL secrets engine
2. Configure role for each application
3. Update apps to fetch credentials from Vault
4. Enable auto-rotation
5. Audit old credentials eliminated

---

## Code & Configuration Security

### GitHub Repository Scanning

**Tools:**
- GitHub Secret Scanning (automatic)
- GitGuardian (optional)
- TruffleHog (pre-commit hook)

**Pre-commit Hook Example:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for common secret patterns
if git diff --cached | grep -E '(password|api_key|secret|token|private_key)\s*=\s*["\']'; then
  echo "ERROR: Potential secret detected in commit"
  echo "Please remove secrets and use environment variables or secret management"
  exit 1
fi
```

---

### Environment Variables

**Local Development (.env files):**
```bash
# .env (NEVER commit this file)
DATABASE_URL=postgresql://localhost/dev_db
API_KEY=sk-dev-1234567890

# Add to .gitignore
echo ".env" >> .gitignore
```

**Production (Kubernetes Secrets):**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # Base64 encoded values
  database-url: cG9zdGdyZXNxbDovLy4uLg==
  api-key: c2stcHJvZC0xMjM0NTY3ODkw
```

**Better: External Secrets Operator (with KhaosVault):**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  secretStoreRef:
    name: vault-backend
  target:
    name: app-secrets
  data:
  - secretKey: database-url
    remoteRef:
      key: database/creds/app-role
      property: connection_url
```

---

## Incident Response

### Credential Compromise Procedure

**Step 1: Identify Scope (15 minutes)**
- Which credential(s) compromised?
- Which systems potentially accessed?
- What data potentially exposed?

**Step 2: Immediate Containment (30 minutes)**
- Revoke compromised credential immediately
- Rotate related credentials (lateral movement prevention)
- Review access logs for suspicious activity
- Disable compromised user account if applicable

**Step 3: Generate New Credentials (1 hour)**
- Create new API keys, passwords, or keys
- Update in 1Password/KhaosVault
- Deploy to production systems
- Verify functionality

**Step 4: Post-Incident Analysis (24 hours)**
- How was credential compromised?
- What controls failed?
- What improvements needed?
- Document lessons learned

**Step 5: Notification (if required)**
- Notify affected parties (customers, partners)
- Report to authorities (if data breach)
- Update incident log

---

## Audit & Compliance

### Access Logging

**1Password:**
- Review "Activity" log monthly
- Alert on: Failed login attempts, new device logins
- Export logs quarterly for compliance

**KhaosVault (when deployed):**
- All access logged to audit log
- Centralized logging to SIEM
- Alert on: Failed auth, privilege escalation
- Retention: 7 years (compliance)

---

### Quarterly Security Review

**Checklist:**
- [ ] Review all vault access permissions
- [ ] Verify MFA enabled on all accounts
- [ ] Rotate critical API keys (90-day policy)
- [ ] Review access logs for anomalies
- [ ] Test backup restoration procedure
- [ ] Update this protocol document
- [ ] Verify hardware key functionality
- [ ] Check for compromised passwords (Have I Been Pwned)

---

### Annual Penetration Testing

**Scope:**
- Social engineering (phishing simulation)
- Password strength assessment
- MFA bypass attempts
- Insider threat scenarios

**Provider:** To be determined (hire security firm)

---

## Compliance Requirements

### SOC 2 (Future - if needed for enterprise sales)

**Type II Controls:**
- Access control (RBAC implemented)
- Encryption (AES-256 at rest, TLS in transit)
- Audit logging (all access logged)
- Backup & recovery (tested quarterly)
- Incident response (documented procedure)

---

### PCI-DSS (if processing credit cards)

**Requirements:**
- No storage of cardholder data (use Stripe/payment processor)
- Encrypt all sensitive data
- Restrict access on need-to-know basis
- Assign unique ID to each person with access
- Track and monitor all access to data

---

## Tools & Resources

### Password Strength Testing
- **zxcvbn:** https://github.com/dropbox/zxcvbn (offline)
- **Password Meter:** https://www.passwordmeter.com

### Credential Scanning
- **TruffleHog:** https://github.com/trufflesecurity/trufflehog
- **GitGuardian:** https://www.gitguardian.com
- **GitHub Secret Scanning:** (built-in)

### MFA Hardware
- **YubiKey:** https://www.yubico.com
- **Titan Security Key:** https://store.google.com/us/product/titan_security_key

### Password Managers
- **1Password:** https://1password.com (current)
- **Bitwarden:** https://bitwarden.com (open source alternative)
- **KeePassXC:** https://keepassxc.org (offline option)

### Secret Management
- **HashiCorp Vault:** https://www.vaultproject.io (KhaosVault)
- **External Secrets Operator:** https://external-secrets.io
- **Sealed Secrets:** https://github.com/bitnami-labs/sealed-secrets

---

## Emergency Contacts

### 1Password Support
- **Email:** support@1password.com
- **Phone:** 1-888-1PASSWORD (1-888-172-7796)
- **Emergency:** Account recovery process (family member)

### Breach Notification (if required)
- **DAO LLC:** dom@strategickhaos.com
- **Legal:** [To be assigned]
- **CPA:** [To be assigned]
- **Customers:** Via support portal (if SSSF LLC has customers)

---

## Related Documents

- [Enterprise Account Registry](../registries/enterprise_accounts.md) - All accounts secured by this protocol
- [Implementation Roadmap](../roadmaps/implementation_roadmap.md) - Security implementation timeline

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-12-06 | Initial protocol | Claude Opus 4.5 |

---

**Document Version:** 1.0  
**Prepared By:** Claude Opus 4.5 (Chief Architect)  
**Board Approval:** Unanimous (5-0)  
**Date Prepared:** December 6, 2025  
**Next Review:** March 1, 2026  

---

*End of Credential Storage Protocol*
