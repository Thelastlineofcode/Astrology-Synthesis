---
title: "Build Navigation Bar & Mobile Menu"
labels: ["component:navigation", "P0-Critical", "layout"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Create a responsive navigation bar with logo, menu items, theme toggle, and collapsible mobile menu (hamburger).

## 📋 Description

The navigation bar provides access to all major app sections. It must work seamlessly on mobile (hamburger menu) and desktop (horizontal nav), with clear active states and accessibility.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Layout - Navigation)
- **Design Artifact**: `UX_COPY_GUIDE.md` (Navigation labels)
- **Guide**: `AI_COPILOT_GUIDE.md` - Navigation Requirements

## ✅ Acceptance Criteria

- [ ] Horizontal navigation on desktop (≥1024px)
- [ ] Hamburger menu on mobile/tablet (<1024px)
- [ ] Logo/brand displayed (left side)
- [ ] Theme toggle button (light/dark)
- [ ] Active page highlighted in nav
- [ ] Mobile menu slides in from side
- [ ] Mobile menu closes on route change
- [ ] Keyboard navigable (Tab, Escape to close menu)
- [ ] Sticky/fixed positioning option
- [ ] No layout shift when switching pages

## 💻 Implementation Notes

### Navigation Component

```jsx
// /frontend/src/components/layout/Navigation.jsx
import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from '../shared/ThemeToggle';
import './Navigation.css';

const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  
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
          <div className="nav__mobile-menu" role="dialog" aria-label="Mobile menu">
            <ul>
              {navItems.map(item => (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`nav__mobile-link ${location.pathname === item.path ? 'nav__mobile-link--active' : ''}`}
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
```

### Navigation Styles

```css
/* /frontend/src/components/layout/Navigation.css */
.nav {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-4) var(--space-5);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo */
.nav__logo {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  text-decoration: none;
  color: var(--text-primary);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-h4);
}

.nav__logo-icon {
  font-size: 24px;
}

/* Desktop Menu */
.nav__menu {
  display: none;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--space-2);
}

.nav__link {
  display: block;
  padding: var(--space-3) var(--space-4);
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 8px;
  transition: all 150ms ease;
  font-weight: var(--font-weight-medium);
}

.nav__link:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.nav__link--active {
  background: var(--color-primary);
  color: var(--color-neutral-light);
}

.nav__link:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Actions (Theme Toggle + Hamburger) */
.nav__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

/* Hamburger Button */
.nav__hamburger {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  padding: var(--space-2);
  cursor: pointer;
}

.nav__hamburger-line {
  width: 24px;
  height: 3px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 200ms ease;
}

.nav__hamburger:hover .nav__hamburger-line {
  background: var(--color-primary);
}

/* Mobile Menu */
.nav__overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
}

.nav__mobile-menu {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 80%;
  max-width: 320px;
  background: var(--bg-secondary);
  padding: var(--space-6);
  z-index: 300;
  animation: slideIn 250ms ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.nav__mobile-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav__mobile-menu li {
  margin-bottom: var(--space-2);
}

.nav__mobile-link {
  display: block;
  padding: var(--space-4);
  color: var(--text-primary);
  text-decoration: none;
  border-radius: 8px;
  font-weight: var(--font-weight-medium);
  transition: background 150ms ease;
}

.nav__mobile-link:hover {
  background: var(--bg-hover);
}

.nav__mobile-link--active {
  background: var(--color-primary);
  color: var(--color-neutral-light);
}

/* Desktop (≥1024px) */
@media (min-width: 1024px) {
  .nav__menu {
    display: flex;
  }
  
  .nav__hamburger {
    display: none;
  }
  
  .nav__mobile-menu,
  .nav__overlay {
    display: none;
  }
}

/* Mobile adjustments */
@media (max-width: 767px) {
  .nav__logo-text {
    display: none;
  }
}
```

## 🧪 Testing Checklist

- [ ] Navigation renders on all pages
- [ ] Desktop menu horizontal at ≥1024px
- [ ] Hamburger menu appears at <1024px
- [ ] Mobile menu slides in smoothly
- [ ] Mobile menu closes on route change
- [ ] Mobile menu closes on overlay click
- [ ] Mobile menu closes on Escape key
- [ ] Active page highlighted correctly
- [ ] Theme toggle functional
- [ ] All links keyboard navigable (Tab)
- [ ] Focus visible on all links
- [ ] Logo links to home page
- [ ] No layout shift when opening/closing menu

## 🔍 Accessibility Requirements

- [ ] Navigation has `role="navigation"` and `aria-label`
- [ ] Mobile menu button has `aria-label` and `aria-expanded`
- [ ] Mobile menu has `role="dialog"` and `aria-label`
- [ ] Active links use `aria-current="page"` (bonus)
- [ ] Focus trapped in mobile menu when open (bonus)
- [ ] Skip to main content link (bonus)

## 📦 Files to Create/Modify

- `frontend/src/components/layout/Navigation.jsx` (create)
- `frontend/src/components/layout/Navigation.css` (create)
- `frontend/src/components/layout/Navigation.test.jsx` (create)
- `frontend/src/App.jsx` (add Navigation to layout)

## 🔗 Dependencies

- Issue #1 (ThemeToggle) - Theme toggle button in nav
- React Router (`react-router-dom`)

## 📝 Additional Notes

- Consider adding user profile/avatar (future)
- Consider breadcrumbs for sub-navigation (future)
- Test on iOS Safari (sticky positioning issues)
- Ensure z-index hierarchy correct (nav > modals)

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 6 hours  
**Assignee**: TBD  
**Epic**: Epic 2 - Layout & Navigation
