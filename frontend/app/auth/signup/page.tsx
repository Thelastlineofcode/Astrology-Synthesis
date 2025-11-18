"use client";
import { useState } from "react";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error("Signup failed");
      window.location.href = "/auth/login";
    } catch (err: any) {
      setError(err.message ?? "Signup failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Create account</h1>
      <form onSubmit={onSubmit} className="space-y-4">
        <input className="w-full px-3 py-2 rounded bg-neutral-900 border border-white/10" placeholder="Email" type="email" value={email} onChange={e=>setEmail(e.target.value)} required />
        <input className="w-full px-3 py-2 rounded bg-neutral-900 border border-white/10" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button disabled={loading} className="px-4 py-2 rounded bg-white text-black disabled:opacity-60">
          {loading ? "Creating..." : "Create account"}
        </button>
      </form>
    </div>
  );
}
