# Blue Team Operations

## Mission

Build sovereign, self-hosted replacements that achieve feature parity with vendor applications while maintaining **zero external dependencies**.

---

## Technology Stack

### Frontend

```yaml
frontend:
  frameworks:
    preferred: [React, Svelte, HTMX]
    rationale: "React for rich apps, Svelte for performance, HTMX for simplicity"
  
  styling:
    library: Tailwind CSS
    approach: "Utility-first, mobile-first"
  
  state_management:
    options: [Zustand, Jotai, Redux Toolkit]
    preference: Zustand (lightweight)
  
  build:
    bundler: Vite
    target: [ES2020, modern browsers]
```

### Backend

```yaml
backend:
  runtime:
    options: [Node.js, Deno, Bun]
    preference: Node.js (maturity) or Bun (performance)
  
  framework:
    options: [Hono, Fastify, Express]
    preference: Hono (lightweight, edge-ready)
  
  api:
    protocols: [REST, GraphQL, WebSocket]
    rest: "Primary for CRUD"
    graphql: "Optional for complex queries"
    websocket: "Real-time updates"
  
  validation:
    library: Zod
    approach: "Schema-first, type-safe"
```

### Database

```yaml
database:
  primary:
    engine: PostgreSQL
    version: "15+"
    extensions: [pgvector, pg_trgm, uuid-ossp]
  
  cache:
    engine: Redis
    use_cases: [session, rate_limiting, pub_sub]
  
  search:
    engine: Meilisearch / Typesense
    rationale: "Fast, typo-tolerant, self-hosted"
  
  vector:
    options: [pgvector, Qdrant]
    use_case: "AI embeddings, semantic search"
```

### Infrastructure

```yaml
infrastructure:
  orchestration:
    platform: Kubernetes
    distribution: [k3s, k0s, vanilla]
    
  container:
    runtime: Docker
    registry: "Self-hosted Harbor or GitLab"
  
  ingress:
    controller: [Traefik, NGINX]
    tls: "cert-manager + Let's Encrypt"
  
  secrets:
    management: [Sealed Secrets, SOPS, Vault]
    preference: "Sealed Secrets (GitOps-friendly)"
  
  observability:
    metrics: Prometheus + Grafana
    logs: Loki
    traces: Jaeger
```

### Authentication

```yaml
authentication:
  identity_provider:
    options: [Keycloak, Authelia, Authentik]
    preference: Keycloak (enterprise-grade)
  
  protocols:
    supported: [OIDC, SAML, LDAP]
    primary: OIDC
  
  session:
    storage: Redis
    duration: "7 days (configurable)"
```

---

## Build Constraints

Every Blue Team build **MUST** satisfy:

### 1. Zero External Dependencies

**Test:** Application runs with network disabled

```bash
# Disconnect network
sudo ip link set eth0 down

# Start application
docker-compose up -d

# Verify core functionality
curl http://localhost:3000/health
# Expected: 200 OK

# Reconnect network
sudo ip link set eth0 up
```

### 2. Self-Hostable

**Test:** Single `docker-compose.yaml` deploys full stack

```yaml
# docker-compose.yaml must include:
services:
  - app (frontend + backend)
  - database (PostgreSQL)
  - cache (Redis)
  - search (Meilisearch)
  
# All data volumes persist locally
volumes:
  - postgres_data
  - redis_data
  - meilisearch_data
```

### 3. Kubernetes Native

**Test:** Helm chart passes validation and deploys cleanly

```bash
helm lint ./charts/khaosbase
helm install khaosbase ./charts/khaosbase --dry-run
kubectl apply -f ./kubernetes/
kubectl rollout status deployment/khaosbase
```

### 4. Data Portable

**Test:** Full export/import in standard formats

```bash
# Export all data
./bin/khaosbase export --format json > backup.json
./bin/khaosbase export --format csv --output ./csv_export/
./bin/khaosbase export --format sql > backup.sql

# Import to new instance
./bin/khaosbase import --format json < backup.json
```

### 5. Offline Capable

**Test:** Core functionality works without internet

```yaml
offline_features:
  must_work:
    - CRUD operations
    - Search (local index)
    - Authentication (local users)
    - File uploads (local storage)
    
  may_fail:
    - External integrations
    - Email notifications (if SMTP external)
    - AI features (if external API)
```

### 6. MIT Licensed

**Test:** All dependencies are permissively licensed

```bash
# Check licenses
npm run license-check
# OR
pip-licenses --format=markdown

# Verify no GPL, AGPL, or proprietary licenses
```

---

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/strategickhaos/sovereign-forge.git
cd sovereign-forge/khaosbase

