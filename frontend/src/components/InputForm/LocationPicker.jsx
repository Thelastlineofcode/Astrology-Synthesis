import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import L from "leaflet";

// Fix for default marker icons in Leaflet with React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

const MapUpdater = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom());
  }, [center, map]);
  return null;
};

const LocationPicker = ({ onLocationSelect }) => {
  const [address, setAddress] = useState("");
  const [mapCenter, setMapCenter] = useState([0, 0]);
  const [marker, setMarker] = useState(null);
  const [showMap, setShowMap] = useState(false);
  const [error, setError] = useState("");

  const handleAddressSearch = async () => {
    try {
      setError("");
      // Using Nominatim for geocoding (OpenStreetMap)
      const response = await axios.get(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`
      );

      if (response.data && response.data.length > 0) {
        const location = response.data[0];
        const newLocation = [
          parseFloat(location.lat),
          parseFloat(location.lon),
        ];
        setMapCenter(newLocation);
        setMarker(newLocation);
        setShowMap(true);
        onLocationSelect({
          latitude: newLocation[0],
          longitude: newLocation[1],
          address: location.display_name,
        });
      } else {
        setError("Location not found");
      }
    } catch (error) {
      console.error("Geocoding error:", error);
      setError("Error searching for location");
    }
  };

  const handleMapClick = (e) => {
    const newLocation = [e.latlng.lat, e.latlng.lng];
    setMarker(newLocation);
    onLocationSelect({
      latitude: newLocation[0],
      longitude: newLocation[1],
    });

    // Reverse geocoding to get address
    axios
      .get(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${newLocation[0]}&lon=${newLocation[1]}`
      )
      .then((response) => {
        if (response.data && response.data.display_name) {
          onLocationSelect({
            latitude: newLocation[0],
            longitude: newLocation[1],
            address: response.data.display_name,
          });
        }
      })
      .catch((error) => console.error("Reverse geocoding error:", error));
  };

  return (
    <div className="location-picker">
      <div className="address-input">
        <input
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Enter an address"
          className="form-control"
        />
        <button onClick={handleAddressSearch} className="btn btn-primary">
          Search
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="map-container">
        <MapContainer
          center={mapCenter}
          zoom={2}
          style={{ height: "300px", width: "100%" }}
          onClick={handleMapClick}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapUpdater center={mapCenter} />
          {marker && <Marker position={marker} />}
        </MapContainer>
      </div>
    </div>
  );
};

export default LocationPicker;
