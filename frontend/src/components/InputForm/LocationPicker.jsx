import React, { useState } from "react";
import axios from "axios";
import "./LocationPicker.css";

const LocationPicker = ({ onLocationSelect }) => {
  const [address, setAddress] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAddressSearch = async () => {
    if (!address.trim()) {
      setError("Please enter a location");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSuggestions([]);
      
      // Using Nominatim for geocoding (OpenStreetMap)
      const response = await axios.get(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=5`,
        {
          headers: {
            'User-Agent': 'AstrologyApp/1.0'
          }
        }
      );

      if (response.data && response.data.length > 0) {
        setSuggestions(response.data);
        setError("");
      } else {
        setError("Location not found. Please try a different search term.");
        setSuggestions([]);
      }
    } catch (error) {
      console.error("Geocoding error:", error);
      setError("Error searching for location. Please try again.");
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectLocation = (location) => {
    const lat = parseFloat(location.lat);
    const lon = parseFloat(location.lon);
    
    setSelectedLocation({
      latitude: lat,
      longitude: lon,
      address: location.display_name
    });

    onLocationSelect({
      latitude: lat,
      longitude: lon,
      address: location.display_name
    });

    setSuggestions([]);
  };

  const handleClear = () => {
    setAddress("");
    setSuggestions([]);
    setSelectedLocation(null);
    setError("");
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddressSearch();
    }
  };

  return (
    <div className="location-picker">
      <div className="location-search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter city, address, or landmark (e.g., New York, USA)"
            className="location-input"
            disabled={loading}
          />
          <button 
            type="button"
            onClick={handleAddressSearch}
            className="search-button"
            disabled={loading}
          >
            {loading ? "Searching..." : "🔍 Search"}
          </button>
          {address && (
            <button 
              type="button" 
              onClick={handleClear}
              className="clear-button"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {error && <div className="location-error">{error}</div>}

      {selectedLocation && (
        <div className="selected-location">
          <div className="location-badge">✓ Selected Location</div>
          <div className="location-details">
            <div className="location-name">{selectedLocation.address}</div>
            <div className="location-coords">
              📍 {selectedLocation.latitude.toFixed(6)}, {selectedLocation.longitude.toFixed(6)}
            </div>
          </div>
        </div>
      )}

      {suggestions.length > 0 && (
        <div className="location-suggestions">
          <div className="suggestions-header">Select a location:</div>
          {suggestions.map((location, index) => (
            <div
              key={index}
              className="suggestion-item"
              onClick={() => handleSelectLocation(location)}
            >
              <div className="suggestion-name">{location.display_name}</div>
              <div className="suggestion-coords">
                {parseFloat(location.lat).toFixed(4)}, {parseFloat(location.lon).toFixed(4)}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="location-help">
        💡 <strong>Tip:</strong> Search for your city name and country for best results
      </div>
    </div>
  );
};

export default LocationPicker;
