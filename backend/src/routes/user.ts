import { Router, Response, NextFunction } from 'express';
import { body, validationResult } from 'express-validator';
import { authenticateToken, AuthRequest } from '../middleware/auth';
import { createError } from '../middleware/errorHandler';
import { users } from './auth';

const router = Router();

// GET /api/users/profile - Get current user's profile
router.get('/profile', authenticateToken, async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const userId = req.user?.id;
    const user = users.find((u) => u.id === userId);

    if (!user) {
      return next(createError('User not found', 404));
    }

    // Return user without password
    const { password, ...userProfile } = user;
    
    res.json({
      success: true,
      data: userProfile,
    });
  } catch (error) {
    next(error);
  }
});

// PUT /api/users/profile - Update current user's profile
router.put(
  '/profile',
  authenticateToken,
  [
    body('name').optional().notEmpty().withMessage('Name cannot be empty'),
    body('birthDate').optional().isISO8601().withMessage('Valid birth date required (ISO 8601 format)'),
    body('birthTime').optional().matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/).withMessage('Valid time required (HH:MM format)'),
    body('birthPlace').optional().isString().withMessage('Birth place must be a string'),
    body('latitude').optional().isFloat({ min: -90, max: 90 }).withMessage('Valid latitude required (-90 to 90)'),
    body('longitude').optional().isFloat({ min: -180, max: 180 }).withMessage('Valid longitude required (-180 to 180)'),
    body('zodiacSign').optional().isString().withMessage('Zodiac sign must be a string'),
    body('sunSign').optional().isString().withMessage('Sun sign must be a string'),
    body('moonSign').optional().isString().withMessage('Moon sign must be a string'),
    body('risingSign').optional().isString().withMessage('Rising sign must be a string'),
  ],
  async (req: AuthRequest, res: Response, next: NextFunction) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    try {
      const userId = req.user?.id;
      const userIndex = users.findIndex((u) => u.id === userId);

      if (userIndex === -1) {
        return next(createError('User not found', 404));
      }

      // Update allowed fields
      const allowedUpdates = [
        'name',
        'birthDate',
        'birthTime',
        'birthPlace',
        'latitude',
        'longitude',
        'zodiacSign',
        'sunSign',
        'moonSign',
        'risingSign',
      ];

      const updates: any = {};
      allowedUpdates.forEach((field) => {
        if (req.body[field] !== undefined) {
          updates[field] = req.body[field];
        }
      });

      // Update user
      users[userIndex] = {
        ...users[userIndex],
        ...updates,
        updatedAt: new Date().toISOString(),
      };

      const { password, ...userProfile } = users[userIndex];

      res.json({
        success: true,
        message: 'Profile updated successfully',
        data: userProfile,
      });
    } catch (error) {
      next(error);
    }
  }
);

export default router;
