import React, { useId } from 'react';
import './FormInputs.css';

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

// Radio Group Component
export const RadioGroup = ({
  label,
  name,
  options = [],
  value,
  onChange,
  error,
  required = false,
  className = '',
  ...props
}) => {
  const id = useId();
  const errorId = `${id}-error`;
  const labelId = `${id}-label`;
  
  return (
    <div className={`form-radio-group ${error ? 'form-radio-group--error' : ''} ${className}`}>
      <div className="form-radio-group__label">
        <span id={labelId}>
          {label}
          {required && <span className="form-label__required" aria-label="required">*</span>}
        </span>
      </div>
      
      <div 
        className="form-radio-group__options" 
        role="radiogroup"
        aria-labelledby={labelId}
        aria-describedby={error ? errorId : undefined}
        {...props}
      >
        {options.map(option => (
          <Radio
            key={option.value}
            label={option.label}
            name={name}
            value={option.value}
            checked={value === option.value}
            onChange={onChange}
            disabled={option.disabled}
          />
        ))}
      </div>
      
      {error && (
        <p id={errorId} className="form-error-text" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default Radio;
