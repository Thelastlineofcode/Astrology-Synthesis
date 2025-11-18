"use client";

import React from "react";
import Card from "../shared/Card";
import Button from "../shared/Button";
import "./QuickChartCard.css";

const QuickChartCard = () => {
  return (
    <Card className="quick-chart-card">
      <div className="quick-chart-card__content">
        <div className="quick-chart-card__header">
          <h2>Your Spiritual Journey</h2>
          <p>Get guidance from the cosmos through cards and charts</p>
        </div>

        <div className="quick-chart-card__actions">
          <Button variant="primary" href="/fortune">
            Daily Fortune
          </Button>
          <Button variant="secondary" href="/chart-demo">
            View Chart
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default QuickChartCard;
