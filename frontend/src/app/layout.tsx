import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../styles/variables.css";
import "../styles/themes.css";
import "./globals.css";
import ThemeToggle from "../components/shared/ThemeToggle";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

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
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
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

        <div style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 1000 }}>
          <ThemeToggle />
        </div>
        {children}
      </body>
    </html>
  );
}
