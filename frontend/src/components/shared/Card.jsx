import React from 'react';
import './Card.css';

const Card = ({
  children,
  variant = 'default',
  padding = 'medium',
  hoverable = false,
  onClick,
  className = '',
  header,
  footer,
  ...props
}) => {
  const classNames = [
    'card',
    `card--${variant}`,
    `card--padding-${padding}`,
    hoverable && 'card--hoverable',
    onClick && 'card--clickable',
    className
  ].filter(Boolean).join(' ');
  
  const handleClick = () => {
    if (onClick) onClick();
  };
  
  const handleKeyDown = (e) => {
    if (onClick && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      onClick();
    }
  };
  
  return (
    <div
      className={classNames}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      tabIndex={onClick ? 0 : undefined}
      role={onClick ? 'button' : undefined}
      {...props}
    >
      {header && <div className="card__header">{header}</div>}
      <div className="card__content">{children}</div>
      {footer && <div className="card__footer">{footer}</div>}
    </div>
  );
};

export default Card;
