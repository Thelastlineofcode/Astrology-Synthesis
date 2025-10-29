import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center font-sans">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-center gap-8 py-16 px-8">
        <div className="flex flex-col items-center gap-6 text-center">
          <h1 className="text-4xl font-bold leading-tight tracking-tight">
            Roots Revealed
          </h1>
          <p className="max-w-md text-lg leading-8 text-secondary">
            Discover the roots of your astrological birth chart and explore your cosmic journey
          </p>
        </div>
        
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <Link
            href="/dashboard"
            className="flex h-12 w-full items-center justify-center rounded-lg px-8 transition-colors md:w-auto interactive-strong"
          >
            Go to Dashboard
          </Link>
          <Link
            href="/symbolon-demo"
            className="flex h-12 w-full items-center justify-center rounded-lg btn-outline px-8 transition-colors md:w-auto"
          >
            Symbolon Demo
          </Link>
        </div>
      </main>
    </div>
  );
}
