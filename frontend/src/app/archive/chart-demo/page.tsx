"use client";

import React, { useState } from 'react';
import ChartCanvas from '@/components/chart/ChartCanvas';
import { mockChartData } from '@/components/chart/mockChartData';

export default function ChartDemoPage() {
  const [chartData] = useState(mockChartData);
  const [showInfo, setShowInfo] = useState(false);

  return (
    <div style={{ 
      padding: '2rem', 
      maxWidth: '1200px', 
      margin: '0 auto',
      minHeight: '100vh'
    }}>
      <h1 style={{ 
        fontSize: '2rem', 
        fontWeight: 'bold', 
        marginBottom: '1rem',
        color: 'var(--text-primary)'
      }}>
        Interactive Natal Chart Demo
      </h1>
      
      <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            Sample Chart: December 19, 1984, Metairie, LA
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            (Using mock data - see below for real API usage)
          </p>
        </div>
        <button
          onClick={() => setShowInfo(!showInfo)}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--primary-color)',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.875rem',
            whiteSpace: 'nowrap'
          }}
        >
          {showInfo ? 'Hide Info' : 'Show API Info'}
        </button>
      </div>
      
      {showInfo && (
        <div style={{
          marginBottom: '2rem',
          padding: '1.5rem',
          backgroundColor: 'var(--bg-secondary)',
          borderRadius: '8px'
        }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem', color: 'var(--text-primary)' }}>
            Backend API Available
          </h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            The backend calculation service is running at <code style={{ backgroundColor: 'var(--bg-tertiary)', padding: '0.25rem 0.5rem', borderRadius: '4px' }}>http://localhost:8000</code>
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1rem' }}>
            Chart calculation uses Swiss Ephemeris for accurate planetary positions. Authentication required to save charts.
          </p>
          <pre style={{
            backgroundColor: 'var(--bg-tertiary)',
            padding: '1rem',
            borderRadius: '4px',
            overflow: 'auto',
            fontSize: '0.75rem'
          }}>
{`# Test with curl:
curl -X POST http://localhost:8000/api/v1/chart \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -d '{
    "birth_data": {
      "date": "1984-12-19",
      "time": "12:00:00",
      "latitude": 29.9844,
      "longitude": -90.1547,
      "timezone": "America/Chicago",
      "location_name": "Metairie, LA"
    }
  }'`}
          </pre>
        </div>
      )}
      
      <ChartCanvas chartData={chartData} />
      
      <div style={{ 
        marginTop: '3rem', 
        padding: '1.5rem', 
        backgroundColor: 'var(--bg-secondary)',
        borderRadius: '8px'
      }}>
        <h3 style={{ 
          fontSize: '1.125rem', 
          fontWeight: '600', 
          marginBottom: '1rem',
          color: 'var(--text-primary)'
        }}>
          Chart Features
        </h3>
        <ul style={{ 
          listStyleType: 'disc', 
          paddingLeft: '1.5rem',
          color: 'var(--text-primary)',
          lineHeight: '1.8'
        }}>
          <li>Interactive SVG chart with zoom controls</li>
          <li>12 houses with division lines</li>
          <li>Planet glyphs with accurate positioning</li>
          <li>Zodiac signs around perimeter</li>
          <li>Toggleable aspect lines between planets</li>
          <li>Hover tooltips showing planet details</li>
          <li>Keyboard accessible</li>
          <li>Responsive design</li>
        </ul>
      </div>
    </div>
  );
}
