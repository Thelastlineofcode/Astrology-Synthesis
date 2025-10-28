---
title: "Create Modal/Dialog Component"
labels: ["component:design-system", "P0-Critical", "ui-component"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Build a reusable, accessible Modal/Dialog component for confirmations, forms, and detailed content display.

## 📋 Description

Modals are used throughout the app for confirmations (delete actions), forms (settings), and detail views (Symbolon cards, chart info). Create a flexible component with proper accessibility (focus trapping, Escape key, ARIA).

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Shared Components)
- **Guide**: `AI_COPILOT_GUIDE.md` - Modal Accessibility

## ✅ Acceptance Criteria

- [ ] Modal opens and closes programmatically
- [ ] Overlay darkens background
- [ ] Modal centers on screen (all viewports)
- [ ] Close button in header
- [ ] Close on Escape key
- [ ] Close on overlay click (optional prop)
- [ ] Sizes: small, medium, large, fullscreen
- [ ] Header, content, footer sections
- [ ] Focus trapped within modal when open
- [ ] Focus returned to trigger element on close
- [ ] Body scroll locked when modal open
- [ ] Smooth fade-in animation

## 💻 Implementation Notes

### Modal Component

```jsx
// /frontend/src/components/shared/Modal.jsx
import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import Button from './Button';
import './Modal.css';

const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'medium',
  closeOnOverlayClick = true,
  showCloseButton = true,
  className = ''
}) => {
  const modalRef = useRef(null);
  const previousActiveElement = useRef(null);
  
  useEffect(() => {
    if (isOpen) {
      // Store previously focused element
      previousActiveElement.current = document.activeElement;
      
      // Lock body scroll
      document.body.style.overflow = 'hidden';
      
      // Focus modal
      setTimeout(() => {
        modalRef.current?.focus();
      }, 100);
    } else {
      // Unlock body scroll
      document.body.style.overflow = '';
      
      // Return focus
      previousActiveElement.current?.focus();
    }
    
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);
  
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);
  
  // Focus trap
  const handleTabKey = (e) => {
    if (!modalRef.current) return;
    
    const focusableElements = modalRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  };
  
  if (!isOpen) return null;
  
  return createPortal(
    <>
      <div 
        className="modal-overlay"
        onClick={closeOnOverlayClick ? onClose : undefined}
        aria-hidden="true"
      />
      <div
        ref={modalRef}
        className={`modal modal--${size} ${className}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        onKeyDown={handleTabKey}
      >
        {showCloseButton && (
          <button
            className="modal__close"
            onClick={onClose}
            aria-label="Close modal"
          >
            ×
          </button>
        )}
        
        {title && (
          <div className="modal__header">
            <h2 id="modal-title" className="modal__title">{title}</h2>
          </div>
        )}
        
        <div className="modal__content">
          {children}
        </div>
        
        {footer && (
          <div className="modal__footer">
            {footer}
          </div>
        )}
      </div>
    </>,
    document.body
  );
};

export default Modal;
```

### Modal Styles

```css
/* /frontend/src/components/shared/Modal.css */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  animation: fadeIn 200ms ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg-secondary);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  z-index: 1100;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 250ms ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translate(-50%, -48%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

/* Sizes */
.modal--small {
  width: 90%;
  max-width: 400px;
}

.modal--medium {
  width: 90%;
  max-width: 600px;
}

.modal--large {
  width: 90%;
  max-width: 900px;
}

.modal--fullscreen {
  width: 100%;
  max-width: 100%;
  height: 100vh;
  max-height: 100vh;
  border-radius: 0;
}

/* Close Button */
.modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
  border: none;
  border-radius: 50%;
  font-size: 32px;
  line-height: 1;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 150ms ease;
  z-index: 10;
}

.modal__close:hover {
  background: var(--color-error);
  color: white;
  transform: scale(1.1);
}

.modal__close:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Header */
.modal__header {
  padding: var(--space-6) var(--space-6) var(--space-4);
  border-bottom: 1px solid var(--border-color);
}

.modal__title {
  margin: 0;
  padding-right: var(--space-8); /* Space for close button */
  font-size: var(--font-size-h3);
  color: var(--text-primary);
}

/* Content */
.modal__content {
  padding: var(--space-6);
}

/* Footer */
.modal__footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
}

/* Mobile adjustments */
@media (max-width: 767px) {
  .modal--small,
  .modal--medium,
  .modal--large {
    width: 95%;
    max-height: 85vh;
  }
  
  .modal__header,
  .modal__content,
  .modal__footer {
    padding: var(--space-4);
  }
}
```

### Usage Example

```jsx
// Example: Confirmation Modal
const DeleteConfirmationModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  const handleDelete = () => {
    // Perform delete action
    setIsOpen(false);
  };
  
  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Delete Chart</Button>
      
      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Confirm Deletion"
        size="small"
        footer={
          <>
            <Button variant="secondary" onClick={() => setIsOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleDelete}>
              Delete
            </Button>
          </>
        }
      >
        <p>Are you sure you want to delete this chart? This action cannot be undone.</p>
      </Modal>
    </>
  );
};
```

## 🧪 Testing Checklist

- [ ] Modal opens when `isOpen={true}`
- [ ] Modal closes on close button click
- [ ] Modal closes on Escape key
- [ ] Modal closes on overlay click (when enabled)
- [ ] Focus trapped within modal (Tab/Shift+Tab cycles)
- [ ] Focus returns to trigger element on close
- [ ] Body scroll locked when modal open
- [ ] All sizes (small, medium, large) display correctly
- [ ] Header, content, footer sections render
- [ ] Animation smooth (fade-in, slide-up)
- [ ] Responsive on mobile (95% width, max-height)
- [ ] Multiple modals stack correctly (z-index)

## 🔍 Accessibility Requirements

- [ ] Modal has `role="dialog"` and `aria-modal="true"`
- [ ] Title linked via `aria-labelledby`
- [ ] Close button has `aria-label`
- [ ] Focus trapped within modal when open
- [ ] Focus returned to trigger element on close
- [ ] Escape key closes modal
- [ ] Screen reader announces modal open/close
- [ ] Background content inert (not focusable) when modal open

## 📦 Files to Create/Modify

- `frontend/src/components/shared/Modal.jsx` (create)
- `frontend/src/components/shared/Modal.css` (create)
- `frontend/src/components/shared/Modal.test.jsx` (create)

## 🔗 Dependencies

- Issue #3 (Button Component) - For footer actions
- React (`react-dom` for portal)

## 📝 Additional Notes

- Use `createPortal` to render modal at document body level
- Focus trapping prevents users from tabbing outside modal
- Consider adding confirmation prompts (e.g., "Are you sure?")
- Test with nested modals (e.g., modal within modal)
- Ensure z-index hierarchy correct (modals > nav > content)

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 6 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
