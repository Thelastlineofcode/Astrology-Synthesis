import { Router, Request, Response, NextFunction } from 'express';
import { body, validationResult } from 'express-validator';
import bcrypt from 'bcryptjs';
import { config } from '../config';
import { authenticateAdmin, AuthRequest } from '../middleware/auth';
import { createError } from '../middleware/errorHandler';
import { getUsers } from './auth';

const router = Router();

// All admin routes require admin authentication
router.use(authenticateAdmin);

// NOTE: In production, these routes should be rate-limited to prevent abuse.
// Consider using express-rate-limit or similar middleware.
// Example: router.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

// Get all users (admin only)
router.get('/users', (_req: Request, res: Response, next: NextFunction) => {
  try {
    const users = getUsers();
    const sanitizedUsers = users.map((user) => ({
      id: user.id,
      email: user.email,
      name: user.name,
      role: user.role,
    }));

    res.json({
      success: true,
      data: {
        users: sanitizedUsers,
        total: sanitizedUsers.length,
      },
    });
  } catch (error) {
    next(error);
  }
});

// Get single user by ID (admin only)
router.get('/users/:id', (req: Request, res: Response, next: NextFunction) => {
  try {
    const users = getUsers();
    const user = users.find((u) => u.id === req.params.id);

    if (!user) {
      return next(createError('User not found', 404));
    }

    res.json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role,
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

// Create user (admin only)
router.post(
  '/users',
  [
    body('email').isEmail().withMessage('Valid email is required'),
    body('password')
      .isLength({ min: 6 })
      .withMessage('Password must be at least 6 characters'),
    body('name').notEmpty().withMessage('Name is required'),
    body('role').isIn(['user', 'admin']).withMessage('Role must be user or admin'),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    try {
      const { email, password, name, role } = req.body;
      const users = getUsers();

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
        role,
      };
      users.push(user);

      res.status(201).json({
        success: true,
        message: 'User created successfully',
        data: {
          user: { id: user.id, email: user.email, name: user.name, role: user.role },
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Update user (admin only)
router.put(
  '/users/:id',
  [
    body('email').optional().isEmail().withMessage('Valid email is required'),
    body('name').optional().notEmpty().withMessage('Name cannot be empty'),
    body('role')
      .optional()
      .isIn(['user', 'admin'])
      .withMessage('Role must be user or admin'),
    body('password')
      .optional()
      .isLength({ min: 6 })
      .withMessage('Password must be at least 6 characters'),
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    try {
      const users = getUsers();
      const userIndex = users.findIndex((u) => u.id === req.params.id);

      if (userIndex === -1) {
        return next(createError('User not found', 404));
      }

      const { email, name, role, password } = req.body;

      if (email) users[userIndex].email = email;
      if (name) users[userIndex].name = name;
      if (role) users[userIndex].role = role;
      if (password) {
        users[userIndex].password = await bcrypt.hash(password, config.bcrypt.saltRounds);
      }

      res.json({
        success: true,
        message: 'User updated successfully',
        data: {
          user: {
            id: users[userIndex].id,
            email: users[userIndex].email,
            name: users[userIndex].name,
            role: users[userIndex].role,
          },
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// Delete user (admin only)
router.delete('/users/:id', (req: Request, res: Response, next: NextFunction) => {
  try {
    const users = getUsers();
    const userIndex = users.findIndex((u) => u.id === req.params.id);

    if (userIndex === -1) {
      return next(createError('User not found', 404));
    }

    // Prevent deleting the last admin
    if (users[userIndex].role === 'admin') {
      const adminCount = users.filter((u) => u.role === 'admin').length;
      if (adminCount <= 1) {
        return next(createError('Cannot delete the last admin user', 400));
      }
    }

    users.splice(userIndex, 1);

    res.json({
      success: true,
      message: 'User deleted successfully',
    });
  } catch (error) {
    next(error);
  }
});

// Get platform statistics (admin only)
router.get('/stats', (_req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const users = getUsers();
    const totalUsers = users.length;
    const adminUsers = users.filter((u) => u.role === 'admin').length;
    const regularUsers = users.filter((u) => u.role === 'user').length;

    res.json({
      success: true,
      data: {
        users: {
          total: totalUsers,
          admins: adminUsers,
          regular: regularUsers,
        },
        system: {
          uptime: process.uptime(),
          nodeVersion: process.version,
          platform: process.platform,
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

export default router;
