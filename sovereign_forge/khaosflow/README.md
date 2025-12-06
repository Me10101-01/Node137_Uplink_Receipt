# KhaosFlow - Sovereign Zapier Replacement

## Overview

KhaosFlow is a self-hosted, zero-dependency workflow automation platform that connects applications and automates repetitive tasks without vendor lock-in.

**Status**: 🟡 Planned  
**Target Release**: Q1 2026  
**Feature Parity**: 0% → 95% (target)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      KHAOSFLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (React + Tailwind)                                │
│  ├── Visual Flow Builder (drag-drop)                       │
│  ├── Trigger Configuration                                  │
│  ├── Action Templates                                       │
│  ├── Testing & Debugging Console                           │
│  └── Execution History                                      │
│                                                             │
│  Workflow Engine (Node.js + BullMQ)                         │
│  ├── Trigger Listener (webhook, schedule, manual)          │
│  ├── Action Executor (HTTP, DB, file ops)                  │
│  ├── Data Transformer (JSONata, Jq)                        │
│  ├── Error Handler (retry logic, alerts)                   │
│  └── Queue Manager (priority, concurrency)                 │
│                                                             │
│  Connector Library                                          │
│  ├── HTTP Connector (REST, GraphQL, SOAP)                  │
│  ├── Database Connector (PostgreSQL, MySQL, MongoDB)       │
│  ├── File Connector (local, S3, FTP, SFTP)                 │
│  ├── Email Connector (SMTP, IMAP)                          │
│  └── Custom Connectors (JavaScript plugins)                │
│                                                             │
│  Data Store (PostgreSQL + Redis)                            │
│  ├── Workflow definitions                                   │
│  ├── Execution logs                                         │
│  ├── Scheduled tasks (cron)                                │
│  └── Secrets vault (encrypted)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Features

### 1. Trigger Types

#### Webhook Trigger
```yaml
trigger:
  type: webhook
  url: https://khaosflow.local/hooks/{workflow_id}
  method: POST
  authentication:
    type: api_key
    header: X-API-Key
  
  # Incoming data automatically available in workflow
```

#### Schedule Trigger
```yaml
trigger:
  type: schedule
  cron: "0 9 * * 1-5"  # Weekdays at 9 AM
  timezone: America/Chicago
  
  # Or simpler syntax
  schedule: "every weekday at 9am"
```

#### Manual Trigger
```yaml
trigger:
  type: manual
  button_label: "Run Backup"
  confirmation: true
  parameters:
    - name: environment
      type: select
      options: [dev, staging, prod]
```

#### Database Trigger
```yaml
trigger:
  type: database
  connection: postgres_main
  table: orders
  event: INSERT
  filter: "status = 'new'"
```

#### File Watcher
```yaml
trigger:
  type: file_watcher
  path: /data/uploads/
  pattern: "*.csv"
  event: created
```

### 2. Action Types

#### HTTP Request
```yaml
action:
  type: http_request
  method: POST
  url: https://api.example.com/orders
  headers:
    Authorization: "Bearer {{secrets.api_token}}"
    Content-Type: application/json
  body:
    order_id: "{{trigger.data.id}}"
    customer: "{{trigger.data.customer_name}}"
  
  retry:
    attempts: 3
    backoff: exponential
```

#### Database Operation
```yaml
action:
  type: database_query
  connection: postgres_main
  query: |
    INSERT INTO customers (name, email, created_at)
    VALUES ($1, $2, NOW())
  parameters:
    - "{{trigger.data.name}}"
    - "{{trigger.data.email}}"
```

#### Send Email
```yaml
action:
  type: send_email
  smtp: default
  to: "{{trigger.data.customer_email}}"
  subject: "Order Confirmation #{{trigger.data.order_id}}"
  template: order_confirmation
  data:
    order_number: "{{trigger.data.order_id}}"
    total: "{{trigger.data.total}}"
```

