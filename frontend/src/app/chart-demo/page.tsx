"use client";

import React from 'react';
import { ChartCanvas, PlanetTable, HouseTable } from '@/components/chart';
import { ChartData } from '@/types/chart';

// Sample chart data based on the my_chart_calculator.py output format
const sampleChartData: ChartData = {
  planets: {
    'Sun': { sign: 'Leo', degree: 15.5, house: 5, retrograde: false, longitude: 135.5 },
    'Moon': { sign: 'Cancer', degree: 22.3, house: 4, retrograde: false, longitude: 112.3 },
    'Mercury': { sign: 'Virgo', degree: 8.1, house: 6, retrograde: false, longitude: 158.1 },
    'Venus': { sign: 'Leo', degree: 28.7, house: 5, retrograde: false, longitude: 148.7 },
    'Mars': { sign: 'Gemini', degree: 12.4, house: 3, retrograde: false, longitude: 72.4 },
    'Jupiter': { sign: 'Sagittarius', degree: 5.2, house: 9, retrograde: true, longitude: 245.2 },
    'Saturn': { sign: 'Capricorn', degree: 18.9, house: 10, retrograde: false, longitude: 288.9 },
    'Uranus': { sign: 'Aquarius', degree: 2.1, house: 11, retrograde: false, longitude: 302.1 },
    'Neptune': { sign: 'Pisces', degree: 14.5, house: 12, retrograde: false, longitude: 344.5 },
    'Pluto': { sign: 'Capricorn', degree: 22.8, house: 10, retrograde: false, longitude: 292.8 },
    'North Node': { sign: 'Gemini', degree: 8.5, house: 3, retrograde: true, longitude: 68.5 },
    'South Node': { sign: 'Sagittarius', degree: 8.5, house: 9, retrograde: true, longitude: 248.5 },
    'Chiron': null
  },
  houses: {
    'house_1': { sign: 'Aries', degree: 12.0, longitude: 12.0 },
    'house_2': { sign: 'Taurus', degree: 8.5, longitude: 38.5 },
    'house_3': { sign: 'Gemini', degree: 5.2, longitude: 65.2 },
    'house_4': { sign: 'Cancer', degree: 12.0, longitude: 102.0 },
    'house_5': { sign: 'Leo', degree: 18.7, longitude: 138.7 },
    'house_6': { sign: 'Virgo', degree: 21.3, longitude: 171.3 },
    'house_7': { sign: 'Libra', degree: 12.0, longitude: 192.0 },
    'house_8': { sign: 'Scorpio', degree: 8.5, longitude: 218.5 },
    'house_9': { sign: 'Sagittarius', degree: 5.2, longitude: 245.2 },
    'house_10': { sign: 'Capricorn', degree: 12.0, longitude: 282.0 },
    'house_11': { sign: 'Aquarius', degree: 18.7, longitude: 318.7 },
    'house_12': { sign: 'Pisces', degree: 21.3, longitude: 351.3 }
  },
  ascendant: { sign: 'Aries', degree: 12.0, longitude: 12.0 },
  midheaven: { sign: 'Capricorn', degree: 12.0, longitude: 282.0 }
};

export default function ChartDemo() {
  return (
    <div style={{
      padding: '48px 24px',
      maxWidth: '1400px',
      margin: '0 auto',
      minHeight: '100vh',
      background: 'var(--bg-primary)'
    }}>
      <div style={{ marginBottom: '48px', textAlign: 'center' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          marginBottom: '16px',
          color: 'var(--color-primary)'
        }}>
          Birth Chart Visualization
        </h1>
        <p style={{ 
          fontSize: '1.125rem', 
          color: 'var(--text-secondary)',
          maxWidth: '600px',
          margin: '0 auto'
        }}>
          Interactive astrological chart with planetary positions, house cusps, and zodiac wheel.
        </p>
      </div>

      {/* Chart Canvas */}
      <div style={{ marginBottom: '48px' }}>
        <ChartCanvas chartData={sampleChartData} width={600} height={600} />
      </div>

      {/* Two-column layout for tables */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
        gap: '24px',
        marginBottom: '48px'
      }}>
        {/* Planet Table */}
        <PlanetTable planets={sampleChartData.planets} />

        {/* House Table */}
        <HouseTable 
          houses={sampleChartData.houses}
          ascendant={sampleChartData.ascendant}
          midheaven={sampleChartData.midheaven}
        />
      </div>

      {/* Information section */}
      <div style={{ 
        marginTop: '48px', 
        padding: '24px',
        background: 'var(--bg-secondary)',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <h2 style={{ 
          fontSize: '1.5rem', 
          marginBottom: '16px',
          color: 'var(--color-primary)'
        }}>
          About Birth Charts
        </h2>
        <p style={{ 
          color: 'var(--text-secondary)',
          lineHeight: '1.6',
          maxWidth: '800px',
          margin: '0 auto'
        }}>
          A birth chart (natal chart) is a snapshot of the heavens at the exact moment and 
          location of your birth. It shows the positions of planets in zodiac signs and houses, 
          revealing unique personality traits, life patterns, and potential paths for growth.
        </p>
      </div>
    </div>
  );
}
