"use client";

import React from 'react';
import './Spinner.css';

const Spinner = ({ 
  size = 'medium', 
  color = 'primary',
  label = 'Loading...',
  className = '' 
}) => {
  return (
    <div 
      className={`spinner spinner--${size} spinner--${color} ${className}`}
      role="status"
      aria-label={label}
    >
      <svg className="spinner__svg" viewBox="0 0 50 50">
        <circle
          className="spinner__circle"
          cx="25"
          cy="25"
          r="20"
          fill="none"
          strokeWidth="4"
        />
      </svg>
      <span className="visually-hidden">{label}</span>
    </div>
  );
};

export default Spinner;
