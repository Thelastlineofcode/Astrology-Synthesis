"use client";

import React from 'react';
import Link from 'next/link';
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
          <Link href="/chart">
            <Button variant="primary">
              New Chart
            </Button>
          </Link>
          <Link href="/symbolon-demo">
            <Button variant="secondary">
              Explore Symbolon
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
};

export default QuickChartCard;
