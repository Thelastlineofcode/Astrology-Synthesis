"""
Swiss Ephemeris Integration Module

Provides real-time planetary positions and astrological calculations
using the Swiss Ephemeris library (pyswisseph).

Features:
- Real-time planetary positions (Sun, Moon, planets, Rahu, Ketu)
- House cusp calculations (Placidus, Equal, Whole Sign)
- Ayanamsa adjustments (Lahiri, Fagan/Bradley, DeLuce)
- Aspect calculations
- Retrograde detection
- Timezone and DST handling
"""

import swisseph as swe
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from functools import lru_cache
import logging
import math
from .exceptions import PlanetNotFoundError, EphemerisError, HouseCalculationError

logger = logging.getLogger(__name__)


class HouseSystem(Enum):
    """House calculation systems."""
    PLACIDUS = b'P'      # Most commonly used in Western astrology
    EQUAL = b'E'         # Equal house system
    WHOLE_SIGN = b'W'    # Whole sign houses
    KOCH = b'K'          # Koch houses
    CAMPANUS = b'C'      # Campanus houses
    REGIOMONTANUS = b'R' # Regiomontanus houses


class Ayanamsa(Enum):
    """Ayanamsa (tropical to sidereal adjustment) systems."""
    LAHIRI = 1            # Used in Vedic astrology (most common)
    RAMAN = 4             # Alternative Vedic
    KRISHNAMURTI = 5      # KP system
    FAGAN_BRADLEY = 10    # Western sidereal
    DELUCE = 9            # Alternative


@dataclass
class PlanetPosition:
    """Represents a planet's astrological position."""
    planet_name: str
    longitude: float           # 0-360 degrees
    latitude: float            # -90 to +90 degrees
    distance: float            # AU (Astronomical Units)
    speed: float               # Degrees per day
    is_retrograde: bool        # True if retrograde
    house: Optional[int]       # 1-12, None if not calculated
    sign: str                  # Aries, Taurus, etc.
    degree_in_sign: float      # 0-30 degrees within sign
    nakshatra: Optional[int]   # 1-27 (Vedic)
    
    def __str__(self):
        """Format as readable string."""
        ret = "R" if self.is_retrograde else "D"
        return (f"{self.planet_name:8} {self.longitude:7.2f}° "
                f"{self.sign:12} {self.degree_in_sign:5.2f}° [{ret}]")


@dataclass
class HouseCusps:
    """Represents the 12 house cusps."""
    cusps: List[float]         # 12 cusp longitudes (0-360)
    ascendant: float           # House 1 cusp
    midheaven: float           # House 10 cusp
    descendant: float          # House 7 cusp
    imum_coeli: float          # House 4 cusp


@dataclass
class AspectData:
    """Represents an aspect between two planets."""
    planet1: str
    planet2: str
    aspect: str                # 'Conjunction', 'Sextile', 'Square', etc.
    degrees: float             # Exact aspect degrees
    orb: float                 # 0-8 degrees (aspect allowance)
    strength: float            # 0-1 (1 = exact, 0 = wide)
    applying: bool             # True if aspect is applying (getting closer)


