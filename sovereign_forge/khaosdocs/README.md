# KhaosDocs - Sovereign Notion Replacement

## Overview

KhaosDocs is a self-hosted, all-in-one workspace for notes, wikis, documentation, and knowledge management without vendor lock-in.

**Status**: 🟡 Planned  
**Target Release**: Q1 2026  
**Feature Parity**: 0% → 95% (target)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      KHAOSDOCS                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (React + Tailwind)                                │
│  ├── Block-based Editor (Slate.js / ProseMirror)           │
│  ├── Sidebar Navigation (tree view)                        │
│  ├── Search (full-text + semantic)                         │
│  ├── Page Templates                                         │
│  └── Sharing & Permissions                                  │
│                                                             │
│  Backend (Node.js + Hono)                                   │
│  ├── Block Storage (PostgreSQL JSONB)                      │
│  ├── Full-text Search (Meilisearch)                        │
│  ├── File Storage (MinIO)                                   │
│  ├── Real-time Sync (WebSocket)                            │
│  └── Export Engine (Markdown, PDF, HTML)                   │
│                                                             │
│  Database (PostgreSQL)                                      │
│  ├── Workspaces                                             │
│  ├── Pages (hierarchical)                                   │
│  ├── Blocks (content units)                                │
│  ├── Comments                                               │
│  └── Permissions                                            │
│                                                             │
│  Extensions                                                 │
│  ├── AI Assistant (local LLM via Ollama)                   │
│  ├── Code Execution (sandboxed)                            │
│  ├── Database Views (table, kanban, etc.)                  │
│  └── Charts & Visualizations                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Features

### 1. Block-Based Editor

#### Supported Block Types

```typescript
// Text Blocks
- Heading (H1, H2, H3, H4, H5, H6)
- Paragraph
- Bullet List
- Numbered List
- Quote
- Callout (info, warning, success, error)
- Code Block (syntax highlighting)

// Media Blocks
- Image
- Video (embed)
- Audio
- File Attachment

// Embed Blocks
- Web Bookmark
- PDF
- YouTube/Vimeo
- Maps
- Figma/Miro

// Advanced Blocks
- Table
- Database View
- Chart/Graph
- Math Equation (KaTeX)
- Mermaid Diagram
- Code Execution

// Interactive Blocks
- Todo Checkbox
- Toggle List
- Tabs/Accordion
- Button
```

#### Block Manipulation

```yaml
editor_features:
  - drag_and_drop_reordering
  - block_menu (type "/" to open)
  - inline_formatting (bold, italic, code, link)
  - markdown_shortcuts
  - slash_commands
  - keyboard_shortcuts
  - multi_block_selection
  - block_duplication
  - block_deletion_with_undo
```

### 2. Page Hierarchy

```
Workspace
├── 📁 Projects
│   ├── 📄 Project Alpha
│   │   ├── 📄 Requirements
│   │   ├── 📄 Design Docs
│   │   └── 📄 Meeting Notes
│   └── 📄 Project Beta
│
├── 📁 Team Wiki
│   ├── 📄 Onboarding
│   ├── 📄 Processes
│   └── 📄 FAQs
│
└── 📁 Personal
    ├── 📄 Daily Notes
    └── 📄 Ideas
```

### 3. Database Views

Transform pages into databases with multiple views:

#### Table View
```
┌────────────────────────────────────────────────────┐
│ Name          │ Status      │ Owner    │ Due Date │
├────────────────────────────────────────────────────┤
│ Task 1        │ In Progress │ Alice    │ 2025-12-10│
│ Task 2        │ Done        │ Bob      │ 2025-12-08│
│ Task 3        │ Todo        │ Charlie  │ 2025-12-15│
└────────────────────────────────────────────────────┘
```

#### Kanban View
```
┌─────────────┬─────────────┬─────────────┐
│ Todo        │ In Progress │ Done        │
├─────────────┼─────────────┼─────────────┤
│ [Task 3]    │ [Task 1]    │ [Task 2]    │
│             │             │             │
└─────────────┴─────────────┴─────────────┘
```

#### Calendar View
```
December 2025
┌────┬────┬────┬────┬────┬────┬────┐
│ M  │ T  │ W  │ T  │ F  │ S  │ S  │
├────┼────┼────┼────┼────┼────┼────┤
│ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │
│    │    │    │    │    │    │    │
├────┼────┼────┼────┼────┼────┼────┤
│ 8  │ 9  │ 10 │ 11 │ 12 │ 13 │ 14 │
│[T2]│    │[T1]│    │    │    │    │
└────┴────┴────┴────┴────┴────┴────┘
```

