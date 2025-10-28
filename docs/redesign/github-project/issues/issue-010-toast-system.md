---
title: "Build Toast/Notification System"
labels: ["component:design-system", "P1-High", "ui-component"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Create a toast notification system for displaying success, error, info, and warning messages with auto-dismiss and manual close options.

## 📋 Description

Toasts provide feedback for user actions (chart saved, error occurred, form submitted). Build a notification system that displays messages in the corner of the screen, stacks multiple toasts, and auto-dismisses after a timeout.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Shared Components)
- **Guide**: `AI_COPILOT_GUIDE.md` - Feedback Patterns

## ✅ Acceptance Criteria

- [ ] Four variants: success, error, warning, info
- [ ] Toast appears in corner (top-right by default)
- [ ] Auto-dismiss after 5 seconds (configurable)
- [ ] Manual close button
- [ ] Multiple toasts stack vertically
- [ ] Slide-in animation on appear
- [ ] Slide-out animation on dismiss
- [ ] Icon for each variant
- [ ] Context API or hook for easy usage (`useToast`)
- [ ] Pause auto-dismiss on hover
- [ ] Screen reader announces toast messages

## 💻 Implementation Notes

### Toast Context & Provider

```jsx
// /frontend/src/contexts/ToastContext.jsx
import React, { createContext, useContext, useState, useCallback } from 'react';
import Toast from '../components/shared/Toast';

const ToastContext = createContext();

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);
  
  const addToast = useCallback((message, variant = 'info', duration = 5000) => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message, variant, duration }]);
    return id;
  }, []);
  
  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);
  
  const toast = {
    success: (message, duration) => addToast(message, 'success', duration),
    error: (message, duration) => addToast(message, 'error', duration),
    warning: (message, duration) => addToast(message, 'warning', duration),
    info: (message, duration) => addToast(message, 'info', duration),
  };
  
  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="toast-container">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            {...toast}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
};
```

### Toast Component

```jsx
// /frontend/src/components/shared/Toast.jsx
import React, { useEffect, useState } from 'react';
import './Toast.css';

const icons = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ'
};

const Toast = ({ id, message, variant, duration, onClose }) => {
  const [isPaused, setIsPaused] = useState(false);
  const [progress, setProgress] = useState(100);
  
  useEffect(() => {
    if (isPaused || !duration) return;
    
    const startTime = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, 100 - (elapsed / duration) * 100);
      setProgress(remaining);
      
      if (remaining === 0) {
        onClose();
      }
    }, 50);
    
    return () => clearInterval(interval);
  }, [duration, onClose, isPaused]);
  
  return (
    <div
      className={`toast toast--${variant}`}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      role="alert"
      aria-live="polite"
    >
      <div className="toast__icon">{icons[variant]}</div>
      <div className="toast__message">{message}</div>
      <button
        className="toast__close"
        onClick={onClose}
        aria-label="Close notification"
      >
        ×
      </button>
      {duration && (
        <div 
          className="toast__progress"
          style={{ width: `${progress}%` }}
        />
      )}
    </div>
  );
};

export default Toast;
```

### Toast Styles

```css
/* /frontend/src/components/shared/Toast.css */
.toast-container {
  position: fixed;
  top: var(--space-6);
  right: var(--space-6);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  max-width: 400px;
}

.toast {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--bg-secondary);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  animation: slideIn 250ms ease;
  overflow: hidden;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Variants */
.toast--success {
  border-left: 4px solid var(--color-success);
}

.toast--error {
  border-left: 4px solid var(--color-error);
}

.toast--warning {
  border-left: 4px solid var(--color-warning);
}

.toast--info {
  border-left: 4px solid var(--color-info);
}

/* Icon */
.toast__icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  flex-shrink: 0;
}

.toast--success .toast__icon {
  color: var(--color-success);
}

.toast--error .toast__icon {
  color: var(--color-error);
}

.toast--warning .toast__icon {
  color: var(--color-warning);
}

.toast--info .toast__icon {
  color: var(--color-info);
}

/* Message */
.toast__message {
  flex: 1;
  font-size: var(--font-size-body);
  color: var(--text-primary);
  line-height: var(--line-height-normal);
}

/* Close Button */
.toast__close {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  font-size: 24px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 150ms ease;
  flex-shrink: 0;
}

.toast__close:hover {
  color: var(--text-primary);
}

/* Progress Bar */
.toast__progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: var(--color-primary);
  transition: width 50ms linear;
}

/* Mobile */
@media (max-width: 767px) {
  .toast-container {
    top: var(--space-4);
    right: var(--space-4);
    left: var(--space-4);
    max-width: none;
  }
}
```

### Usage Example

```jsx
// Example: Using toast in a component
import { useToast } from '../contexts/ToastContext';

const ChartForm = () => {
  const toast = useToast();
  
  const handleSubmit = async (data) => {
    try {
      await saveChart(data);
      toast.success('Chart saved successfully!');
    } catch (error) {
      toast.error('Failed to save chart. Please try again.');
    }
  };
  
  return <form onSubmit={handleSubmit}>...</form>;
};
```

## 🧪 Testing Checklist

- [ ] Toast appears when triggered
- [ ] All four variants display with correct colors
- [ ] Icons display for each variant
- [ ] Auto-dismiss works after 5 seconds
- [ ] Manual close button works
- [ ] Multiple toasts stack vertically
- [ ] Slide-in animation smooth
- [ ] Progress bar animates correctly
- [ ] Hover pauses auto-dismiss
- [ ] Mouse leave resumes auto-dismiss
- [ ] Screen reader announces new toasts
- [ ] Responsive on mobile (full width)

## 🔍 Accessibility Requirements

- [ ] Toasts have `role="alert"` and `aria-live="polite"`
- [ ] Close button has `aria-label`
- [ ] Toast messages announced by screen readers
- [ ] Toast dismissal announced (bonus)
- [ ] Keyboard accessible (Escape to dismiss all)
- [ ] No motion for users with `prefers-reduced-motion`

## 📦 Files to Create/Modify

- `frontend/src/contexts/ToastContext.jsx` (create)
- `frontend/src/components/shared/Toast.jsx` (create)
- `frontend/src/components/shared/Toast.css` (create)
- `frontend/src/components/shared/Toast.test.jsx` (create)
- `frontend/src/App.jsx` (wrap with ToastProvider)

## 🔗 Dependencies

- Issue #1 (CSS Variables)
- React Context API

## 📝 Additional Notes

- Consider adding action button in toast (e.g., "Undo")
- Consider positioning options (top-left, bottom-right, etc.)
- Test with rapid successive toasts (queue management)
- Ensure toasts don't block critical UI
- Add unit tests for toast queue logic

---

**Priority**: P1 (High)  
**Estimated Effort**: 5 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
