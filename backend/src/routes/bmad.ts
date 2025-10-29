/**
 * BMAD Pattern Recognition API Routes
 */

import { Router, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import { BMADPatternRecognizer } from '../services/bmad/patternRecognizer';
import { BirthData, PatternCategory } from '../services/bmad/types';

const router = Router();
const recognizer = new BMADPatternRecognizer();

/**
 * POST /api/bmad/analyze
 * Analyze birth data for BMAD patterns
 */
router.post(
  '/analyze',
  [
    body('year').isInt({ min: 1900, max: 2100 }).withMessage('Valid year required (1900-2100)'),
    body('month').isInt({ min: 1, max: 12 }).withMessage('Valid month required (1-12)'),
    body('day').isInt({ min: 1, max: 31 }).withMessage('Valid day required (1-31)'),
    body('hour').optional().isInt({ min: 0, max: 23 }).withMessage('Valid hour required (0-23)'),
    body('minute')
      .optional()
      .isInt({ min: 0, max: 59 })
      .withMessage('Valid minute required (0-59)'),
  ],
  (req: Request, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({
        success: false,
        errors: errors.array(),
      });
      return;
    }

    try {
      const birthData: BirthData = {
        year: req.body.year,
        month: req.body.month,
        day: req.body.day,
        hour: req.body.hour,
        minute: req.body.minute,
      };

      const analysis = recognizer.analyze(birthData);

      res.json({
        success: true,
        data: analysis,
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Analysis failed',
        },
      });
    }
  }
);

/**
 * POST /api/bmad/detect
 * Detect patterns only (without full analysis)
 */
router.post(
  '/detect',
  [
    body('year').isInt({ min: 1900, max: 2100 }).withMessage('Valid year required (1900-2100)'),
    body('month').isInt({ min: 1, max: 12 }).withMessage('Valid month required (1-12)'),
    body('day').isInt({ min: 1, max: 31 }).withMessage('Valid day required (1-31)'),
  ],
  (req: Request, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({
        success: false,
        errors: errors.array(),
      });
      return;
    }

    try {
      const birthData: BirthData = {
        year: req.body.year,
        month: req.body.month,
        day: req.body.day,
      };

      const patterns = recognizer.detectPatterns(birthData);

      res.json({
        success: true,
        data: {
          birthData,
          patterns,
          count: patterns.length,
        },
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Detection failed',
        },
      });
    }
  }
);

/**
 * POST /api/bmad/patterns/category
 * Get patterns by specific category
 */
router.post(
  '/patterns/category',
  [
    body('year').isInt({ min: 1900, max: 2100 }).withMessage('Valid year required'),
    body('month').isInt({ min: 1, max: 12 }).withMessage('Valid month required'),
    body('day').isInt({ min: 1, max: 31 }).withMessage('Valid day required'),
    body('category').isIn(Object.values(PatternCategory)).withMessage('Valid category required'),
  ],
  (req: Request, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({
        success: false,
        errors: errors.array(),
      });
      return;
    }

    try {
      const birthData: BirthData = {
        year: req.body.year,
        month: req.body.month,
        day: req.body.day,
      };

      const category = req.body.category as PatternCategory;
      const patterns = recognizer.getPatternsByCategory(birthData, category);

      res.json({
        success: true,
        data: {
          birthData,
          category,
          patterns,
          count: patterns.length,
        },
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Category filter failed',
        },
      });
    }
  }
);

/**
 * POST /api/bmad/compare
 * Compare two birth dates for pattern compatibility
 */
router.post(
  '/compare',
  [
    body('birthData1.year').isInt({ min: 1900, max: 2100 }),
    body('birthData1.month').isInt({ min: 1, max: 12 }),
    body('birthData1.day').isInt({ min: 1, max: 31 }),
    body('birthData2.year').isInt({ min: 1900, max: 2100 }),
    body('birthData2.month').isInt({ min: 1, max: 12 }),
    body('birthData2.day').isInt({ min: 1, max: 31 }),
  ],
  (req: Request, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({
        success: false,
        errors: errors.array(),
      });
      return;
    }

    try {
      const birthData1: BirthData = req.body.birthData1;
      const birthData2: BirthData = req.body.birthData2;

      const comparison = recognizer.comparePatterns(birthData1, birthData2);

      res.json({
        success: true,
        data: {
          birthData1,
          birthData2,
          comparison,
        },
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Comparison failed',
        },
      });
    }
  }
);

/**
 * GET /api/bmad/categories
 * Get available pattern categories
 */
router.get('/categories', (_req: Request, res: Response) => {
  res.json({
    success: true,
    data: {
      categories: Object.values(PatternCategory),
      descriptions: {
        [PatternCategory.NUMERIC]: 'Numerological patterns in birth data',
        [PatternCategory.CYCLIC]: 'Recurring and cyclical patterns',
        [PatternCategory.HARMONIC]: 'Harmonious and balanced patterns',
        [PatternCategory.SEQUENTIAL]: 'Sequential number patterns',
        [PatternCategory.MASTER_NUMBER]: 'Master numbers (11, 22, 33)',
        [PatternCategory.REPETITIVE]: 'Repeated digits and numbers',
        [PatternCategory.SYMBOLIC]: 'Symbolically significant numbers',
      },
    },
  });
});

/**
 * POST /api/bmad/high-confidence
 * Get high confidence patterns only
 */
router.post(
  '/high-confidence',
  [
    body('year').isInt({ min: 1900, max: 2100 }),
    body('month').isInt({ min: 1, max: 12 }),
    body('day').isInt({ min: 1, max: 31 }),
    body('minConfidence')
      .optional()
      .isFloat({ min: 0, max: 1 })
      .withMessage('Confidence must be between 0 and 1'),
  ],
  (req: Request, res: Response): void => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      res.status(400).json({
        success: false,
        errors: errors.array(),
      });
      return;
    }

    try {
      const birthData: BirthData = {
        year: req.body.year,
        month: req.body.month,
        day: req.body.day,
      };

      const minConfidence = req.body.minConfidence || 0.9;
      const patterns = recognizer.getHighConfidencePatterns(birthData, minConfidence);

      res.json({
        success: true,
        data: {
          birthData,
          minConfidence,
          patterns,
          count: patterns.length,
        },
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'High confidence filter failed',
        },
      });
    }
  }
);

export default router;
