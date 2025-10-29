---
title: "Redesign Birth Data Input Form"
labels: ["component:chart", "P0-Critical", "forms"]
assignees: []
milestone: "Milestone 2: Core Features"
---

## 🎯 Objective

Redesign the birth data input form with improved UX: date/time pickers, location autocomplete, timezone auto-detection, and validation.

## 📋 Description

The birth data form is the entry point for chart generation. Improve usability with modern date/time inputs, location search, and clear validation. This replaces the existing `SimpleBirthDataForm.jsx`.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Chart Input section)
- **Design Artifact**: `UX_COPY_GUIDE.md` (Form labels and validation)
- **Existing Code**: `/frontend/src/components/InputForm/SimpleBirthDataForm.jsx`

## ✅ Acceptance Criteria

- [ ] Date picker for birth date (native or library)
- [ ] Time picker with AM/PM or 24-hour format
- [ ] Location input with autocomplete (city search)
- [ ] Latitude/longitude auto-filled from location
- [ ] Timezone auto-detected based on location
- [ ] Manual lat/long/timezone override option
- [ ] Validation: required fields, valid date/time, valid coordinates
- [ ] Error messages for invalid input
- [ ] "Load Sample Data" button (Metairie, LA)
- [ ] Responsive layout (stacked on mobile, grid on desktop)
- [ ] Submit button triggers chart calculation

## 💻 Implementation Notes

### Birth Data Form Component

```jsx
// /frontend/src/components/chart/BirthDataForm.jsx
import React, { useState } from 'react';
import TextInput from '../shared/TextInput';
import Select from '../shared/Select';
import Button from '../shared/Button';
import LocationSearch from './LocationSearch';
import './BirthDataForm.css';

const BirthDataForm = ({ onSubmit, loading = false }) => {
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '',
    latitude: '',
    longitude: '',
    timezone: '',
    location: ''
  });
  
  const [errors, setErrors] = useState({});
  
  const loadSampleData = () => {
    setFormData({
      name: 'Sample Chart',
      date: '1984-12-19',
      time: '18:59',
      latitude: 30.0019,
      longitude: -90.1767,
      timezone: 'America/Chicago',
      location: 'Metairie, LA, USA'
    });
  };
  
  const handleLocationSelect = (location) => {
    setFormData(prev => ({
      ...prev,
      latitude: location.lat,
      longitude: location.lng,
      timezone: location.timezone,
      location: location.name
    }));
  };
  
  const validate = () => {
    const newErrors = {};
    
    if (!formData.date) {
      newErrors.date = 'Birth date is required';
    }
    
    if (!formData.time) {
      newErrors.time = 'Birth time is required';
    }
    
    if (!formData.latitude || !formData.longitude) {
      newErrors.location = 'Location is required';
    }
    
    if (formData.latitude < -90 || formData.latitude > 90) {
      newErrors.latitude = 'Latitude must be between -90 and 90';
    }
    
    if (formData.longitude < -180 || formData.longitude > 180) {
      newErrors.longitude = 'Longitude must be between -180 and 180';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };
  
  return (
    <form className="birth-data-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Enter Birth Information</h2>
        <Button
          type="button"
          variant="ghost"
          size="small"
          onClick={loadSampleData}
        >
          Load Sample Data
        </Button>
      </div>
      
      <div className="form-grid">
        <TextInput
          label="Name (optional)"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="e.g., John Doe"
        />
        
        <TextInput
          label="Birth Date"
          type="date"
          value={formData.date}
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          error={errors.date}
          required
        />
        
        <TextInput
          label="Birth Time"
          type="time"
          value={formData.time}
          onChange={(e) => setFormData({ ...formData, time: e.target.value })}
          error={errors.time}
          required
          helperText="Use 24-hour format or select AM/PM"
        />
        
        <LocationSearch
          label="Birth Location"
          value={formData.location}
          onSelect={handleLocationSelect}
          error={errors.location}
          required
        />
        
        <TextInput
          label="Latitude"
          type="number"
          step="0.0001"
          value={formData.latitude}
          onChange={(e) => setFormData({ ...formData, latitude: parseFloat(e.target.value) })}
          error={errors.latitude}
          helperText="Auto-filled from location"
        />
        
        <TextInput
          label="Longitude"
          type="number"
          step="0.0001"
          value={formData.longitude}
          onChange={(e) => setFormData({ ...formData, longitude: parseFloat(e.target.value) })}
          error={errors.longitude}
          helperText="Auto-filled from location"
        />
        
        <TextInput
          label="Timezone"
          value={formData.timezone}
          onChange={(e) => setFormData({ ...formData, timezone: e.target.value })}
          placeholder="e.g., America/Chicago"
          helperText="Auto-detected from location"
        />
      </div>
      
      <div className="form-actions">
        <Button
          type="submit"
          variant="primary"
          size="large"
          loading={loading}
          fullWidth
        >
          {loading ? 'Calculating...' : 'Generate Chart'}
        </Button>
      </div>
    </form>
  );
};

export default BirthDataForm;
```

