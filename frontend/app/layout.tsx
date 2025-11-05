import "./globals.css";
import type { ReactNode } from "react";
import { LogoutButton } from "@/components/logout-button";

export const metadata = {
  title: "Mula Dasha Timer",
  description: "MVP app to view Vedic dasha periods",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-white/10">
          <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between gap-3">
            <a href="/" className="font-semibold">Mula Dasha Timer</a>
            <nav className="flex items-center gap-4 text-sm">
              <a href="/auth/login" className="hover:underline">Login</a>
              <a href="/auth/signup" className="hover:underline">Signup</a>
              <a href="/dashboard" className="hover:underline">Dashboard</a>
              <LogoutButton />
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-10">{children}</main>
      </body>
    </html>
  );
}
