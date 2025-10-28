import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from '../shared/ThemeToggle';
import './Navigation.css';

const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const mobileMenuRef = useRef(null);
  const hamburgerRef = useRef(null);
  
  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location]);
  
  // Close menu on Escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') setMobileMenuOpen(false);
    };
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, []);
  
  // Focus trap for mobile menu
  useEffect(() => {
    if (mobileMenuOpen && mobileMenuRef.current) {
      const focusableElements = mobileMenuRef.current.querySelectorAll(
        'a[href], button:not([disabled])'
      );
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      
      const handleTabKey = (e) => {
        if (e.key !== 'Tab') return;
        
        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      };
      
      document.addEventListener('keydown', handleTabKey);
      firstElement?.focus();
      
      return () => document.removeEventListener('keydown', handleTabKey);
    } else if (!mobileMenuOpen && hamburgerRef.current) {
      // Return focus to hamburger button when menu closes
      hamburgerRef.current.focus();
    }
  }, [mobileMenuOpen]);
  
  const navItems = [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/chart', label: 'New Chart' },
    { path: '/bmad', label: 'BMAD Analysis' },
    { path: '/symbolon', label: 'Symbolon Cards' },
    { path: '/journal', label: 'Journal' },
  ];
  
  return (
    <>
      <nav className="nav" role="navigation" aria-label="Main navigation">
        <div className="nav__container">
          {/* Logo */}
          <Link to="/" className="nav__logo">
            <span className="nav__logo-icon">✨</span>
            <span className="nav__logo-text">BMAD Astrology</span>
          </Link>
          
          {/* Desktop Navigation */}
          <ul className="nav__menu">
            {navItems.map(item => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`nav__link ${location.pathname === item.path ? 'nav__link--active' : ''}`}
                  aria-current={location.pathname === item.path ? 'page' : undefined}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
          
          {/* Theme Toggle */}
          <div className="nav__actions">
            <ThemeToggle />
            
            {/* Mobile Menu Button */}
            <button
              ref={hamburgerRef}
              className="nav__hamburger"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={mobileMenuOpen}
            >
              <span className="nav__hamburger-line"></span>
              <span className="nav__hamburger-line"></span>
              <span className="nav__hamburger-line"></span>
            </button>
          </div>
        </div>
      </nav>
      
      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <>
          <div 
            className="nav__overlay"
            onClick={() => setMobileMenuOpen(false)}
            aria-hidden="true"
          />
          <div 
            ref={mobileMenuRef}
            className="nav__mobile-menu" 
            role="dialog" 
            aria-label="Mobile menu"
          >
            <ul>
              {navItems.map(item => (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`nav__mobile-link ${location.pathname === item.path ? 'nav__mobile-link--active' : ''}`}
                    aria-current={location.pathname === item.path ? 'page' : undefined}
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </>
  );
};

export default Navigation;
