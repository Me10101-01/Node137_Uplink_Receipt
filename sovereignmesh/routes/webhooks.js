/**
 * Webhook Routes
 * 
 * Handles incoming webhooks from external sources:
 * - GitHub App webhooks
 * - Zapier automation signals
 * - Discord webhooks
 */

const express = require('express');
const router = express.Router();
const config = require('../config/mesh.config');
const auth = require('../middleware/auth');
const auditLogger = require('../utils/auditLogger');

/**
 * Classify a GitHub event to determine routing
 * @param {string} event - GitHub event type
 * @param {object} payload - Event payload
 * @returns {string} Signal type (academic, financial, security, etc.)
 */
function classifyGitHubEvent(event, payload) {
  // Security-related events
  const securityEvents = [
    'security_advisory',
    'repository_vulnerability_alert',
    'secret_scanning_alert',
    'code_scanning_alert'
  ];
  
  if (securityEvents.includes(event)) {
    return 'security';
  }

  // Academic/knowledge events (documentation, wiki, etc.)
  if (event === 'wiki' || event === 'gollum') {
    return 'academic';
  }

  // Default to intelligence for code-related events
  return 'intelligence';
}

/**
 * POST /webhooks/github
 * Receive GitHub App webhooks
 */
router.post('/github', auth.verifyGitHubWebhook, (req, res) => {
  const event = req.get('x-github-event');
  const delivery = req.get('x-github-delivery');
  const payload = req.body;

  auditLogger.logWebhook('github', {
    type: event,
    action: payload.action,
    delivery
  }, 'received');

  // Classify and route the event
  const signalType = classifyGitHubEvent(event, payload);
  
  // Prepare signal payload
  const signal = {
    source: 'github',
    event,
    action: payload.action,
    repository: payload.repository?.full_name,
    sender: payload.sender?.login,
    delivery,
    timestamp: new Date().toISOString()
  };

  auditLogger.logSignal(signalType, 'github', config.SIGNAL_ROUTES[signalType]?.target || 'unknown', {
    event,
    action: payload.action,
    delivery
  });

  res.json({
    success: true,
    received: true,
    event,
    delivery,
    routed: signalType,
    requestId: req.requestId
  });
});

/**
 * POST /webhooks/zapier
 * Receive Zapier automation signals
 */
router.post('/zapier', auth.verifyZapierWebhook, (req, res) => {
  const { type, source, data, action } = req.body;

  auditLogger.logWebhook('zapier', {
    type: type || 'unknown',
    action,
    id: req.requestId
  }, 'received');

  // Map Zapier signal types to internal signal types
  const typeMapping = {
    'email': 'academic',
    'snhu': 'academic',
    'bank': 'financial',
    'thread': 'financial',
    'trading': 'financial',
    'alert': 'security',
    'security': 'security',
    'ai': 'intelligence',
    'query': 'intelligence'
  };

  const signalType = typeMapping[type] || 'intelligence';
  const targetNode = config.SIGNAL_ROUTES[signalType]?.target || 'dashboard';

  auditLogger.logSignal(signalType, source || 'zapier', targetNode, {
    zapierType: type,
    action
  });

  res.json({
    success: true,
    received: true,
    type,
    routed: signalType,
    target: targetNode,
    requestId: req.requestId
  });
});

/**
 * POST /webhooks/discord
 * Receive Discord webhooks
 */
router.post('/discord', (req, res) => {
  const { type, channel_id, content, author } = req.body;

  auditLogger.logWebhook('discord', {
    type: type || 'message',
    channel: channel_id,
    id: req.requestId
  }, 'received');

  // Route Discord messages to AI Council for processing
  const signal = {
    source: 'discord',
    channel: channel_id,
    content,
    author: author?.username,
    timestamp: new Date().toISOString()
  };

  auditLogger.logSignal('intelligence', 'discord', 'aicouncil', {
    channel: channel_id
  });

  res.json({
    success: true,
    received: true,
    routed: 'intelligence',
    target: 'AI Council',
    requestId: req.requestId
  });
});

/**
 * POST /webhooks/snhu
 * Receive SNHU email notifications (via Zapier or direct)
 */
router.post('/snhu', (req, res) => {
  const { subject, from, body, timestamp } = req.body;

  auditLogger.logWebhook('snhu', {
    type: 'email',
    subject: subject?.substring(0, 50),
    id: req.requestId
  }, 'received');

  // Route to Knowledge Node for academic processing
  auditLogger.logSignal('academic', 'snhu-email', 'knowledge', {
    subject: subject?.substring(0, 50)
  });

  res.json({
    success: true,
    received: true,
    routed: 'academic',
    target: 'Knowledge Node',
    requestId: req.requestId
  });
});

/**
 * POST /webhooks/thread
 * Receive Thread Bank notifications
 */
router.post('/thread', (req, res) => {
  const { type, amount, description, timestamp } = req.body;

  auditLogger.logWebhook('thread', {
    type: type || 'transaction',
    id: req.requestId
  }, 'received');

  // Route to SwarmGate for financial processing
  auditLogger.logSignal('financial', 'thread-bank', 'swarmgate', {
    transactionType: type
  });

  res.json({
    success: true,
    received: true,
    routed: 'financial',
    target: 'SwarmGate',
    requestId: req.requestId
  });
});

/**
 * GET /webhooks/status
 * Get webhook endpoints status
 */
router.get('/status', (req, res) => {
  res.json({
    status: 'operational',
    endpoints: {
      github: { 
        path: '/webhooks/github', 
        enabled: config.EXTERNAL_SOURCES.github.enabled,
        verification: 'hmac-sha256'
      },
      zapier: { 
        path: '/webhooks/zapier', 
        enabled: config.EXTERNAL_SOURCES.zapier.enabled,
        verification: 'header-token'
      },
      discord: { 
        path: '/webhooks/discord', 
        enabled: config.EXTERNAL_SOURCES.discord.enabled,
        verification: 'header-token'
      },
      snhu: { 
        path: '/webhooks/snhu', 
        enabled: true,
        verification: 'none'
      },
      thread: { 
        path: '/webhooks/thread', 
        enabled: true,
        verification: 'none'
      }
    },
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
