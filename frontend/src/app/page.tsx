export default function Home() {
  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'var(--bg-primary)',
      color: 'var(--text-primary)',
      fontFamily: 'var(--font-geist-sans), Arial, sans-serif'
    }}>
      <main style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        gap: '24px', 
        textAlign: 'center', 
        padding: '64px 32px' 
      }}>
        <h1 style={{ 
          fontSize: '3rem', 
          fontWeight: 'bold',
          color: 'var(--text-primary)',
          marginBottom: '16px'
        }}>
          Roots Revealed
        </h1>
        <p style={{ 
          fontSize: '1.25rem', 
          maxWidth: '500px',
          color: 'var(--text-secondary)',
          lineHeight: '1.6'
        }}>
          Explore your cosmic journey with our astrology dashboard. Discover the celestial influences that shape your destiny.
        </p>
        <a
          href="/dashboard"
          className="cta-button"
          style={{
            marginTop: '24px',
            padding: '16px 32px',
            borderRadius: '12px',
            fontWeight: '600',
            textDecoration: 'none',
            background: 'var(--color-primary)',
            color: 'var(--color-neutral-50)',
            transition: 'all 0.3s ease',
            boxShadow: 'var(--elevation-2)',
            border: 'none',
            cursor: 'pointer',
            display: 'inline-block'
          }}
        >
          View Dashboard
        </a>
      </main>
    </div>
  );
}
