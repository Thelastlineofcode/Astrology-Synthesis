import React, { useState } from "react";
import LocationPicker from "./LocationPicker";
import "./BirthDataForm.css";

const BirthDataForm = ({ onCalculate, loading }) => {
  const [formData, setFormData] = useState({
    year: "",
    month: "",
    day: "",
    hour: "",
    minute: "",
    latitude: "",
    longitude: "",
    address: "",
    useManualCoordinates: false,
  });

  const [options, setOptions] = useState({
    zodiacType: "sidereal",
    ayanamsa: "LAHIRI",
    houseSystem: "P",
    includeMinorAspects: false,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleOptionChange = (e) => {
    const { name, value, type, checked } = e.target;
    setOptions((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const birthData = {
      year: parseInt(formData.year),
      month: parseInt(formData.month),
      day: parseInt(formData.day),
      hour: parseInt(formData.hour),
      minute: parseInt(formData.minute),
      latitude: parseFloat(formData.latitude),
      longitude: parseFloat(formData.longitude),
    };

    onCalculate(birthData, options);
  };

  const loadSampleData = () => {
    setFormData({
      year: "1990",
      month: "8",
      day: "15",
      hour: "14",
      minute: "30",
      latitude: "29.7604",
      longitude: "-95.3698",
      location: "Houston, TX",
      timezone: "CST",
    });
  };

  return (
    <div className="birth-data-form">
      <h2>Birth Information</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>📅 Date</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Year</label>
              <input
                type="number"
                name="year"
                value={formData.year}
                onChange={handleInputChange}
                placeholder="1990"
                required
                min="1900"
                max="2100"
              />
            </div>
            <div className="form-group">
              <label>Month</label>
              <input
                type="number"
                name="month"
                value={formData.month}
                onChange={handleInputChange}
                placeholder="8"
                required
                min="1"
                max="12"
              />
            </div>
            <div className="form-group">
              <label>Day</label>
              <input
                type="number"
                name="day"
                value={formData.day}
                onChange={handleInputChange}
                placeholder="15"
                required
                min="1"
                max="31"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>⏰ Time</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Hour</label>
              <input
                type="number"
                name="hour"
                value={formData.hour}
                onChange={handleInputChange}
                placeholder="14"
                required
                min="0"
                max="23"
              />
            </div>
            <div className="form-group">
              <label>Minute</label>
              <input
                type="number"
                name="minute"
                value={formData.minute}
                onChange={handleInputChange}
                placeholder="30"
                required
                min="0"
                max="59"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Location Details</h3>
          <div className="location-toggle">
            <label>
              <input
                type="checkbox"
                name="useManualCoordinates"
                checked={formData.useManualCoordinates}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    useManualCoordinates: e.target.checked,
                  }))
                }
              />
              Enter coordinates manually
            </label>
          </div>

          {formData.useManualCoordinates ? (
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="latitude">Latitude</label>
                <input
                  type="number"
                  step="0.000001"
                  id="latitude"
                  name="latitude"
                  value={formData.latitude}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="longitude">Longitude</label>
                <input
                  type="number"
                  step="0.000001"
                  id="longitude"
                  name="longitude"
                  value={formData.longitude}
                  onChange={handleInputChange}
                />
              </div>
            </div>
          ) : (
            <LocationPicker
              onLocationSelect={({ latitude, longitude, address }) => {
                setFormData((prev) => ({
                  ...prev,
                  latitude: String(latitude),
                  longitude: String(longitude),
                  address,
                }));
              }}
            />
          )}
        </div>

        <div className="form-section">
          <h3>⚙️ Chart Options</h3>

          <div className="form-group">
            <label>Zodiac Type</label>
            <select
              name="zodiacType"
              value={options.zodiacType}
              onChange={handleOptionChange}
            >
              <option value="sidereal">Sidereal (Vedic)</option>
              <option value="tropical">Tropical (Western)</option>
            </select>
          </div>

          {options.zodiacType === "sidereal" && (
            <div className="form-group">
              <label>Ayanamsa</label>
              <select
                name="ayanamsa"
                value={options.ayanamsa}
                onChange={handleOptionChange}
              >
                <option value="LAHIRI">Lahiri</option>
                <option value="KRISHNAMURTI">Krishnamurti (KP)</option>
                <option value="RAMAN">Raman</option>
                <option value="FAGAN_BRADLEY">Fagan-Bradley</option>
              </select>
            </div>
          )}

          <div className="form-group">
            <label>House System</label>
            <select
              name="houseSystem"
              value={options.houseSystem}
              onChange={handleOptionChange}
            >
              <option value="P">Placidus</option>
              <option value="K">Koch</option>
              <option value="W">Whole Sign</option>
              <option value="E">Equal</option>
              <option value="R">Regiomontanus</option>
              <option value="C">Campanus</option>
            </select>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="includeMinorAspects"
                checked={options.includeMinorAspects}
                onChange={handleOptionChange}
              />
              Include Minor Aspects
            </label>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={loadSampleData}
            className="btn-secondary"
            disabled={loading}
          >
            Load Sample
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Calculating..." : "Calculate Chart"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BirthDataForm;
