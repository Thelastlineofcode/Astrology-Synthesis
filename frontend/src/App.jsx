import React, { useState } from 'react';
import SimpleBirthDataForm from './components/InputForm/SimpleBirthDataForm';
import PlanetList from './components/PlanetList/PlanetList';
import AspectTable from './components/AspectTable/AspectTable';
import HouseTable from './components/HouseTable/HouseTable';
import { calculateChart } from './services/api';
import './App.css';

function App() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCalculate = async (birthData, options) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await calculateChart(birthData, options);
      
      if (response.success) {
        setChartData(response.chart);
      } else {
        setError('Failed to calculate chart');
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.error || 'Failed to calculate chart. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌟 Astrology Chart Calculator</h1>
        <p>Vedic & Western Astrology Charts with Swiss Ephemeris</p>
      </header>

      <div className="app-container">
        <div className="sidebar">
          <SimpleBirthDataForm 
            onCalculate={handleCalculate}
            loading={loading}
          />
        </div>

        <div className="main-content">
          {loading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Calculating your chart...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <h3>Error</h3>
              <p>{error}</p>
            </div>
          )}

          {chartData && !loading && (
            <>
              <div className="chart-info">
                <h2>Chart Information</h2>
                <div className="info-grid">
                  <div><strong>Zodiac Type:</strong> {chartData.metadata?.zodiac_type || 'tropical'}</div>
                  {chartData.metadata?.ayanamsa && (
                    <div><strong>Ayanamsa:</strong> {chartData.metadata.ayanamsa}</div>
                  )}
                  <div><strong>House System:</strong> {chartData.metadata?.house_system || 'P'}</div>
                </div>
              </div>

              <div className="chart-sections">
                <section className="chart-section">
                  <PlanetList planets={chartData.planets} />
                </section>

                <section className="chart-section">
                  <HouseTable 
                    houses={chartData.houses} 
                  />
                </section>

                <section className="chart-section full-width">
                  <AspectTable aspects={chartData.aspects} />
                </section>
              </div>
            </>
          )}

          {!chartData && !loading && !error && (
            <div className="welcome-message">
              <h2>Welcome!</h2>
              <p>Enter birth data in the form to calculate an astrology chart.</p>
              <div className="features">
                <h3>Features:</h3>
                <ul>
                  <li>✨ Sidereal (Vedic) & Tropical (Western) calculations</li>
                  <li>🏠 Multiple house systems (Placidus, Koch, Whole Sign, etc.)</li>
                  <li>🌙 Planetary positions with retrograde detection</li>
                  <li>⭐ Major and minor aspects with orbs</li>
                  <li>🎯 High-precision Swiss Ephemeris calculations</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
