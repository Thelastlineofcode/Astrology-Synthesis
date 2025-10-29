import type { Metadata } from "next";
import "../styles/variables.css";
import "../styles/themes.css";
import "./globals.css";
import ThemeToggle from "../components/shared/ThemeToggle";

// Note: Google Fonts may be blocked in some environments
// Fallback to system fonts is defined in variables.css
// --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
// --font-mono: 'JetBrains Mono', 'Courier New', monospace

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
                var saved = localStorage.getItem('theme');
                var systemPref = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                var theme = saved || systemPref;
                document.documentElement.setAttribute('data-theme', theme);
              } catch (e) { /* ignore */ }
            })})();`,
          }}
        />

        <ThemeToggle />
        {children}
      </body>
    </html>
  );
}
