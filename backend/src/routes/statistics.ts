import { Router, Request, Response } from 'express';

const router = Router();

// Mock data for statistics
const mockStats = {
  totalReadings: 127,
  completedReadings: 89,
  pendingReadings: 38,
  avgCompletionTime: 24.5,
};

const mockReadingsByType = [
  { type: 'Natal Charts', count: 45, percentage: 35.4 },
  { type: 'Synastry', count: 32, percentage: 25.2 },
  { type: 'Transits', count: 28, percentage: 22.0 },
  { type: 'Solar Returns', count: 22, percentage: 17.3 },
];

const mockTrendData = [
  { date: '2025-10-01', readings: 12, completed: 8 },
  { date: '2025-10-08', readings: 15, completed: 11 },
  { date: '2025-10-15', readings: 18, completed: 14 },
  { date: '2025-10-22', readings: 20, completed: 17 },
  { date: '2025-10-29', readings: 16, completed: 12 },
];

const mockTasks = [
  { id: '1', title: 'Birth Chart Analysis 17', dueDate: '2025-10-29', status: 'pending', priority: 'high' },
  { id: '2', title: 'Synastry Reading', dueDate: '2025-10-30', status: 'in-progress', priority: 'medium' },
  { id: '3', title: 'Transit Report', dueDate: '2025-11-01', status: 'pending', priority: 'low' },
];

/**
 * GET /api/statistics/overview
 * Get overall statistics overview
 */
router.get('/overview', (_req: Request, res: Response) => {
  res.json({
    success: true,
    data: {
      stats: mockStats,
      lastUpdated: new Date().toISOString(),
    },
  });
});

/**
 * GET /api/statistics/readings-by-type
 * Get readings breakdown by type
 */
router.get('/readings-by-type', (req: Request, res: Response) => {
  const { startDate, endDate, categories } = req.query;
  
  let filteredData = [...mockReadingsByType];
  
  // Filter by categories if provided
  if (categories && typeof categories === 'string') {
    const categoryArray = categories.split(',');
    filteredData = filteredData.filter(item => 
      categoryArray.some(cat => item.type.toLowerCase().includes(cat.toLowerCase()))
    );
  }
  
  res.json({
    success: true,
    data: {
      readings: filteredData,
      filters: { startDate, endDate, categories },
    },
  });
});

/**
 * GET /api/statistics/trends
 * Get trend data over time
 */
router.get('/trends', (req: Request, res: Response) => {
  const { startDate, endDate, interval = 'week' } = req.query;
  
  let filteredData = [...mockTrendData];
  
  // Filter by date range if provided
  if (startDate && endDate) {
    filteredData = filteredData.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= new Date(startDate as string) && 
             itemDate <= new Date(endDate as string);
    });
  }
  
  res.json({
    success: true,
    data: {
      trends: filteredData,
      interval,
      filters: { startDate, endDate },
    },
  });
});

/**
 * GET /api/statistics/tasks
 * Get pending tasks and to-dos
 */
router.get('/tasks', (req: Request, res: Response) => {
  const { status, priority } = req.query;
  
  let filteredTasks = [...mockTasks];
  
  // Filter by status if provided
  if (status) {
    filteredTasks = filteredTasks.filter(task => task.status === status);
  }
  
  // Filter by priority if provided
  if (priority) {
    filteredTasks = filteredTasks.filter(task => task.priority === priority);
  }
  
  res.json({
    success: true,
    data: {
      tasks: filteredTasks,
      total: filteredTasks.length,
      filters: { status, priority },
    },
  });
});

/**
 * GET /api/statistics/insights
 * Get analytical insights and recommendations
 */
router.get('/insights', (_req: Request, res: Response) => {
  const insights = [
    {
      id: '1',
      type: 'trend',
      title: 'Increasing Demand',
      description: 'Your readings have increased by 12.5% this month compared to last month.',
      severity: 'positive',
      actionable: true,
      recommendation: 'Consider increasing availability for new clients.',
    },
    {
      id: '2',
      type: 'completion',
      title: 'High Completion Rate',
      description: 'You have maintained a 70% completion rate for the past 30 days.',
      severity: 'positive',
      actionable: false,
    },
    {
      id: '3',
      type: 'pending',
      title: 'Pending Readings',
      description: 'You have 38 pending readings. Focus on completing high-priority items first.',
      severity: 'warning',
      actionable: true,
      recommendation: 'Prioritize readings due within the next 3 days.',
    },
  ];
  
  res.json({
    success: true,
    data: {
      insights,
      generatedAt: new Date().toISOString(),
    },
  });
});

export default router;
