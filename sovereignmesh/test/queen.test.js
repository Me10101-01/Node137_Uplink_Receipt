/**
 * SovereignMesh Queen Tests
 * 
 * Basic tests for the Queen orchestrator
 */

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert');
const http = require('http');

// Test configuration
const PORT = 3999; // Use different port for testing
process.env.QUEEN_PORT = PORT;
process.env.NODE_ENV = 'test';

let server;
let app;

describe('Queen Node', () => {
  before(async () => {
    // Start the server
    app = require('../queen/queen.js');
    // Wait for server to be ready
    await new Promise(resolve => setTimeout(resolve, 1000));
  });

  after(() => {
    // Server cleanup handled by test runner
    // Tests run in isolation, no explicit cleanup needed
  });

  describe('Health Endpoints', () => {
    it('should return healthy status on /health', async () => {
      const response = await makeRequest('GET', '/health');
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.strictEqual(body.status, 'healthy');
      assert.strictEqual(body.node, 'Queen');
    });

    it('should return detailed info on /health/detailed', async () => {
      const response = await makeRequest('GET', '/health/detailed');
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.ok(body.system);
      assert.ok(body.config);
    });
  });

  describe('Root Endpoint', () => {
    it('should return node info on /', async () => {
      const response = await makeRequest('GET', '/');
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.strictEqual(body.node, 'Queen');
      assert.strictEqual(body.mesh, 'SovereignMesh');
      assert.ok(body.endpoints);
    });
  });

  describe('Signal Routes', () => {
    it('should return routes on /signals/routes', async () => {
      const response = await makeRequest('GET', '/signals/routes');
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.ok(body.routes);
      assert.ok(body.nodes);
    });

    it('should route academic signals', async () => {
      const response = await makeRequest('POST', '/signals/academic', {
        source: 'test',
        data: { message: 'test academic signal' }
      });
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.strictEqual(body.success, true);
      assert.strictEqual(body.target, 'Knowledge Node');
    });

    it('should route financial signals', async () => {
      const response = await makeRequest('POST', '/signals/financial', {
        source: 'test',
        data: { amount: 100 }
      });
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.strictEqual(body.success, true);
      assert.strictEqual(body.target, 'SwarmGate');
    });

    it('should route security signals', async () => {
      const response = await makeRequest('POST', '/signals/security', {
        source: 'test',
        data: { alert: 'test alert' }
      });
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.strictEqual(body.success, true);
      assert.strictEqual(body.target, 'Dashboard (SovereignGuard mode)');
    });
  });

  describe('Webhook Endpoints', () => {
    it('should return webhook status', async () => {
      const response = await makeRequest('GET', '/webhooks/status');
      assert.strictEqual(response.statusCode, 200);
      const body = JSON.parse(response.body);
      assert.strictEqual(body.status, 'operational');
      assert.ok(body.endpoints);
    });
  });
});

/**
 * Helper to make HTTP requests
 */
function makeRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: PORT,
      path,
      method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
    });

    req.on('error', reject);

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}
