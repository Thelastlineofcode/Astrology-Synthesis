"use client";
import { useRequireAuth } from "@/lib/requireAuth";
import { useEffect, useState } from "react";

export default function DashboardPage() {
  useRequireAuth();

  type Me = { id: string; email: string; first_name?: string; last_name?: string };
  const [me, setMe] = useState<Me | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/users/me`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("mula_token") ?? ""}` },
        });
        if (res.ok) setMe(await res.json());
      } catch {}
    })();
  }, []);

  return (
    <div className="space-y-2 mb-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      {me && (
        <p className="text-sm text-neutral-300">Welcome back{me.first_name ? `, ${me.first_name}` : ""}.</p>
      )}
    </div>
  );
}