### Form Styles

```css
/* /frontend/src/components/chart/BirthDataForm.css */
.birth-data-form {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-6);
  background: var(--bg-secondary);
  border-radius: 12px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.form-header h2 {
  margin: 0;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
}

.form-actions {
  margin-top: var(--space-6);
}

/* Desktop: 2-column layout */
@media (min-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  /* Name and Location span full width */
  .form-grid > :first-child,
  .form-grid > :nth-child(4) {
    grid-column: span 2;
  }
}
```

### Location Search Component (Stub)

```jsx
// /frontend/src/components/chart/LocationSearch.jsx
import React, { useState } from 'react';
import TextInput from '../shared/TextInput';

// TODO: Integrate with geocoding API (Google Places, OpenCage, etc.)
const LocationSearch = ({ label, value, onSelect, error, required }) => {
  const [suggestions, setSuggestions] = useState([]);
  
  const handleSearch = async (query) => {
    // Placeholder for geocoding API call
    // Example: fetch(`https://api.opencagedata.com/geocode/v1/json?q=${query}&key=YOUR_KEY`)
    console.log('Searching for:', query);
  };
  
  return (
    <div className="location-search">
      <TextInput
        label={label}
        value={value}
        onChange={(e) => handleSearch(e.target.value)}
        error={error}
        required={required}
        placeholder="e.g., New York, NY"
      />
      {/* TODO: Add dropdown for suggestions */}
    </div>
  );
};

export default LocationSearch;
```

## 🧪 Testing Checklist

- [ ] Form renders without errors
- [ ] All fields display correctly
- [ ] Date picker opens and allows date selection
- [ ] Time picker allows time input (test AM/PM if used)
- [ ] Location search placeholder (API integration later)
- [ ] Lat/long auto-filled when location selected
- [ ] Timezone auto-detected
- [ ] Manual lat/long input works
- [ ] Validation shows errors for missing fields
- [ ] Validation prevents invalid lat/long
- [ ] "Load Sample Data" populates Metairie, LA data
- [ ] Submit button triggers onSubmit callback
- [ ] Loading state disables form during submission
- [ ] Responsive layout on mobile (375px) and desktop (1440px)

## 🔍 Accessibility Requirements

- [ ] All inputs have proper labels
- [ ] Required fields marked with asterisk
- [ ] Error messages announced to screen readers
- [ ] Date/time pickers keyboard accessible
- [ ] Form can be completed with keyboard only
- [ ] Focus order logical (top to bottom)
- [ ] Submit button disabled during loading (with aria-busy)

## 📦 Files to Create/Modify

- `frontend/src/components/chart/BirthDataForm.jsx` (create - replace SimpleBirthDataForm)
- `frontend/src/components/chart/BirthDataForm.css` (create)
- `frontend/src/components/chart/LocationSearch.jsx` (create stub)
- `frontend/src/components/chart/BirthDataForm.test.jsx` (create)
- `frontend/src/components/InputForm/SimpleBirthDataForm.jsx` (deprecate/remove)

## 🔗 Dependencies

- Issue #5 (Form Input Components) - Uses TextInput, Select
- Issue #3 (Button Component) - Submit and sample data buttons
- Geocoding API (OpenCage, Google Places, or similar) - future integration

## 🚫 Blocked By

- None (location search can use manual input initially)

## 📝 Additional Notes

- Location search API integration can be phase 2
- Consider adding "Unknown birth time" option (set to noon)
- Consider adding "Daylight Saving Time" checkbox for manual override
- Test with edge cases: midnight births, international date line
- Preserve form data in localStorage on page refresh (future)

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 8 hours  
**Assignee**: TBD  
**Epic**: Epic 4 - Enhanced Natal Chart Viewer
