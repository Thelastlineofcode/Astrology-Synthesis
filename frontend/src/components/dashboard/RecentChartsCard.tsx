"use client";

import React from 'react';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import './RecentChartsCard.css';

interface Chart {
  id: string;
  name?: string;
  date: string;
}

interface RecentChartsCardProps {
  charts: Chart[];
  loading: boolean;
}

const RecentChartsCard: React.FC<RecentChartsCardProps> = ({ charts, loading }) => {
  if (loading) {
    return (
      <Card className="recent-charts-card" onClick={() => {}}>
        <h3>Recent Charts</h3>
        <div className="loading-skeleton">
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
        </div>
      </Card>
    );
  }
  
  if (charts.length === 0) {
    return (
      <Card className="recent-charts-card" onClick={() => {}}>
        <h3>Recent Charts</h3>
        <div className="empty-state">
          <p className="empty-state__text">
            No charts yet. Generate your first chart to get started!
          </p>
        </div>
      </Card>
    );
  }
  
  return (
    <Card className="recent-charts-card" onClick={() => {}}>
      <div className="card-header">
        <h3>Recent Charts</h3>
        <Button 
          variant="secondary" 
          size="small"
          onClick={() => window.location.href = '/charts'}
        >
          View All
        </Button>
      </div>
      
      <ul className="chart-list">
        {charts.map((chart) => (
          <li key={chart.id} className="chart-item">
            <div className="chart-item__info">
              <strong>{chart.name || 'Unnamed Chart'}</strong>
              <span className="chart-item__date">
                {new Date(chart.date).toLocaleDateString()}
              </span>
            </div>
            <Button 
              variant="secondary" 
              size="small"
              onClick={() => window.location.href = `/chart/${chart.id}`}
            >
              View
            </Button>
          </li>
        ))}
      </ul>
    </Card>
  );
};

export default RecentChartsCard;
