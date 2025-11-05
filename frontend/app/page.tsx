export default function HomePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Welcome</h1>
      <p className="text-neutral-300">
        This is the MVP for viewing your current and upcoming Vedic dasha periods.
      </p>
      <div className="flex gap-3">
        <a href="/auth/signup" className="px-4 py-2 rounded bg-white text-black">Get Started</a>
        <a href="/auth/login" className="px-4 py-2 rounded border border-white/20">Log in</a>
      </div>
    </div>
  );
}
