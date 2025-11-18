import type { Metadata } from "next";
import { Inter, Cinzel } from "next/font/google";
import "../styles/variables.css";
import "../styles/themes.css";
import "./globals.css";
import ThemeToggle from "../components/shared/ThemeToggle";

// Configure Inter for body text
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

// Configure Cinzel for display headings
const cinzel = Cinzel({
  subsets: ["latin"],
  variable: "--font-cinzel",
  weight: ["400", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Mula: The Root",
  description:
    "A modern spiritual companion app combining Vedic astrology, Vodou oracle, and AI guidance",
  icons: {
    icon: [
      { url: "/icon-16.png", sizes: "16x16", type: "image/png" },
      { url: "/icon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/icon-64.png", sizes: "64x64", type: "image/png" },
      { url: "/icon-128.png", sizes: "128x128", type: "image/png" },
      { url: "/icon-256.png", sizes: "256x256", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/icon-256.png", sizes: "256x256", type: "image/png" }],
  },
  openGraph: {
    title: "Mula: The Root",
    description:
      "A modern spiritual companion app combining Vedic astrology, Vodou oracle, and AI guidance",
    images: ["/icon-512.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${cinzel.variable}`}>
      <head>
        {/* Favicon and App Icons */}
        <link rel="icon" type="image/png" sizes="16x16" href="/icon-16.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/icon-32.png" />
        <link rel="icon" type="image/png" sizes="64x64" href="/icon-64.png" />
        <link rel="apple-touch-icon" sizes="256x256" href="/icon-256.png" />
      </head>
      <body className={`${inter.className} antialiased`}>
        {/* Inline script to set initial theme before React hydrates to avoid FOIT/flash */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(${String(function () {
              try {
                const saved = localStorage.getItem("theme");
                const systemPref =
                  window.matchMedia &&
                  window.matchMedia("(prefers-color-scheme: dark)").matches
                    ? "dark"
                    : "light";
                const theme = saved || systemPref;
                document.documentElement.setAttribute("data-theme", theme);
              } catch (_e) {
                /* ignore */
              }
            })})();`,
          }}
        />

        <div
          style={{
            position: "fixed",
            top: "20px",
            right: "20px",
            zIndex: 1000,
          }}
        >
          <ThemeToggle />
        </div>
        {children}
      </body>
    </html>
  );
}
