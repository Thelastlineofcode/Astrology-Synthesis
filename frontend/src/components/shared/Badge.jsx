"use client";

import React from 'react';
import './Badge.css';

const Badge = ({ 
  children, 
  variant = 'neutral', 
  size = 'medium',
  className = '',
  ...props 
}) => {
  const classNames = [
    'badge',
    `badge--${variant}`,
    `badge--${size}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <span className={classNames} {...props}>
      {children}
    </span>
  );
};

export default Badge;
