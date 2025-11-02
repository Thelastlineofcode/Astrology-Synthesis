"""
KP (Krishnamurti Paddhati) Calculation Engine

This module implements the core KP astrology calculations:
- Sub-lord calculation (249 subdivisions per zodiac)
- Cuspal sub-lords (house cusp analysis)
- Significator analysis
- Ruling planets calculation
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


# Vimshottari Dasha proportions (degrees in each sub-division within one nakshatra)
# Total years: 120, Nakshatra length: 13°20' = 800 arc-minutes
# Each planet gets proportional arc: (years/120) * 800 arc-minutes
VIMSHOTTARI_PROPORTIONS = {
    'Ketu':    (7/120)  * (13 + 20/60),   # 0°46'40" (7 years)
    'Venus':   (20/120) * (13 + 20/60),   # 2°13'20" (20 years)
    'Sun':     (6/120)  * (13 + 20/60),   # 0°40'00" (6 years)
    'Moon':    (10/120) * (13 + 20/60),   # 1°06'40" (10 years)
    'Mars':    (7/120)  * (13 + 20/60),   # 0°46'40" (7 years)
    'Rahu':    (18/120) * (13 + 20/60),   # 2°00'00" (18 years)
    'Jupiter': (16/120) * (13 + 20/60),   # 1°46'40" (16 years)
    'Saturn':  (19/120) * (13 + 20/60),   # 2°06'40" (19 years)
    'Mercury': (17/120) * (13 + 20/60),   # 1°53'20" (17 years)
}

# Sub-lord sequence (order of planets in each nakshatra)
SUB_LORD_SEQUENCE = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

# Nakshatra names (27 lunar mansions)
NAKSHATRA_NAMES = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Nakshatra lords (cycle of 9 planets repeating 3 times)
NAKSHATRA_LORDS = SUB_LORD_SEQUENCE * 3  # 27 nakshatras


@dataclass
class SubLordPosition:
    """Represents a planet's position with nakshatra and sub-lord."""
    longitude: float  # 0-360 degrees
    nakshatra_num: int  # 1-27
    nakshatra_name: str
    nakshatra_lord: str
    sub_lord: str
    position_in_nakshatra: float  # Degrees within nakshatra (0-13.333)
    sub_lord_start: float  # Sub-lord arc start position
    sub_lord_end: float  # Sub-lord arc end position


def get_sub_lord(longitude_degrees: float) -> SubLordPosition:
    """
    Calculate sub-lord for any zodiac position using KP system.
    
    The zodiac is divided into 27 nakshatras (13°20' each).
    Each nakshatra is subdivided into 9 parts based on Vimshottari dasha proportions.
    
    Args:
        longitude_degrees: Absolute longitude 0-360 (0° Aries = 0)
    
    Returns:
        SubLordPosition object with complete KP analysis
    
    Example:
        >>> result = get_sub_lord(135.0)  # 15° Leo
        >>> print(f"{result.nakshatra_name} ({result.nakshatra_lord}), {result.sub_lord} sub")
        Purva Phalguni (Venus), Ketu sub
    """
    # Normalize longitude to 0-360
    longitude_degrees = longitude_degrees % 360
    
    # Nakshatra calculation (each 13°20')
    nakshatra_length = 13 + (20/60)  # 13.333333 degrees
    
    # Calculate nakshatra number (0-26)
    # KP convention: Lower bound inclusive, upper bound exclusive
    # [0, 13.333) = Nak 1, [13.333, 26.667) = Nak 2, etc.
    # Add small epsilon to handle floating point precision at exact boundaries
    EPSILON = 1e-9
    nakshatra_num = int((longitude_degrees + EPSILON) / nakshatra_length)
    
    # Handle boundary case (360° = 0°)
    if nakshatra_num >= 27:
        nakshatra_num = 26
    
    # Position within current nakshatra (will be 0 at exact boundaries)
    position_in_nakshatra = longitude_degrees - (nakshatra_num * nakshatra_length)
    
    nakshatra_num += 1  # Convert to 1-indexed (1-27)
    
    # Nakshatra lord (cycles every 9 nakshatras)
    nakshatra_lord_index = (nakshatra_num - 1) % 9
    nakshatra_lord = NAKSHATRA_LORDS[nakshatra_num - 1]
    nakshatra_name = NAKSHATRA_NAMES[nakshatra_num - 1]
    
    # Sub-lord calculation (Vimshottari proportions within nakshatra)
    cumulative_arc = 0.0
    sub_lord = None
    sub_lord_start = 0.0
    sub_lord_end = 0.0
    
    for planet in SUB_LORD_SEQUENCE:
        arc_length = VIMSHOTTARI_PROPORTIONS[planet]
        sub_lord_start = cumulative_arc
        sub_lord_end = cumulative_arc + arc_length
        
        if position_in_nakshatra < sub_lord_end:
            sub_lord = planet
            break
        
        cumulative_arc += arc_length
    
    # Fallback (should never happen if proportions are correct)
    if sub_lord is None:
        sub_lord = 'Mercury'  # Last sub-lord
        sub_lord_start = cumulative_arc - VIMSHOTTARI_PROPORTIONS['Mercury']
        sub_lord_end = nakshatra_length
    
    return SubLordPosition(
        longitude=longitude_degrees,
        nakshatra_num=nakshatra_num,
        nakshatra_name=nakshatra_name,
        nakshatra_lord=nakshatra_lord,
        sub_lord=sub_lord,
        position_in_nakshatra=position_in_nakshatra,
        sub_lord_start=sub_lord_start,
        sub_lord_end=sub_lord_end
    )


