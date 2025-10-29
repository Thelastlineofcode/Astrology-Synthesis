"use client";

import React from 'react';
import Link from 'next/link';
import Card from '../shared/Card';
import Button from '../shared/Button';
import './SymbolonCard.css';

const SymbolonCard = () => {
  return (
    <Card className="symbolon-card">
      <h3>Symbolon Cards</h3>
      <div className="symbolon-card__content">
        <p className="symbolon-description">
          Explore archetypal insights through Symbolon card readings
        </p>
        <div className="symbolon-cta">
          <Link href="/symbolon-demo">
            <Button variant="primary" className="symbolon-button">
              Draw a Card
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
};

export default SymbolonCard;
