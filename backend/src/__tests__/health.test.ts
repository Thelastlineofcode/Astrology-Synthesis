import request from 'supertest';
import app from '../index';

describe('Health Check', () => {
  it('should return health status', async () => {
    const response = await request(app).get('/api/health');
    
    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
    expect(response.body.message).toBe('API is healthy');
    expect(response.body).toHaveProperty('timestamp');
    expect(response.body).toHaveProperty('uptime');
  });
});

describe('Root Endpoint', () => {
  it('should return API info', async () => {
    const response = await request(app).get('/');
    
    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Astrology Synthesis API');
    expect(response.body).toHaveProperty('endpoints');
  });
});