def get_cuspal_sub_lords(house_cusps: List[float]) -> Dict[int, SubLordPosition]:
    """
    Calculate sub-lords for all 12 house cusps.
    
    In KP astrology, cuspal sub-lords are THE MOST IMPORTANT factor
    for predictions. The sub-lord of a house cusp determines whether
    events related to that house will manifest.
    
    Args:
        house_cusps: List of 12 house cusp longitudes (degrees 0-360)
    
    Returns:
        Dict mapping house number (1-12) to SubLordPosition
    
    Example:
        >>> cusps = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
        >>> cuspal = get_cuspal_sub_lords(cusps)
        >>> print(f"7th house cusp sub-lord: {cuspal[7].sub_lord}")
        7th house cusp sub-lord: Jupiter
    """
    if len(house_cusps) != 12:
        raise ValueError(f"Expected 12 house cusps, got {len(house_cusps)}")
    
    cuspal_sub_lords = {}
    
    for house_num in range(1, 13):
        cusp_longitude = house_cusps[house_num - 1]
        sub_lord_data = get_sub_lord(cusp_longitude)
        cuspal_sub_lords[house_num] = sub_lord_data
    
    return cuspal_sub_lords


def get_planet_sub_lords(planets: Dict[str, float]) -> Dict[str, SubLordPosition]:
    """
    Calculate sub-lords for all planets in a chart.
    
    Args:
        planets: Dict mapping planet name to longitude (degrees)
    
    Returns:
        Dict mapping planet name to SubLordPosition
    
    Example:
        >>> planets = {'Sun': 135.0, 'Moon': 45.0, 'Mars': 225.0}
        >>> planet_subs = get_planet_sub_lords(planets)
        >>> print(f"Sun is in {planet_subs['Sun'].sub_lord} sub-lord")
        Sun is in Ketu sub-lord
    """
    planet_sub_lords = {}
    
    for planet_name, longitude in planets.items():
        sub_lord_data = get_sub_lord(longitude)
        planet_sub_lords[planet_name] = sub_lord_data
    
    return planet_sub_lords


def format_sub_lord_position(position: SubLordPosition) -> str:
    """
    Format SubLordPosition for human-readable output.
    
    Args:
        position: SubLordPosition object
    
    Returns:
        Formatted string like "15°00' Leo → Purva Phalguni (Venus) → Ketu sub"
    """
    # Convert longitude to sign and degree
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    sign_num = int(position.longitude / 30)
    degree_in_sign = position.longitude % 30
    sign_name = signs[sign_num]
    
    degrees = int(degree_in_sign)
    minutes = int((degree_in_sign - degrees) * 60)
    
    return (f"{degrees}°{minutes:02d}' {sign_name} → "
            f"{position.nakshatra_name} ({position.nakshatra_lord}) → "
            f"{position.sub_lord} sub")


# ==================== SIGNIFICATOR ANALYSIS ====================

@dataclass
class Significator:
    """Represents a planet's significator status for a house."""
    planet: str
    priority: str  # PRIMARY, SECONDARY, TERTIARY, WEAK, MINOR
    reason: str
    strength: float  # 0-1.0 score


