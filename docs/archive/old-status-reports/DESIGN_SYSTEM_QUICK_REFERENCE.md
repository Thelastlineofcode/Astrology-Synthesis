# Mula Design System - Quick Reference Guide

## 🎨 Color Palette at a Glance

### Primary Colors

```
Dark Background:    #0f172a ◼️
Surface:            #1e293b ◼️
Light Variant:      #334155 ◼️
```

### Accent Colors

```
Electric Cyan:      #06b6d4 ◼️
Electric Blue:      #3b82f6 ◼️
```

### Semantic Colors

```
Success (Emerald):  #10b981 ◼️
Warning (Amber):    #f59e0b ◼️
Error (Crimson):    #dc2626 ◼️
Info (Blue):        #3b82f6 ◼️
```

### Text Colors

```
Primary Text:       #f8fafc ◼️
Muted Text:         #94a3b8 ◼️
Subtle Text:        #64748b ◼️
Dark Mode Text:     #1e293b ◼️
```

### Planet Colors (Modern Synthesis)

```
☉ Sun:     #f59e0b ◼️
☽ Moon:    #94a3b8 ◼️
☿ Mercury: #06b6d4 ◼️
♀ Venus:   #ec4899 ◼️
♂ Mars:    #dc2626 ◼️
♃ Jupiter: #6366f1 ◼️
♄ Saturn:  #475569 ◼️
♅ Uranus:  #14b8a6 ◼️
♆ Neptune: #8b5cf6 ◼️
♇ Pluto:   #9f1239 ◼️
```

### Aspect Colors

```
Trine (Harmony):    #10b981 ◼️
Square (Tension):   #f59e0b ◼️
Conjunction (Neutral): #64748b ◼️
```

---

## 🔤 Typography

### Font Families

- **Display:** Rubik (geometric, modern, bold)
- **Body:** Inter (highly readable, professional)
- **Mono:** Source Code Pro (crisp, technical)

### Font Sizes

```
xs:   12px  (metadata)
sm:   14px
base: 16px  (standard body)
lg:   18px
xl:   20px
2xl:  24px
3xl:  32px
4xl:  40px
5xl:  48px  (hero headings)
```

### Line Heights

```
tight:  1.2  (headings)
normal: 1.5  (body)
loose:  1.75 (expanded text)
```

---

## 📏 Spacing Scale (4px base)

```
1   = 4px
2   = 8px
3   = 12px
4   = 16px   (standard)
5   = 20px
6   = 24px   (standard)
8   = 32px
10  = 40px
12  = 48px
16  = 64px
20  = 80px
24  = 96px
```

---

## 🔘 Border Radius

```
sm:   2px   (subtle)
md:   6px
lg:   8px   (default)
xl:   12px
2xl:  16px  (large)
full: 9999px (pill shape)
```

---

## 💫 Shadows & Elevation

```
sm:  0 1px 2px rgba(0,0,0,0.05)
md:  0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)
lg:  0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)
xl:  0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)
2xl: 0 25px 50px rgba(0,0,0,0.25)
```

### Glow Effects

```
Cyan Glow:   0 0 20px rgba(6, 182, 212, 0.3)
Accent Glow: 0 0 15px rgba(59, 130, 246, 0.2)
Chart Glow:  0 0 10px rgba(6, 182, 212, 0.2)
```

---

## ⏱️ Timing & Easing

```
Fast:     100ms  cubic-bezier(0.4, 0, 0.2, 1)
Base:     150ms  cubic-bezier(0.4, 0, 0.2, 1)
Slow:     300ms  cubic-bezier(0.4, 0, 0.2, 1)
Spring:   400ms  cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

---

## 📱 Responsive Breakpoints

```
sm:  640px   (mobile)
md:  768px   (tablet)
lg:  1024px  (small desktop)
xl:  1280px  (large desktop)
2xl: 1536px  (extra large)
```

---

## 🎬 Core Animations

### Page Transitions

```
Fade In:   300ms fade (0 to 100% opacity)
Slide Up:  300ms slide (10px → 0px) + fade
```

### Chart Wheel

```
Planets:   600ms fade-in, 100ms stagger per planet
Aspects:   800ms draw animation, starts after planets
Hover:     150ms scale 1.05× + cyan glow
```

### Loading States

```
Shimmer:   1500ms infinite wave
Skeleton:  Subtle animation with stagger
```

### Button Interactions

```
Press:     100ms scale 0.98×
Toggle:    150-200ms smooth slide
Checkbox:  100-150ms checkmark draw
```

### Data Visualization

```
Count-up:  400ms number animation
Progress:  300ms fill bar
Reorder:   300ms position shift
```

---

## 🎯 CSS Custom Properties Cheat Sheet

### Colors

```css
--color-primary: #1e293b --color-primary-dark: #0f172a --color-accent: #06b6d4
  --color-success: #10b981 --color-warning: #f59e0b --color-error: #dc2626
  --color-text: #f8fafc --color-text-muted: #94a3b8 --color-bg: #0f172a
  --color-bg-surface: #1e293b;
