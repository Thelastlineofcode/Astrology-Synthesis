"use client";

import React from "react";
import Card from "@/components/shared/Card";
import Button from "@/components/shared/Button";
import "./RecentChartsCard.css";

interface Chart {
  id: string;
  name?: string;
  date: string;
}

interface RecentChartsCardProps {
  charts: Chart[];
  loading: boolean;
}

const RecentChartsCard: React.FC<RecentChartsCardProps> = ({
  charts,
  loading,
}) => {
  if (loading) {
    return (
      <Card className="recent-charts-card">
        <h3>Recent Charts</h3>
        <div className="loading-skeleton" role="status" aria-label="Loading recent charts">
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <div className="skeleton-line" />
          <span className="sr-only">Loading your recent charts...</span>
        </div>
      </Card>
    );
  }

  if (charts.length === 0) {
    return (
      <Card className="recent-charts-card">
        <h3>Recent Charts</h3>
        <div className="empty-state" role="status">
          <p className="empty-state__text">
            No charts yet. Generate your first chart to get started!
          </p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="recent-charts-card">
      <div className="card-header">
        <h3>Recent Charts</h3>
        <Button
          variant="secondary"
          size="small"
          href="/chart-demo"
          aria-label="View all recent charts"
        >
          View All
        </Button>
      </div>

      <ul className="chart-list" aria-label="Recent charts list">
        {charts.map((chart) => (
          <li key={chart.id} className="chart-item">
            <div className="chart-item__info">
              <strong>{chart.name || "Unnamed Chart"}</strong>
              <span className="chart-item__date">
                {new Date(chart.date).toLocaleDateString()}
              </span>
            </div>
            <Button
              variant="secondary"
              size="small"
              href={`/chart-demo`}
              aria-label={`View chart for ${chart.name || "Unnamed Chart"}`}
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
