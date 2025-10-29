"use client";

import React from 'react';
import './Skeleton.css';

const Skeleton = ({ 
  variant = 'text', 
  width,
  height,
  count = 1,
  className = '' 
}) => {
  const skeletons = Array.from({ length: count }, (_, i) => (
    <div
      key={i}
      className={`skeleton skeleton--${variant} ${className}`}
      style={{ width, height }}
      aria-hidden="true"
    />
  ));
  
  return (
    <div className="skeleton-container" aria-busy="true" aria-live="polite">
      {skeletons}
    </div>
  );
};

// Preset skeleton patterns
export const SkeletonCard = () => (
  <div className="skeleton-card" aria-busy="true">
    <Skeleton variant="rect" height={200} />
    <div style={{ padding: 'var(--space-4)' }}>
      <Skeleton variant="text" width="60%" height={24} />
      <Skeleton variant="text" width="100%" count={3} />
    </div>
  </div>
);

export const SkeletonTable = ({ rows = 5 }) => (
  <div className="skeleton-table" aria-busy="true">
    {Array.from({ length: rows }, (_, i) => (
      <div key={i} className="skeleton-table__row">
        <Skeleton variant="text" width="30%" />
        <Skeleton variant="text" width="50%" />
        <Skeleton variant="text" width="20%" />
      </div>
    ))}
  </div>
);

export default Skeleton;
