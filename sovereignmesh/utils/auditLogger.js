/**
 * Audit Logger Utility
 * 
 * Comprehensive audit trail for all SovereignMesh operations
 * Logs to file and console with structured formatting
 */

const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, '../logs');
const AUDIT_LOG = path.join(LOG_DIR, 'audit.log');
const SIGNAL_LOG = path.join(LOG_DIR, 'signals.log');

// Ensure log directory exists
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

/**
 * Format a log entry
 * @param {string} event - Event type
 * @param {object} data - Event data
 * @returns {string} Formatted log entry
 */
function formatLogEntry(event, data) {
  return JSON.stringify({
    timestamp: new Date().toISOString(),
    event,
    ...data
  }) + '\n';
}

/**
 * Write to log file
 * @param {string} logFile - Log file path
 * @param {string} entry - Log entry
 */
function writeLog(logFile, entry) {
  try {
    fs.appendFileSync(logFile, entry);
  } catch (error) {
    console.error('[AUDIT] Failed to write log:', error.message);
  }
}

/**
 * Log a general event
 * @param {string} event - Event type
 * @param {object} data - Event data
 */
function logEvent(event, data = {}) {
  const entry = formatLogEntry(event, data);
  writeLog(AUDIT_LOG, entry);
  
  if (process.env.NODE_ENV !== 'production') {
    console.log(`[AUDIT] ${event}:`, JSON.stringify(data));
  }
}

/**
 * Log an incoming request
 * @param {object} req - Express request object
 */
function logRequest(req) {
  const data = {
    requestId: req.requestId,
    method: req.method,
    path: req.path,
    query: req.query,
    ip: req.ip || req.connection?.remoteAddress,
    userAgent: req.get('user-agent'),
    contentType: req.get('content-type')
  };
  
  logEvent('REQUEST', data);
}

/**
 * Log a signal routing event
 * @param {string} signalType - Type of signal (academic, financial, security)
 * @param {string} source - Source of signal
 * @param {string} target - Target node
 * @param {object} metadata - Additional metadata
 */
function logSignal(signalType, source, target, metadata = {}) {
  const entry = formatLogEntry('SIGNAL_ROUTED', {
    signalType,
    source,
    target,
    ...metadata
  });
  
  writeLog(SIGNAL_LOG, entry);
  writeLog(AUDIT_LOG, entry);
  
  console.log(`[SIGNAL] ${signalType} from ${source} → ${target}`);
}

/**
 * Log a webhook event
 * @param {string} webhookType - Type of webhook (github, zapier, discord)
 * @param {object} payload - Webhook payload (sanitized)
 * @param {string} status - Processing status
 */
function logWebhook(webhookType, payload, status) {
  const sanitizedPayload = {
    type: payload.type || 'unknown',
    action: payload.action,
    id: payload.id || payload.delivery
  };
  
  logEvent('WEBHOOK_RECEIVED', {
    webhookType,
    payload: sanitizedPayload,
    status
  });
}

/**
 * Log authentication events
 * @param {string} authType - Type of auth (github-app, token, etc.)
 * @param {boolean} success - Whether auth succeeded
 * @param {object} details - Additional details
 */
function logAuth(authType, success, details = {}) {
  logEvent(success ? 'AUTH_SUCCESS' : 'AUTH_FAILURE', {
    authType,
    ...details
  });
}

/**
 * Log node communication
 * @param {string} sourceNode - Source node name
 * @param {string} targetNode - Target node name
 * @param {string} action - Action being performed
 * @param {string} status - Status of communication
 */
function logNodeComm(sourceNode, targetNode, action, status) {
  logEvent('NODE_COMMUNICATION', {
    sourceNode,
    targetNode,
    action,
    status
  });
}

module.exports = {
  logEvent,
  logRequest,
  logSignal,
  logWebhook,
  logAuth,
  logNodeComm
};
