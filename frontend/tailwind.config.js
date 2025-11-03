/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Core Brand Colors
        primary: {
          DEFAULT: "#1e293b", // deep slate background
          dark: "#0f172a", // darkest layer
          light: "#334155", // lighter slate variant
        },
        accent: {
          DEFAULT: "#06b6d4", // electric cyan
          light: "#3b82f6", // electric blue variant
        },

        // Semantic States
        success: "#10b981", // emerald green (harmony aspects)
        warning: "#f59e0b", // amber (sun color, warnings)
        error: "#dc2626", // deep crimson (Mars)
        info: "#3b82f6", // blue (Mercury)

        // Text Colors
        text: {
          DEFAULT: "#f8fafc", // near-white text
          muted: "#94a3b8", // silver-blue (moon) secondary text
          subtle: "#64748b", // slate for tertiary text
          dark: "#1e293b", // for light backgrounds
        },

        // Background Layers
        background: {
          DEFAULT: "#0f172a", // darkest layer
          surface: "#1e293b", // slightly lighter surface
          card: "#1e293b", // card backgrounds
          overlay: "rgba(15, 23, 42, 0.8)", // overlay background
        },

        // Chart-Specific Planet Colors (Synthesis Palette)
        chartSun: "#f59e0b", // ☉ Sun: warm amber
        chartMoon: "#94a3b8", // ☽ Moon: cool silver-blue
        chartMercury: "#06b6d4", // ☿ Mercury: electric cyan
        chartVenus: "#ec4899", // ♀ Venus: rose copper
        chartMars: "#dc2626", // ♂ Mars: deep crimson
        chartJupiter: "#6366f1", // ♃ Jupiter: royal indigo
        chartSaturn: "#475569", // ♄ Saturn: graphite slate
        chartUranus: "#14b8a6", // ♅ Uranus: bright teal
        chartNeptune: "#8b5cf6", // ♆ Neptune: misty violet
        chartPluto: "#9f1239", // ♇ Pluto: deep burgundy

        // Aspect Colors
        aspectTrine: "#10b981", // harmonious aspects (emerald)
        aspectSquare: "#f59e0b", // tense aspects (amber)
        aspectConjunct: "#64748b", // neutral conjunction (slate)

        // House Fill Colors
        houseLight: "#0f172a", // alternating house fills
        houseDark: "#1e293b",

        // Extended Gray Scale (for flexibility)
        gray: {
          50: "#f9fafb",
          100: "#f3f4f6",
          200: "#e5e7eb",
          300: "#d1d5db",
          400: "#9ca3af",
          500: "#6b7280",
          600: "#4b5563",
          700: "#374151",
          800: "#1f2937",
          900: "#111827",
          950: "#0f1419",
        },
      },

      fontFamily: {
        display: ["var(--font-rubik)", "sans-serif"], // geometric modern display
        body: ["var(--font-inter)", "sans-serif"], // highly legible body text
        mono: ["var(--font-source-code-pro)", "monospace"], // technical data font
      },

      fontSize: {
        xs: ["0.75rem", { lineHeight: "1rem" }], // 12px
        sm: ["0.875rem", { lineHeight: "1.25rem" }], // 14px
        base: ["1rem", { lineHeight: "1.5rem" }], // 16px (base)
        lg: ["1.125rem", { lineHeight: "1.75rem" }], // 18px
        xl: ["1.25rem", { lineHeight: "1.75rem" }], // 20px
        "2xl": ["1.5rem", { lineHeight: "2rem" }], // 24px
        "3xl": ["2rem", { lineHeight: "2.5rem" }], // 32px
        "4xl": ["2.5rem", { lineHeight: "3rem" }], // 40px
        "5xl": ["3rem", { lineHeight: "3.5rem" }], // 48px (hero)
        "6xl": ["3.75rem", { lineHeight: "4.5rem" }], // 60px
      },

      spacing: {
        px: "1px",
        0: "0px",
        1: "0.25rem", // 4px
        2: "0.5rem", // 8px
        3: "0.75rem", // 12px
        4: "1rem", // 16px
        5: "1.25rem", // 20px
        6: "1.5rem", // 24px
        7: "1.75rem", // 28px
        8: "2rem", // 32px
        10: "2.5rem", // 40px
        12: "3rem", // 48px
        14: "3.5rem", // 56px
        16: "4rem", // 64px
        20: "5rem", // 80px
        24: "6rem", // 96px
        28: "7rem", // 112px
        32: "8rem", // 128px
        36: "9rem", // 144px
        40: "10rem", // 160px
        44: "11rem", // 176px
        48: "12rem", // 192px
        52: "13rem", // 208px
        56: "14rem", // 224px
        60: "15rem", // 240px
        64: "16rem", // 256px
        72: "18rem", // 288px
        80: "20rem", // 320px
        96: "24rem", // 384px
      },

      borderRadius: {
        none: "0",
        sm: "0.125rem", // 2px
        DEFAULT: "0.25rem", // 4px
        md: "0.375rem", // 6px
        lg: "0.5rem", // 8px
        xl: "0.75rem", // 12px
        "2xl": "1rem", // 16px
        "3xl": "1.5rem", // 24px
        full: "9999px",
      },

      boxShadow: {
        none: "none",
        sm: "0 1px 2px rgba(0, 0, 0, 0.05)",
        DEFAULT: "0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)",
        md: "0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)",
        lg: "0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05)",
        xl: "0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04)",
        "2xl": "0 25px 50px rgba(0, 0, 0, 0.25)",
        inner: "inset 0 2px 4px rgba(0, 0, 0, 0.06)",

        // Glow effects for chart interactions
        "glow-cyan": "0 0 20px rgba(6, 182, 212, 0.3)",
        "glow-accent": "0 0 15px rgba(59, 130, 246, 0.2)",
        "glow-chart": "0 0 10px rgba(6, 182, 212, 0.2)",
      },

      screens: {
        sm: "640px", // mobile
        md: "768px", // tablet
        lg: "1024px", // small desktop
        xl: "1280px", // large desktop
        "2xl": "1536px", // extra large desktop
      },

      transitionTimingFunction: {
        smooth: "cubic-bezier(0.4, 0, 0.2, 1)",
        spring: "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
        "ease-out": "cubic-bezier(0.4, 0, 0.2, 1)",
        "ease-in": "cubic-bezier(0.4, 0, 1, 1)",
      },

      animation: {
        // Page transitions
        "fade-in": "fadeIn 300ms ease-out forwards",
        "slide-up": "slideUp 300ms ease-out forwards",

        // Skeleton shimmer
        shimmer: "shimmer 1500ms infinite",

        // Data viz animations
        "count-up": "countUp 400ms ease-out forwards",
        "fill-progress": "fillProgress 300ms ease-in-out forwards",

        // Subtle interactions
        "pulse-soft": "pulseSoft 2s ease-in-out infinite",
      },

      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-1200px 0" },
          "100%": { backgroundPosition: "1200px 0" },
        },
        countUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        fillProgress: {
          "0%": { width: "0%" },
          "100%": { width: "100%" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.8" },
        },
      },
    },
  },
  plugins: [],
};
