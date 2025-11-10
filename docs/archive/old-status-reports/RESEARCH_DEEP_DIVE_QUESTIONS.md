# Deep Research Framework: Koch Houses & Horoscope Generation

## SECTION A: KOCH HOUSE SYSTEM DEEP DIVE

### Question Set 1: Koch Mathematical Foundation

1. **Koch vs. Placidus Calculation**
   - What is the Placidus method's limitation that Koch addresses?
   - In what latitude ranges does Koch differ from Placidus by >5 minutes of arc?
   - How does Koch handle houses 7-12 (the "lower hemisphere")?
   - Why is interpolation required in Koch but not in Equal House systems?

2. **Semiarc Formula**
   - Define Semiarc and how it differs from declination.
   - Derive: If MC is at 127° and ASC at 45°, what is the semiarc?
   - How does semiarc vary with latitude?
   - Calculate by hand: House 5 cusp for someone born at 40°N, MC=127°, ASC=45°

3. **Polar Region Handling**
   - What happens at the North Pole (90° latitude)?
   - Why do houses 1-6 collapse above the Arctic Circle (66°34'N)?
   - How do professional software (Astro.com, Jyotish Bhaav) handle this?
   - Test case: Calculate chart for Reykjavik (64.15°N) and compare with Astro.com

4. **Latitude Influence**
   - How does ecliptic latitude of planets affect Koch house positions?
   - Example: If a planet is at 45° ecliptic longitude but 5° ecliptic latitude, does its house change?
   - What is the maximum latitude effect on house cusp (degrees of arc)?

5. **Mathematical Precision**
   - What precision (decimal places) is needed for:
     - House cusps (±0.1° professional standard = ±6 arcseconds)
     - Planet positions (±1 arcminute = ±0.016° precision)
   - Float32 vs. Float64: Which is required for astrology?
   - How does floating-point rounding affect final house calculations?

### Question Set 2: pyswisseph Koch Implementation

1. **Swiss Ephemeris Function Reference**
   - What is `swe.calc_houses()` syntax? Full parameters and return values.
   - What does each flag in `swe_housesys` represent?
   - How to extract: ASC, MC, AVX, VX from `swe.calc_houses()` output?
   - What is the difference between `swe.calc_houses()` and `swe.cusps()`?

2. **Practical Implementation**

   ```python
   # Sample problem: Given these inputs, what is output?
   import swisseph as swe

   jd = 2460000.0  # Julian day for Nov 3, 2025
   lat = 30.27     # Birth latitude (New Orleans area)
   lon = -90.18    # Birth longitude (New Orleans area)

   # How to call Koch?
   # cusps, asmc = swe.calc_houses(jd, lat, lon, ???)

   # What is ??? (house system flag)?
   # What do cusps[0] through cusps[11] represent?
   # What are asmc[0] and asmc[1]?
   ```

3. **Accuracy Verification**
   - Generate chart for: 1980-07-13, 10:30:00, New York
   - Compare output with:
     - Astro.com (under "Calculation")
     - Jyotish Bhaav software
     - Swiss Ephemeris reference
   - Tolerance: How close must they be? Document discrepancies.

4. **Edge Case Handling**
   - Test chart for North Pole birth (90°N)
   - Test chart for equatorial birth (0°00')
   - Test chart for Tropic of Capricorn (23°26'S)
   - For each: Document any warnings/errors in pyswisseph

5. **Performance Profiling**
   - Benchmark: Time to calculate 1,000 charts using Koch
   - Benchmark: Time to calculate 1,000 charts using Placidus
   - Memory usage for single chart calculation
   - Is caching ephemeris data beneficial?

### Question Set 3: House Interpretation & Integration

1. **House Meanings in Context**
   - For each house (1-12), provide:
     - **Traditional meaning** (what that house represents)
     - **Vedic interpretation** (how Vedic astrology views it)
     - **Modern interpretation** (psychological/practical)
     - **Interrogation**: "What about this area of life?"
   - Example format:
     ```
     House 7 (Partnerships):
     - Traditional: Spouse, partner, contracts, enemies, open conflicts
     - Vedic: Kalatra (spouse), saptama bhava, 7th lord
     - Modern: Close relationships, shadow projection, other people's perspective
     - Interrogation: "Who is the significant other? What is partnership quality?"
     ```

2. **House Rulership in Different Systems**
   - Vedic default: Aries=1st, Taurus=2nd, ... Pisces=12th
   - Western: Sun=5th, Moon=4th, Mercury=3rd & 6th, etc.
   - When does house system choice matter?
   - How to use ruling planets in interpretation?

3. **Multiple Planets in One House**
   - 3 planets in house 10 (career) - how to interpret?
   - Order of significance: Distance from cusp? Rulership? Aspect strength?
   - Example: Sun, Mars, Venus in 10th - who "rules" the house?

4. **Intercepted Houses & Duplicated Signs**
   - Define: Intercepted house (sign doesn't touch either cusp)
   - Define: Duplicated sign (appears on multiple house cusps)
   - Why does Koch have different intercepts than Placidus?
   - Interpretation: How does interception change house meaning?
   - Example: Scorpio on both 7th and 8th cusp = what impact?

5. **House Profections & Annual Charts**
   - If someone is 35 years old, which house is profected?
   - Formula for house profection: (Age mod 12) = ?
   - What significance does this have for annual predictions?
   - How to integrate with Koch houses?

### Question Set 4: Database Schema & Persistence

1. **Table Design**

   ```sql
   -- Design table to store Koch houses
   CREATE TABLE koch_houses (
     id UUID PRIMARY KEY,
     chart_id UUID FOREIGN KEY,
     house_1_cusp FLOAT64,  -- Why FLOAT64 not FLOAT32?
     house_2_cusp FLOAT64,
     ...
     house_12_cusp FLOAT64,
     ascendant FLOAT64,     -- House 1 cusp again? Or separate?
     midheaven FLOAT64,
     anti_vertex FLOAT64,
     vertex FLOAT64,
     house_system VARCHAR(20),  -- "KOCH", "PLACIDUS", etc
     intercepted_houses JSON,   -- How to store?
     calculated_at TIMESTAMP,
   );

   -- Questions:
   -- 1. Why store ASC separately if it's House 1 cusp?
   -- 2. What JSON structure for intercepted_houses?
   -- 3. Need version tracking in case calculation method changes?
   -- 4. Indexes needed: What queries will hit this table?
   ```

2. **Query Patterns**
   - "Get all charts in house system X" - index needed?
   - "Get all charts where Jupiter in 7th" - how to query?
   - "Find intercepts in houses 2-3" - query structure?
   - Worst case: 1M birth charts, 100k customers. Performance?

3. **Data Validation**
   - House cusps must be 0-360°? Or allow wrapping?
   - Cusps must be in ascending order (cusp1 < cusp2 < ... < cusp12)?
   - What validation rules prevent corrupted data?

4. **Backward Compatibility**
   - If switching from Placidus to Koch, what breaks?
   - How to migrate existing birth charts?
   - How to handle charts calculated in both systems?

---

## SECTION B: HOROSCOPE GENERATION RESEARCH

### Question Set 5: Aspect Interpretation Database

Create a comprehensive interpretation dictionary:

```python
ASPECT_MEANINGS = {
    "conjunction": {
        "aspect_angle": 0,
        "orb": 8,
        "nature": "conjunctive_blending",
        "keywords": ["fusion", "new beginning", "potential", "power"],
        "meaning": "Energies merge completely. New cycle begins."
    },
    "sextile": {
        "aspect_angle": 60,
        "orb": 6,
        "nature": "harmonic",
        "keywords": ["opportunity", "flow", "skill", "grace"],
        "meaning": "Harmonious. Talents available with slight effort."
    },
    # ... continue for all 5 major aspects
}

PLANET_TRANSIT_MEANINGS = {
    "Sun": {
        "1st_house": "Identity, new beginnings, self-assertion",
        "7th_house": "Partnership, relationships, significant others",
        # ... 12 houses
    },
    "Mars": {
        # Similar structure
    },
    # ... all planets
}

HOUSE_ACTIVATION_MEANINGS = {
    1: "Personal identity, appearance, how others see you",
    7: "Partnerships, marriage, open enemies, contracts",
    10: "Career, public image, reputation, goals",
    # ... 12 houses
}
```

**Research questions:**

1. What are the "correct" interpretations for each aspect? (Source: professional astrology texts)
2. How to rank aspects: Is conjunction always stronger than trine?
3. Do orbs depend on planet pairs or just planet type?
4. How does retrograde status change interpretation?

### Question Set 6: Multi-Factor Confidence Scoring

Design a scoring system:

```python
def score_event(event):
    """
    Score a transit event by multiple factors
    Returns: confidence 0.0 to 1.0
    """

    factors = {
        "aspect_strength": 0.0,     # 0-1 based on orb tightness
        "dasha_support": 0.0,       # 0-1 if dasha lord supports
        "progressed_alignment": 0.0,# 0-1 if progression reinforces
        "natal_emphasis": 0.0,      # 0-1 if already strong in birth chart
        "seasonal_timing": 0.0,     # 0-1 if season supports
        "house_relevance": 0.0,     # 0-1 if house significant to query
    }

    weights = {
        "aspect_strength": 0.25,
        "dasha_support": 0.25,
        "progressed_alignment": 0.15,
        "natal_emphasis": 0.15,
        "seasonal_timing": 0.10,
        "house_relevance": 0.10,
    }

    # Calculate weighted score
    # How to combine Vedic (dasha) + Western (progressed) factors?
    # What's "correct" weighting?
```

**Research questions:**

1. Is 25% dasha + 25% aspect equal weighting philosophically sound?
2. How to score "house relevance" if user didn't specify query area?
3. How to handle tied scores (two equally strong events)?
4. Should confidence degrade over time (older transits = less relevant)?

### Question Set 7: Narrative Generation

Create templates for common scenarios:

```python
NARRATIVE_TEMPLATES = {
    "transit_conjunction_friendly": {
        "template": "With {planet} entering your {house_num} house, {meaning}. This period invites you to {action}. Key dates: {dates}",
        "conditions": ["aspect_strength > 0.7", "aspect_type == conjunction", "natal_planet_strength < 5"],
    },
    "transit_square_challenging": {
        "template": "A square from {planet} to your {natal_planet} may trigger {challenge}. Rather than resist, channel this energy into {positive}. This is a growth opportunity lasting {duration}.",
        "conditions": ["aspect_strength > 0.6", "aspect_type == square"],
    },
    # ... many more templates
}
```

**Research questions:**

1. How many templates needed for ~80% coverage? (Target: <100)
2. How to vary language to avoid repetition? (Parameter variation vs. template diversity?)
3. Should interpretation change if person is already "difficult" in that life area?
4. Example: Mars in 7th for someone with already tense relationships vs. peaceful relationships - same interpretation?

### Question Set 8: Event Grouping & Clustering

Algorithm research:

```python
def cluster_events(events_list):
    """
    Group related events into narrative clusters
    Input: List of 50+ events over 90 days
    Output: 5-8 thematic clusters

    Example output:
    [
        {
            "theme": "Relationship Focus",
            "events": [event1, event2, event5],
            "dates": "Nov 3-20",
            "narrative": "Venus enters..."
        },
        {
            "theme": "Career Advancement",
            "events": [event7, event12],
            "dates": "Nov 28 - Dec 15",
            "narrative": "Jupiter's influence..."
        }
    ]
    """
    pass
```

**Research questions:**

1. Clustering algorithm: K-means? Hierarchical? Affinity propagation?
2. How to determine optimal number of clusters?
3. How to define "related" events? (Shared planet? Shared house? Shared element?)
4. How to handle events that don't fit any cluster?

### Question Set 9: Temporal Ordering & Progression

Timeline construction:

```python
def build_timeline(horoscope_data):
    """
    Create chronological narrative arc

    Challenge: Balance
    1. Chronological order (event A happens before B)
    2. Thematic flow (grouping related topics)
    3. Reader engagement (not monotonous)

    Example bad: "Nov 3: Mars. Nov 4: Venus. Nov 5: Jupiter. Nov 6: Saturn."
    (Boring, no narrative flow)

    Example good: "Early November: Venus creates harmony in relationships (Nov 3).
    Mid-month builds momentum (Jupiter Nov 6). Late month brings challenges (Mars Nov 28)."
    """
    pass
```

**Research questions:**

1. How to weight recency vs. relevance? (Today's event vs. major event next week?)
2. When to use date ranges vs. exact dates?
3. How to forecast beyond 90 days without overcommitting?

### Question Set 10: Personalization Depth

Using birth chart in horoscope:

```python
def personalize_narrative(template: str, birth_chart: dict) -> str:
    """
    Customize generic narrative with birth chart details

    Generic: "This period brings relationship focus"
    Personalized (Venus in 7th): "Your natural gift for harmony is activated"
    Personalized (Mars in 7th): "Normally reserved in relationships, you'll feel bolder"
    Personalized (Capricorn 7th): "Your need for stability in partnerships is tested"
    """
    pass
```

**Research questions:**

1. What birth chart features are most predictive of response to transits?
   - Sign emphasis (Fire/Earth/Air/Water)?
   - Planet strength (aspect count, rulership)?
   - House emphasis?
2. How to avoid contradiction? "You like stability" then "time for adventure"?
3. Should horoscope change if person is in Mahadasha vs. Antardasha?

---

## SECTION C: INTEGRATION CHALLENGES

### Question Set 11: Vedic + Western Integration

1. **Philosophical Compatibility**
   - KP uses sidereal positions; Western astrology uses tropical
   - Vimshottari dasha is 120-year cycle; Western uses annual cycles
   - How to score event: KP says "major" but transit says "minor"?
   - Resolution philosophy: Which system is "more correct"?

2. **Timing Alignment**
   - Dasha change on Nov 15 (Venus → Sun)
   - Transit ingress on Nov 10 (Mercury → Sagittarius)
   - How to interpret? "Pre-dasha shift tension" or independent events?
   - Multi-system framework needed?

3. **Remedies Integration**
   - Western: No remedies tradition
   - Vedic: Gems, mantras, fasting, donations
   - For horoscope user, which remedies to suggest?
   - Should remedies align with dasha lord or transit planet?

### Question Set 12: Edge Cases & Conflicts

1. **Retrograde Planet Transits**
   - Planet retrograde May 1, direct June 15
   - Does retrograde period = different interpretation than direct?
   - How many times does same planet transit same point? (3x rule)
   - Should horoscope mention all 3 passes or just primary?

2. **Stationary Direct/Retrograde**
   - When planet changes direction (0° motion) = most powerful moment?
   - Should these get boosted confidence scores?
   - How to describe in horoscope? "At its strongest, this transit..."?

3. **Exact Aspect Rare Event**
   - Aspect exact to 1 arcminute = super powerful?
   - How rare is this? Probability calculation needed?
   - Should these get special horoscope mention?

4. **Eclipse Season**
   - Solar/Lunar eclipses reset prediction timelines?
   - Do eclipses override other transits for importance?
   - How to present: "Ignore other events, focus on eclipse"?

---

## SECTION D: TESTING FRAMEWORK

### Test Case Template

```python
TEST_CASE_TEMPLATE = {
    "case_id": "KOCH-001",
    "description": "Koch house calculation for NYC birth",
    "inputs": {
        "birth_datetime": "1980-07-13 10:30:00",
        "timezone": "America/New_York",
        "latitude": 40.7128,
        "longitude": -74.0060,
    },
    "expected_output": {
        "house_cusps": [45.2, 78.5, 112.3, 150.1, 187.2, 215.4, 225.2, 258.5, 292.3, 330.1, 7.2, 35.4],
        "tolerance": 0.016,  # ±1 arcminute
        "source": "Astro.com export",
    },
    "verification": {
        "system": "Astro.com",
        "date_checked": "2025-11-03",
        "status": "PASS|FAIL",
        "discrepancy_arcmin": 0.5,
    }
}
```

### Test Suite Coverage

**Chart Calculation Tests:**

- [ ] 50 random charts across globe, compare with Astro.com
- [ ] 10 edge cases (poles, equator, extremes)
- [ ] 20 historical events (famous births)

**Transit Analysis Tests:**

- [ ] 100 known events (JFK assassination, moon landing, etc.)
  - Does system identify these as "important" periods?
  - Accuracy: Did transits coincide with life events?
- [ ] 30 personal test cases with documented life events

**Horoscope Quality Tests:**

- [ ] Read horoscopes for grammatical correctness (n=100)
- [ ] Verify all claims are astrologically justified
- [ ] Check for contradictions (n=100 reviews)
- [ ] Compare with professional horoscopes (n=50 samples)

**Performance Tests:**

- [ ] Single chart: <100ms
- [ ] 100 charts: <5s total
- [ ] 1000 charts: <45s total
- [ ] Horoscope generation: <2s

---

## DELIVERABLES CHECKLIST

### By End of Research Phase

- [ ] Koch house system validated (±1 arcminute accuracy)
- [ ] Aspect interpretation dictionary (5+ major aspects × 12 planets = 60+ entries minimum)
- [ ] 50+ narrative templates with usage guidelines
- [ ] Event clustering algorithm pseudocode
- [ ] Confidence scoring framework (documented, tested)
- [ ] Multi-factor integration strategy (Vedic + Western)
- [ ] Database schema with migration scripts
- [ ] Test suite with 200+ cases
- [ ] Implementation roadmap (phases with timeline)
- [ ] Performance benchmarks and optimization strategies
- [ ] Professional standards comparison (vs. Astro.com, JHora, etc.)

---

## NEXT STEPS FOR IMPLEMENTATION TEAM

Once research is complete:

1. **Sprint 1**: Implement Koch, validate with test suite
2. **Sprint 2**: Build transit analysis engine, event clustering
3. **Sprint 3**: Develop narrative generation with templates
4. **Sprint 4**: Integration testing, performance optimization
5. **Sprint 5**: API endpoints, frontend integration
6. **Sprint 6**: Production deployment, monitoring setup

---

**Document Version**: 1.0  
**Created**: November 3, 2025  
**Research Status**: Ready for Deep Analysis
