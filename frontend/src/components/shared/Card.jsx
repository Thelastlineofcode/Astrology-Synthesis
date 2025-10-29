"use client";

import React from 'react';
import './Card.css';

const Card = ({ 
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
