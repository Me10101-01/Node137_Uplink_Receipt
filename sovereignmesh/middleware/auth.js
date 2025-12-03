/**
 * Authentication Middleware
 * 
 * Handles GitHub App authentication and webhook verification
 * Supports multiple authentication methods for different sources
 */

const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const config = require('../config/mesh.config');
const auditLogger = require('../utils/auditLogger');

/**
 * Verify GitHub webhook signature
 * @param {object} req - Express request
 * @param {object} res - Express response
 * @param {function} next - Next middleware
 */
function verifyGitHubWebhook(req, res, next) {
  const signature = req.get('x-hub-signature-256');
  const webhookSecret = config.GITHUB_WEBHOOK_SECRET;

  // Skip verification in development if no secret configured
  if (!webhookSecret && process.env.NODE_ENV !== 'production') {
    auditLogger.logAuth('github-webhook', true, { mode: 'development-skip' });
    return next();
  }

  if (!signature) {
    auditLogger.logAuth('github-webhook', false, { reason: 'missing-signature' });
    return res.status(401).json({ error: 'Missing signature' });
  }

  const body = JSON.stringify(req.body);
  const expectedSignature = 'sha256=' + crypto
    .createHmac('sha256', webhookSecret)
    .update(body)
    .digest('hex');

  // Ensure both buffers have the same length before comparison
  const signatureBuffer = Buffer.from(signature, 'utf8');
  const expectedBuffer = Buffer.from(expectedSignature, 'utf8');
  
  // If lengths don't match, signatures can't be equal
  if (signatureBuffer.length !== expectedBuffer.length) {
    auditLogger.logAuth('github-webhook', false, { reason: 'invalid-signature' });
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const valid = crypto.timingSafeEqual(signatureBuffer, expectedBuffer);

  if (!valid) {
    auditLogger.logAuth('github-webhook', false, { reason: 'invalid-signature' });
    return res.status(401).json({ error: 'Invalid signature' });
  }

  auditLogger.logAuth('github-webhook', true, {});
  next();
}

/**
 * Verify Zapier webhook token
 * @param {object} req - Express request
 * @param {object} res - Express response
 * @param {function} next - Next middleware
 */
function verifyZapierWebhook(req, res, next) {
  const token = req.get('x-zapier-token') || req.query.token;
  const expectedToken = process.env.ZAPIER_WEBHOOK_TOKEN;

  // Skip verification in development if no token configured
  if (!expectedToken && process.env.NODE_ENV !== 'production') {
    auditLogger.logAuth('zapier-webhook', true, { mode: 'development-skip' });
    return next();
  }

  if (!token || token !== expectedToken) {
    auditLogger.logAuth('zapier-webhook', false, { reason: 'invalid-token' });
    return res.status(401).json({ error: 'Invalid or missing token' });
  }

  auditLogger.logAuth('zapier-webhook', true, {});
  next();
}

/**
 * Generate GitHub App JWT for API authentication
 * @returns {string|null} JWT token or null if key not available
 */
function generateGitHubAppJWT() {
  try {
    const privateKeyPath = path.resolve(config.GITHUB_PRIVATE_KEY_PATH);
    
    if (!fs.existsSync(privateKeyPath)) {
      console.warn('[AUTH] GitHub App private key not found at:', privateKeyPath);
      return null;
    }

    const privateKey = fs.readFileSync(privateKeyPath, 'utf8');
    const now = Math.floor(Date.now() / 1000);

    const payload = {
      iat: now - 60,           // Issued 60 seconds ago
      exp: now + (10 * 60),    // Expires in 10 minutes
      iss: config.GITHUB_APP_ID
    };

    return jwt.sign(payload, privateKey, { algorithm: 'RS256' });
  } catch (error) {
    console.error('[AUTH] Failed to generate GitHub App JWT:', error.message);
    return null;
  }
}

/**
 * Middleware to require GitHub App authentication
 * Adds appJwt to request if successful
 */
function requireGitHubApp(req, res, next) {
  const appJwt = generateGitHubAppJWT();
  
  if (!appJwt) {
    auditLogger.logAuth('github-app', false, { reason: 'jwt-generation-failed' });
    return res.status(503).json({ 
      error: 'GitHub App not configured',
      message: 'Private key file not found or invalid'
    });
  }

  req.appJwt = appJwt;
  req.appId = config.GITHUB_APP_ID;
  auditLogger.logAuth('github-app', true, { appId: config.GITHUB_APP_ID });
  next();
}

/**
 * General API key authentication
 * @param {object} req - Express request
 * @param {object} res - Express response
 * @param {function} next - Next middleware
 */
function requireApiKey(req, res, next) {
  const apiKey = req.get('x-api-key') || req.query.apiKey;
  const validApiKey = process.env.SOVEREIGN_API_KEY;

  // Skip in development if not configured
  if (!validApiKey && process.env.NODE_ENV !== 'production') {
    return next();
  }

  if (!apiKey || apiKey !== validApiKey) {
    auditLogger.logAuth('api-key', false, { reason: 'invalid-key' });
    return res.status(401).json({ error: 'Invalid or missing API key' });
  }

  auditLogger.logAuth('api-key', true, {});
  next();
}

module.exports = {
  verifyGitHubWebhook,
  verifyZapierWebhook,
  generateGitHubAppJWT,
  requireGitHubApp,
  requireApiKey
};
