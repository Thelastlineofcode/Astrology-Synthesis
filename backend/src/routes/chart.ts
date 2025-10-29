import { Router, Response } from 'express';
import { body, validationResult, query } from 'express-validator';
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

/**
 * @swagger
 * /api/charts:
 *   get:
 *     summary: Get all charts for authenticated user
 *     description: Retrieve all birth charts belonging to the authenticated user with pagination support
 *     tags: [Charts]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           minimum: 1
 *           default: 1
 *         description: Page number
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           minimum: 1
 *           maximum: 100
 *           default: 10
 *         description: Number of items per page
 *     responses:
 *       200:
 *         description: List of charts
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Chart'
 *                 pagination:
 *                   type: object
 *                   properties:
 *                     page:
 *                       type: integer
 *                       example: 1
 *                     limit:
 *                       type: integer
 *                       example: 10
 *                     total:
 *                       type: integer
 *                       example: 25
 *                     totalPages:
 *                       type: integer
 *                       example: 3
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 */
// Get all charts for authenticated user
router.get('/', 
  authenticateToken,
  [
    query('page').optional().isInt({ min: 1 }).toInt().withMessage('Page must be a positive integer'),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt().withMessage('Limit must be between 1 and 100'),
  ],
  (req: AuthRequest, res: Response) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({ success: false, errors: errors.array() });
      return;
    }

    const page = parseInt(req.query.page as string) || 1;
    const limit = parseInt(req.query.limit as string) || 10;
    
    const userCharts = charts.filter((chart) => chart.userId === req.user?.id);
    const total = userCharts.length;
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + limit;
    const paginatedCharts = userCharts.slice(startIndex, endIndex);

    res.json({
      success: true,
      data: paginatedCharts,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    });
});

/**
 * @swagger
 * /api/charts:
 *   post:
 *     summary: Create a new chart
 *     description: Create a new birth chart for the authenticated user
 *     tags: [Charts]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - birthDate
 *               - birthTime
 *               - latitude
 *               - longitude
 *             properties:
 *               name:
 *                 type: string
 *                 example: My Birth Chart
 *               birthDate:
 *                 type: string
 *                 format: date
 *                 example: 1990-01-15
 *               birthTime:
 *                 type: string
 *                 pattern: '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
 *                 example: '14:30'
 *               latitude:
 *                 type: number
 *                 minimum: -90
 *                 maximum: 90
 *                 example: 40.7128
 *               longitude:
 *                 type: number
 *                 minimum: -180
 *                 maximum: 180
 *                 example: -74.0060
 *     responses:
 *       201:
 *         description: Chart created successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: Chart created successfully
 *                 data:
 *                   $ref: '#/components/schemas/Chart'
 *       400:
 *         $ref: '#/components/responses/ValidationError'
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 */
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

/**
 * @swagger
 * /api/charts/{id}:
 *   get:
 *     summary: Get specific chart
 *     description: Retrieve a specific chart by ID for the authenticated user
 *     tags: [Charts]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Chart ID
 *     responses:
 *       200:
 *         description: Chart found
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   $ref: '#/components/schemas/Chart'
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 *       404:
 *         $ref: '#/components/responses/NotFoundError'
 */
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

/**
 * @swagger
 * /api/charts/{id}:
 *   put:
 *     summary: Update a chart
 *     description: Update an existing birth chart for the authenticated user
 *     tags: [Charts]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Chart ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *                 example: Updated Chart Name
 *               birthDate:
 *                 type: string
 *                 format: date
 *                 example: 1990-01-15
 *               birthTime:
 *                 type: string
 *                 pattern: '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
 *                 example: '14:30'
 *               latitude:
 *                 type: number
 *                 minimum: -90
 *                 maximum: 90
 *                 example: 40.7128
 *               longitude:
 *                 type: number
 *                 minimum: -180
 *                 maximum: 180
 *                 example: -74.0060
 *     responses:
 *       200:
 *         description: Chart updated successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: Chart updated successfully
 *                 data:
 *                   $ref: '#/components/schemas/Chart'
 *       400:
 *         $ref: '#/components/responses/ValidationError'
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 *       404:
 *         $ref: '#/components/responses/NotFoundError'
 */
