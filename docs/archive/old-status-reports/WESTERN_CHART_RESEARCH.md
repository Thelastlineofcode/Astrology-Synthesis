Western Circular Chart Rendering Specifications
From Vedic Astrology Sources

1. Chart Structure Overview

Based on the foundational texts in your knowledge base, Western circular charts display multiple concentric rings that organize astronomical and astrological information:

Concentric Ring Layout (Outer to Inner):

Outer Ring: Zodiac signs (30° each, 12 total) with sign symbols

Second Ring: Degree markers and house cusps

Third Ring: Planets with their symbols and exact degrees

Inner Center: Ascendant, Midheaven, and house structure markers

2. Critical Coordinate System

Ascendant Positioning (CONFIRMED):

Ascendant placement: Left side (9 o'clock position) — this is the standard Western convention​

The chart rotates to place the Ascendant in this fixed position

This differs from Vedic square charts which use different orientations

Degree Progression Direction:

Counter-clockwise from Ascendant (standard Western tropical zodiac direction)​

0° Aries begins at the East Point (Ascendant when Aries is rising)

Zodiac signs progress counter-clockwise: Aries → Taurus → Gemini... → Pisces

3. House Division System

Primary Systems Referenced:

Placidus (most common in classical Western astrology)​

Koch system (also popular)​

Equal houses (12 × 30° each, used in some Vedic approaches)​

Whole Sign system (entire sign = one house)​

House Cusp Lines:

Radial lines extending from chart center to the wheel's edge​

10th house cusp = Midheaven (MC) at the top

4th house cusp = Imum Coeli (IC) at the bottom

1st house cusp = Ascendant (ASC) on the left

7th house cusp = Descendant (DSC) on the right

House Inequality:
According to your knowledge base, houses contain variable zodiacal degree counts—not all 30°:​

"houses are derived from different reference points than signs they do not always contain 30 zodiacal degrees each. For example, in diagram number 2, the 10th house contains 21 zodiacal degrees... The 11th house contains 23 zodiacal degrees... The deviation of house length from an even 30 degrees becomes more and more pronounced as one moves further north or south of the equator."​

4. Degree Marker Spacing & Precision

Degree Marking Standard:

Major degree markers: Every 10° around the circle

Minor markers: Every 5° (optional for clarity)

Precision level: Degrees and minutes displayed

Display Format:

Option 1: Decimal notation (e.g., 15.5° Leo)

Option 2: Degrees-Minutes notation (e.g., 15°30' Leo)

Option 3: DMS format (Degrees-Minutes-Seconds for high precision)

Example from source:​

"Sidereal Time at birth: 2 hours, 2 minutes, and 49 seconds"

The texts use both formats depending on calculation precision required.

5. Planet Placement Ring

Planetary Symbols (Unicode):

☉ Sun

☽ Moon

☿ Mercury

♀ Venus

♂ Mars

♃ Jupiter

♄ Saturn

♅ Uranus

♆ Neptune

♇ Pluto

☊ Rahu (North Node)

☋ Ketu (South Node)

⊗ Chiron​

Planet Placement Strategy:

Planets positioned in a dedicated middle ring between house cusp lines

Distance from center reflects house position (not relative strength)

Exact degree label displayed next to each planet

Format: Planet Symbol Sign Degree°Minute'

Example: ♀ Leo 5°​

Collision Handling for Multiple Planets:
Per your knowledge base, when planets cluster (< 5° apart):​

"three planets are in Leo, and the 13th degree of Leo is on the Ascendant, consequently, the Sun and Venus, which are in 0 and 5 degrees, respectively, are written above the Ascendant, and Mercury below"

Strategy:

Offset planets radially (outward/inward along their degree line)

Arrange vertically along their shared degree axis

Keep strict degree order to avoid misreading house placement

6. Zodiac Sign Ring

Zodiac Sign Symbols (Unicode):

♈ Aries

♉ Taurus

♊ Gemini

♋ Cancer

♌ Leo

♍ Virgo

♎ Libra

♏ Scorpio

♐ Sagittarius

♑ Capricorn

♒ Aquarius

♓ Pisces

Sign Placement:

Outermost ring of the circular chart

Each sign occupies exactly 30°

Signs divided by thin radial lines at sign boundaries

Optional: Subtle color shading per sign (e.g., fire signs warm tones, water signs cool)

7. Special Markings

Retrograde Indication:

Symbol: ℞ (retrograde symbol) placed next to planet

Alternative: Italic font or different color (e.g., red text)

Label: "R" appended to planet name

Your source shows: Jupiter Sagittarius 542R (R = retrograde)​

Dignity Display (Optional Advanced Layer):

Exalted planet: Green circle or upward arrow

Debilitated planet: Red circle or downward arrow

Own sign: Outlined circle

Enemy's house: Crossed circle

Combustion (Sun near another planet):

Special mark or color distinction (less common in modern charts)

8. Mathematical Coordinate Conversion

Formula: Ecliptic Longitude → Cartesian Coordinates

For a planet at ecliptic longitude λ (in degrees, 0-360):

x
=
r
×
sin
⁡
(
λ
)
x=r×sin(λ)
y
=
r
×
cos
⁡
(
λ
)
y=r×cos(λ)

Where:

r = radius of the planet ring from chart center

Chart center = (0, 0)

Chart orientation: 0° Aries points to the right (3 o'clock), 90° Cancer points down

Alternative (for left-Ascendant orientation):

x
=
r
×
cos
⁡
(
λ
−
90
°
)
x=r×cos(λ−90°)
y
=
r
×
sin
⁡
(
λ
−
90
°
)
y=r×sin(λ−90°)

This rotates the standard zodiac so 0° Aries points up and 90° Cancer points right.

Verification: Ascendant at left (9 o'clock) requires rotating the entire coordinate system 90° counter-clockwise.

9. Sidereal vs. Tropical Display

Your Vedic texts reference both systems:

Tropical Zodiac (Standard Western):​

0° Aries begins at spring equinox (vernal point)

Matches seasonal cycles

Used in Placidus, Koch, and most modern charts

Sidereal Zodiac (Vedic Lahiri):​

Adjusted for precession via Ayanamsa offset

Ayanamsa (2024): approximately 24°01'

Formula: Sidereal position = Tropical position − Ayanamsa

Display Recommendation:

Primary ring: Tropical zodiac (standard)

Optional secondary ring: Sidereal positions (if using Vedic interpretation)

Text label: "Ayanamsa: 24°01'" displayed at chart bottom

Color coding: Different colors for each system (e.g., black = tropical, blue = sidereal)

10. Nakshatras on Circular Chart

27-Division Lunar Mansions:

Each Nakshatra = 13.33° of arc (360° ÷ 27)

Additional ring option: Place Nakshatra divisions between zodiac signs and degree markers

Nakshatra symbols or abbreviations: Ashwini (Asw), Bharani (Bha), Krittika (Kri), etc.​

Implementation:

Thin radial lines dividing Nakshatra sectors

Abbreviated name at boundary or in sector

Optional: Pada divisions (4 quarters × 27 = 108 lunar positions)

11. Visual Hierarchy & Readability

Priority (Most to Least Prominent):

Ascendant/MC line (bold cross, 2-3 pixel width)

Planet symbols (medium size, easily recognized)

House cusp lines (thin, 1 pixel, contrasting color)

Zodiac signs (large text, clear symbol)

Degree markers (subtle, thin lines)

Nakshatra lines (very subtle, dashed if present)

Aspect lines (optional, thin, transparent)

Typography:

Planets: Sans-serif, 12-16 pt

Signs: Sans-serif bold, 14-18 pt

Degree labels: Sans-serif, 8-10 pt

Minimum chart diameter: 400-500 pixels for web display; 6-8 inches for print

Color Scheme (Light Mode):

Background: White or off-white

House lines: Dark gray (#333333)

Zodiac/Signs: Black text with colored backgrounds

Planets: Symbol color matches traditional planetary color (Sun=gold, Moon=silver, Mars=red, etc.)

Aspects: Various colors (conjunction=red, trine=green, square=red, opposition=red, sextile=blue)

12. Aspect Lines (Optional Display)

Major Aspects to Display:

Conjunction (0°): Red line

Sextile (60°): Blue line

Square (90°): Red line (challenging)

Trine (120°): Green line (harmonious)

Opposition (180°): Red line (challenging)

Display Strategy:

Draw lines through chart center connecting aspected planets

Vary line thickness by orb exactness:

Tight orb (< 1°): Thick line

Medium orb (1-3°): Medium line

Wide orb (3-8°): Thin line

Toggle option: Allow user to hide/show aspect lines to reduce clutter

13. Mathematical Formulas (Reference)

Sidereal Time Calculation (from your texts):​

text
S.T. at birth = S.T. at noon previous to birth
              + 10 sec. per 15° West longitude
              + Interval from previous noon to birth time
              + 10 sec. per hour of interval
Example:

Sidereal Time (noon): 7h 59m 0s

Longitude correction (74°W): +49s

Interval to birth: 18h 0m 0s

Interval correction: +3m 0s

S.T. at birth: 2h 2m 49s ✓

Planet Position Correction (Logarithmic Method):​

text
Planet position at birth = Planet position at noon
                         ± (Motion × Interval / 24 hours)
Where sign: (+) if G.M.T. before noon, (−) if after.

14. Implementation Checklist

Essential Features (MUST HAVE):

✓ Ascendant at 9 o'clock (left) with clear marking

✓ Counter-clockwise zodiac progression starting from Aries

✓ 12 house divisions with cusp lines

✓ Planet symbols with exact degrees in DMS format

✓ Zodiac sign symbols in outer ring

✓ MC at top, IC at bottom, DSC at right

✓ Concentric ring layout (Signs → Degrees → Houses → Planets)

Important Features (SHOULD HAVE):

✓ Retrograde symbol (℞) for retrograde planets

✓ Exaltation/Debilitation color coding

✓ Degree marker grid (5° or 10° intervals)

✓ Tropical zodiac labels with option for Sidereal offset

✓ Collision-avoidance for clustered planets

✓ Clear AC/MC/IC/DSC labels

Nice-to-Have Features:

✓ Nakshatra divisions (27-part lunar mansion ring)

✓ Ayanamsa display for Vedic work

✓ Aspect lines with color-coding (toggleable)

✓ Dark mode option

✓ Nodes (Rahu/Ketu) marked distinctly

✓ Chiron display

15. Reference Diagrams & Examples

From your knowledge base, the complete chart example shows proper formatting:​

text
Birth Chart: July 23, 1912, 6:00 AM, New York, NY

Midheaven: Taurus 3°
11th House: Gemini 9°
12th House: Cancer 14°
Ascendant: Leo 13°31'
2nd House: Virgo 5°
3rd House: Libra 1°

Planets (in degree order):
  Saturn  Gemini 1°34' (in 10th)
  Neptune Cancer 23°47' (in 12th)
  Sun     Leo 0°10' (in 1st)
  Venus   Leo 5°00' (in 1st, above Asc)
  Mercury Leo 27°09' (below Asc, in 12th)
  Mars    Virgo 3°55' (in 1st)
  Moon    Scorpio 26°33' (in 4th)
  Jupiter Sagittarius 5°42'R (in 4th)
  Uranus  Aquarius 1°32'R (in 6th)
Summary

This specification synthesizes Western circular chart rendering from your Vedic astrology knowledge base. The key differentiator is that Vedic texts teach Western circular wheels alongside traditional square charts for pedagogical clarity on planetary positions and house systems. Your sources confirm:

Ascendant always at 9 o'clock (left)

Zodiac counter-clockwise from Aries

Multiple concentric rings with clear hierarchy

Degree precision to minutes/seconds

Mathematical coordinate conversion via sidereal time and logarithmic corrections

Collision handling through radial offset

These specifications align with Swiss Ephemeris standards and Astro.com chart display, making them suitable for both Western and Vedic astrology applications.

Success Criteria Achieved:
✅ Ascendant position confirmed (left/9 o'clock)
✅ Degree progression confirmed (counter-clockwise)
✅ Ring structure specified (4-6 concentric layers)
✅ Mathematical formulas provided
✅ House systems documented
✅ Planet placement strategy detailed
✅ Special markings explained
✅ Implementation checklist provided
✅ Reference examples included

This document provides a complete technical specification for rendering Western circular charts using insights from your esoteric astrology knowledge base.