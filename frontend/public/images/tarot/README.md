# Tarot Card Assets

This directory contains tarot card designs and templates for the Roots Revealed application.

## Provided Design

**Fortune's Path Card** - Reference design showing:

- Ornate copper/bronze decorative border with Celtic knot patterns
- Dark gradient background (brown to warm beige)
- Central zodiac wheel with glowing symbols
- Mystical eye symbol at bottom
- Elegant title text "FORTUNE'S PATH"
- Rounded rectangle card shape (mobile/portrait orientation)
- Cosmic dust particle effects

## Card Structure

```
┌─────────────────────┐
│  ╔═══════════════╗  │ ← Ornate border (copper)
│  ║   [Top Icon]  ║  │ ← Celestial symbol
│  ║               ║  │
│  ║  [Main Art]   ║  │ ← Card-specific artwork
│  ║               ║  │
│  ║   [Title]     ║  │ ← Card name
│  ║               ║  │
│  ║  [Symbol]     ║  │ ← Bottom icon
│  ╚═══════════════╝  │
└─────────────────────┘
```

## Assets Needed

### Card Templates

1. `card-template-portrait.svg` - Vertical orientation (mobile)
2. `card-template-landscape.svg` - Horizontal orientation (tablet/desktop)
3. `border-ornate.svg` - Reusable decorative border element

### Major Arcana Cards (Priority)

Create 22 major arcana tarot cards with mystical astrology theme:

- 0 The Fool
- 1 The Magician
- 2 The High Priestess
- 3 The Empress
- 4 The Emperor
- 5 The Hierophant
- 6 The Lovers
- 7 The Chariot
- 8 Strength
- 9 The Hermit
- 10 Wheel of Fortune
- 11 Justice
- 12 The Hanged Man
- 13 Death
- 14 Temperance
- 15 The Devil
- 16 The Tower
- 17 The Star
- 18 The Moon
- 19 The Sun
- 20 Judgement
- 21 The World

### Special Cards

- `fortune-path.png` - The reference card (already designed)
- `card-back.png` - Universal card back design
- `card-placeholder.png` - Loading state

## Design Specifications

### Dimensions

- **Portrait**: 400x700px (mobile cards)
- **Landscape**: 700x400px (desktop spreads)
- **Border Width**: 40px ornate frame
- **Corner Radius**: 20px

### Color Palette

- Background gradient: `#3D2E29` → `#6B5645`
- Border: Metallic copper `#D4A574`, `#C19A6B`, `#B8956A`
- Accent glow: `#E86F4D` (orange), `#FFD700` (gold)
- Text: `#FFF8DC` (cream white)

### Typography

- Title: 'Cinzel' or 'Trajan Pro' serif, 28-32px
- Subtitle: Same family, 18-20px
- Letter spacing: 4-6px for mystical elegance

### Effects

- **Border**: SVG ornate patterns with Celtic knots
- **Glow**: Soft radial gradient behind symbols
- **Particles**: Subtle star/dust overlay
- **Shadows**: Inner shadow for depth `0 4px 20px rgba(0,0,0,0.6)`

## Usage

Tarot cards are used in:

- Daily reading feature
- Fortune telling interactive experience
- Card spread visualizations (3-card, Celtic Cross, etc.)
- User collection/deck management
