import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { createError } from './errorHandler';

export interface AuthRequest extends Request {
  user?: {
    id: string;
    email: string;
    role: 'user' | 'admin';
  };
}

export const authenticateToken = (
  req: AuthRequest,
  _res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return next(createError('Access token required', 401));
  }

  try {
    const decoded = jwt.verify(token, config.jwt.secret) as {
      id: string;
      email: string;
      role: 'user' | 'admin';
    };
    req.user = decoded;
    next();
  } catch (error) {
    return next(createError('Invalid or expired token', 403));
  }
};

// Admin authentication middleware
export const authenticateAdmin = (
  req: AuthRequest,
  _res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return next(createError('Access token required', 401));
  }

  try {
    const decoded = jwt.verify(token, config.jwt.secret) as {
      id: string;
      email: string;
      role: 'user' | 'admin';
    };
    
    if (decoded.role !== 'admin') {
      return next(createError('Admin access required', 403));
    }
    
    req.user = decoded;
    next();
  } catch (error) {
    return next(createError('Invalid or expired token', 403));
  }
};
