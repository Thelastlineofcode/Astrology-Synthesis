"use client";

import React from 'react';
import Link from 'next/link';
import Card from '../shared/Card';
import Button from '../shared/Button';
import './BMADSummaryCard.css';

const BMADSummaryCard = () => {
  return (
    <Card className="bmad-summary-card">
      <h3>BMAD Analysis</h3>
      <div className="bmad-summary-card__content">
        <p className="bmad-description">
          Discover insights from your Birth Matrix Analysis Dashboard
        </p>
        <div className="bmad-cta">
          <Link href="/bmad">
            <Button variant="primary" className="bmad-button">
              View Analysis
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
};

export default BMADSummaryCard;
