"use client";

import React from 'react';
import Card from '../shared/Card';
import Button from '../shared/Button';
import './RecentChartsCard.css';

interface Chart {
  id: string;
  name: string;
  date: string;
}

interface RecentChartsCardProps {
  charts: Chart[];
  loading: boolean;
}

const RecentChartsCard: React.FC<RecentChartsCardProps> = ({ charts, loading }) => {
  if (loading) {
    return (
      <Card className="recent-charts-card">
        <h3>Recent Charts</h3>
        <div className="loading-skeleton">
          <div className="skeleton-item"></div>
          <div className="skeleton-item"></div>
          <div className="skeleton-item"></div>
        </div>
      </Card>
    );
  }

  if (charts.length === 0) {
    return (
      <Card className="recent-charts-card">
        <h3>Recent Charts</h3>
        <div className="empty-state">
          <p>No charts yet. Generate your first chart to get started!</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="recent-charts-card">
      <div className="card-header">
        <h3>Recent Charts</h3>
        <Button variant="tertiary" size="small">
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
            <Button variant="tertiary" size="small">
              View
            </Button>
          </li>
        ))}
      </ul>
    </Card>
  );
};

export default RecentChartsCard;
