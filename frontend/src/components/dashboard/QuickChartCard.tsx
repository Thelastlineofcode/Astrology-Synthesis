"use client";

import React from 'react';
import Card from '../shared/Card';
import Button from '../shared/Button';
import './QuickChartCard.css';

const QuickChartCard = () => {
  return (
    <Card className="quick-chart-card">
      <div className="quick-chart-card__content">
        <div className="quick-chart-card__header">
          <h2>Generate Your Chart</h2>
          <p>Start your astrological journey by creating a natal chart</p>
        </div>
        
        <div className="quick-chart-card__actions">
          <Button variant="primary" onClick={() => window.location.href = '/chart'}>
            New Chart
          </Button>
          <Button variant="secondary" onClick={() => window.location.href = '/symbolon-demo'}>
            Explore Symbolon
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default QuickChartCard;
