"use client";

import React, { useEffect, useState } from "react";
import "./ThemeToggle.css";

const ThemeToggle = () => {
  const [theme, setTheme] = useState('light');
  const [hasMounted, setHasMounted] = useState(false);

  useEffect(() => {
    // Set mounted flag
    setHasMounted(true);
    
    // Initialize theme from localStorage or system preference
    let initial = 'light';
    try {
      const saved = localStorage.getItem('theme');
      const system = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      initial = saved || system;
      document.documentElement.setAttribute('data-theme', initial);
    } catch (_e) {
      // ignore (server or privacy constraints)
    }
    
    // Update state after mount
    setTheme(initial);

    // Listen to changes in system preference if user hasn't chosen explicitly
    try {
      const mql = window.matchMedia('(prefers-color-scheme: dark)');
      const onChange = (e) => {
        const savedTheme = localStorage.getItem('theme');
        if (!savedTheme) {
          const newTheme = e.matches ? 'dark' : 'light';
          setTheme(newTheme);
          document.documentElement.setAttribute('data-theme', newTheme);
        }
      };
      if (mql && mql.addEventListener) mql.addEventListener('change', onChange);
      else if (mql && mql.addListener) mql.addListener(onChange);

      return () => {
        if (mql && mql.removeEventListener) mql.removeEventListener('change', onChange);
        else if (mql && mql.removeListener) mql.removeListener(onChange);
      };
    } catch (_e) {
      // ignore
    }
  }, []);

  const toggleTheme = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    try { localStorage.setItem('theme', next); } catch (_e) { /* ignore */ }
    document.documentElement.setAttribute('data-theme', next);
  };

  // Avoid rendering UI until mounted (prevents mismatch)
  if (!hasMounted) return null;

  return (
    <button
      className="theme-toggle"
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      <span className="sr-only">Toggle theme</span>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
};

export default ThemeToggle;
