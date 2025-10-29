import express, { Application } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import swaggerUi from 'swagger-ui-express';
import { errorHandler } from './middleware/errorHandler';
import { swaggerSpec } from './config/swagger';
import healthRouter from './routes/health';
import authRouter from './routes/auth';
import chartRouter from './routes/chart';

// Load environment variables
dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true,
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Swagger Documentation
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'Roots Revealed API Docs',
}));

// Swagger JSON endpoint
app.get('/api-docs.json', (_req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.send(swaggerSpec);
});

// Routes
app.use('/api/health', healthRouter);
app.use('/api/auth', authRouter);
app.use('/api/charts', chartRouter);

// Root route
/**
 * @swagger
 * /:
 *   get:
 *     summary: API information
 *     description: Get basic information about the API and available endpoints
 *     tags: [Health]
 *     responses:
 *       200:
 *         description: API information
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                   example: Roots Revealed API
 *                 version:
 *                   type: string
 *                   example: 1.0.0
 *                 endpoints:
 *                   type: object
 *                   properties:
 *                     health:
 *                       type: string
 *                       example: /api/health
 *                     auth:
 *                       type: string
 *                       example: /api/auth
 *                     charts:
 *                       type: string
 *                       example: /api/charts
 */
app.get('/', (_req, res) => {
  res.json({
    message: 'Roots Revealed API',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      auth: '/api/auth',
      charts: '/api/charts',
      docs: '/api-docs',
    },
  });
});

// Error handling middleware (should be last)
app.use(errorHandler);

// Start server
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
  });
}

export default app;