#### Gallery View
```
┌──────────────┬──────────────┬──────────────┐
│  ┌────────┐  │  ┌────────┐  │  ┌────────┐  │
│  │ Image  │  │  │ Image  │  │  │ Image  │  │
│  └────────┘  │  └────────┘  │  └────────┘  │
│  Project A   │  Project B   │  Project C   │
└──────────────┴──────────────┴──────────────┘
```

### 4. Collaboration

#### Real-time Features
- Live cursor positions
- User presence indicators
- Simultaneous editing
- Conflict resolution (CRDT or OT)

#### Comments & Discussions
```yaml
comment:
  author: Alice
  timestamp: 2025-12-06T15:30:00Z
  block_id: abc123
  content: "Should we add more details here?"
  mentions: ["@Bob", "@Charlie"]
  resolved: false
```

#### Activity Feed
```
Recent Activity:
- Alice edited "Project Requirements" (2 min ago)
- Bob commented on "Design Mockups" (15 min ago)
- Charlie created "Sprint Planning" (1 hour ago)
```

### 5. Search

#### Full-text Search
```
Search: "project timeline"

Results:
1. Project Alpha > Timeline (90% match)
   ...shows the project timeline and key milestones...

2. Meeting Notes > Q4 Planning (75% match)
   ...discussed project timeline adjustments...
```

#### Filters
```yaml
search_filters:
  - by_author: "Alice"
  - by_date_range: "last 7 days"
  - by_type: "page" | "database" | "comment"
  - by_workspace: "Engineering"
  - by_tags: ["project", "important"]
```

### 6. Templates

#### Page Templates
```yaml
templates:
  - name: Meeting Notes
    blocks:
      - type: heading
        content: "Meeting: {{title}}"
      - type: paragraph
        content: "Date: {{date}}"
      - type: heading
        content: "Attendees"
      - type: bullet_list
      - type: heading
        content: "Agenda"
      - type: numbered_list
      - type: heading
        content: "Action Items"
      - type: database
        view: table
        properties:
          - name: Task
          - name: Owner
          - name: Due Date
```

#### Database Templates
```yaml
database_templates:
  - name: Task List
    properties:
      - name: Task
        type: title
      - name: Status
        type: select
        options: [Todo, In Progress, Done]
      - name: Assignee
        type: person
      - name: Due Date
        type: date
      - name: Priority
        type: select
        options: [Low, Medium, High]
```

### 7. Export & Import

#### Export Formats
- **Markdown**: Full workspace or individual pages
- **PDF**: Styled export with table of contents
- **HTML**: Static site generation
- **JSON**: Structured data export
- **Notion**: Compatible format for migration

#### Import Sources
- Markdown files
- Notion exports (.zip)
- Confluence exports
- Google Docs (via API)
- Plain text files

---

## Technology Stack

### Editor
- **Framework**: Slate.js or ProseMirror
- **Rendering**: React
- **Syntax Highlighting**: Prism.js
- **Math**: KaTeX
- **Diagrams**: Mermaid

### Backend
- **Runtime**: Node.js / Bun
- **Framework**: Hono
- **Database**: PostgreSQL (JSONB for blocks)
- **Search**: Meilisearch
- **Storage**: MinIO (S3-compatible)
- **Real-time**: WebSocket (uWebSockets.js)

### AI Features
- **Local LLM**: Ollama (Llama, Mistral, etc.)
- **Embeddings**: all-MiniLM-L6-v2
- **Vector Store**: pgvector

---

## Data Model

