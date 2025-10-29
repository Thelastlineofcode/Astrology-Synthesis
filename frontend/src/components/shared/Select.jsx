"use client";

import React, { useId } from 'react';
import './FormInputs.css';

/**
 * Select component - accessible dropdown with options
 * 
 * @param {string} label - Required label text
 * @param {string} value - Selected value
 * @param {function} onChange - Change handler
 * @param {Array} options - Array of {value, label} objects
 * @param {string} error - Error message to display
 * @param {string} helperText - Helper text below select
 * @param {boolean} required - Whether field is required
 * @param {boolean} disabled - Whether select is disabled
 * @param {string} placeholder - Placeholder option text
 * @param {string} className - Additional CSS classes
 * 
 * @accessibility
 * - Label associated via htmlFor/id
 * - Error messages announced with role="alert"
 * - Helper text linked via aria-describedby
 * - Required fields marked with aria-required and visual indicator
 * - Focus states clearly visible
 * - Keyboard navigable with arrow keys
 */
const Select = ({
  label,
  value,
  onChange,
  options = [],
  error,
  helperText,
  required = false,
  disabled = false,
  placeholder,
  className = '',
  ...props
}) => {
  const id = useId();
  const errorId = `${id}-error`;
  const helperId = `${id}-helper`;
  
  return (
    <div className={`form-group ${error ? 'form-group--error' : ''} ${className}`}>
      <label htmlFor={id} className="form-label">
        {label}
        {required && <span className="form-label__required" aria-label="required">*</span>}
      </label>
      
      <select
        id={id}
        value={value}
        onChange={onChange}
        disabled={disabled}
        required={required}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : helperText ? helperId : undefined}
        className="form-select"
        {...props}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      
      {helperText && !error && (
        <p id={helperId} className="form-helper-text">{helperText}</p>
      )}
      
      {error && (
        <p id={errorId} className="form-error-text" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default Select;