// Statistics Dashboard Types

export interface DashboardStats {
  totalReadings: number;
  completedReadings: number;
  pendingReadings: number;
  avgReadingTime: number;
}

export interface ChartData {
  label: string;
  value: number;
  color?: string;
}

export interface TimeSeriesData {
  date: string;
  value: number;
  category: string;
}

export interface TodoItem {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
}

export interface AnalyticsMetric {
  name: string;
  value: number | string;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  unit?: string;
}

export interface FilterOptions {
  dateRange: {
    start: string;
    end: string;
  };
  category?: string;
  status?: string;
}

export interface WidgetData {
  id: string;
  title: string;
  type: 'stat' | 'chart' | 'list' | 'grid';
  data: any;
}
