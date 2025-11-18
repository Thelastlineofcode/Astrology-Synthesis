import { NavLink } from "@/components/nav-link";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-white/10">
          <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between gap-3">
            <a href="/" className="font-semibold">Mula Dasha Timer</a>
            <nav className="flex items-center gap-4 text-sm">
              <NavLink href="/auth/login">Login</NavLink>
              <NavLink href="/auth/signup">Signup</NavLink>
              <NavLink href="/dashboard">Dashboard</NavLink>
              <NavLink href="/settings/notifications">Settings</NavLink>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-10">{children}</main>
      </body>
    </html>
  );
}
