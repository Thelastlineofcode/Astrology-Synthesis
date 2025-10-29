"use client";

import React from 'react';
import ChartCanvas from '@/components/chart/ChartCanvas';
import { mockChartData } from '@/components/chart/mockChartData';

export default function ChartDemoPage() {
  return (
    <div style={{ 
      padding: '2rem', 
      maxWidth: '800px', 
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
      
      <p style={{ 
        marginBottom: '2rem', 
        color: 'var(--text-secondary)',
        lineHeight: '1.6'
      }}>
        This is a demonstration of the interactive natal chart canvas. 
        Try zooming in and out, toggling aspects, and hovering over planets 
        to see their details.
      </p>
      
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ 
          fontSize: '1.25rem', 
          fontWeight: '600', 
          marginBottom: '0.5rem',
          color: 'var(--text-primary)'
        }}>
          Sample Chart Data
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Birth: December 19, 1984, Metairie, LA
        </p>
      </div>
      
      <ChartCanvas chartData={mockChartData} />
      
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
          Features
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
          <li>Keyboard accessible (Tab to planets, Enter to show tooltip)</li>
          <li>Responsive design for mobile, tablet, and desktop</li>
        </ul>
      </div>
    </div>
  );
}
