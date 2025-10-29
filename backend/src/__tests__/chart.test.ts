import request from 'supertest';
import app from '../index';

describe('Chart Routes', () => {
  let authToken: string;
  let userId: string;

  beforeAll(async () => {
    // Create a test user and get token
    const testUser = {
      email: 'charttest@example.com',
      password: 'password123',
      name: 'Chart Test User',
    };

    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send(testUser);

    authToken = registerResponse.body.data.token;
    userId = registerResponse.body.data.user.id;
  });

  describe('POST /api/charts', () => {
    it('should create a new chart with valid data', async () => {
      const chartData = {
        name: 'Test Chart',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      expect(response.status).toBe(201);
      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Chart created successfully');
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.name).toBe(chartData.name);
      expect(response.body.data.birthDate).toBe(chartData.birthDate);
      expect(response.body.data.userId).toBe(userId);
    });

    it('should fail without authentication', async () => {
      const chartData = {
        name: 'Test Chart',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .send(chartData);

      expect(response.status).toBe(401);
      expect(response.body.success).toBe(false);
    });

    it('should fail with invalid birth date', async () => {
      const chartData = {
        name: 'Test Chart',
        birthDate: 'invalid-date',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should fail with invalid time format', async () => {
      const chartData = {
        name: 'Test Chart',
        birthDate: '1990-01-01',
        birthTime: '25:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should fail with invalid latitude', async () => {
      const chartData = {
        name: 'Test Chart',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 91,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should fail with invalid longitude', async () => {
      const chartData = {
        name: 'Test Chart',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: 181,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should fail with missing required fields', async () => {
      const chartData = {
        name: 'Test Chart',
        // Missing birthDate, birthTime, latitude, longitude
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });
  });

  describe('GET /api/charts', () => {
    beforeAll(async () => {
      // Create test charts
      const charts = [
        {
          name: 'Chart 1',
          birthDate: '1990-01-01',
          birthTime: '12:00',
          latitude: 40.7128,
          longitude: -74.0060,
        },
        {
          name: 'Chart 2',
          birthDate: '1995-06-15',
          birthTime: '18:30',
          latitude: 51.5074,
          longitude: -0.1278,
        },
      ];

      for (const chart of charts) {
        await request(app)
          .post('/api/charts')
          .set('Authorization', `Bearer ${authToken}`)
          .send(chart);
      }
    });

    it('should get all charts for authenticated user', async () => {
      const response = await request(app)
        .get('/api/charts')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.data.length).toBeGreaterThanOrEqual(2);
      expect(response.body.data[0]).toHaveProperty('id');
      expect(response.body.data[0]).toHaveProperty('name');
    });

    it('should fail without authentication', async () => {
      const response = await request(app).get('/api/charts');

      expect(response.status).toBe(401);
      expect(response.body.success).toBe(false);
    });
  });

  describe('GET /api/charts/:id', () => {
    let chartId: string;

    beforeAll(async () => {
      // Create a test chart
      const chartData = {
        name: 'Specific Chart Test',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      chartId = response.body.data.id;
    });

    it('should get a specific chart by id', async () => {
      const response = await request(app)
        .get(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(chartId);
      expect(response.body.data).toHaveProperty('name');
    });

    it('should fail without authentication', async () => {
      const response = await request(app).get(`/api/charts/${chartId}`);

      expect(response.status).toBe(401);
      expect(response.body.success).toBe(false);
    });

    it('should return 404 for non-existent chart', async () => {
      const response = await request(app)
        .get('/api/charts/nonexistent')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(404);
      expect(response.body.success).toBe(false);
      expect(response.body.error.message).toBe('Chart not found');
    });
  });

  describe('DELETE /api/charts/:id', () => {
    let chartId: string;

    beforeEach(async () => {
      // Create a test chart to delete
      const chartData = {
        name: 'Chart to Delete',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const response = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${authToken}`)
        .send(chartData);

      chartId = response.body.data.id;
    });

    it('should delete a chart', async () => {
      const response = await request(app)
        .delete(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Chart deleted successfully');

      // Verify chart is deleted
      const getResponse = await request(app)
        .get(`/api/charts/${chartId}`)
        .set('Authorization', `Bearer ${authToken}`);

      expect(getResponse.status).toBe(404);
    });

    it('should fail without authentication', async () => {
      const response = await request(app).delete(`/api/charts/${chartId}`);

      expect(response.status).toBe(401);
      expect(response.body.success).toBe(false);
    });

    it('should return 404 for non-existent chart', async () => {
      const response = await request(app)
        .delete('/api/charts/nonexistent')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(404);
      expect(response.body.success).toBe(false);
      expect(response.body.error.message).toBe('Chart not found');
    });
  });

  describe('Authorization', () => {
    let user1Token: string;
    let user2Token: string;
    let user1ChartId: string;

    beforeAll(async () => {
      // Create two separate users
      const user1 = {
        email: 'user1@example.com',
        password: 'password123',
        name: 'User One',
      };

      const user2 = {
        email: 'user2@example.com',
        password: 'password123',
        name: 'User Two',
      };

      const response1 = await request(app)
        .post('/api/auth/register')
        .send(user1);
      user1Token = response1.body.data.token;

      const response2 = await request(app)
        .post('/api/auth/register')
        .send(user2);
      user2Token = response2.body.data.token;

      // Create a chart for user1
      const chartData = {
        name: 'User 1 Chart',
        birthDate: '1990-01-01',
        birthTime: '12:00',
        latitude: 40.7128,
        longitude: -74.0060,
      };

      const chartResponse = await request(app)
        .post('/api/charts')
        .set('Authorization', `Bearer ${user1Token}`)
        .send(chartData);

      user1ChartId = chartResponse.body.data.id;
    });

    it('should not allow user2 to access user1 chart', async () => {
      const response = await request(app)
        .get(`/api/charts/${user1ChartId}`)
        .set('Authorization', `Bearer ${user2Token}`);

      expect(response.status).toBe(404);
      expect(response.body.success).toBe(false);
    });

    it('should not allow user2 to delete user1 chart', async () => {
      const response = await request(app)
        .delete(`/api/charts/${user1ChartId}`)
        .set('Authorization', `Bearer ${user2Token}`);

      expect(response.status).toBe(404);
      expect(response.body.success).toBe(false);
    });
  });
});