router.put(
  '/:id',
  authenticateToken,
  [
    body('name').optional().notEmpty().withMessage('Chart name cannot be empty'),
    body('birthDate').optional().isISO8601().withMessage('Valid birth date is required'),
    body('birthTime').optional().matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/).withMessage('Valid time format required (HH:MM)'),
    body('latitude').optional().isFloat({ min: -90, max: 90 }).withMessage('Valid latitude required'),
    body('longitude').optional().isFloat({ min: -180, max: 180 }).withMessage('Valid longitude required'),
  ],
  (req: AuthRequest, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({ success: false, errors: errors.array() });
      return;
    }

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

    const { name, birthDate, birthTime, latitude, longitude } = req.body;
    const chart = charts[index];

    // Update only provided fields
    if (name !== undefined) chart.name = name;
    if (birthDate !== undefined) chart.birthDate = birthDate;
    if (birthTime !== undefined) chart.birthTime = birthTime;
    if (latitude !== undefined) chart.latitude = latitude;
    if (longitude !== undefined) chart.longitude = longitude;

    res.json({
      success: true,
      message: 'Chart updated successfully',
      data: chart,
    });
  }
);

/**
 * @swagger
 * /api/charts/{id}:
 *   delete:
 *     summary: Delete a chart
 *     description: Delete a specific chart by ID for the authenticated user
 *     tags: [Charts]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Chart ID
 *     responses:
 *       200:
 *         description: Chart deleted successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: Chart deleted successfully
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 *       404:
 *         $ref: '#/components/responses/NotFoundError'
 */
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

/**
 * @swagger
 * /api/charts/calculate:
 *   post:
 *     summary: Calculate birth chart
 *     description: Calculate astrological chart data for given birth information
 *     tags: [Calculations]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - birthDate
 *               - birthTime
 *               - latitude
 *               - longitude
 *             properties:
 *               birthDate:
 *                 type: string
 *                 format: date
 *                 example: 1990-01-15
 *               birthTime:
 *                 type: string
 *                 pattern: '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
 *                 example: '14:30'
 *               latitude:
 *                 type: number
 *                 minimum: -90
 *                 maximum: 90
 *                 example: 40.7128
 *               longitude:
 *                 type: number
 *                 minimum: -180
 *                 maximum: 180
 *                 example: -74.0060
 *               houseSystem:
 *                 type: string
 *                 enum: [Placidus, Koch, Whole Sign, Equal]
 *                 default: Placidus
 *                 example: Placidus
 *     responses:
 *       200:
 *         description: Chart calculated successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   $ref: '#/components/schemas/ChartCalculation'
 *       400:
 *         $ref: '#/components/responses/ValidationError'
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 */
router.post(
  '/calculate',
  authenticateToken,
  [
    body('birthDate').isISO8601().withMessage('Valid birth date is required'),
    body('birthTime').matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/).withMessage('Valid time format required (HH:MM)'),
    body('latitude').isFloat({ min: -90, max: 90 }).withMessage('Valid latitude required'),
    body('longitude').isFloat({ min: -180, max: 180 }).withMessage('Valid longitude required'),
    body('houseSystem').optional().isIn(['Placidus', 'Koch', 'Whole Sign', 'Equal']).withMessage('Invalid house system'),
  ],
  (req: AuthRequest, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({ success: false, errors: errors.array() });
      return;
    }

    const { birthDate, birthTime, latitude, longitude, houseSystem = 'Placidus' } = req.body;

    // Mock calculation result
    // In production, this would call Swiss Ephemeris or similar calculation engine
    const calculationResult = {
      planets: [
        { name: 'Sun', longitude: 295.5, latitude: 0.0, sign: 'Capricorn', house: 10, isRetrograde: false },
        { name: 'Moon', longitude: 123.2, latitude: 5.1, sign: 'Cancer', house: 4, isRetrograde: false },
        { name: 'Mercury', longitude: 280.3, latitude: -1.2, sign: 'Capricorn', house: 9, isRetrograde: true },
        { name: 'Venus', longitude: 310.8, latitude: 2.3, sign: 'Aquarius', house: 11, isRetrograde: false },
        { name: 'Mars', longitude: 45.6, latitude: -0.8, sign: 'Taurus', house: 1, isRetrograde: false },
      ],
      houses: [
        { number: 1, longitude: 120.5, sign: 'Cancer' },
        { number: 2, longitude: 150.3, sign: 'Leo' },
        { number: 3, longitude: 180.7, sign: 'Virgo' },
        { number: 4, longitude: 210.2, sign: 'Libra' },
        { number: 5, longitude: 240.8, sign: 'Scorpio' },
        { number: 6, longitude: 270.1, sign: 'Sagittarius' },
        { number: 7, longitude: 300.5, sign: 'Capricorn' },
        { number: 8, longitude: 330.3, sign: 'Aquarius' },
        { number: 9, longitude: 0.7, sign: 'Pisces' },
        { number: 10, longitude: 30.2, sign: 'Aries' },
        { number: 11, longitude: 60.8, sign: 'Taurus' },
        { number: 12, longitude: 90.1, sign: 'Gemini' },
      ],
      aspects: [
        { planet1: 'Sun', planet2: 'Moon', aspect: 'Trine', orb: 2.5 },
        { planet1: 'Sun', planet2: 'Mars', aspect: 'Square', orb: 1.2 },
        { planet1: 'Venus', planet2: 'Mars', aspect: 'Sextile', orb: 0.8 },
      ],
      metadata: {
        birthDate,
        birthTime,
        latitude,
        longitude,
        houseSystem,
        calculatedAt: new Date().toISOString(),
      },
    };

    res.json({
      success: true,
      data: calculationResult,
    });
  }
);

