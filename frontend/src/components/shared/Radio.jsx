"use client";

import React, { useId } from 'react';
import './FormInputs.css';

/**
 * Radio component - accessible radio button for groups
 * 
 * @param {string} label - Required label text
 * @param {string} name - Radio group name (required for grouping)
 * @param {string} value - Radio button value
 * @param {boolean} checked - Whether radio is selected
 * @param {function} onChange - Change handler
 * @param {boolean} disabled - Whether radio is disabled
 * @param {string} className - Additional CSS classes
 * 
 * @accessibility
 * - Label associated via htmlFor/id
 * - Grouped by name attribute
 * - Focus states clearly visible
 * - Keyboard accessible (Arrow keys to navigate group)
 */
const Radio = ({
  label,
  name,
  value,
  checked,
  onChange,
  disabled = false,
  className = '',
  ...props
}) => {
  const id = useId();
  
  return (
    <div className={`form-radio ${className}`}>
      <input
        id={id}
        type="radio"
        name={name}
        value={value}
        checked={checked}
        onChange={onChange}
        disabled={disabled}
        className="form-radio__input"
        {...props}
      />
      <label htmlFor={id} className="form-radio__label">
        {label}
      </label>
    </div>
  );
};

/**
 * RadioGroup component - wrapper for radio button groups
 * 
 * @param {string} legend - Group legend/title
 * @param {string} name - Radio group name
 * @param {string} value - Selected value
 * @param {function} onChange - Change handler
 * @param {Array} options - Array of {value, label} objects
 * @param {string} error - Error message
 * @param {boolean} required - Whether selection is required
 * @param {string} className - Additional CSS classes
 */
export const RadioGroup = ({
  legend,
  name,
  value,
  onChange,
  options = [],
  error,
  required = false,
  className = '',
  ...props
}) => {
  const groupId = useId();
  const errorId = `${groupId}-error`;
  
  return (
    <fieldset className={`form-radio-group ${error ? 'form-radio-group--error' : ''} ${className}`}>
      <legend className="form-legend">
        {legend}
        {required && <span className="form-label__required" aria-label="required">*</span>}
      </legend>
      
      <div className="form-radio-group__options">
        {options.map(option => (
          <Radio
            key={option.value}
            name={name}
            value={option.value}
            label={option.label}
            checked={value === option.value}
            onChange={onChange}
            {...props}
          />
        ))}
      </div>
      
      {error && (
        <p id={errorId} className="form-error-text" role="alert">
          {error}
        </p>
      )}
    </fieldset>
  );
};

export default Radio;