```sql
-- Workspaces
CREATE TABLE workspaces (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Pages (hierarchical)
CREATE TABLE pages (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    parent_page_id UUID REFERENCES pages(id),
    title TEXT,
    icon VARCHAR(50),
    cover_image VARCHAR(500),
    is_database BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Blocks (content units)
CREATE TABLE blocks (
    id UUID PRIMARY KEY,
    page_id UUID REFERENCES pages(id),
    type VARCHAR(50),  -- heading, paragraph, image, etc.
    content JSONB,     -- flexible content storage
    properties JSONB,  -- block-specific properties
    order_index INT,
    parent_block_id UUID REFERENCES blocks(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Database Properties (for database pages)
CREATE TABLE database_properties (
    id UUID PRIMARY KEY,
    page_id UUID REFERENCES pages(id),
    name VARCHAR(255),
    type VARCHAR(50),  -- text, number, select, date, etc.
    config JSONB,      -- property-specific config
    order_index INT
);

-- Comments
CREATE TABLE comments (
    id UUID PRIMARY KEY,
    block_id UUID REFERENCES blocks(id),
    user_id UUID,
    content TEXT,
    resolved BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Search index
CREATE INDEX idx_blocks_content ON blocks USING GIN (to_tsvector('english', content::text));
```

---

## Example Use Cases

### 1. Team Wiki

```
Engineering Wiki
├── Onboarding
│   ├── Day 1 Checklist
│   ├── Development Setup
│   └── Team Contacts
├── Architecture
│   ├── System Overview
│   ├── Database Schema
│   └── API Documentation
└── Processes
    ├── Code Review Guidelines
    ├── Deployment Process
    └── Incident Response
```

### 2. Project Management

```
Project Alpha [Database]

Table View:
┌────────────────┬──────────┬──────────┬──────────┐
│ Task           │ Status   │ Owner    │ Due Date │
├────────────────┼──────────┼──────────┼──────────┤
│ Design mockups │ Done     │ Alice    │ Dec 1    │
│ API endpoints  │ Progress │ Bob      │ Dec 10   │
│ Frontend       │ Todo     │ Charlie  │ Dec 15   │
└────────────────┴──────────┴──────────┴──────────┘
```

### 3. Personal Knowledge Base

```
My Second Brain
├── Daily Notes
│   ├── 2025-12-06
│   ├── 2025-12-05
│   └── ...
├── Reading List
│   ├── [Book] Building a Second Brain
│   ├── [Article] Zettelkasten Method
│   └── ...
└── Ideas
    ├── Startup Ideas
    ├── Writing Topics
    └── Side Projects
```

---

## Notion Migration Path

**⚠️ Security Note**: When handling file uploads and zip extractions:
- Validate file paths to prevent directory traversal
- Use secure temporary directories
- Verify zip contents before extraction
- Implement file size limits

### 1. Export from Notion

```
Settings → Settings & Members → Export content → Export all workspace content
Format: Markdown & CSV
```

### 2. Import to KhaosDocs

```python
# tools/notion_migrator.py

import zipfile
import os
from pathlib import Path

class NotionMigrator:
    def import_export(self, zip_path: str):
        """Import Notion export zip"""
        
        with zipfile.ZipFile(zip_path) as z:
            z.extractall('/tmp/notion_export')
        
        # Process markdown files
        for md_file in Path('/tmp/notion_export').rglob('*.md'):
            self._import_page(md_file)
        
        # Process CSV databases
        for csv_file in Path('/tmp/notion_export').rglob('*.csv'):
            self._import_database(csv_file)
```

---

## Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  khaosdocs:
    image: strategickhaos/khaosdocs:latest
    ports:
      - "3002:3000"
    environment:
      - DATABASE_URL=postgresql://khaos:secret@db:5432/khaosdocs
      - MINIO_ENDPOINT=http://storage:9000
      - MEILISEARCH_URL=http://search:7700
    depends_on:
      - db
      - storage
      - search
  
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  storage:
    image: minio/minio
    volumes:
      - minio_data:/data
  
  search:
    image: getmeili/meilisearch:latest
    volumes:
      - meili_data:/meili_data

volumes:
  postgres_data:
  minio_data:
  meili_data:
```

---

## Roadmap

### Phase 1: MVP (4 weeks)
- [ ] Block-based editor (basic blocks)
- [ ] Page hierarchy
- [ ] Search (full-text)
- [ ] Export (Markdown)

### Phase 2: Core Features (4 weeks)
- [ ] Database views (table, kanban)
- [ ] Real-time collaboration
- [ ] Comments
- [ ] Templates

### Phase 3: Advanced (4 weeks)
- [ ] AI assistant (local LLM)
- [ ] Advanced blocks (charts, diagrams)
- [ ] Notion import tool
- [ ] Mobile responsive

---

**Project Status**: 🟡 Planned  
**License**: MIT  
**Estimated Hours**: 60  

⚔️🔥💜
