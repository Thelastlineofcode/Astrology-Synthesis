import express, { Application } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { errorHandler } from './middleware/errorHandler';
import healthRouter from './routes/health';
import authRouter, { createAdminUser } from './routes/auth';
import chartRouter from './routes/chart';
import adminRouter from './routes/admin';

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

// Initialize admin user
createAdminUser().catch(console.error);

// Routes
app.use('/api/health', healthRouter);
app.use('/api/auth', authRouter);
app.use('/api/charts', chartRouter);
app.use('/api/admin', adminRouter);

// Root route
app.get('/', (_req, res) => {
  res.json({
    message: 'Roots Revealed API',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      auth: '/api/auth',
      charts: '/api/charts',
      admin: '/api/admin',
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
