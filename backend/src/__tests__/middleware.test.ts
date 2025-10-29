import { Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { authenticateToken, AuthRequest } from '../middleware/auth';
import { config } from '../config';

describe('Auth Middleware', () => {
  let mockRequest: Partial<AuthRequest>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction;

  beforeEach(() => {
    mockRequest = {
      headers: {},
    };
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
    };
    nextFunction = jest.fn();
  });

  describe('authenticateToken', () => {
    it('should authenticate valid token', () => {
      const token = jwt.sign(
        { id: '123', email: 'test@example.com' },
        config.jwt.secret,
        { expiresIn: '1h' }
      );

      mockRequest.headers = {
        authorization: `Bearer ${token}`,
      };

      authenticateToken(
        mockRequest as AuthRequest,
        mockResponse as Response,
        nextFunction
      );

      expect(nextFunction).toHaveBeenCalled();
      expect(mockRequest.user).toBeDefined();
      expect(mockRequest.user?.id).toBe('123');
      expect(mockRequest.user?.email).toBe('test@example.com');
      
      // nextFunction should have been called without error
      const errorArg = (nextFunction as jest.Mock).mock.calls[0][0];
      expect(errorArg).toBeUndefined();
    });

    it('should call next with error when no authorization header', () => {
      authenticateToken(
        mockRequest as AuthRequest,
        mockResponse as Response,
        nextFunction
      );

      expect(nextFunction).toHaveBeenCalled();
      const error = (nextFunction as jest.Mock).mock.calls[0][0];
      expect(error).toBeDefined();
      expect(error.message).toBe('Access token required');
      expect(error.statusCode).toBe(401);
    });

    it('should call next with error for invalid token format', () => {
      mockRequest.headers = {
        authorization: 'InvalidFormat token123',
      };

      authenticateToken(
        mockRequest as AuthRequest,
        mockResponse as Response,
        nextFunction
      );

      expect(nextFunction).toHaveBeenCalled();
      const error = (nextFunction as jest.Mock).mock.calls[0][0];
      expect(error).toBeDefined();
      expect(error.message).toBe('Invalid or expired token');
      expect(error.statusCode).toBe(403);
    });

    it('should call next with error for expired token', () => {
      const expiredToken = jwt.sign(
        { id: '123', email: 'test@example.com' },
        config.jwt.secret,
        { expiresIn: '-1h' } // Already expired
      );

      mockRequest.headers = {
        authorization: `Bearer ${expiredToken}`,
      };

      authenticateToken(
        mockRequest as AuthRequest,
        mockResponse as Response,
        nextFunction
      );

      expect(nextFunction).toHaveBeenCalled();
      const error = (nextFunction as jest.Mock).mock.calls[0][0];
      expect(error).toBeDefined();
      expect(error.message).toBe('Invalid or expired token');
      expect(error.statusCode).toBe(403);
    });

    it('should call next with error for token with invalid signature', () => {
      const invalidToken = jwt.sign(
        { id: '123', email: 'test@example.com' },
        'wrong-secret',
        { expiresIn: '1h' }
      );

      mockRequest.headers = {
        authorization: `Bearer ${invalidToken}`,
      };

      authenticateToken(
        mockRequest as AuthRequest,
        mockResponse as Response,
        nextFunction
      );

      expect(nextFunction).toHaveBeenCalled();
      const error = (nextFunction as jest.Mock).mock.calls[0][0];
      expect(error).toBeDefined();
      expect(error.message).toBe('Invalid or expired token');
      expect(error.statusCode).toBe(403);
    });

    it('should call next with error for malformed token', () => {
      mockRequest.headers = {
        authorization: 'Bearer not-a-valid-jwt-token',
      };

      authenticateToken(
        mockRequest as AuthRequest,
        mockResponse as Response,
        nextFunction
      );

      expect(nextFunction).toHaveBeenCalled();
      const error = (nextFunction as jest.Mock).mock.calls[0][0];
      expect(error).toBeDefined();
      expect(error.message).toBe('Invalid or expired token');
      expect(error.statusCode).toBe(403);
    });
  });
});
