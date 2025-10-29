"use client";

import React, { useId, useRef, useEffect } from 'react';
import './FormInputs.css';

/**
 * Checkbox component - accessible checkbox with indeterminate state
 * 
 * @param {string} label - Required label text
 * @param {boolean} checked - Whether checkbox is checked
 * @param {function} onChange - Change handler
 * @param {boolean} disabled - Whether checkbox is disabled
 * @param {boolean} indeterminate - Whether checkbox is in indeterminate state
 * @param {string} className - Additional CSS classes
 * 
 * @accessibility
 * - Label associated via htmlFor/id
 * - Focus states clearly visible
 * - Keyboard accessible (Space to toggle)
 * - Indeterminate state properly handled
 */
const Checkbox = ({
  label,
  checked,
  onChange,
  disabled = false,
  indeterminate = false,
  className = '',
  ...props
}) => {
  const id = useId();
  const ref = useRef(null);
  
  useEffect(() => {
    if (ref.current) {
      ref.current.indeterminate = indeterminate;
    }
  }, [indeterminate]);
  
  return (
    <div className={`form-checkbox ${className}`}>
      <input
        ref={ref}
        id={id}
        type="checkbox"
        checked={checked}
        onChange={onChange}
        disabled={disabled}
        className="form-checkbox__input"
        {...props}
      />
      <label htmlFor={id} className="form-checkbox__label">
        {label}
      </label>
    </div>
  );
};

export default Checkbox;