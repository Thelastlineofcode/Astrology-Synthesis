import { Router, Response } from 'express';
import { body, validationResult } from 'express-validator';
import { authenticateToken, AuthRequest } from '../middleware/auth';

const router = Router();

// In-memory chart storage (replace with database in production)
const charts: Array<{
  id: string;
  userId: string;
  name: string;
  birthDate: string;
  birthTime: string;
  latitude: number;
  longitude: number;
  createdAt: string;
}> = [];

// Get all charts for authenticated user
router.get('/', authenticateToken, (req: AuthRequest, res: Response) => {
  const userCharts = charts.filter((chart) => chart.userId === req.user?.id);
  res.json({
    success: true,
    data: userCharts,
  });
});

// Create new chart
router.post(
  '/',
  authenticateToken,
  [
    body('name').notEmpty().withMessage('Chart name is required'),
    body('birthDate').isISO8601().withMessage('Valid birth date is required'),
    body('birthTime').matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/).withMessage('Valid time format required (HH:MM)'),
    body('latitude').isFloat({ min: -90, max: 90 }).withMessage('Valid latitude required'),
    body('longitude').isFloat({ min: -180, max: 180 }).withMessage('Valid longitude required'),
  ],
  (req: AuthRequest, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({ success: false, errors: errors.array() });
      return;
    }

    const { name, birthDate, birthTime, latitude, longitude } = req.body;

    const chart = {
      id: Date.now().toString(),
      userId: req.user!.id,
      name,
      birthDate,
      birthTime,
      latitude,
      longitude,
      createdAt: new Date().toISOString(),
    };

    charts.push(chart);

    res.status(201).json({
      success: true,
      message: 'Chart created successfully',
      data: chart,
    });
  }
);

// Get specific chart
router.get('/:id', authenticateToken, (req: AuthRequest, res: Response): void => {
  const chart = charts.find(
    (c) => c.id === req.params.id && c.userId === req.user?.id
  );

  if (!chart) {
    res.status(404).json({
      success: false,
      error: { message: 'Chart not found' },
    });
    return;
  }

  res.json({
    success: true,
    data: chart,
  });
});

// Delete chart
router.delete('/:id', authenticateToken, (req: AuthRequest, res: Response): void => {
  const index = charts.findIndex(
    (c) => c.id === req.params.id && c.userId === req.user?.id
  );

  if (index === -1) {
    res.status(404).json({
      success: false,
      error: { message: 'Chart not found' },
    });
    return;
  }

  charts.splice(index, 1);

  res.json({
    success: true,
    message: 'Chart deleted successfully',
  });
});

export default router;