```

### Typography

```css
--font-rubik:
  "Rubik", sans-serif --font-inter: "Inter",
  sans-serif --font-source-code-pro: "Source Code Pro",
  monospace --font-size-base: 1rem --font-size-lg: 1.125rem;
```

### Spacing

```css
--spacing-4: 1rem (16px) --spacing-6: 1.5rem (24px) --spacing-8: 2rem (32px);
```

### Effects

```css
--shadow-md:
  0 4px 6px rgba(0, 0, 0, 0.1),
  ... --glow-cyan: 0 0 20px rgba(6, 182, 212, 0.3) --transition-slow: 300ms
    cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 🚀 Quick CSS Examples

### Button with Design Tokens

```css
.button {
  background-color: var(--color-accent);
  color: var(--color-text);
  font-family: var(--font-inter);
  padding: var(--spacing-4) var(--spacing-6);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background-color: var(--color-accent-light);
}

.button:active {
  transform: scale(0.98);
}
```

### Card Component

```css
.card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(6, 182, 212, 0.1);
  transition: all var(--transition-slow);
}

.card:hover {
  transform: translateY(-4px);
  border-color: rgba(6, 182, 212, 0.3);
  box-shadow: var(--glow-cyan);
}
```

### Heading

```css
h1 {
  font-family: var(--font-rubik);
  font-size: var(--font-size-5xl);
  font-weight: 700;
  color: var(--color-text);
  line-height: 1.1;
}
```

### Loading Skeleton

```css
.skeleton {
  background-color: var(--color-bg-surface);
  border-radius: var(--radius-lg);
  animation: shimmer 1500ms infinite;
}
```

---

## ✅ Implementation Checklist

- [x] Colors defined (40+ values)
- [x] Typography set up (3 fonts, 13 sizes)
- [x] Spacing scale created (26 values)
- [x] Border radius tokens
- [x] Shadow/glow system
- [x] Animations (15+ keyframes)
- [x] Breakpoints (5 tiers)
- [x] CSS custom properties
- [x] Google Fonts imported
- [x] Accessibility (prefers-reduced-motion)
- [ ] Dashboard updated with tokens
- [ ] Chart tool styled with tokens
- [ ] Responsive testing complete
- [ ] Component library created

---

## 📖 File Locations

- **Configuration:** `/frontend/tailwind.config.js`
- **Global Styles:** `/frontend/src/app/globals.css`
- **Animations:** `/frontend/src/app/animations.css`
- **Landing CSS:** `/frontend/src/app/landing.css`
- **Dashboard CSS:** `/frontend/src/app/dashboard/dashboard.css`
- **Documentation:** `/DESIGN_SYSTEM_IMPLEMENTATION.md`

---

## 🎨 Design Philosophy

**"Mula: The Root"** - Synthesis of traditional wisdom with modern intelligence

- **Not** mystical, cosmic, or ornate
- **Not** consumer-focused astrology app
- **Yes** professional SaaS aesthetic (Linear, Notion, Arc)
- **Yes** clean geometric minimalism
- **Yes** data-focused, information-rich
- **Yes** modern planet color palette
- **Yes** smooth, purposeful animations

---

## 🚀 Status

✅ **Design system is production-ready!**

Your app now has:

- Professional dark mode color palette
- Geometric, modern typography hierarchy
- Smooth, accessible animations
- Mobile-first responsive design
- Complete CSS token system
- Real brand assets (logos)

**Next:** Apply tokens to dashboard and chart tool, then test responsive design. 🎯
