"use client";

import React, { useState } from 'react';
import { Spinner, Skeleton, SkeletonCard, SkeletonTable } from '@/components/shared';

export default function LoadingDemoPage() {
  const [showContent, setShowContent] = useState(false);

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem', fontSize: '2rem', fontWeight: 'bold' }}>Loading Components Demo</h1>
      
      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>Spinners</h2>
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <p style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}>Small</p>
            <Spinner size="small" />
          </div>
          <div>
            <p style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}>Medium (default)</p>
            <Spinner size="medium" />
          </div>
          <div>
            <p style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}>Large</p>
            <Spinner size="large" />
          </div>
        </div>
        
        <h3 style={{ marginTop: '2rem', marginBottom: '1rem', fontSize: '1.25rem', fontWeight: '600' }}>Color Variants</h3>
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <p style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}>Primary</p>
            <Spinner color="primary" />
          </div>
          <div>
            <p style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}>Secondary</p>
            <Spinner color="secondary" />
          </div>
          <div style={{ background: 'var(--color-primary)', padding: '1rem', borderRadius: '8px' }}>
            <p style={{ marginBottom: '0.5rem', fontSize: '0.875rem', color: 'white' }}>Light</p>
            <Spinner color="light" />
          </div>
        </div>
      </section>

      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>Skeleton Variants</h2>
        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: '600' }}>Text Lines</h3>
          <Skeleton variant="text" width="100%" count={3} />
        </div>
        
        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: '600' }}>Rectangle</h3>
          <Skeleton variant="rect" width="100%" height={200} />
        </div>
        
        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: '600' }}>Circle</h3>
          <Skeleton variant="circle" width={100} height={100} />
        </div>
      </section>

      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>Skeleton Card</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
      </section>

      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>Skeleton Table</h2>
        <SkeletonTable rows={5} />
      </section>

      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>Layout Shift Test</h2>
        <button 
          onClick={() => setShowContent(!showContent)}
          style={{
            padding: '0.5rem 1rem',
            background: 'var(--color-primary)',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginBottom: '1rem'
          }}
        >
          Toggle Content
        </button>
        
        <div style={{ border: '2px solid var(--border-color)', borderRadius: '8px', padding: '1rem' }}>
          {showContent ? (
            <div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>Real Content Loaded</h3>
              <p style={{ marginBottom: '0.5rem' }}>This is the actual content that replaces the skeleton.</p>
              <p style={{ marginBottom: '0.5rem' }}>Notice there is no layout shift when content loads.</p>
              <p>The skeleton dimensions match the actual content dimensions.</p>
            </div>
          ) : (
            <div>
              <Skeleton variant="text" width="60%" height={24} count={1} />
              <Skeleton variant="text" width="100%" count={3} />
            </div>
          )}
        </div>
      </section>

      <section>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', fontWeight: '600' }}>Accessibility Notes</h2>
        <ul style={{ listStyle: 'disc', paddingLeft: '2rem' }}>
          <li>Spinner has <code>role="status"</code> and <code>aria-label</code></li>
          <li>Skeleton has <code>aria-busy="true"</code> and <code>aria-live="polite"</code></li>
          <li>Loading text is available to screen readers via visually-hidden class</li>
          <li>Skeleton elements are hidden from screen readers with <code>aria-hidden="true"</code></li>
        </ul>
      </section>
    </div>
  );
}