#### Run Script
```yaml
action:
  type: run_script
  runtime: node
  code: |
    const data = context.trigger.data;
    const total = data.items.reduce((sum, item) => sum + item.price, 0);
    return { total, item_count: data.items.length };
  
  timeout: 30s
```

#### File Operation
```yaml
action:
  type: file_write
  path: /data/reports/daily-{{date}}.json
  content: "{{json(trigger.data)}}"
  encoding: utf8
```

### 3. Data Transformation

#### Filter Data
```yaml
action:
  type: transform
  operation: filter
  input: "{{trigger.data.items}}"
  condition: "price > 100"
```

#### Map/Transform
```yaml
action:
  type: transform
  operation: map
  input: "{{trigger.data.orders}}"
  transform: |
    {
      "id": $.order_id,
      "customer": $.customer_name,
      "total": $.items[].price | sum
    }
```

#### Aggregate
```yaml
action:
  type: transform
  operation: aggregate
  input: "{{trigger.data.sales}}"
  group_by: region
  aggregations:
    total_revenue: sum(amount)
    avg_order: avg(amount)
    order_count: count()
```

### 4. Conditional Logic

```yaml
workflow:
  name: Order Processing
  
  steps:
    - name: Receive Order
      trigger:
        type: webhook
    
    - name: Check Inventory
      action:
        type: database_query
        query: "SELECT stock FROM products WHERE id = $1"
      
    - name: Branch on Stock
      condition:
        if: "{{steps.check_inventory.result.stock > 0}}"
        then:
          - name: Process Order
            action: { ... }
        else:
          - name: Notify Out of Stock
            action: { ... }
```

### 5. Error Handling

```yaml
workflow:
  error_handling:
    strategy: retry_then_alert
    
    retry:
      max_attempts: 3
      backoff: exponential
      backoff_multiplier: 2
      max_backoff: 300s
    
    on_failure:
      - type: send_email
        to: admin@example.com
        subject: "Workflow Failed: {{workflow.name}}"
      
      - type: log
        level: error
        message: "{{error.message}}"
      
      - type: webhook
        url: https://monitoring.example.com/alerts
```

---

## Technology Stack

### Workflow Engine
- **Runtime**: Node.js / Bun
- **Queue**: BullMQ (Redis-backed)
- **Scheduler**: Cron + Node-cron
- **Event Bus**: Redis Pub/Sub

### Connector Framework
- **HTTP**: Axios / Undici
- **Database**: Knex.js (multi-DB)
- **File**: Node.js fs + AWS SDK (S3-compatible)
- **Email**: Nodemailer
- **Custom**: JavaScript plugin system

### Data Transformation
- **JSONata**: JSON query and transformation
- **Jq**: Command-line JSON processor
- **JavaScript**: Custom transformation scripts

### Frontend
- **Framework**: React 18
- **Flow Builder**: React Flow
- **Forms**: React Hook Form + Zod
- **Code Editor**: Monaco Editor

---

## Example Workflows

### 1. New Customer Onboarding

```yaml
workflow:
  name: Customer Onboarding
  
  trigger:
    type: webhook
    path: /customers/new
  
  steps:
    - name: Create Customer Record
      action:
        type: database_insert
        table: customers
        data: "{{trigger.data}}"
    
    - name: Send Welcome Email
      action:
        type: send_email
        to: "{{trigger.data.email}}"
        template: welcome
    
    - name: Create Task for Sales
      action:
        type: http_request
        url: "{{khaosbase_url}}/api/tasks"
        method: POST
        body:
          title: "Onboard {{trigger.data.name}}"
          assigned_to: "{{trigger.data.account_manager}}"
```

### 2. Daily Backup

