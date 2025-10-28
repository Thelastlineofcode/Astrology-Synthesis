import React, { useId } from 'react';
import './FormInputs.css';

const Select = ({
  label,
  value,
  onChange,
  options = [],
  error,
  required = false,
  disabled = false,
  placeholder,
  className = '',
  ...props
}) => {
  const id = useId();
  const errorId = `${id}-error`;
  
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
        aria-describedby={error ? errorId : undefined}
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
      
      {error && (
        <p id={errorId} className="form-error-text" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default Select;