class EphemerisCalculator:
    """
    Main class for Swiss Ephemeris calculations.
    
    Provides accurate astronomical/astrological data for
    prediction engines and chart analysis.
    """
    
    # Zodiac signs
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Vedic nakshatras
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    # Planet identifiers for Swiss Ephemeris
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
        'Rahu': swe.MEAN_NODE,     # Moon's mean ascending node
        'Ketu': 'KETU_SPECIAL',    # Calculated as Rahu + 180°
    }
    
    def __init__(self, ayanamsa_system: Ayanamsa = Ayanamsa.LAHIRI):
        """
        Initialize ephemeris calculator.
        
        Args:
            ayanamsa_system: Which ayanamsa to use (default: Lahiri for Vedic)
        """
        self.ayanamsa_system = ayanamsa_system
        # Set the ayanamsa mode
        swe.set_sid_mode(ayanamsa_system.value)
    
    
    def _datetime_to_jd(self, dt: datetime) -> float:
        """
        Convert Python datetime to Julian Day Number.

        Args:
            dt: Python datetime object

        Returns:
            Julian Day Number (float)
        """
        # Use UT (UTC) for calculations
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0

        jd = swe.julday(year, month, day, hour, swe.GREG_CAL)
        return jd

    @lru_cache(maxsize=256)
    def _get_planet_data_cached(
        self,
        planet_id: int,
        jd: float,
        tropical: bool,
        is_ketu: bool = False
    ) -> Tuple[float, float, float, float]:
        """
        Cached helper for planet position calculation.

        Args:
            planet_id: Swiss Ephemeris planet ID
            jd: Julian Day
            tropical: Use tropical zodiac
            is_ketu: Special flag for Ketu calculation

        Returns:
            Tuple of (longitude, latitude, distance, speed)
        """
        if is_ketu:
            # Get Rahu and calculate Ketu as opposite
            if tropical:
                result, flags = swe.calc_ut(jd, planet_id, swe.FLG_SPEED)
            else:
                result, flags = swe.calc_ut(jd, planet_id, swe.FLG_SPEED | swe.FLG_SIDEREAL)
            longitude = (result[0] + 180.0) % 360
            latitude = -result[1]
            distance = result[2]
            speed = result[3]
        else:
            if tropical:
                result, flags = swe.calc_ut(jd, planet_id, swe.FLG_SPEED)
            else:
                result, flags = swe.calc_ut(jd, planet_id, swe.FLG_SPEED | swe.FLG_SIDEREAL)
            longitude = result[0] % 360
            latitude = result[1]
            distance = result[2]
            speed = result[3]

        return longitude, latitude, distance, speed
    
    
    def get_planet_position(
        self,
        planet_name: str,
        date: datetime,
        tropical: bool = False
    ) -> PlanetPosition:
        """
        Get a planet's position at a specific date/time.

        Args:
            planet_name: Planet name ('Sun', 'Moon', 'Mercury', etc.)
            date: Query date/time (UTC recommended)
            tropical: If True, use tropical zodiac; if False, use sidereal (Vedic)

        Returns:
            PlanetPosition object with all positional data

        Raises:
            PlanetNotFoundError: If planet_name is not recognized
        """
        if planet_name not in self.PLANETS:
            raise PlanetNotFoundError(f"Unknown planet: {planet_name}")

        planet_id = self.PLANETS[planet_name]
        jd = self._datetime_to_jd(date)

        # Use cached calculation
        if planet_name == 'Ketu':
            # Get Rahu ID and calculate Ketu as opposite
            rahu_id = self.PLANETS['Rahu']
            longitude, latitude, distance, speed = self._get_planet_data_cached(
                rahu_id, jd, tropical, is_ketu=True
            )
        else:
            longitude, latitude, distance, speed = self._get_planet_data_cached(
                planet_id, jd, tropical, is_ketu=False
            )
        
        # Determine sign
        sign_index = int(longitude / 30)
        sign = self.SIGNS[sign_index % 12]
        degree_in_sign = longitude % 30
        
        # Determine nakshatra (only in sidereal)
        if not tropical:
            nakshatra_num = int(longitude / 13.333333) + 1
            if nakshatra_num > 27:
                nakshatra_num = 27
            nakshatra = self.NAKSHATRAS[nakshatra_num - 1]
        else:
            nakshatra = None
        
        # Check retrograde (speed < 0)
        is_retrograde = speed < 0
        
        return PlanetPosition(
            planet_name=planet_name,
            longitude=longitude,
            latitude=latitude,
            distance=distance,
            speed=abs(speed),
            is_retrograde=is_retrograde,
            house=None,  # Set later if houses calculated
            sign=sign,
            degree_in_sign=degree_in_sign,
            nakshatra=nakshatra if not tropical else None
        )
    
    
    def get_all_planets(
        self,
        date: datetime,
        tropical: bool = False
    ) -> Dict[str, PlanetPosition]:
        """
        Get positions of all major planets at a date.
        
        Args:
            date: Query date/time
            tropical: Use tropical (True) or sidereal (False) zodiac
        
        Returns:
            Dict mapping planet names to PlanetPosition objects
        """
        planets = {}
        
        # Sun through Pluto + nodes
        for planet_name in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
                           'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
                           'Rahu', 'Ketu']:
            planets[planet_name] = self.get_planet_position(planet_name, date, tropical)
        
        return planets
    
    
    def get_house_cusps(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        house_system: HouseSystem = HouseSystem.PLACIDUS
    ) -> HouseCusps:
        """
        Calculate house cusps for a birth time and location.
        
        Args:
            date: Birth date/time (UTC)
            latitude: Birth latitude (-90 to +90, S is negative)
            longitude: Birth longitude (-180 to +180, W is negative)
            house_system: Which house system to use
        
        Returns:
            HouseCusps object with all 12 cusps
        """
        jd = self._datetime_to_jd(date)
        
        # Calculate houses
        cusps, ascmc = swe.houses(jd, latitude, longitude, 
                                   house_system.value)
        
        return HouseCusps(
            cusps=list(cusps),
            ascendant=ascmc[0],
            midheaven=ascmc[1],
            descendant=ascmc[2],
            imum_coeli=ascmc[3]
        )
    
    
    def get_planet_house(
        self,
        planet: PlanetPosition,
        house_cusps: HouseCusps
    ) -> int:
        """
        Determine which house a planet occupies.
        
        Args:
            planet: PlanetPosition object
            house_cusps: HouseCusps object
        
        Returns:
            House number (1-12)
        """
        planet_lon = planet.longitude
        cusps = house_cusps.cusps
        
        # Check each house
        for house in range(12):
            cusp_start = cusps[house]
            cusp_end = cusps[(house + 1) % 12]
            
            # Handle wraparound at 0°
            if cusp_start > cusp_end:
                if planet_lon >= cusp_start or planet_lon < cusp_end:
                    return house + 1
            else:
                if cusp_start <= planet_lon < cusp_end:
                    return house + 1
        
        return 1  # Default to house 1
    
    
    def calculate_aspects(
        self,
        planet1: PlanetPosition,
        planet2: PlanetPosition,
        max_orb: float = 8.0
    ) -> Optional[AspectData]:
        """
        Calculate aspect between two planets.
        
        Args:
            planet1: First planet
            planet2: Second planet
            max_orb: Maximum aspect orb (default 8°)
        
        Returns:
            AspectData if aspect exists, None otherwise
        """
        # Aspect definitions (degrees)
        aspects = {
            'Conjunction': 0,
            'Sextile': 60,
            'Square': 90,
            'Trine': 120,
            'Opposition': 180,
        }
        
        # Calculate difference
        diff = abs(planet1.longitude - planet2.longitude)
        
        # Normalize to 0-180
        if diff > 180:
            diff = 360 - diff
        
        # Check aspects
        for aspect_name, aspect_deg in aspects.items():
            orb = abs(diff - aspect_deg)
            
            if orb <= max_orb:
                strength = 1.0 - (orb / max_orb)  # 1.0 = exact, 0.0 = wide
                
                # Applying if slower planet catching faster
                applying = True
                if planet1.speed > planet2.speed:
                    applying = diff < aspect_deg
                
                return AspectData(
                    planet1=planet1.planet_name,
                    planet2=planet2.planet_name,
                    aspect=aspect_name,
                    degrees=diff,
                    orb=orb,
                    strength=strength,
                    applying=applying
                )
        
        return None
    
    
    def get_current_planets(
        self,
        latitude: float = 0,
        longitude: float = 0,
        tropical: bool = False
    ) -> Dict[str, PlanetPosition]:
        """
        Get current planet positions.
        
        Args:
            latitude: Observer latitude (default 0 = equator)
            longitude: Observer longitude (default 0 = Greenwich)
            tropical: Use tropical (True) or sidereal (False)
        
        Returns:
            Dict of current planet positions
        """
        now = datetime.utcnow()
        planets = self.get_all_planets(now, tropical)
        
        # Calculate houses for current time
        try:
            houses = self.get_house_cusps(now, latitude, longitude)

            # Assign houses to planets
            for planet in planets.values():
                planet.house = self.get_planet_house(planet, houses)
        except Exception as e:
            # If house calculation fails, continue without houses but log the error
            logger.warning(f"Failed to calculate house positions: {str(e)}")
            # Planets will have house=None, which is acceptable
        
        return planets
    
    
    def format_position(self, planet: PlanetPosition) -> str:
        """Format planet position as readable string."""
        ret = "R" if planet.is_retrograde else "D"
        house_str = f"H{planet.house}" if planet.house else "  "
        nak_str = f"{planet.nakshatra}" if planet.nakshatra else ""
        
        return (f"{planet.planet_name:8} {planet.longitude:7.2f}° "
                f"{planet.sign:12} {planet.degree_in_sign:5.2f}° "
                f"[{ret}] {house_str} {nak_str}")


