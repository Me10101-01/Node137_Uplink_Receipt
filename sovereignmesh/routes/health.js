/**
 * Health Routes
 * 
 * Health check and status endpoints for the Queen node
 */

const express = require('express');
const router = express.Router();
const config = require('../config/mesh.config');
const os = require('os');

/**
 * GET /health
 * Basic health check
 */
router.get('/', (req, res) => {
  res.json({
    status: 'healthy',
    node: 'Queen',
    mesh: 'SovereignMesh',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

/**
 * GET /health/detailed
 * Detailed health information
 */
router.get('/detailed', (req, res) => {
  res.json({
    status: 'healthy',
    node: {
      name: 'Queen',
      role: 'orchestrator',
      version: '1.0.0',
      mesh: 'SovereignMesh'
    },
    system: {
      platform: os.platform(),
      arch: os.arch(),
      nodeVersion: process.version,
      uptime: process.uptime(),
      memory: {
        total: os.totalmem(),
        free: os.freemem(),
        used: os.totalmem() - os.freemem()
      },
      cpus: os.cpus().length
    },
    config: {
      port: config.QUEEN_PORT,
      env: config.NODE_ENV,
      githubAppId: config.GITHUB_APP_ID
    },
    meshNodes: Object.keys(config.MESH_NODES).length,
    timestamp: new Date().toISOString()
  });
});

/**
 * GET /health/nodes
 * Check status of all mesh nodes
 */
router.get('/nodes', async (req, res) => {
  const nodeStatuses = {};

  for (const [key, node] of Object.entries(config.MESH_NODES)) {
    // In production, this would ping each node
    // For now, we simulate the status
    nodeStatuses[key] = {
      name: node.name,
      role: node.role,
      url: node.url,
      status: key === 'queen' ? 'online' : 'pending',
      lastCheck: new Date().toISOString()
    };
  }

  res.json({
    cluster: 'SovereignMesh',
    totalNodes: Object.keys(nodeStatuses).length,
    nodes: nodeStatuses,
    timestamp: new Date().toISOString()
  });
});

/**
 * GET /health/ready
 * Kubernetes-style readiness probe
 */
router.get('/ready', (req, res) => {
  // Check if all dependencies are ready
  const ready = true; // Add actual checks here

  if (ready) {
    res.json({ ready: true });
  } else {
    res.status(503).json({ ready: false });
  }
});

/**
 * GET /health/live
 * Kubernetes-style liveness probe
 */
router.get('/live', (req, res) => {
  res.json({ live: true });
});

module.exports = router;
