'use client';

import React, { useState } from 'react';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar';
import DashboardHeader from '@/components/dashboard/DashboardHeader';
import TabNavigation from '@/components/dashboard/TabNavigation';
import StatCard from '@/components/dashboard/StatCard';
import ListWidget from '@/components/dashboard/ListWidget';
import ChartWidget from '@/components/dashboard/ChartWidget';
import DateRangeFilter from '@/components/dashboard/DateRangeFilter';
import CategoryFilter from '@/components/dashboard/CategoryFilter';

// Mock data for demonstration
const mockStats = {
  totalReadings: 127,
  completedReadings: 89,
  pendingReadings: 38,
  avgCompletionTime: 24.5,
};

const mockTodos = [
  { id: '1', title: 'Birth Chart Analysis 17', subtitle: 'Due today', status: 'Pending' },
  { id: '2', title: 'Synastry Reading', subtitle: 'Due tomorrow', status: 'In Progress' },
  { id: '3', title: 'Transit Report', subtitle: 'Due in 3 days', status: 'Pending' },
];

const mockHolds = [
  { id: '1', title: 'Solar Return Analysis 17', subtitle: 'Client: Sarah M.', status: 'On Hold' },
  { id: '2', title: 'Natal Chart Review', subtitle: 'Client: John D.', status: 'Waiting' },
  { id: '3', title: 'Progressed Chart', subtitle: 'Client: Emma W.', status: 'On Hold' },
];

const mockInbox = [
  { id: '1', title: 'Chart Reading Request', subtitle: 'April 12, 2019, 8:00 am' },
  { id: '2', title: 'Follow-up Consultation', subtitle: 'April 12, 2019, 8:00 am' },
  { id: '3', title: 'New Client Inquiry', subtitle: 'April 12, 2019, 8:00 am' },
  { id: '4', title: 'Reading Feedback', subtitle: 'April 12, 2019, 8:00 am' },
];

const mockChartData = [
  { label: 'Natal Charts', value: 45, color: 'var(--color-primary)' },
  { label: 'Synastry Readings', value: 32, color: 'var(--color-secondary)' },
  { label: 'Transit Reports', value: 28, color: 'var(--color-accent)' },
  { label: 'Solar Returns', value: 22, color: 'var(--color-cta)' },
];

const tabs = [
  { id: 'general', label: 'General' },
  { id: 'studies', label: 'Studies' },
  { id: 'finance', label: 'Finance' },
  { id: 'teaching', label: 'Teaching' },
];

const categories = [
  'Natal Charts',
  'Synastry',
  'Transits',
  'Solar Returns',
  'Progressions',
  'Composite Charts',
];

export default function StatisticsPage() {
  const [activeTab, setActiveTab] = useState('general');
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);

  const handleDateRangeChange = (start: string, end: string) => {
    setDateRange({ start, end });
    // In a real app, you would fetch filtered data here
    console.log('Date range changed:', { start, end });
  };

  const handleCategoryChange = (categories: string[]) => {
    setSelectedCategories(categories);
    // In a real app, you would fetch filtered data here
    console.log('Categories changed:', categories);
  };

  return (
    <div className="flex min-h-screen bg-[var(--bg-primary)]">
      <DashboardSidebar currentPath="/dashboard/statistics" />
      
      <div className="flex-1 flex flex-col">
        <DashboardHeader userName="George" title="Dashboard" />
        
        <div className="p-6">
          {/* Tab Navigation */}
          <div className="mb-6 flex items-center justify-between">
            <TabNavigation tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />
            <div className="flex items-center gap-2">
              <button 
                onClick={() => setShowFilters(!showFilters)}
                className={`flex items-center gap-2 px-4 py-2 text-sm border border-[var(--border-color)] rounded-lg transition-colors ${
                  showFilters 
                    ? 'bg-[var(--color-primary)] text-white' 
                    : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
                }`}
              >
                <span>🔍</span>
                Filters
              </button>
              <button className="flex items-center gap-2 px-4 py-2 text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] border border-[var(--border-color)] rounded-lg">
                <span>⚙️</span>
                Edit My Widgets
              </button>
            </div>
          </div>

          {/* Filters Section */}
          {showFilters && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
              <DateRangeFilter onFilterChange={handleDateRangeChange} />
              <CategoryFilter 
                categories={categories}
                selectedCategories={selectedCategories}
                onFilterChange={handleCategoryChange}
              />
            </div>
          )}

          {/* Key Metrics Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <StatCard 
              title="Total Readings" 
              value={mockStats.totalReadings} 
              change={12.5}
              trend="up"
            />
            <StatCard 
              title="Completed" 
              value={mockStats.completedReadings} 
              change={8.3}
              trend="up"
            />
            <StatCard 
              title="Pending" 
              value={mockStats.pendingReadings} 
              change={-3.2}
              trend="down"
            />
            <StatCard 
              title="Avg. Time" 
              value={mockStats.avgCompletionTime} 
              unit="hours"
              trend="neutral"
            />
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left Column */}
            <div className="space-y-6">
              <ListWidget 
                title="To Dos" 
                items={mockTodos}
                viewMoreLink="#"
                emptyMessage="No pending tasks"
              />
              
              <ChartWidget 
                title="Reading Types Distribution"
                data={mockChartData}
                type="bar"
              />
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              <ListWidget 
                title="Holds" 
                items={mockHolds}
                viewMoreLink="#"
                emptyMessage="No items on hold"
              />
              
              <ListWidget 
                title="Inbox" 
                items={mockInbox}
                viewMoreLink="#"
                emptyMessage="No messages"
              />
            </div>
          </div>

          {/* Additional Analytics Section */}
          <div className="mt-6">
            <div className="bg-white dark:bg-[var(--bg-secondary)] rounded-lg p-6 shadow-[var(--elevation-2)] border border-[var(--border-color)]">
              <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-4">Analytics Overview</h2>
              <p className="text-[var(--text-secondary)]">
                Your astrological reading statistics show a positive trend with increased client engagement. 
                Complete pending readings to improve your completion rate.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
