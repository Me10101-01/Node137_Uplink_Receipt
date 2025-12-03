/**
 * Signal Routes
 * 
 * Routes for handling different signal types
 * - /signals/academic → Knowledge Node
 * - /signals/financial → SwarmGate
 * - /signals/security → SovereignGuard
 * - /signals/intelligence → AI Council
 */

const express = require('express');
const router = express.Router();
const config = require('../config/mesh.config');
const { signalLimiter } = require('../middleware/rateLimit');
const auditLogger = require('../utils/auditLogger');

// Apply rate limiting to all signal routes
router.use(signalLimiter);

/**
 * Forward signal to target node
 * @param {string} targetNode - Target node key from config
 * @param {object} payload - Signal payload
 * @returns {Promise<object>} Response from target node
 */
async function forwardToNode(targetNode, payload) {
  const node = config.MESH_NODES[targetNode];
  
  if (!node) {
    throw new Error(`Unknown node: ${targetNode}`);
  }

  // In production, this would make an HTTP request to the target node
  // For now, we simulate the routing and return a success response
  auditLogger.logNodeComm('queen', targetNode, 'signal_forward', 'initiated');

  try {
    // Simulated response - in production this would be:
    // const response = await fetch(`${node.url}/ingest`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(payload)
    // });
    
    const response = {
      success: true,
      node: node.name,
      receivedAt: new Date().toISOString(),
      payloadSize: JSON.stringify(payload).length
    };

    auditLogger.logNodeComm('queen', targetNode, 'signal_forward', 'success');
    return response;
  } catch (error) {
    auditLogger.logNodeComm('queen', targetNode, 'signal_forward', 'failed');
    throw error;
  }
}

/**
 * POST /signals/academic
 * Route academic signals to Knowledge Node
 */
router.post('/academic', async (req, res) => {
  try {
    const source = req.body.source || 'unknown';
    const payload = {
      type: 'academic',
      source,
      data: req.body.data || req.body,
      timestamp: new Date().toISOString(),
      requestId: req.requestId
    };

    auditLogger.logSignal('academic', source, 'knowledge', { requestId: req.requestId });
    
    const result = await forwardToNode('knowledge', payload);
    
    res.json({
      success: true,
      routed: true,
      target: 'Knowledge Node',
      result,
      requestId: req.requestId
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      requestId: req.requestId
    });
  }
});

/**
 * POST /signals/financial
 * Route financial signals to SwarmGate
 */
router.post('/financial', async (req, res) => {
  try {
    const source = req.body.source || 'unknown';
    const payload = {
      type: 'financial',
      source,
      data: req.body.data || req.body,
      timestamp: new Date().toISOString(),
      requestId: req.requestId,
      priority: 'high'
    };

    auditLogger.logSignal('financial', source, 'swarmgate', { 
      requestId: req.requestId,
      priority: 'high'
    });
    
    const result = await forwardToNode('swarmgate', payload);
    
    res.json({
      success: true,
      routed: true,
      target: 'SwarmGate',
      result,
      requestId: req.requestId
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      requestId: req.requestId
    });
  }
});

/**
 * POST /signals/security
 * Route security signals to Dashboard (SovereignGuard mode)
 * These are treated as critical priority
 * Note: Dashboard handles security in SovereignGuard mode
 */
router.post('/security', async (req, res) => {
  try {
    const source = req.body.source || 'unknown';
    const payload = {
      type: 'security',
      source,
      data: req.body.data || req.body,
      timestamp: new Date().toISOString(),
      requestId: req.requestId,
      priority: 'critical'
    };

    auditLogger.logSignal('security', source, 'dashboard', { 
      requestId: req.requestId,
      priority: 'critical',
      mode: 'sovereignguard'
    });
    
    // Dashboard handles security signals in SovereignGuard mode
    const result = await forwardToNode('dashboard', payload);
    
    res.json({
      success: true,
      routed: true,
      target: 'Dashboard (SovereignGuard mode)',
      result,
      requestId: req.requestId
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      requestId: req.requestId
    });
  }
});

/**
 * POST /signals/intelligence
 * Route AI queries to AI Council
 */
router.post('/intelligence', async (req, res) => {
  try {
    const source = req.body.source || 'unknown';
    const payload = {
      type: 'intelligence',
      source,
      query: req.body.query || req.body.data,
      models: req.body.models || ['claude', 'gpt', 'grok'],
      consensusRequired: req.body.consensus !== false,
      timestamp: new Date().toISOString(),
      requestId: req.requestId
    };

    auditLogger.logSignal('intelligence', source, 'aicouncil', { 
      requestId: req.requestId,
      models: payload.models
    });
    
    const result = await forwardToNode('aicouncil', payload);
    
    res.json({
      success: true,
      routed: true,
      target: 'AI Council',
      result,
      requestId: req.requestId
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      requestId: req.requestId
    });
  }
});

/**
 * POST /signals/broadcast
 * Broadcast signal to all nodes
 */
router.post('/broadcast', async (req, res) => {
  try {
    const source = req.body.source || 'unknown';
    const payload = {
      type: 'broadcast',
      source,
      data: req.body.data || req.body,
      timestamp: new Date().toISOString(),
      requestId: req.requestId
    };

    auditLogger.logSignal('broadcast', source, 'all', { requestId: req.requestId });
    
    const results = {};
    const nodeKeys = Object.keys(config.MESH_NODES).filter(k => k !== 'queen');
    
    for (const nodeKey of nodeKeys) {
      try {
        results[nodeKey] = await forwardToNode(nodeKey, payload);
      } catch (error) {
        results[nodeKey] = { success: false, error: error.message };
      }
    }
    
    res.json({
      success: true,
      routed: true,
      target: 'All Nodes',
      results,
      requestId: req.requestId
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      requestId: req.requestId
    });
  }
});

/**
 * GET /signals/routes
 * Get available signal routes
 */
router.get('/routes', (req, res) => {
  res.json({
    routes: config.SIGNAL_ROUTES,
    nodes: Object.entries(config.MESH_NODES).map(([key, node]) => ({
      key,
      name: node.name,
      role: node.role,
      description: node.description
    }))
  });
});

module.exports = router;