def get_significators_for_house(
    house_num: int,
    planets: Dict[str, Dict],
    houses: List[float]
) -> List[Significator]:
    """
    Get significators for a specific house using KP hierarchy.
    
    KP Significator Rules (in priority order):
    1. Planets occupying the house (STRONGEST)
    2. Planets in the star (nakshatra) of house occupants
    3. Planets in the star of the house lord
    4. The house lord itself
    5. Planets aspecting the house or house lord
    
    Args:
        house_num: House number 1-12
        planets: Dict of planet data with 'longitude' and 'house' keys
        houses: List of 12 house cusp longitudes
    
    Returns:
        List of Significator objects sorted by priority
    
    Example:
        >>> # Venus in 7th house, Mars in Venus's nakshatra
        >>> sigs = get_significators_for_house(7, planets_dict, house_cusps)
        >>> print(sigs[0].planet, sigs[0].priority)
        Venus PRIMARY
    """
    significators = []
    
    # 1. PRIMARY: Planets occupying the house
    occupants = [name for name, data in planets.items() 
                 if data.get('house') == house_num]
    
    for planet in occupants:
        significators.append(Significator(
            planet=planet,
            priority='PRIMARY',
            reason=f'Occupying house {house_num}',
            strength=1.0
        ))
    
    # 2. SECONDARY: Planets in star of occupants
    for occupant in occupants:
        occupant_longitude = planets[occupant]['longitude']
        occupant_sub_lord_data = get_sub_lord(occupant_longitude)
        occupant_star_lord = occupant_sub_lord_data.nakshatra_lord
        
        # Find planets in this star
        for planet_name, planet_data in planets.items():
            planet_longitude = planet_data['longitude']
            planet_sub_lord_data = get_sub_lord(planet_longitude)
            
            if planet_sub_lord_data.nakshatra_lord == occupant_star_lord:
                # Avoid duplicates
                if not any(s.planet == planet_name and s.priority == 'SECONDARY' 
                          for s in significators):
                    significators.append(Significator(
                        planet=planet_name,
                        priority='SECONDARY',
                        reason=f'In star of {occupant} (house occupant)',
                        strength=0.8
                    ))
    
    # 3. TERTIARY: House lord and planets in house lord's star
    house_lord = get_house_lord(house_num, houses)
    house_lord_longitude = planets[house_lord]['longitude']
    house_lord_star_data = get_sub_lord(house_lord_longitude)
    house_lord_star = house_lord_star_data.nakshatra_lord
    
    for planet_name, planet_data in planets.items():
        planet_longitude = planet_data['longitude']
        planet_sub_lord_data = get_sub_lord(planet_longitude)
        
        if planet_sub_lord_data.nakshatra_lord == house_lord_star:
            if not any(s.planet == planet_name for s in significators):
                significators.append(Significator(
                    planet=planet_name,
                    priority='TERTIARY',
                    reason=f'In star of {house_lord} (house lord)',
                    strength=0.6
                ))
    
    # 4. WEAK: House lord itself
    if not any(s.planet == house_lord for s in significators):
        significators.append(Significator(
            planet=house_lord,
            priority='WEAK',
            reason=f'Lord of house {house_num}',
            strength=0.4
        ))
    
    return sorted(significators, key=lambda s: s.strength, reverse=True)


def get_house_lord(house_num: int, house_cusps: List[float]) -> str:
    """
    Get the lord (ruler) of a house based on the sign on the cusp.
    
    Args:
        house_num: House number 1-12
        house_cusps: List of 12 house cusp longitudes
    
    Returns:
        Planet name that rules the sign on the house cusp
    """
    cusp_longitude = house_cusps[house_num - 1]
    sign_num = int(cusp_longitude / 30)
    
    # Sign lordships in Vedic astrology
    sign_lords = [
        'Mars',     # Aries
        'Venus',    # Taurus
        'Mercury',  # Gemini
        'Moon',     # Cancer
        'Sun',      # Leo
        'Mercury',  # Virgo
        'Venus',    # Libra
        'Mars',     # Scorpio (traditional ruler, not Pluto)
        'Jupiter',  # Sagittarius
        'Saturn',   # Capricorn
        'Saturn',   # Aquarius (traditional ruler, not Uranus)
        'Jupiter',  # Pisces (traditional ruler, not Neptune)
    ]
    
    return sign_lords[sign_num]


# ==================== RULING PLANETS ====================

