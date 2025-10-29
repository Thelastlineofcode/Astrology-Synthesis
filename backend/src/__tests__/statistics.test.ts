import request from 'supertest';
import express, { Application } from 'express';
import statisticsRouter from '../routes/statistics';

describe('Statistics Routes', () => {
  let app: Application;

  beforeAll(() => {
    app = express();
    app.use(express.json());
    app.use('/api/statistics', statisticsRouter);
  });

  describe('GET /api/statistics/overview', () => {
    it('should return statistics overview', async () => {
      const response = await request(app)
        .get('/api/statistics/overview')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('stats');
      expect(response.body.data.stats).toHaveProperty('totalReadings');
      expect(response.body.data.stats).toHaveProperty('completedReadings');
      expect(response.body.data.stats).toHaveProperty('pendingReadings');
      expect(response.body.data).toHaveProperty('lastUpdated');
    });
  });

  describe('GET /api/statistics/readings-by-type', () => {
    it('should return readings breakdown by type', async () => {
      const response = await request(app)
        .get('/api/statistics/readings-by-type')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('readings');
      expect(Array.isArray(response.body.data.readings)).toBe(true);
      expect(response.body.data.readings.length).toBeGreaterThan(0);
    });

    it('should filter readings by categories', async () => {
      const response = await request(app)
        .get('/api/statistics/readings-by-type?categories=Natal,Synastry')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.filters).toHaveProperty('categories');
    });
  });

  describe('GET /api/statistics/trends', () => {
    it('should return trend data', async () => {
      const response = await request(app)
        .get('/api/statistics/trends')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('trends');
      expect(Array.isArray(response.body.data.trends)).toBe(true);
      expect(response.body.data).toHaveProperty('interval');
    });

    it('should filter trends by date range', async () => {
      const response = await request(app)
        .get('/api/statistics/trends?startDate=2025-10-01&endDate=2025-10-31')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.filters).toHaveProperty('startDate');
      expect(response.body.data.filters).toHaveProperty('endDate');
    });
  });

  describe('GET /api/statistics/tasks', () => {
    it('should return tasks list', async () => {
      const response = await request(app)
        .get('/api/statistics/tasks')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('tasks');
      expect(response.body.data).toHaveProperty('total');
      expect(Array.isArray(response.body.data.tasks)).toBe(true);
    });

    it('should filter tasks by status', async () => {
      const response = await request(app)
        .get('/api/statistics/tasks?status=pending')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.filters).toHaveProperty('status');
    });

    it('should filter tasks by priority', async () => {
      const response = await request(app)
        .get('/api/statistics/tasks?priority=high')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.filters).toHaveProperty('priority');
    });
  });

  describe('GET /api/statistics/insights', () => {
    it('should return analytical insights', async () => {
      const response = await request(app)
        .get('/api/statistics/insights')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('insights');
      expect(Array.isArray(response.body.data.insights)).toBe(true);
      expect(response.body.data).toHaveProperty('generatedAt');
      
      // Check insight structure
      if (response.body.data.insights.length > 0) {
        const insight = response.body.data.insights[0];
        expect(insight).toHaveProperty('id');
        expect(insight).toHaveProperty('type');
        expect(insight).toHaveProperty('title');
        expect(insight).toHaveProperty('description');
        expect(insight).toHaveProperty('severity');
      }
    });
  });
});
