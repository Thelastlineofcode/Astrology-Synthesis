import React, { useId } from 'react';
import './FormInputs.css';

const TextInput = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  error,
  helperText,
  required = false,
  disabled = false,
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
      
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : helperText ? helperId : undefined}
        className="form-input"
        {...props}
      />
      
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

export default TextInput;
