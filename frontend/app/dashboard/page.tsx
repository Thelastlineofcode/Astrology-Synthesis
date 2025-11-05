"use client";
import { useEffect, useState } from "react";

type DashaPeriod = {
  name: string;
  start: string; // ISO
  end: string;   // ISO
};

function fmt(ms: number) {
  const s = Math.max(0, Math.floor(ms / 1000));
  const d = Math.floor(s / 86400);
  const h = Math.floor((s % 86400) / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = s % 60;
  return `${d}d ${h}h ${m}m ${ss}s`;
}

export default function DashboardPage() {
  const [periods, setPeriods] = useState<DashaPeriod[]>([]);
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    // Replace with real endpoint when available, e.g., /dasha/active or /users/me/dasha
    (async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/dasha/active`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("mula_token") ?? ""}`,
          },
        });
        if (!res.ok) throw new Error("Failed to load periods");
        const data = await res.json();
        setPeriods(data?.periods ?? []);
      } catch {
        // Fallback demo data for MVP until backend route is live
        setPeriods([
          { name: "Mahadasha: Saturn", start: new Date(Date.now() - 5*24*3600*1000).toISOString(), end: new Date(Date.now() + 20*24*3600*1000).toISOString() },
          { name: "Antardasha: Mercury", start: new Date(Date.now() - 2*24*3600*1000).toISOString(), end: new Date(Date.now() + 3*24*3600*1000).toISOString() },
        ]);
      }
    })();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <p className="text-neutral-300">Your active and upcoming dasha periods.</p>
      <div className="grid sm:grid-cols-2 gap-4">
        {periods.map((p, i) => {
          const endMs = new Date(p.end).getTime();
          const remaining = endMs - now;
          const percent = Math.min(100, Math.max(0, ((now - new Date(p.start).getTime()) / (endMs - new Date(p.start).getTime())) * 100));
          return (
            <div key={i} className="rounded border border-white/10 p-4 bg-white/5">
              <div className="flex items-center justify-between mb-2">
                <h2 className="font-medium">{p.name}</h2>
                <span className="text-xs text-neutral-400">ends {new Date(p.end).toLocaleString()}</span>
              </div>
              <div className="w-full h-2 bg-white/10 rounded overflow-hidden mb-2">
                <div className="h-full bg-white" style={{ width: `${percent}%` }} />
              </div>
              <div className="text-sm text-neutral-300">Time remaining: {fmt(remaining)}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
