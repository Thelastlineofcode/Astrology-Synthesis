export default function HomePage() {
  return (
    <section className="space-y-10">
      <div className="space-y-4">
        <h1 className="text-4xl font-semibold tracking-tight">Mula Dasha Timer</h1>
        <p className="text-neutral-300 max-w-2xl">
          Track your current Vedic dasha periods with a clean, focused interface. See what’s active now and how long remains.
        </p>
        <div className="flex flex-wrap gap-3">
          <a href="/auth/signup" className="px-4 py-2 rounded bg-white text-black">Get Started</a>
          <a href="/auth/login" className="px-4 py-2 rounded border border-white/20">Log in</a>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <div className="rounded border border-white/10 bg-white/5 p-4">
          <h2 className="font-medium mb-1">Active Dasha</h2>
          <p className="text-sm text-neutral-300">See what’s influencing you right now with a live countdown.</p>
        </div>
        <div className="rounded border border-white/10 bg-white/5 p-4">
          <h2 className="font-medium mb-1">Simple & Fast</h2>
          <p className="text-sm text-neutral-300">Built as a small MVP—minimal clicks, clear outcomes.</p>
        </div>
        <div className="rounded border border-white/10 bg-white/5 p-4">
          <h2 className="font-medium mb-1">Demo-ready</h2>
          <p className="text-sm text-neutral-300">Works with a demo backend; upgrades seamlessly to production.</p>
        </div>
      </div>
    </section>
  );
}
