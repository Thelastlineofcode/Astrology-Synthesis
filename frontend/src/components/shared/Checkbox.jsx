import React, { useId } from 'react';
import './FormInputs.css';

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
  const ref = React.useRef(null);
  
  React.useEffect(() => {
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