/**
 * @swagger
 * /api/charts/{id}/interpretation:
 *   get:
 *     summary: Get chart interpretation
 *     description: Get BMAD analysis and Symbolon card interpretations for a specific chart
 *     tags: [Calculations]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Chart ID
 *     responses:
 *       200:
 *         description: Interpretation generated successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   $ref: '#/components/schemas/ChartInterpretation'
 *       401:
 *         $ref: '#/components/responses/UnauthorizedError'
 *       404:
 *         $ref: '#/components/responses/NotFoundError'
 */
router.get('/:id/interpretation', authenticateToken, (req: AuthRequest, res: Response): void => {
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

  // Mock interpretation result
  // In production, this would call BMAD analysis engine and Symbolon interpretation service
  const interpretation = {
    chartId: chart.id,
    bmadAnalysis: {
      personalityProfile: {
        coreTraits: ['Leadership', 'Ambition', 'Practical'],
        strengths: ['Strategic thinking', 'Goal-oriented', 'Disciplined'],
        challenges: ['Workaholic tendencies', 'Emotional restraint'],
      },
      behaviorPredictions: {
        careerPath: 'Executive or entrepreneurial roles with high responsibility',
        relationships: 'Seeks stability and commitment, values loyalty',
        lifeThemes: 'Achievement, recognition, and building lasting legacy',
      },
    },
    symbolonCards: [
      {
        name: 'The Father (Sun in Capricorn)',
        meaning: 'Authority, responsibility, and achievement',
        position: 'Sun in Capricorn in 10th House',
        interpretation: 'Strong father archetype energy. Natural leader with high ambitions.',
      },
      {
        name: 'The Mother (Moon in Cancer)',
        meaning: 'Nurturing, emotional depth, and home',
        position: 'Moon in Cancer in 4th House',
        interpretation: 'Deep emotional sensitivity and connection to family roots.',
      },
    ],
    insights: 'This chart shows a powerful blend of ambition and emotional depth. The Sun in Capricorn in the 10th house indicates natural leadership abilities and career focus. The Moon in Cancer provides emotional intelligence and strong family values. The aspect patterns suggest challenges in balancing professional ambitions with personal life.',
    generatedAt: new Date().toISOString(),
  };

  res.json({
    success: true,
    data: interpretation,
  });
});

export default router;
