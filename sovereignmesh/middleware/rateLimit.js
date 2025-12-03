/**
 * Rate Limiting Middleware
 * 
 * Protects against brute-force attacks and abuse
 * Different limits for different endpoint types
 */

const rateLimit = require('express-rate-limit');

/**
 * General rate limiter for most endpoints
 * 100 requests per 15 minutes per IP
 */
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {
    error: 'Too many requests',
    message: 'Please try again later',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false
});

/**
 * Strict rate limiter for authenticated endpoints
 * 30 requests per 15 minutes per IP
 */
const strictLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 30,
  message: {
    error: 'Too many requests',
    message: 'Rate limit exceeded for authenticated endpoint',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false
});

/**
 * Webhook rate limiter
 * Higher limit for webhooks since they're automated
 * 200 requests per 15 minutes per IP
 */
const webhookLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 200,
  message: {
    error: 'Too many webhook requests',
    message: 'Webhook rate limit exceeded',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false,
  // Use the webhook delivery ID or request ID to track
  keyGenerator: (req) => {
    return req.get('x-github-delivery') || 
           req.get('x-request-id') || 
           req.ip;
  }
});

/**
 * Signal rate limiter
 * 150 requests per 15 minutes per IP
 */
const signalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 150,
  message: {
    error: 'Too many signal requests',
    message: 'Signal rate limit exceeded',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false
});

module.exports = {
  generalLimiter,
  strictLimiter,
  webhookLimiter,
  signalLimiter
};
