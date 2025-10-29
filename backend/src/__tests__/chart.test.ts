import request from 'supertest';
import app from '../index';

describe('Chart Routes', () => {
  let authToken: string;
  let chartId: string;

  // Create a test user and get auth token before running chart tests
  beforeAll(async () => {
    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'charttest@example.com',
        password: 'password123',
        name: 'Chart Test User',
      });

    authToken = registerResponse.body.data.token;
  });

  describe('POST /api/charts', () => {
    it('should create a new chart with valid data', async () => {
      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Test Chart',
          birthDate: '1990-01-15',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(201);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.name).toBe('Test Chart');

      chartId = response.body.data.id;
    });

    it('should fail without authentication', async () => {
      const response = await request(app)
        .post('/api/charts')
        .send({
          name: 'Test Chart',
          birthDate: '1990-01-15',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(401);
    });

    it('should fail with invalid birth date', async () => {
      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Test Chart',
          birthDate: 'invalid-date',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should fail with invalid time format', async () => {
      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Test Chart',
          birthDate: '1990-01-15',
          birthTime: '25:70',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should fail with invalid coordinates', async () => {
      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Test Chart',
          birthDate: '1990-01-15',
          birthTime: '14:30',
          latitude: 95,
          longitude: -74.0060,
        });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });
  });

  describe('GET /api/charts', () => {
    beforeAll(async () => {
      // Create a few more charts for pagination testing
      await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Chart 2',
          birthDate: '1985-03-20',
          birthTime: '09:15',
          latitude: 51.5074,
          longitude: -0.1278,
        });

      await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Chart 3',
          birthDate: '1992-07-08',
          birthTime: '18:45',
          latitude: 48.8566,
          longitude: 2.3522,
        });
    });

    it('should get all charts for authenticated user', async () => {
      const response = await request(app)
        .get('/api/charts')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.data.length).toBeGreaterThan(0);
      expect(response.body).toHaveProperty('pagination');
    });

    it('should support pagination', async () => {
      const response = await request(app)
        .get('/api/charts?page=1&limit=2')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.pagination.page).toBe(1);
      expect(response.body.pagination.limit).toBe(2);
      expect(response.body.data.length).toBeLessThanOrEqual(2);
    });

    it('should fail without authentication', async () => {
      const response = await request(app).get('/api/charts');

      expect(response.status).toBe(401);
    });
  });

  describe('GET /api/charts/:id', () => {
    it('should get a specific chart', async () => {
      const response = await request(app)
        .get(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(chartId);
    });

    it('should return 404 for non-existent chart', async () => {
      const response = await request(app)
        .get('/api/charts/nonexistent')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(404);
    });

    it('should fail without authentication', async () => {
      const response = await request(app).get(`/api/charts/${chartId}`);

      expect(response.status).toBe(401);
    });
  });

  describe('PUT /api/charts/:id', () => {
    it('should update a chart', async () => {
      const response = await request(app)
        .put(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Updated Chart Name',
        });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data.name).toBe('Updated Chart Name');
    });

    it('should update multiple fields', async () => {
      const response = await request(app)
        .put(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Another Update',
          birthTime: '16:00',
        });

      expect(response.status).toBe(200);
      expect(response.body.data.name).toBe('Another Update');
      expect(response.body.data.birthTime).toBe('16:00');
    });

    it('should return 404 for non-existent chart', async () => {
      const response = await request(app)
        .put('/api/charts/nonexistent')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Updated',
        });

      expect(response.status).toBe(404);
    });

    it('should fail with invalid data', async () => {
      const response = await request(app)
        .put(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          latitude: 95,
        });

      expect(response.status).toBe(400);
    });

    it('should fail without authentication', async () => {
      const response = await request(app)
        .put(`/api/charts/${chartId}`)
        .send({
          name: 'Updated',
        });

      expect(response.status).toBe(401);
    });
  });

  describe('POST /api/charts/calculate', () => {
    it('should calculate chart data', async () => {
      const response = await request(app)
        .post('/api/charts/calculate')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          birthDate: '1990-01-15',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('planets');
      expect(response.body.data).toHaveProperty('houses');
      expect(response.body.data).toHaveProperty('aspects');
      expect(Array.isArray(response.body.data.planets)).toBe(true);
    });

    it('should support house system parameter', async () => {
      const response = await request(app)
        .post('/api/charts/calculate')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          birthDate: '1990-01-15',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
          houseSystem: 'Koch',
        });

      expect(response.status).toBe(200);
      expect(response.body.data.metadata.houseSystem).toBe('Koch');
    });

    it('should fail with invalid data', async () => {
      const response = await request(app)
        .post('/api/charts/calculate')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          birthDate: 'invalid',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(400);
    });

    it('should fail without authentication', async () => {
      const response = await request(app)
        .post('/api/charts/calculate')
        .send({
          birthDate: '1990-01-15',
          birthTime: '14:30',
          latitude: 40.7128,
          longitude: -74.0060,
        });

      expect(response.status).toBe(401);
    });
  });

  describe('GET /api/charts/:id/interpretation', () => {
    it('should get chart interpretation', async () => {
      const response = await request(app)
        .get(`/api/charts/${chartId}/interpretation`)
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('chartId');
      expect(response.body.data).toHaveProperty('bmadAnalysis');
      expect(response.body.data).toHaveProperty('symbolonCards');
      expect(response.body.data).toHaveProperty('insights');
      expect(Array.isArray(response.body.data.symbolonCards)).toBe(true);
    });

    it('should return 404 for non-existent chart', async () => {
      const response = await request(app)
        .get('/api/charts/nonexistent/interpretation')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(404);
    });

    it('should fail without authentication', async () => {
      const response = await request(app).get(`/api/charts/${chartId}/interpretation`);

      expect(response.status).toBe(401);
    });
  });

  describe('DELETE /api/charts/:id', () => {
    it('should delete a chart', async () => {
      const response = await request(app)
        .delete(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Chart deleted successfully');
    });

    it('should return 404 for non-existent chart', async () => {
      const response = await request(app)
        .delete('/api/charts/nonexistent')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(404);
    });

    it('should fail without authentication', async () => {
      const response = await request(app).delete(`/api/charts/${chartId}`);

      expect(response.status).toBe(401);
    });
  });
});
