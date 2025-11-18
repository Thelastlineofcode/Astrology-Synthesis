"use client";

import React from "react";
import Link from "next/link";
import "./Button.css";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "tertiary";
  size?: "small" | "medium" | "large";
  href?: string;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "medium",
  disabled = false,
  href,
  onClick,
  className = "",
  ...props
}) => {
  const classNames = [
    "button",
    `button--${variant}`,
    `button--${size}`,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  // If href is provided, render as Link
  if (href && !disabled) {
    return (
      <Link href={href} className={classNames}>
        {children}
      </Link>
    );
  }

  // Otherwise render as button
  return (
    <button
      className={classNames}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