```yaml
workflow:
  name: Daily Database Backup
  
  trigger:
    type: schedule
    cron: "0 2 * * *"  # 2 AM daily
  
  steps:
    - name: Dump Database
      action:
        type: run_script
        runtime: bash
        code: |
          pg_dump -h localhost -U postgres khaosbase > /tmp/backup.sql
    
    - name: Compress Backup
      action:
        type: run_script
        runtime: bash
        code: |
          gzip /tmp/backup.sql
    
    - name: Upload to S3
      action:
        type: file_upload
        source: /tmp/backup.sql.gz
        destination: s3://backups/daily-{{date}}.sql.gz
    
    - name: Cleanup Local File
      action:
        type: file_delete
        path: /tmp/backup.sql.gz
    
    - name: Notify Admin
      action:
        type: send_email
        to: admin@example.com
        subject: "Backup Complete: {{date}}"
```

### 3. Order Processing Pipeline

```yaml
workflow:
  name: E-commerce Order Processing
  
  trigger:
    type: webhook
    path: /orders/new
  
  steps:
    - name: Validate Order
      action:
        type: run_script
        code: |
          const order = context.trigger.data;
          if (!order.items || order.items.length === 0) {
            throw new Error('Order has no items');
          }
          return order;
    
    - name: Check Inventory
      action:
        type: database_query
        query: |
          SELECT id, stock FROM products
          WHERE id = ANY($1)
        parameters:
          - "{{trigger.data.items[].product_id}}"
    
    - name: Process Payment
      condition:
        if: "{{all(steps.check_inventory.result[].stock > 0)}}"
        then:
          - action:
              type: http_request
              url: "{{payment_gateway_url}}/charge"
              method: POST
    
    - name: Update Inventory
      action:
        type: database_query
        query: |
          UPDATE products
          SET stock = stock - 1
          WHERE id = ANY($1)
    
    - name: Send Confirmation
      action:
        type: send_email
        to: "{{trigger.data.customer_email}}"
        template: order_confirmation
```

---

## Zapier Migration Path

### 1. Export Zaps

```bash
# Use Zapier API to export Zaps
curl "https://api.zapier.com/v1/zaps" \
  -H "Authorization: Bearer ${ZAPIER_API_KEY}" \
  > zapier_export.json
```

### 2. Convert to KhaosFlow

```python
# tools/zapier_migrator.py

import json
from typing import Dict

class ZapierMigrator:
    def convert_zap(self, zap: Dict) -> Dict:
        """Convert Zapier Zap to KhaosFlow workflow"""
        
        workflow = {
            'name': zap['title'],
            'trigger': self._convert_trigger(zap['trigger']),
            'steps': []
        }
        
        for action in zap['actions']:
            workflow['steps'].append(self._convert_action(action))
        
        return workflow
    
    def _convert_trigger(self, trigger: Dict) -> Dict:
        """Convert Zapier trigger to KhaosFlow trigger"""
        # Implementation...
        pass
    
    def _convert_action(self, action: Dict) -> Dict:
        """Convert Zapier action to KhaosFlow action"""
        # Implementation...
        pass
```

---

## Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  khaosflow:
    image: strategickhaos/khaosflow:latest
    ports:
      - "3001:3000"
    environment:
      - DATABASE_URL=postgresql://khaos:secret@db:5432/khaosflow
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
  
  worker:
    image: strategickhaos/khaosflow:latest
    command: worker
    environment:
      - DATABASE_URL=postgresql://khaos:secret@db:5432/khaosflow
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
  
  db:
    image: postgres:15-alpine
  
  cache:
    image: redis:7-alpine
```

---

## Roadmap

### Phase 1: MVP (6 weeks)
- [ ] Workflow engine (basic triggers + actions)
- [ ] HTTP connector
- [ ] Database connector
- [ ] Visual flow builder
- [ ] Manual execution

### Phase 2: Core Features (4 weeks)
- [ ] Scheduling (cron)
- [ ] Error handling + retry
- [ ] Email connector
- [ ] File connector
- [ ] Data transformation (JSONata)

### Phase 3: Advanced (4 weeks)
- [ ] Conditional logic
- [ ] Loops and iterations
- [ ] Custom connectors (plugins)
- [ ] Monitoring dashboard
- [ ] Zapier import tool

---

**Project Status**: 🟡 Planned  
**License**: MIT  
**Estimated Hours**: 120  

⚔️🔥💜
