"use client";

import React from 'react';
import './DashboardWidget.css';

interface DashboardWidgetProps {
  title: string;
  children: React.ReactNode;
  headerAction?: React.ReactNode;
  className?: string;
}

const DashboardWidget: React.FC<DashboardWidgetProps> = ({
  title,
  children,
  headerAction,
  className = ''
}) => {
  return (
    <div className={`dashboard-widget ${className}`}>
      <div className="dashboard-widget-header">
        <h3 className="dashboard-widget-title">{title}</h3>
        {headerAction && (
          <div className="dashboard-widget-action">
            {headerAction}
          </div>
        )}
      </div>
      <div className="dashboard-widget-content">
        {children}
      </div>
    </div>
  );
};

export default DashboardWidget;
