/**
 * SovereignMesh Queen Orchestrator
 * 
 * GitHub Codespaces as free Kubernetes alternative
 * Queen Node - Central signal router for the SovereignMesh cluster
 * 
 * App ID: 1884781
 * Client ID: Iv23liTGwnOOha2UYNuf
 * 
 * Architecture:
 * - Receives signals from external sources (Zapier, SNHU, Thread Bank, Discord)
 * - Routes to appropriate Codespace nodes (SwarmGate, Knowledge, Dashboard)
 * - Authenticates with GitHub App credentials
 * - Logs everything to audit trail
 * 
 * @author Node 137 - Strategickhaos
 * @license See LICENSE
 */

const express = require('express');
const helmet = require('helmet');
const morgan = require('morgan');
const { v4: uuidv4 } = require('uuid');
const path = require('path');
const fs = require('fs');

// Import custom modules
const config = require('../config/mesh.config');
const authMiddleware = require('../middleware/auth');
const auditLogger = require('../utils/auditLogger');
const signalRouter = require('../routes/signals');
const webhooksRouter = require('../routes/webhooks');
const healthRouter = require('../routes/health');

// Initialize Express app
const app = express();

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://*.github.dev", "https://api.github.com"]
    }
  },
  crossOriginEmbedderPolicy: false
}));

// Request parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request ID middleware
app.use((req, res, next) => {
  req.requestId = uuidv4();
  res.setHeader('X-Request-ID', req.requestId);
  next();
});

// Logging middleware
const logStream = fs.createWriteStream(
  path.join(__dirname, '../logs/access.log'),
  { flags: 'a' }
);

app.use(morgan(':date[iso] :method :url :status :response-time ms - :res[content-length]', { 
  stream: logStream 
}));

// Also log to console in development
if (process.env.NODE_ENV !== 'production') {
  app.use(morgan('dev'));
}

// Audit logging for all requests
app.use((req, res, next) => {
  auditLogger.logRequest(req);
  next();
});

// Routes
app.use('/signals', signalRouter);
app.use('/webhooks', webhooksRouter);
app.use('/health', healthRouter);

// Root endpoint - Queen status
app.get('/', (req, res) => {
  res.json({
    node: 'Queen',
    mesh: 'SovereignMesh',
    status: 'operational',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    owner: 'Node 137 - Strategickhaos',
    endpoints: {
      signals: '/signals/*',
      webhooks: '/webhooks/*',
      health: '/health'
    },
    cluster: {
      nodes: config.MESH_NODES,
      orchestrator: 'queen'
    }
  });
});

// 404 handler
app.use((req, res) => {
  auditLogger.logEvent('404_NOT_FOUND', {
    path: req.path,
    method: req.method,
    requestId: req.requestId
  });
  
  res.status(404).json({
    error: 'Endpoint not found',
    path: req.path,
    requestId: req.requestId,
    timestamp: new Date().toISOString()
  });
});

// Error handler
app.use((err, req, res, _next) => {
  const errorId = uuidv4();
  
  auditLogger.logEvent('ERROR', {
    errorId,
    message: err.message,
    stack: err.stack,
    requestId: req.requestId
  });

  res.status(err.status || 500).json({
    error: 'Internal server error',
    errorId,
    requestId: req.requestId,
    timestamp: new Date().toISOString()
  });
});

// Start server
const PORT = process.env.PORT || config.QUEEN_PORT || 3000;

app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════════════╗
║                    SOVEREIGNMESH QUEEN NODE                       ║
╠═══════════════════════════════════════════════════════════════════╣
║  Status:      OPERATIONAL                                         ║
║  Port:        ${PORT}                                                  ║
║  Node:        Queen (Orchestrator)                                ║
║  Mesh:        SovereignMesh                                       ║
║  Owner:       Node 137 - Strategickhaos                           ║
║                                                                   ║
║  GitHub App:  ID ${config.GITHUB_APP_ID}                                     ║
║  Client:      ${config.GITHUB_CLIENT_ID}                  ║
╠═══════════════════════════════════════════════════════════════════╣
║  Endpoints:                                                       ║
║    /signals/academic   → Knowledge Node                           ║
║    /signals/financial  → SwarmGate                                ║
║    /signals/security   → SovereignGuard                           ║
║    /webhooks/github    → GitHub App webhooks                      ║
║    /webhooks/zapier    → Zapier automation signals                ║
║    /health             → Health check                             ║
╚═══════════════════════════════════════════════════════════════════╝
  `);

  auditLogger.logEvent('QUEEN_STARTED', {
    port: PORT,
    timestamp: new Date().toISOString(),
    pid: process.pid
  });
});

module.exports = app;
