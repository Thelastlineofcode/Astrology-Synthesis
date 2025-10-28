import React, { useState } from 'react';
import Button from './Button';
import './ButtonDemo.css';

const ButtonDemo = () => {
  const [clickCount, setClickCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    setClickCount(prev => prev + 1);
  };

  const handleLoadingClick = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 3000);
  };

  const PlusIcon = () => (
    <svg viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );

  const ArrowIcon = () => (
    <svg viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );

  return (
    <div className="button-demo">
      <h1>Button Component Demo</h1>
      <p className="demo-subtitle">Testing all variants, sizes, and states</p>
      <p className="click-counter">Button clicks: {clickCount}</p>

      <section className="demo-section">
        <h2>Variants</h2>
        <div className="button-row">
          <Button variant="primary" onClick={handleClick}>Primary Button</Button>
          <Button variant="secondary" onClick={handleClick}>Secondary Button</Button>
          <Button variant="ghost" onClick={handleClick}>Ghost Button</Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>Sizes</h2>
        <div className="button-row">
          <Button size="small" onClick={handleClick}>Small</Button>
          <Button size="medium" onClick={handleClick}>Medium</Button>
          <Button size="large" onClick={handleClick}>Large</Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>Disabled State</h2>
        <div className="button-row">
          <Button variant="primary" disabled>Disabled Primary</Button>
          <Button variant="secondary" disabled>Disabled Secondary</Button>
          <Button variant="ghost" disabled>Disabled Ghost</Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>Loading State</h2>
        <div className="button-row">
          <Button variant="primary" loading={isLoading} onClick={handleLoadingClick}>
            {isLoading ? 'Loading...' : 'Click to Load'}
          </Button>
          <Button variant="secondary" loading>Loading Secondary</Button>
          <Button variant="ghost" loading>Loading Ghost</Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>With Icons</h2>
        <div className="button-row">
          <Button iconLeft={<PlusIcon />} onClick={handleClick}>Add Item</Button>
          <Button iconRight={<ArrowIcon />} onClick={handleClick}>Next</Button>
          <Button variant="secondary" iconLeft={<PlusIcon />} iconRight={<ArrowIcon />} onClick={handleClick}>
            Both Icons
          </Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>Full Width</h2>
        <Button fullWidth variant="primary" onClick={handleClick}>
          Full Width Button
        </Button>
        <br />
        <Button fullWidth variant="secondary" onClick={handleClick}>
          Full Width Secondary
        </Button>
      </section>

      <section className="demo-section">
        <h2>As Links</h2>
        <div className="button-row">
          <Button href="#primary-link" variant="primary">Primary Link</Button>
          <Button href="#secondary-link" variant="secondary">Secondary Link</Button>
          <Button href="#ghost-link" variant="ghost">Ghost Link</Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>Button Types</h2>
        <form onSubmit={(e) => { e.preventDefault(); alert('Form submitted!'); }}>
          <div className="button-row">
            <Button type="submit" variant="primary">Submit Form</Button>
            <Button type="button" variant="secondary" onClick={handleClick}>Regular Button</Button>
            <Button type="reset" variant="ghost">Reset Form</Button>
          </div>
        </form>
      </section>

      <section className="demo-section">
        <h2>Combined Examples</h2>
        <div className="button-row">
          <Button size="small" iconLeft={<PlusIcon />} onClick={handleClick}>
            Small with Icon
          </Button>
          <Button size="large" iconRight={<ArrowIcon />} onClick={handleClick}>
            Large with Icon
          </Button>
          <Button variant="secondary" size="small" disabled>
            Small Disabled
          </Button>
        </div>
      </section>

      <section className="demo-section">
        <h2>Accessibility Testing</h2>
        <div className="button-row">
          <Button aria-label="Add new user" iconLeft={<PlusIcon />} onClick={handleClick}>
            Add User (with aria-label)
          </Button>
          <Button onClick={handleClick}>
            Keyboard Test (Tab + Enter/Space)
          </Button>
        </div>
        <p className="accessibility-note">
          ⌨️ Test keyboard navigation: Use Tab to focus, Enter or Space to activate
        </p>
      </section>
    </div>
  );
};

export default ButtonDemo;