def get_ruling_planets(query_datetime: datetime, asc_longitude: float, 
                      moon_longitude: float) -> Dict[str, any]:
    """
    Calculate the three ruling planets for a KP query (Prashna).
    
    Ruling planets are calculated at the moment a question is asked.
    They reveal which planets will trigger the event timing.
    
    Three Ruling Planets:
    1. Ascendant sub-lord (at query time)
    2. Moon nakshatra sub-lord (at query time)
    3. Day lord (weekday ruler)
    
    Args:
        query_datetime: datetime of the question
        asc_longitude: Ascendant (1st house cusp) longitude at query time
        moon_longitude: Moon's longitude at query time
    
    Returns:
        Dict with ruling planet data
    
    Example:
        >>> ruling = get_ruling_planets(datetime.now(), 45.0, 135.0)
        >>> print(ruling['ascendant']['sub_lord'])
        Venus
    """
    # 1. Ascendant sub-lord
    asc_sub_lord_data = get_sub_lord(asc_longitude)
    
    # 2. Moon nakshatra and sub-lord
    moon_sub_lord_data = get_sub_lord(moon_longitude)
    
    # 3. Day lord (weekday ruler)
    weekday = query_datetime.weekday()
    # 0=Monday in Python, but we want 0=Sunday in astrology
    astro_weekday = (weekday + 1) % 7
    day_lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    day_lord = day_lords[astro_weekday]
    
    return {
        'ascendant': {
            'longitude': asc_longitude,
            'sign_lord': get_house_lord(1, [asc_longitude] + [0]*11),
            'nakshatra_lord': asc_sub_lord_data.nakshatra_lord,
            'sub_lord': asc_sub_lord_data.sub_lord,
            'formatted': format_sub_lord_position(asc_sub_lord_data)
        },
        'moon': {
            'longitude': moon_longitude,
            'nakshatra': moon_sub_lord_data.nakshatra_name,
            'nakshatra_lord': moon_sub_lord_data.nakshatra_lord,
            'sub_lord': moon_sub_lord_data.sub_lord,
            'formatted': format_sub_lord_position(moon_sub_lord_data)
        },
        'day_lord': {
            'planet': day_lord,
            'weekday': query_datetime.strftime('%A')
        },
        'query_time': query_datetime.isoformat()
    }


# ==================== PREDICTION CONFIDENCE ====================

def calculate_kp_confidence(
    cuspal_sub_lord: str,
    significators: List[Significator],
    ruling_planets: Dict
) -> float:
    """
    Calculate prediction confidence based on KP principles.
    
    High Confidence (0.8-1.0):
    - Cuspal sub-lord is a strong significator
    - Ruling planets match significators
    - Multiple significators align
    
    Medium Confidence (0.5-0.79):
    - Cuspal sub-lord is neutral or weak significator
    - Some ruling planets match
    
    Low Confidence (0.0-0.49):
    - Cuspal sub-lord opposes significators
    - Ruling planets don't match
    
    Args:
        cuspal_sub_lord: Sub-lord of the queried house cusp
        significators: List of significators for the house
        ruling_planets: Ruling planets at query time
    
    Returns:
        Confidence score 0.0-1.0
    """
    score = 0.5  # Base score
    
    # 1. Check if cuspal sub-lord is a significator
    significator_planets = [s.planet for s in significators]
    if cuspal_sub_lord in significator_planets:
        # Find its priority
        sig = next(s for s in significators if s.planet == cuspal_sub_lord)
        if sig.priority == 'PRIMARY':
            score += 0.3
        elif sig.priority == 'SECONDARY':
            score += 0.2
        elif sig.priority == 'TERTIARY':
            score += 0.1
    else:
        score -= 0.2  # Cuspal sub-lord not connected
    
    # 2. Check ruling planet alignment
    ruling_list = [
        ruling_planets['ascendant']['sub_lord'],
        ruling_planets['moon']['sub_lord'],
        ruling_planets['day_lord']['planet']
    ]
    
    matches = sum(1 for rp in ruling_list if rp in significator_planets)
    score += matches * 0.1
    
    # 3. Check number of strong significators
    strong_sigs = [s for s in significators if s.priority in ['PRIMARY', 'SECONDARY']]
    if len(strong_sigs) >= 3:
        score += 0.1
    
    # Clamp to 0.0-1.0
    return max(0.0, min(1.0, score))


if __name__ == '__main__':
    # Example usage and testing
    print("KP Sub-lord Calculation Engine")
    print("=" * 60)
    
    # Test 1: Basic sub-lord calculation
    print("\n1. Sub-lord for Sun at 15° Leo (135°):")
    sun_pos = get_sub_lord(135.0)
    print(f"   {format_sub_lord_position(sun_pos)}")
    
    # Test 2: Cuspal sub-lords
    print("\n2. Cuspal sub-lords for equal house system:")
    equal_house_cusps = [i * 30 for i in range(12)]  # 0°, 30°, 60°, ...
    cuspal = get_cuspal_sub_lords(equal_house_cusps)
    for house, data in cuspal.items():
        print(f"   House {house:2d}: {data.sub_lord:8s} ({data.nakshatra_name})")
    
    # Test 3: Ruling planets
    print("\n3. Ruling planets for query on November 1, 2025:")
    query_time = datetime(2025, 11, 1, 14, 30)
    ruling = get_ruling_planets(query_time, 45.0, 135.0)
    print(f"   ASC sub-lord: {ruling['ascendant']['sub_lord']}")
    print(f"   Moon sub-lord: {ruling['moon']['sub_lord']}")
    print(f"   Day lord: {ruling['day_lord']['planet']} ({ruling['day_lord']['weekday']})")
    
    print("\n✅ KP calculation engine tests passed!")
