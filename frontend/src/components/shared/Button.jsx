import React from 'react';
import './Button.css';

const Button = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  fullWidth = false,
  iconLeft,
  iconRight,
  onClick,
  type = 'button',
  href,
  className = '',
  ...props
}) => {
  const classNames = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    fullWidth && 'btn--full-width',
    loading && 'btn--loading',
    disabled && 'btn--disabled',
    className
  ].filter(Boolean).join(' ');
  
  const content = (
    <>
      {loading && <span className="btn__spinner" aria-hidden="true" />}
      {!loading && iconLeft && <span className="btn__icon btn__icon--left">{iconLeft}</span>}
      <span className="btn__text">{children}</span>
      {!loading && iconRight && <span className="btn__icon btn__icon--right">{iconRight}</span>}
    </>
  );
  
  if (href && !disabled) {
    return (
      <a
        href={href}
        className={classNames}
        aria-disabled={disabled}
        {...props}
      >
        {content}
      </a>
    );
  }
  
  return (
    <button
      type={type}
      className={classNames}
      onClick={onClick}
      disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {content}
    </button>
  );
};

export default Button;
