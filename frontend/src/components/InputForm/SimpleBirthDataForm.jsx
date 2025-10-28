import React, { useState } from 'react';
import './BirthDataForm.css';

const SimpleBirthDataForm = ({ onCalculate, loading }) => {
  const [formData, setFormData] = useState({
    year: 1990,
    month: 7,
    day: 4,
    hour: 12,
    minute: 0,
    latitude: 40.7128,
    longitude: -74.0060
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const options = {
      zodiacType: 'tropical',
      houseSystem: 'P'
    };
    onCalculate(formData, options);
  };

  const loadSample = () => {
    setFormData({
      year: 1990,
      month: 7,
      day: 4,
      hour: 12,
      minute: 0,
      latitude: 40.7128,
      longitude: -74.0060
    });
  };

  return (
    <div className="simple-birth-form">
      <h2>🌟 Astrological Chart Calculator</h2>
      <p>Enter your birth information to generate your complete astrological chart</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>📅 Birth Date & Time</h3>
          <div className="form-row">
            <label>
              Year:
              <input
                type="number"
                name="year"
                value={formData.year}
                onChange={handleChange}
                min="1800"
                max="2200"
                required
              />
            </label>
            <label>
              Month:
              <input
                type="number"
                name="month"
                value={formData.month}
                onChange={handleChange}
                min="1"
                max="12"
                required
              />
            </label>
            <label>
              Day:
              <input
                type="number"
                name="day"
                value={formData.day}
                onChange={handleChange}
                min="1"
                max="31"
                required
              />
            </label>
          </div>
          
          <div className="form-row">
            <label>
              Hour (24h):
              <input
                type="number"
                name="hour"
                value={formData.hour}
                onChange={handleChange}
                min="0"
                max="23"
                required
              />
            </label>
            <label>
              Minute:
              <input
                type="number"
                name="minute"
                value={formData.minute}
                onChange={handleChange}
                min="0"
                max="59"
                required
              />
            </label>
          </div>
        </div>

        <div className="form-section">
          <h3>🌍 Birth Location</h3>
          <div className="form-row">
            <label>
              Latitude:
              <input
                type="number"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                step="0.0001"
                min="-90"
                max="90"
                required
              />
            </label>
            <label>
              Longitude:
              <input
                type="number"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                step="0.0001"
                min="-180"
                max="180"
                required
              />
            </label>
          </div>
          <p className="help-text">
            💡 Need coordinates? Google "coordinates of [your city]" or use latlong.net
          </p>
        </div>

        <div className="form-actions">
          <button type="button" onClick={loadSample} disabled={loading}>
            Load Sample (July 4, 1990, NYC)
          </button>
          <button type="submit" disabled={loading} className="primary">
            {loading ? '🔮 Calculating...' : '✨ Calculate My Chart'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SimpleBirthDataForm;