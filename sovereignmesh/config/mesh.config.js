/**
 * SovereignMesh Configuration
 * 
 * Central configuration for the mesh cluster
 * Contains GitHub App credentials and node topology
 */

module.exports = {
  // GitHub App Configuration
  GITHUB_APP_ID: process.env.GITHUB_APP_ID || '1884781',
  GITHUB_CLIENT_ID: process.env.GITHUB_CLIENT_ID || 'Iv23liTGwnOOha2UYNuf',
  GITHUB_PRIVATE_KEY_PATH: process.env.GITHUB_PRIVATE_KEY_PATH || './github-app.pem',
  GITHUB_WEBHOOK_SECRET: process.env.GITHUB_WEBHOOK_SECRET || '',

  // Queen Node Configuration
  QUEEN_PORT: process.env.QUEEN_PORT || 3000,
  NODE_ENV: process.env.NODE_ENV || 'development',

  // Mesh Node Topology
  // In production, these would be Codespace URLs like: https://stunning-broccoli-abc123.github.dev
  MESH_NODES: {
    queen: {
      name: 'Queen',
      role: 'orchestrator',
      port: 3000,
      url: process.env.QUEEN_URL || 'http://localhost:3000',
      description: 'Signal router and central orchestrator'
    },
    swarmgate: {
      name: 'SwarmGate',
      role: 'financial',
      port: 3001,
      url: process.env.SWARMGATE_URL || 'http://localhost:3001',
      description: 'Trading, Treasury, 7% allocation',
      features: ['trading', 'treasury', 'allocation']
    },
    knowledge: {
      name: 'Knowledge',
      role: 'academic',
      port: 3002,
      url: process.env.KNOWLEDGE_URL || 'http://localhost:3002',
      description: 'Obsidian, Memory, Ingest',
      features: ['obsidian', 'memory', 'ingest']
    },
    dashboard: {
      name: 'Dashboard',
      role: 'interface',
      port: 3003,
      url: process.env.DASHBOARD_URL || 'http://localhost:3003',
      description: 'SovereignOS UI, Metrics, Control',
      features: ['ui', 'metrics', 'control']
    },
    aicouncil: {
      name: 'AI Council',
      role: 'intelligence',
      port: 3004,
      url: process.env.AICOUNCIL_URL || 'http://localhost:3004',
      description: 'Legion of Minds - Claude, GPT, Grok, Local models',
      features: ['claude', 'gpt', 'grok', 'local-proxy', 'consensus']
    }
  },

  // Signal Types and Routing
  // Note: security routes to dashboard which handles SovereignGuard mode
  SIGNAL_ROUTES: {
    academic: {
      target: 'knowledge',
      priority: 'normal',
      sources: ['snhu', 'obsidian', 'research']
    },
    financial: {
      target: 'swarmgate',
      priority: 'high',
      sources: ['thread', 'trading', 'treasury']
    },
    security: {
      target: 'dashboard', // Dashboard in SovereignGuard mode
      priority: 'critical',
      sources: ['audit', 'alert', 'breach']
    },
    intelligence: {
      target: 'aicouncil',
      priority: 'normal',
      sources: ['query', 'consensus', 'analysis']
    },
    interface: {
      target: 'dashboard',
      priority: 'normal',
      sources: ['metrics', 'control', 'display']
    }
  },

  // External Signal Sources
  EXTERNAL_SOURCES: {
    zapier: {
      enabled: true,
      webhookPath: '/webhooks/zapier',
      verification: 'header-token'
    },
    github: {
      enabled: true,
      webhookPath: '/webhooks/github',
      verification: 'hmac-sha256'
    },
    discord: {
      enabled: true,
      webhookPath: '/webhooks/discord',
      verification: 'header-token'
    }
  },

  // Local Nodes (Hardware)
  LOCAL_NODES: {
    nova: {
      name: 'Nova',
      type: 'ollama',
      description: 'Local AI model server'
    },
    lyra: {
      name: 'Lyra',
      type: 'ollama',
      description: 'Local AI model server'
    },
    athena: {
      name: 'Athena',
      type: 'k8s',
      description: 'Kubernetes cluster'
    },
    ipower: {
      name: 'iPower',
      type: 'router',
      description: 'Network router'
    }
  },

  // Audit Trail Configuration
  AUDIT: {
    enabled: true,
    logPath: './logs/audit.log',
    retentionDays: 90,
    includeHeaders: false, // Don't log sensitive headers
    includeBody: true
  }
};
