export default function TestPage() {
  return (
    <div style={{ padding: '20px', background: 'white', color: 'black' }}>
      <h1>Test Page</h1>
      <p>If you can see this, the app is working.</p>
      <div style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)', padding: '10px', marginTop: '10px' }}>
        CSS Variables Test: This should use theme colors
      </div>
    </div>
  );
}