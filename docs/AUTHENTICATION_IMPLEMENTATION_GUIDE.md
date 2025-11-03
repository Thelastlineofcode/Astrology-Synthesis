# Authentication System Implementation Guide

## Quick Reference for Developers

This guide provides practical implementation details for the authentication system designed in `AUTHENTICATION_PRODUCT_DESIGN.md`.

---

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Backend Implementation](#backend-implementation)
3. [Frontend Implementation](#frontend-implementation)
4. [Testing Guide](#testing-guide)
5. [Deployment Checklist](#deployment-checklist)

---

## Environment Setup

### Required Environment Variables

Create a `.env` file in the backend directory:

```bash
# Server Configuration
NODE_ENV=development
PORT=5000

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=roots_revealed_db
DB_USER=roots_revealed_user
DB_PASSWORD=your_secure_password
DB_SSL=false

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production-min-32-chars
JWT_EXPIRES_IN=24h
JWT_REFRESH_SECRET=your-super-secret-refresh-key-change-in-production
JWT_REFRESH_EXPIRES_IN=7d

# Email Configuration (SendGrid)
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=noreply@rootsrevealed.com
FROM_NAME=Mula: The Root

# Alternative: Nodemailer (SMTP)
# EMAIL_PROVIDER=smtp
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your_email@gmail.com
# SMTP_PASS=your_app_password

# CORS Configuration
CORS_ORIGIN=http://localhost:3000,http://localhost:3001

# Bcrypt Configuration
BCRYPT_SALT_ROUNDS=10

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_CALLBACK_URL=http://localhost:5000/api/auth/google/callback

FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_CALLBACK_URL=http://localhost:5000/api/auth/facebook/callback
```

### Database Setup

Run the following SQL to set up the database:

```sql
-- Create database
CREATE DATABASE roots_revealed_db;

-- Connect to database
\c roots_revealed_db;

-- Create user
CREATE USER roots_revealed_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE roots_revealed_db TO roots_revealed_user;

-- Create tables (see DATABASE_SCHEMA.md for full schema)
-- Run migrations
```

---

## Backend Implementation

### 1. Install Dependencies

```bash
cd backend
npm install bcryptjs jsonwebtoken express-validator nodemailer pg
npm install --save-dev @types/bcryptjs @types/jsonwebtoken
```

### 2. Database Service Layer

Create `src/services/database.ts`:

```typescript
import { Pool } from 'pg';
import { config } from '../config';

export const pool = new Pool({
  host: config.database.host,
  port: config.database.port,
  database: config.database.name,
  user: config.database.user,
  password: config.database.password,
  ssl: config.database.ssl ? { rejectUnauthorized: false } : false,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected database error:', err);
  process.exit(-1);
});

export const query = async (text: string, params?: any[]) => {
  const start = Date.now();
  try {
    const result = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: result.rowCount });
    return result;
  } catch (error) {
    console.error('Database query error:', error);
    throw error;
  }
};
```

### 3. User Repository

Create `src/repositories/userRepository.ts`:

```typescript
import { query } from '../services/database';
import bcrypt from 'bcryptjs';
import { config } from '../config';

export interface User {
  id: number;
  uuid: string;
  email: string;
  username?: string;
  password_hash: string;
  first_name?: string;
  last_name?: string;
  birth_date?: Date;
  birth_time?: string;
  birth_location?: string;
  birth_latitude?: number;
  birth_longitude?: number;
  timezone?: string;
  is_active: boolean;
  is_verified: boolean;
  email_verified_at?: Date;
  failed_login_attempts: number;
  locked_until?: Date;
  created_at: Date;
  updated_at: Date;
  last_login?: Date;
  preferences: any;
}

export class UserRepository {
  async create(userData: {
    email: string;
    password: string;
    firstName?: string;
    lastName?: string;
    birthDate?: string;
    birthTime?: string;
    birthLocation?: string;
    timezone?: string;
  }): Promise<User> {
    const passwordHash = await bcrypt.hash(
      userData.password,
      config.bcrypt.saltRounds
    );

    const result = await query(
      `INSERT INTO users (
        email, password_hash, first_name, last_name,
        birth_date, birth_time, birth_location, timezone
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING id, uuid, email, first_name, last_name, 
                is_active, is_verified, created_at`,
      [
        userData.email,
        passwordHash,
        userData.firstName || null,
        userData.lastName || null,
        userData.birthDate || null,
        userData.birthTime || null,
        userData.birthLocation || null,
        userData.timezone || null,
      ]
    );

    return result.rows[0];
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return result.rows[0] || null;
  }

  async findById(id: number): Promise<User | null> {
    const result = await query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }

  async findByUuid(uuid: string): Promise<User | null> {
    const result = await query(
      'SELECT * FROM users WHERE uuid = $1',
      [uuid]
    );
    return result.rows[0] || null;
  }

  async updateLastLogin(userId: number): Promise<void> {
    await query(
      'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1',
      [userId]
    );
  }

  async incrementFailedAttempts(userId: number): Promise<void> {
    await query(
      `UPDATE users 
       SET failed_login_attempts = failed_login_attempts + 1
       WHERE id = $1`,
      [userId]
    );
  }

  async resetFailedAttempts(userId: number): Promise<void> {
    await query(
      'UPDATE users SET failed_login_attempts = 0 WHERE id = $1',
      [userId]
    );
  }

  async lockAccount(userId: number, lockDuration: number): Promise<void> {
    await query(
      `UPDATE users 
       SET locked_until = CURRENT_TIMESTAMP + INTERVAL '${lockDuration} minutes'
       WHERE id = $1`,
      [userId]
    );
  }

  async verifyEmail(userId: number): Promise<void> {
    await query(
      `UPDATE users 
       SET is_verified = TRUE, email_verified_at = CURRENT_TIMESTAMP
       WHERE id = $1`,
      [userId]
    );
  }

  async updatePassword(userId: number, newPassword: string): Promise<void> {
    const passwordHash = await bcrypt.hash(
      newPassword,
      config.bcrypt.saltRounds
    );
    await query(
      'UPDATE users SET password_hash = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2',
      [passwordHash, userId]
    );
  }

  async updateProfile(userId: number, updates: Partial<User>): Promise<User> {
    const fields: string[] = [];
    const values: any[] = [];
    let paramIndex = 1;

    Object.entries(updates).forEach(([key, value]) => {
      if (value !== undefined) {
        fields.push(`${key} = $${paramIndex}`);
        values.push(value);
        paramIndex++;
      }
    });

    if (fields.length === 0) {
      throw new Error('No fields to update');
    }

    fields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(userId);

    const result = await query(
      `UPDATE users SET ${fields.join(', ')} WHERE id = $${paramIndex}
       RETURNING *`,
      values
    );

    return result.rows[0];
  }

  async deleteUser(userId: number): Promise<void> {
    await query('DELETE FROM users WHERE id = $1', [userId]);
  }

  async verifyPassword(user: User, password: string): Promise<boolean> {
    return bcrypt.compare(password, user.password_hash);
  }
}
```

### 4. Session Repository

Create `src/repositories/sessionRepository.ts`:

```typescript
import { query } from '../services/database';

export interface Session {
  id: number;
  user_id: number;
  token_jti: string;
  refresh_token_jti?: string;
  expires_at: Date;
  ip_address?: string;
  user_agent?: string;
  device_info?: any;
  is_revoked: boolean;
  created_at: Date;
  last_activity: Date;
}

export class SessionRepository {
  async create(sessionData: {
    userId: number;
    tokenJti: string;
    refreshTokenJti?: string;
    expiresAt: Date;
    ipAddress?: string;
    userAgent?: string;
    deviceInfo?: any;
  }): Promise<Session> {
    const result = await query(
      `INSERT INTO sessions (
        user_id, token_jti, refresh_token_jti, expires_at,
        ip_address, user_agent, device_info
      ) VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *`,
      [
        sessionData.userId,
        sessionData.tokenJti,
        sessionData.refreshTokenJti || null,
        sessionData.expiresAt,
        sessionData.ipAddress || null,
        sessionData.userAgent || null,
        sessionData.deviceInfo || null,
      ]
    );
    return result.rows[0];
  }

  async findByTokenJti(tokenJti: string): Promise<Session | null> {
    const result = await query(
      'SELECT * FROM sessions WHERE token_jti = $1 AND is_revoked = FALSE',
      [tokenJti]
    );
    return result.rows[0] || null;
  }

  async findByUserId(userId: number): Promise<Session[]> {
    const result = await query(
      `SELECT * FROM sessions 
       WHERE user_id = $1 AND is_revoked = FALSE AND expires_at > CURRENT_TIMESTAMP
       ORDER BY created_at DESC`,
      [userId]
    );
    return result.rows;
  }

  async updateLastActivity(sessionId: number): Promise<void> {
    await query(
      'UPDATE sessions SET last_activity = CURRENT_TIMESTAMP WHERE id = $1',
      [sessionId]
    );
  }

  async revokeSession(sessionId: number): Promise<void> {
    await query(
      `UPDATE sessions 
       SET is_revoked = TRUE, revoked_at = CURRENT_TIMESTAMP
       WHERE id = $1`,
      [sessionId]
    );
  }

  async revokeAllUserSessions(userId: number, exceptSessionId?: number): Promise<number> {
    let queryText = `
      UPDATE sessions 
      SET is_revoked = TRUE, revoked_at = CURRENT_TIMESTAMP
      WHERE user_id = $1 AND is_revoked = FALSE
    `;
    const params: any[] = [userId];

    if (exceptSessionId) {
      queryText += ' AND id != $2';
      params.push(exceptSessionId);
    }

    const result = await query(queryText, params);
    return result.rowCount || 0;
  }

  async cleanupExpiredSessions(): Promise<number> {
    const result = await query(
      `DELETE FROM sessions 
       WHERE expires_at < CURRENT_TIMESTAMP OR 
             (is_revoked = TRUE AND revoked_at < CURRENT_TIMESTAMP - INTERVAL '30 days')`
    );
    return result.rowCount || 0;
  }
}
```

### 5. Email Service

Create `src/services/emailService.ts`:

```typescript
import nodemailer from 'nodemailer';
import { config } from '../config';

interface EmailOptions {
  to: string;
  subject: string;
  html: string;
  text?: string;
}

class EmailService {
  private transporter: nodemailer.Transporter;

  constructor() {
    if (process.env.EMAIL_PROVIDER === 'sendgrid') {
      // SendGrid configuration
      this.transporter = nodemailer.createTransport({
        host: 'smtp.sendgrid.net',
        port: 587,
        auth: {
          user: 'apikey',
          pass: process.env.SENDGRID_API_KEY,
        },
      });
    } else {
      // SMTP configuration
      this.transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: parseInt(process.env.SMTP_PORT || '587'),
        secure: false,
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS,
        },
      });
    }
  }

  async sendEmail(options: EmailOptions): Promise<void> {
    try {
      await this.transporter.sendMail({
        from: `"${process.env.FROM_NAME}" <${process.env.FROM_EMAIL}>`,
        to: options.to,
        subject: options.subject,
        html: options.html,
        text: options.text,
      });
      console.log(`Email sent to ${options.to}: ${options.subject}`);
    } catch (error) {
      console.error('Email sending failed:', error);
      throw error;
    }
  }

  async sendVerificationEmail(email: string, token: string, name: string): Promise<void> {
    const verificationUrl = `${process.env.FRONTEND_URL}/verify-email?token=${token}`;
    
    await this.sendEmail({
      to: email,
      subject: 'Verify Your Email Address - Mula: The Root',
      html: `
        <!DOCTYPE html>
        <html>
          <head>
            <style>
              body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
              .container { max-width: 600px; margin: 0 auto; padding: 20px; }
              .button { display: inline-block; padding: 12px 24px; background-color: #4F46E5; 
                        color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }
              .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; 
                       font-size: 12px; color: #666; }
            </style>
          </head>
          <body>
            <div class="container">
              <h2>Welcome to Mula: The Root, ${name}! ✨</h2>
              <p>Thank you for creating an account. Please verify your email address to unlock all features.</p>
              <a href="${verificationUrl}" class="button">Verify Email Address</a>
              <p>Or copy and paste this link into your browser:</p>
              <p style="word-break: break-all; color: #4F46E5;">${verificationUrl}</p>
              <p>This link will expire in 24 hours.</p>
              <div class="footer">
                <p>If you didn't create an account, please ignore this email.</p>
                <p>&copy; 2025 Mula: The Root. All rights reserved.</p>
              </div>
            </div>
          </body>
        </html>
      `,
      text: `Welcome to Mula: The Root, ${name}! Verify your email: ${verificationUrl}`,
    });
  }

  async sendPasswordResetEmail(email: string, token: string, name: string): Promise<void> {
    const resetUrl = `${process.env.FRONTEND_URL}/reset-password?token=${token}`;
    
    await this.sendEmail({
      to: email,
      subject: 'Reset Your Password - Mula: The Root',
      html: `
        <!DOCTYPE html>
        <html>
          <head>
            <style>
              body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
              .container { max-width: 600px; margin: 0 auto; padding: 20px; }
              .button { display: inline-block; padding: 12px 24px; background-color: #4F46E5; 
                        color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }
              .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; 
                       font-size: 12px; color: #666; }
              .warning { background-color: #FEF3C7; padding: 12px; border-radius: 6px; 
                        border-left: 4px solid #F59E0B; }
            </style>
          </head>
          <body>
            <div class="container">
              <h2>Password Reset Request</h2>
              <p>Hi ${name},</p>
              <p>We received a request to reset your password. Click the button below to create a new password:</p>
              <a href="${resetUrl}" class="button">Reset Password</a>
              <p>Or copy and paste this link into your browser:</p>
              <p style="word-break: break-all; color: #4F46E5;">${resetUrl}</p>
              <div class="warning">
                <strong>⚠️ Security Notice:</strong> This link will expire in 1 hour. 
                If you didn't request this reset, please ignore this email and ensure your account is secure.
              </div>
              <div class="footer">
                <p>&copy; 2025 Mula: The Root. All rights reserved.</p>
              </div>
            </div>
          </body>
        </html>
      `,
      text: `Reset your password: ${resetUrl}`,
    });
  }

  async sendPasswordChangedEmail(email: string, name: string): Promise<void> {
    await this.sendEmail({
      to: email,
      subject: 'Your Password Has Been Changed - Mula: The Root',
      html: `
        <!DOCTYPE html>
        <html>
          <head>
            <style>
              body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
              .container { max-width: 600px; margin: 0 auto; padding: 20px; }
              .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; 
                       font-size: 12px; color: #666; }
            </style>
          </head>
          <body>
            <div class="container">
              <h2>Password Changed Successfully</h2>
              <p>Hi ${name},</p>
              <p>This email confirms that your password was successfully changed.</p>
              <p><strong>If you made this change:</strong> No further action is needed.</p>
              <p><strong>If you didn't make this change:</strong> Please contact our support team immediately.</p>
              <div class="footer">
                <p>&copy; 2025 Mula: The Root. All rights reserved.</p>
              </div>
            </div>
          </body>
        </html>
      `,
      text: `Your password has been changed. Contact support if you didn't make this change.`,
    });
  }
}

export const emailService = new EmailService();
```

### 6. Updated Auth Routes

Update `src/routes/auth.ts` to use the new database layer:

```typescript
import { Router } from 'express';
import { body, validationResult } from 'express-validator';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';
import { config } from '../config';
import { UserRepository } from '../repositories/userRepository';
import { SessionRepository } from '../repositories/sessionRepository';
import { emailService } from '../services/emailService';
import { createError } from '../middleware/errorHandler';
import { authenticateToken, AuthRequest } from '../middleware/auth';

const router = Router();
const userRepo = new UserRepository();
const sessionRepo = new SessionRepository();

// Registration with database persistence
router.post(
  '/register',
  [
    body('email').isEmail().withMessage('Valid email is required'),
    body('password')
      .isLength({ min: 8 })
      .withMessage('Password must be at least 8 characters')
      .matches(/[A-Z]/)
      .withMessage('Password must contain at least one uppercase letter')
      .matches(/[0-9]/)
      .withMessage('Password must contain at least one number'),
    body('firstName').optional().trim(),
    body('lastName').optional().trim(),
  ],
  async (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    try {
      const { email, password, firstName, lastName, birthDate, birthTime, birthLocation, timezone } = req.body;

      // Check if user exists
      const existingUser = await userRepo.findByEmail(email);
      if (existingUser) {
        return next(createError('User already exists', 400));
      }

      // Create user
      const user = await userRepo.create({
        email,
        password,
        firstName,
        lastName,
        birthDate,
        birthTime,
        birthLocation,
        timezone,
      });

      // Generate tokens
      const tokenJti = uuidv4();
      const refreshTokenJti = uuidv4();
      
      const accessToken = jwt.sign(
        { sub: user.uuid, email: user.email, jti: tokenJti },
        config.jwt.secret,
        { expiresIn: config.jwt.expiresIn }
      );

      const refreshToken = jwt.sign(
        { sub: user.uuid, jti: refreshTokenJti },
        config.jwt.refreshSecret,
        { expiresIn: config.jwt.refreshExpiresIn }
      );

      // Create session
      await sessionRepo.create({
        userId: user.id,
        tokenJti,
        refreshTokenJti,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),
        ipAddress: req.ip,
        userAgent: req.get('user-agent'),
      });

      // Send verification email
      const verificationToken = jwt.sign(
        { sub: user.uuid, purpose: 'email-verification' },
        config.jwt.secret,
        { expiresIn: '24h' }
      );
      await emailService.sendVerificationEmail(
        user.email,
        verificationToken,
        firstName || 'there'
      );

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        data: {
          user: {
            id: user.uuid,
            email: user.email,
            firstName: user.first_name,
            lastName: user.last_name,
            isVerified: user.is_verified,
          },
          tokens: {
            accessToken,
            refreshToken,
            expiresIn: 86400,
          },
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Add more routes: login, logout, refresh, password reset, etc.
// See AUTHENTICATION_PRODUCT_DESIGN.md for full API specification

export default router;
```

---

## Frontend Implementation

### 1. Auth Context

Create `src/contexts/AuthContext.tsx`:

```typescript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  isVerified: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing token and load user
    const initAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authService.login(email, password);
    setUser(response.user);
    localStorage.setItem('accessToken', response.tokens.accessToken);
    localStorage.setItem('refreshToken', response.tokens.refreshToken);
  };

  const register = async (userData: any) => {
    const response = await authService.register(userData);
    setUser(response.user);
    localStorage.setItem('accessToken', response.tokens.accessToken);
    localStorage.setItem('refreshToken', response.tokens.refreshToken);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  };

  const refreshToken = async () => {
    const newToken = await authService.refreshToken();
    localStorage.setItem('accessToken', newToken);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### 2. Login Form Component

Create `src/components/auth/LoginForm.tsx`:

```typescript
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/router';

export const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? 'Logging in...' : 'Log In'}
      </button>
    </form>
  );
};
```

---

## Testing Guide

### Backend Tests

Create `src/__tests__/auth.integration.test.ts`:

```typescript
import request from 'supertest';
import app from '../index';
import { pool } from '../services/database';

describe('Authentication Integration Tests', () => {
  beforeAll(async () => {
    // Set up test database
    await pool.query('DELETE FROM users WHERE email LIKE \'%test.com\'');
  });

  afterAll(async () => {
    // Clean up
    await pool.query('DELETE FROM users WHERE email LIKE \'%test.com\'');
    await pool.end();
  });

  describe('POST /api/auth/register', () => {
    it('should register a new user successfully', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'newuser@test.com',
          password: 'SecurePass123',
          firstName: 'John',
          lastName: 'Doe',
        });

      expect(response.status).toBe(201);
      expect(response.body.success).toBe(true);
      expect(response.body.data.user.email).toBe('newuser@test.com');
      expect(response.body.data.tokens.accessToken).toBeDefined();
    });

    it('should reject duplicate email', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'newuser@test.com',
          password: 'SecurePass123',
        });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
    });

    it('should reject weak password', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'weakpass@test.com',
          password: 'weak',
        });

      expect(response.status).toBe(400);
      expect(response.body.errors).toBeDefined();
    });
  });

  describe('POST /api/auth/login', () => {
    it('should login with valid credentials', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'newuser@test.com',
          password: 'SecurePass123',
        });

      expect(response.status).toBe(200);
      expect(response.body.data.tokens.accessToken).toBeDefined();
    });

    it('should reject invalid password', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'newuser@test.com',
          password: 'WrongPassword',
        });

      expect(response.status).toBe(401);
    });
  });
});
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing (unit + integration)
- [ ] Environment variables set for production
- [ ] Database migrations applied
- [ ] SSL certificates configured
- [ ] Email service credentials verified
- [ ] CORS origins configured correctly
- [ ] Rate limiting tested
- [ ] Security audit completed
- [ ] API documentation updated

### Production Environment Variables

```bash
NODE_ENV=production
DB_SSL=true
JWT_SECRET=<strong-random-secret-min-64-chars>
JWT_REFRESH_SECRET=<different-strong-random-secret>
CORS_ORIGIN=https://rootsrevealed.com
FRONTEND_URL=https://rootsrevealed.com
```

### Post-Deployment

- [ ] Smoke tests on production
- [ ] Monitor error logs
- [ ] Check email delivery
- [ ] Verify SSL/TLS configuration
- [ ] Test login/registration flows
- [ ] Monitor performance metrics
- [ ] Set up alerting thresholds

---

## Troubleshooting

### Common Issues

**Database connection fails:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U roots_revealed_user -d roots_revealed_db
```

**Email not sending:**
- Verify SendGrid API key
- Check email logs in console
- Test with Mailtrap or similar service first

**JWT token errors:**
- Ensure JWT_SECRET is set and consistent
- Check token expiration settings
- Verify token format (Bearer <token>)

---

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)

---

*Last Updated: October 29, 2025*