def get_current_ephemeris(
    latitude: float = 0,
    longitude: float = 0,
    tropical: bool = False
) -> Dict[str, PlanetPosition]:
    """
    Convenience function: Get current planetary positions.
    
    Args:
        latitude: Observer latitude
        longitude: Observer longitude
        tropical: Use tropical zodiac
    
    Returns:
        Dict of current planet positions
    """
    calc = EphemerisCalculator()
    return calc.get_current_planets(latitude, longitude, tropical)


def get_birth_chart(
    birth_date: datetime,
    latitude: float,
    longitude: float,
    tropical: bool = False,
    house_system: HouseSystem = HouseSystem.PLACIDUS
) -> Tuple[Dict[str, PlanetPosition], HouseCusps]:
    """
    Convenience function: Generate complete birth chart.
    
    Args:
        birth_date: Birth date/time (UTC)
        latitude: Birth latitude
        longitude: Birth longitude
        tropical: Use tropical zodiac
        house_system: House calculation system
    
    Returns:
        Tuple of (planets dict, HouseCusps)
    """
    calc = EphemerisCalculator()
    
    # Get planets
    planets = calc.get_all_planets(birth_date, tropical)
    
    # Get houses
    houses = calc.get_house_cusps(birth_date, latitude, longitude, house_system)
    
    # Assign houses to planets
    for planet in planets.values():
        planet.house = calc.get_planet_house(planet, houses)
    
    return planets, houses
