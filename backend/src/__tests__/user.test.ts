import request from 'supertest';
import app from '../index';
import { users } from '../routes/auth';

describe('User Profile API', () => {
  let authToken: string;
  let userId: string;

  beforeEach(async () => {
    // Clear users array before each test
    users.length = 0;

    // Register a test user
    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'testuser@example.com',
        password: 'password123',
        name: 'Test User',
      });

    authToken = registerResponse.body.data.token;
    userId = registerResponse.body.data.user.id;
  });

  describe('GET /api/users/profile', () => {
    it('should get user profile with valid token', async () => {
      const response = await request(app)
        .get('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id', userId);
      expect(response.body.data).toHaveProperty('email', 'testuser@example.com');
      expect(response.body.data).toHaveProperty('name', 'Test User');
      expect(response.body.data).not.toHaveProperty('password');
    });

    it('should return 401 without authentication token', async () => {
      const response = await request(app).get('/api/users/profile');

      expect(response.status).toBe(401);
      expect(response.body.success).toBe(false);
    });

    it('should return 403 with invalid token', async () => {
      const response = await request(app)
        .get('/api/users/profile')
        .set('Authorization', 'Bearer invalid-token');

      expect(response.status).toBe(403);
      expect(response.body.success).toBe(false);
    });
  });

  describe('PUT /api/users/profile', () => {
    it('should update user profile with valid data', async () => {
      const updateData = {
        name: 'Updated Name',
        birthDate: '1990-05-15',
        birthTime: '14:30',
        birthPlace: 'New York, NY',
        latitude: 40.7128,
        longitude: -74.0060,
        zodiacSign: 'Taurus',
        sunSign: 'Taurus',
        moonSign: 'Cancer',
        risingSign: 'Virgo',
      };

      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send(updateData);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Profile updated successfully');
      expect(response.body.data).toMatchObject(updateData);
      expect(response.body.data).not.toHaveProperty('password');
    });

    it('should update partial profile fields', async () => {
      const updateData = {
        birthDate: '1985-12-25',
        zodiacSign: 'Capricorn',
      };

      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send(updateData);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data.birthDate).toBe(updateData.birthDate);
      expect(response.body.data.zodiacSign).toBe(updateData.zodiacSign);
      expect(response.body.data.name).toBe('Test User'); // Original name unchanged
    });

    it('should validate birth date format', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ birthDate: 'invalid-date' });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
      expect(response.body.errors).toBeDefined();
    });

    it('should validate birth time format', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ birthTime: '25:99' });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
      expect(response.body.errors).toBeDefined();
    });

    it('should validate latitude range', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ latitude: 100 });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should validate longitude range', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ longitude: -200 });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should return 401 without authentication token', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .send({ name: 'New Name' });

      expect(response.status).toBe(401);
      expect(response.body.success).toBe(false);
    });

    it('should not allow updating password through profile endpoint', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ password: 'newpassword' });

      expect(response.status).toBe(200);
      // Verify the response doesn't include password field
      expect(response.body.data).not.toHaveProperty('password');
    });
  });
});
