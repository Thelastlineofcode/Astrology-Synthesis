"use client";

import React from 'react';
import './Card.css';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  hoverable?: boolean;
  padding?: 'default' | 'none';
}

const Card: React.FC<CardProps> = ({ 
  children, 
  className = '', 
  hoverable = false, 
  onClick, 
  padding = 'default',
  ...props 
}) => {
  const classNames = [
    'card',
    hoverable && 'card--hoverable',
    padding === 'none' && 'card--no-padding',
    className
  ].filter(Boolean).join(' ');

  return (
    <div 
      className={classNames} 
      onClick={onClick}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
