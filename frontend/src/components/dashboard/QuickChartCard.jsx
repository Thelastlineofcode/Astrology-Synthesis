"use client";

import React from 'react';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import './QuickChartCard.css';

const QuickChartCard = () => {
  return (
    <Card className="quick-chart-card">
      <div className="quick-chart-card__content">
        <div className="quick-chart-card__text">
          <h2>Generate Your Chart</h2>
          <p className="quick-chart-card__description">
            Start your cosmic journey. Enter your birth details to reveal your natal chart and unlock personalized insights.
          </p>
        </div>
        <div className="quick-chart-card__actions">
          <Button 
            variant="primary" 
            size="medium"
            onClick={() => window.location.href = '/chart/new'}
          >
            Generate Chart
          </Button>
          <Button 
            variant="secondary" 
            size="medium"
            onClick={() => window.location.href = '/charts'}
          >
            View Saved Charts
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default QuickChartCard;
