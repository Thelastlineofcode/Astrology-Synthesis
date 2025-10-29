import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center font-sans" style={{ background: 'var(--bg-primary)' }}>
      <main className="flex flex-col items-center gap-6 text-center px-8 py-16">
        <h1 className="text-4xl font-bold" style={{ color: 'var(--text-primary)' }}>
          Roots Revealed
        </h1>
        <p className="text-xl max-w-md" style={{ color: 'var(--text-secondary)' }}>
          Explore your cosmic journey with our new dashboard.
        </p>
        <Link
          href="/dashboard"
          className="mt-4 px-8 py-4 rounded-lg font-medium transition-all hover:scale-105"
          style={{ 
            background: 'var(--color-primary)', 
            color: 'var(--color-neutral-50)',
          }}
        >
          View Dashboard
        </Link>
      </main>
    </div>
  );
}