# Install dependencies
npm install  # or: pnpm install, bun install

# Setup environment
cp .env.example .env
vim .env  # Configure local settings

# Start database
docker-compose up -d postgres redis

# Run migrations
npm run migrate

# Start dev server
npm run dev
```

### 2. Feature Development

```typescript
// Example: Adding a new feature

// 1. Define schema (Zod)
import { z } from 'zod';

const TableSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(255),
  baseId: z.string().uuid(),
  schema: z.record(z.any()),
  createdAt: z.date(),
  updatedAt: z.date()
});

// 2. Create database migration
-- migrations/003_add_tables.sql
CREATE TABLE tables (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  base_id UUID REFERENCES bases(id) ON DELETE CASCADE,
  schema JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

// 3. Implement API endpoint
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';

const app = new Hono();

app.post('/api/tables', 
  zValidator('json', TableSchema.omit({ id: true, createdAt: true, updatedAt: true })),
  async (c) => {
    const data = c.req.valid('json');
    const table = await db.tables.create(data);
    return c.json(table, 201);
  }
);

// 4. Add tests
import { describe, it, expect } from 'vitest';

describe('Tables API', () => {
  it('creates a new table', async () => {
    const response = await app.request('/api/tables', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Test Table', baseId: 'uuid...' })
    });
    expect(response.status).toBe(201);
  });
});
```

### 3. Testing

```bash
# Unit tests
npm run test

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

### 4. Building

```bash
# Build frontend
npm run build

# Build Docker image
docker build -t khaosbase:latest .

# Build Helm chart
helm package ./charts/khaosbase
```

---

## Architecture Patterns

### Microservices (Optional)

For complex applications, consider microservices:

```
┌────────────────────────────────────────────────┐
│              API Gateway (Traefik)             │
└────┬─────────┬─────────┬─────────┬────────────┘
     │         │         │         │
     ▼         ▼         ▼         ▼
  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
  │ Auth│  │ Base│  │Table│  │ File│
  │ Svc │  │ Svc │  │ Svc │  │ Svc │
  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
     │        │        │        │
     └────────┴────────┴────────┘
                 │
                 ▼
          ┌──────────────┐
          │  PostgreSQL  │
          └──────────────┘
```

### Monolith (Recommended for Start)

Simpler deployment, easier to maintain:

```
┌────────────────────────────────────┐
│       Application Server           │
│  ┌──────────────────────────────┐ │
│  │  Frontend (React/Svelte)     │ │
│  └──────────────────────────────┘ │
│  ┌──────────────────────────────┐ │
│  │  API Layer (Hono/Fastify)    │ │
│  └──────────────────────────────┘ │
│  ┌──────────────────────────────┐ │
│  │  Business Logic              │ │
│  └──────────────────────────────┘ │
│  ┌──────────────────────────────┐ │
│  │  Data Access (ORM/Query)     │ │
│  └──────────────────────────────┘ │
└────────────────┬───────────────────┘
                 │
                 ▼
          ┌──────────────┐
          │  PostgreSQL  │
          └──────────────┘
```

---

## Code Quality Standards

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "esModuleInterop": true
  }
}
```

### ESLint Configuration

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "prettier"
  ],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

### Code Style

- **Naming**: camelCase for variables/functions, PascalCase for types/components
- **Formatting**: Prettier with 2-space indentation
- **Comments**: JSDoc for public APIs
- **File Structure**: Feature-based organization

```
src/
├── features/
│   ├── auth/
│   ├── bases/
│   ├── tables/
│   └── records/
├── lib/
│   ├── db/
│   ├── validation/
│   └── utils/
└── app.ts
```

---

## Deployment

### Docker Compose (Development)

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/khaosbase
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
  
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret
  
  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes (Production)

```bash
# Install via Helm
helm repo add strategickhaos https://charts.strategickhaos.com
helm install khaosbase strategickhaos/khaosbase \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=khaosbase.example.com \
  --set postgresql.auth.password=supersecret
```

---

## Security Checklist

- [ ] All inputs validated (Zod schemas)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitized output)
- [ ] CSRF protection (tokens)
- [ ] Rate limiting (Redis-based)
- [ ] Authentication required for sensitive endpoints
- [ ] Authorization checks (RBAC)
- [ ] HTTPS enforced
- [ ] Secrets in environment variables (not code)
- [ ] Regular dependency updates
- [ ] Security headers (helmet.js)
- [ ] Input size limits
- [ ] File upload validation

---

**Document Classification:** OPERATIONAL  
**Version:** 1.0  
**Last Updated:** 2025-12-06  

⚔️🔥💜
