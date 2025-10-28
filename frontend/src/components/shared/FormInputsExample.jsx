import React, { useState } from 'react';
import { TextInput, Select, Checkbox, RadioGroup } from './index';

/**
 * FormInputsExample - Demonstrates usage of all form input components
 * 
 * This example shows how to use the form input components with validation,
 * error states, and proper state management.
 */
const FormInputsExample = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    country: '',
    acceptTerms: false,
    gender: '',
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (field) => (e) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value
    }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleCheckboxChange = (e) => {
    setFormData(prev => ({
      ...prev,
      acceptTerms: e.target.checked
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    if (!formData.country) {
      newErrors.country = 'Please select a country';
    }
    
    if (!formData.acceptTerms) {
      newErrors.acceptTerms = 'You must accept the terms';
    }
    
    if (!formData.gender) {
      newErrors.gender = 'Please select a gender';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      console.log('Form submitted:', formData);
      alert('Form submitted successfully!');
    }
  };

  const countryOptions = [
    { value: 'us', label: 'United States' },
    { value: 'uk', label: 'United Kingdom' },
    { value: 'ca', label: 'Canada' },
    { value: 'au', label: 'Australia' },
  ];

  const genderOptions = [
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
    { value: 'other', label: 'Other' },
    { value: 'prefer-not', label: 'Prefer not to say' },
  ];

  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '2rem' }}>
      <h2>Form Input Components Example</h2>
      <form onSubmit={handleSubmit}>
        {/* Text Input Example */}
        <TextInput
          label="Full Name"
          value={formData.name}
          onChange={handleInputChange('name')}
          placeholder="Enter your full name"
          error={errors.name}
          helperText="Please enter your first and last name"
          required
        />

        {/* Text Input with Email Type */}
        <TextInput
          label="Email Address"
          type="email"
          value={formData.email}
          onChange={handleInputChange('email')}
          placeholder="you@example.com"
          error={errors.email}
          required
        />

        {/* Select Dropdown Example */}
        <Select
          label="Country"
          value={formData.country}
          onChange={handleInputChange('country')}
          options={countryOptions}
          placeholder="Select your country"
          error={errors.country}
          required
        />

        {/* Radio Group Example */}
        <RadioGroup
          label="Gender"
          name="gender"
          options={genderOptions}
          value={formData.gender}
          onChange={handleInputChange('gender')}
          error={errors.gender}
          required
        />

        {/* Checkbox Example */}
        <Checkbox
          label="I accept the terms and conditions"
          checked={formData.acceptTerms}
          onChange={handleCheckboxChange}
        />
        {errors.acceptTerms && (
          <p style={{ color: 'var(--color-error, #C17B5C)', fontSize: '14px', marginTop: '4px' }}>
            {errors.acceptTerms}
          </p>
        )}

        <div style={{ marginTop: '2rem' }}>
          <button
            type="submit"
            style={{
              padding: '12px 24px',
              background: 'var(--color-primary, #3E4B6E)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: '500',
            }}
          >
            Submit Form
          </button>
        </div>
      </form>

      <div style={{ marginTop: '3rem', padding: '1.5rem', background: '#f5f5f5', borderRadius: '8px' }}>
        <h3>Current Form Data:</h3>
        <pre style={{ fontSize: '12px', overflow: 'auto' }}>
          {JSON.stringify(formData, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default FormInputsExample;
