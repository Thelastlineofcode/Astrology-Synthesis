"use client";
import { useEffect, useState } from "react";
import { useRequireAuth } from "@/lib/requireAuth";

export default function NotificationSettingsPage() {
  useRequireAuth();

  type Prefs = { email_enabled: boolean; digest: "off" | "daily" | "weekly" };
  const [prefs, setPrefs] = useState<Prefs>({ email_enabled: true, digest: "daily" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notifications/preferences`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("mula_token") ?? ""}` },
        });
        if (res.ok) {
          const data = await res.json();
          setPrefs({
            email_enabled: Boolean(data?.email_enabled),
            digest: (data?.digest as Prefs["digest"]) ?? "daily",
          });
        }
      } catch {}
    })();
  }, []);

  async function save() {
    setSaving(true);
    setError(null);
    setSaved(false);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/notifications/preferences`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("mula_token") ?? ""}`,
        },
        body: JSON.stringify(prefs),
      });
      if (!res.ok) throw new Error(await res.text());
      setSaved(true);
    } catch (e: any) {
      setError(e.message ?? "Failed to save");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6 max-w-lg">
      <div>
        <h1 className="text-2xl font-semibold">Notifications</h1>
        <p className="text-sm text-neutral-300">Control email notifications for dasha transitions.</p>
      </div>

      <div className="rounded border border-white/10 bg-white/5 p-4 space-y-4">
        <label className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={prefs.email_enabled}
            onChange={(e) => setPrefs((p) => ({ ...p, email_enabled: e.target.checked }))}
          />
          <span>Email notifications</span>
        </label>

        <div className="space-y-2">
          <div className="text-sm text-neutral-300">Digest frequency</div>
          <div className="flex gap-3">
            {(["off", "daily", "weekly"] as const).map((d) => (
              <label key={d} className="flex items-center gap-2">
                <input
                  type="radio"
                  name="digest"
                  value={d}
                  checked={prefs.digest === d}
                  onChange={() => setPrefs((p) => ({ ...p, digest: d }))}
                />
                <span className="capitalize">{d}</span>
              </label>
            ))}
          </div>
        </div>

        {error && <p className="text-sm text-red-400">{error}</p>}

        <div className="flex items-center gap-3">
          <button disabled={saving} onClick={save} className="px-4 py-2 rounded bg-white text-black disabled:opacity-60">
            {saving ? "Saving..." : "Save"}
          </button>
          {saved && <span className="text-sm text-green-400">Saved</span>}
        </div>
      </div>
    </div>
  );
}
