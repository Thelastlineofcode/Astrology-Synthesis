import { Router, Request, Response, NextFunction } from 'express';
import { body, validationResult } from 'express-validator';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { createError } from '../middleware/errorHandler';

const router = Router();

// In-memory user storage (replace with database in production)
const users: Array<{ id: string; email: string; password: string; name: string; role: 'user' | 'admin' }> = [];

// Register route
router.post(
  '/register',
  [
    body('email').isEmail().withMessage('Valid email is required'),
    body('password')
      .isLength({ min: 6 })
      .withMessage('Password must be at least 6 characters'),
    body('name').notEmpty().withMessage('Name is required'),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    try {
      const { email, password, name } = req.body;

      // Check if user exists
      const existingUser = users.find((u) => u.email === email);
      if (existingUser) {
        return next(createError('User already exists', 400));
      }

      // Hash password
      const hashedPassword = await bcrypt.hash(password, config.bcrypt.saltRounds);

      // Create user
      const user = {
        id: Date.now().toString(),
        email,
        password: hashedPassword,
        name,
        role: 'user' as 'user' | 'admin',
      };
      users.push(user);

      // Generate token
      const token = jwt.sign(
        { id: user.id, email: user.email, role: user.role },
        config.jwt.secret,
        { expiresIn: config.jwt.expiresIn } as jwt.SignOptions
      );

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        data: {
          user: { id: user.id, email: user.email, name: user.name, role: user.role },
          token,
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Login route
router.post(
  '/login',
  [
    body('email').isEmail().withMessage('Valid email is required'),
    body('password').notEmpty().withMessage('Password is required'),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    try {
      const { email, password } = req.body;

      // Find user
      const user = users.find((u) => u.email === email);
      if (!user) {
        return next(createError('Invalid credentials', 401));
      }

      // Verify password
      const isValidPassword = await bcrypt.compare(password, user.password);
      if (!isValidPassword) {
        return next(createError('Invalid credentials', 401));
      }

      // Generate token
      const token = jwt.sign(
        { id: user.id, email: user.email, role: user.role },
        config.jwt.secret,
        { expiresIn: config.jwt.expiresIn } as jwt.SignOptions
      );

      res.json({
        success: true,
        message: 'Login successful',
        data: {
          user: { id: user.id, email: user.email, name: user.name, role: user.role },
          token,
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Helper function to create initial admin user for testing
export const createAdminUser = async () => {
  const adminExists = users.find((u) => u.email === 'admin@roots-revealed.com');
  if (!adminExists) {
    const hashedPassword = await bcrypt.hash('admin123', config.bcrypt.saltRounds);
    users.push({
      id: 'admin-1',
      email: 'admin@roots-revealed.com',
      password: hashedPassword,
      name: 'Admin User',
      role: 'admin',
    });
  }
};

// Export users for admin routes
export const getUsers = () => users;

export default router;
