"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center font-sans" style={{ background: 'var(--bg-primary)' }}>
      <main className="flex flex-col items-start gap-6 px-8 py-16 max-w-4xl">
        {/* Typography Scale Demo */}
        <section style={{ width: '100%', marginBottom: 'var(--space-5)' }}>
          <h1 style={{ marginBottom: 'var(--space-3)' }}>
            Roots Revealed
          </h1>
          <p className="text-secondary" style={{ fontSize: 'var(--font-size-body)', lineHeight: 'var(--line-height-loose)' }}>
            Discover the roots of your astrological birth chart with comprehensive insights.
          </p>
        </section>

        {/* Typography Hierarchy Examples */}
        <section style={{ width: '100%', marginBottom: 'var(--space-4)' }}>
          <h2 style={{ marginBottom: 'var(--space-3)' }}>Your Cosmic Journey</h2>
          <p style={{ marginBottom: 'var(--space-3)', lineHeight: 'var(--line-height-normal)' }}>
            Explore the depths of your birth chart with our comprehensive astrology platform. 
            We combine ancient wisdom with modern technology to reveal insights about your 
            personality, relationships, and life path.
          </p>
          
          <h3 style={{ marginBottom: 'var(--space-2)', marginTop: 'var(--space-4)' }}>Personalized Insights</h3>
          <p style={{ marginBottom: 'var(--space-3)' }}>
            Each chart is unique, reflecting the precise cosmic configuration at your moment of birth. 
            Our system calculates planetary positions, houses, and aspects with astronomical precision.
          </p>

          <h4 style={{ marginBottom: 'var(--space-2)' }}>Chart Components</h4>
          <p style={{ marginBottom: 'var(--space-2)' }}>
            Your birth chart includes planets, houses, and aspects that create a complex web of meaning.
          </p>
          
          <small className="text-secondary" style={{ display: 'block', marginBottom: 'var(--space-2)' }}>
            Example birth data: January 1, 2000 at 12:00 PM in New York, NY
          </small>
          
          <code className="mono" style={{ 
            display: 'block', 
            padding: 'var(--space-2)', 
            background: 'var(--bg-secondary)',
            borderRadius: 'var(--radius-1)',
            marginBottom: 'var(--space-2)'
          }}>
            Sun: 10°37&apos; Capricorn | Moon: 24°12&apos; Pisces | ASC: 15°45&apos; Libra
          </code>
          
          <p className="text-tiny text-secondary">
            * All calculations use Swiss Ephemeris for maximum accuracy
          </p>
        </section>

        {/* Font Weight Examples */}
        <section style={{ width: '100%', marginBottom: 'var(--space-4)' }}>
          <h3 style={{ marginBottom: 'var(--space-3)' }}>Typography Features</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
            <p className="font-light">Light weight (300) - Delicate and refined</p>
            <p className="font-regular">Regular weight (400) - Standard body text</p>
            <p className="font-medium">Medium weight (500) - Emphasized content</p>
            <p className="font-semibold">Semibold weight (600) - Strong emphasis</p>
            <p className="font-bold">Bold weight (700) - Maximum impact</p>
          </div>
        </section>

        {/* CTA Button */}
        <section style={{ width: '100%', textAlign: 'center', marginTop: 'var(--space-5)' }}>
          <Link
            href="/dashboard"
            className="font-medium"
            style={{ 
              display: 'inline-block',
              padding: 'var(--space-3) var(--space-5)',
              background: 'var(--color-primary)', 
              color: 'var(--color-neutral-50)',
              borderRadius: 'var(--radius-2)',
              textDecoration: 'none',
              transition: 'transform 0.2s ease, box-shadow 0.2s ease',
              fontSize: 'var(--font-size-body)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.05)';
              e.currentTarget.style.boxShadow = 'var(--shadow-2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            View Dashboard
          </Link>
        </section>
      </main>
    </div>
  );
}
