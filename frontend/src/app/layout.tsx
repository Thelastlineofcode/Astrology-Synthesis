import type { Metadata } from "next";
import "../styles/variables.css";
import "../styles/themes.css";
import "./globals.css";
import ThemeToggle from "../components/shared/ThemeToggle";

export const metadata: Metadata = {
  title: "Roots Revealed",
  description: "Discover the roots of your astrological birth chart",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {/* Inline script to set initial theme before React hydrates to avoid FOIT/flash */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(${String(function () {
              try {
                const saved = localStorage.getItem('theme');
                const systemPref = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                const theme = saved || systemPref;
                document.documentElement.setAttribute('data-theme', theme);
              } catch (_e) { /* ignore */ }
            })})();`,
          }}
        />

        <ThemeToggle />
        {children}
      </body>
    </html>
  );
}
