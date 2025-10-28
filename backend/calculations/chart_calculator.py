"""
Astrological Chart Calculator using Swiss Ephemeris
This is the core engine that calculates planetary positions, houses, and chart data.
"""

import swisseph as swe
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
import math

from utils.constants import (
    PLANETS, ZODIAC_SIGNS, AYANAMSA_TYPES, ASPECTS, ASPECT_SYMBOLS
)


# Additional constants for chart calculation
PLANET_NUMBERS = PLANETS  # Alias for compatibility
SIGN_NAMES = ZODIAC_SIGNS
AYANAMSAS = AYANAMSA_TYPES

# House systems mapping
HOUSE_SYSTEMS = {
    'P': 'Placidus',
    'K': 'Koch', 
    'O': 'Porphyrius',
    'R': 'Regiomontanus',
    'C': 'Campanus',
    'A': 'Equal (Ascendant)',
    'E': 'Equal',
    'W': 'Whole Sign',
    'X': 'Axial Rotation',
    'T': 'Topocentric',
    'B': 'Alcabitus',
    'G': 'Gauquelin sectors'
}


class ChartCalculator:
    """
    Main chart calculation engine using Swiss Ephemeris.
    Calculates planetary positions, houses, and provides foundational chart data.
    """
    
    def __init__(self, zodiac_type: str = 'tropical', ayanamsa: str = 'LAHIRI'):
        """
        Initialize the chart calculator.
        
        Args:
            zodiac_type: 'tropical' or 'sidereal'
            ayanamsa: Ayanamsa system for sidereal calculations
        """
        self.zodiac_type = zodiac_type
        self.ayanamsa = ayanamsa
        
        # Set up Swiss Ephemeris flags
        self.swe_flags = swe.FLG_SWIEPH | swe.FLG_SPEED
        
        if zodiac_type == 'sidereal':
            self.swe_flags |= swe.FLG_SIDEREAL
            if ayanamsa in AYANAMSAS:
                swe.set_sid_mode(AYANAMSAS[ayanamsa])
            else:
                swe.set_sid_mode(swe.SIDM_LAHIRI)  # Default
    
    def julian_day(self, year: int, month: int, day: int, hour: int, minute: int) -> float:
        """Calculate Julian Day Number for given date/time."""
        decimal_hour = hour + minute / 60.0
        return swe.julday(year, month, day, decimal_hour)
    
    def calculate_planetary_positions(self, jd: float) -> Dict[str, Dict[str, Any]]:
        """
        Calculate positions for all planets at given Julian Day.
        
        Args:
            jd: Julian Day Number
            
        Returns:
            Dictionary with planet data including longitude, latitude, speed, etc.
        """
        planets = {}
        
        for planet_name, planet_num in PLANET_NUMBERS.items():
            try:
                # Calculate planet position
                result = swe.calc_ut(jd, planet_num, self.swe_flags)
                longitude, latitude, distance, speed_lon, speed_lat, speed_dist = result[0]
                
                # Determine zodiac sign and degree within sign
                sign_num = int(longitude // 30)
                degree_in_sign = longitude % 30
                sign_name = SIGN_NAMES[sign_num]
                
                # Check if planet is retrograde (negative speed)
                is_retrograde = speed_lon < 0
                
                # Handle special case for South Node (opposite of North Node)
                if planet_name == 'SouthNode':
                    longitude = (longitude + 180) % 360
                    sign_num = int(longitude // 30)
                    degree_in_sign = longitude % 30
                    sign_name = SIGN_NAMES[sign_num]
                
                planets[planet_name] = {
                    'longitude': round(longitude, 6),
                    'latitude': round(latitude, 6),
                    'distance': round(distance, 6),
                    'speed': round(speed_lon, 6),
                    'speed_latitude': round(speed_lat, 6),
                    'speed_distance': round(speed_dist, 6),
                    'sign': sign_name,
                    'sign_number': sign_num,
                    'degree': round(degree_in_sign, 6),
                    'degree_absolute': round(longitude, 6),
                    'retrograde': is_retrograde,
                    'house': None  # Will be filled in later
                }
                
            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")
                planets[planet_name] = None
        
        return planets
    
    def calculate_houses(self, jd: float, latitude: float, longitude: float, 
                        house_system: str = 'P') -> Dict[str, Dict[str, Any]]:
        """
        Calculate house cusps using specified house system.
        
        Args:
            jd: Julian Day Number
            latitude: Geographic latitude
            longitude: Geographic longitude  
            house_system: House system ('P' = Placidus, 'K' = Koch, etc.)
            
        Returns:
            Dictionary with house cusp data
        """
        houses = {}
        
        try:
            # Calculate house cusps
            house_cusps, ascmc = swe.houses(jd, latitude, longitude, house_system.encode('ascii'))
            
            # Extract key points
            ascendant = ascmc[0]  # Ascendant
            mc = ascmc[1]         # Midheaven (MC)
            armc = ascmc[2]       # ARMC
            vertex = ascmc[3]     # Vertex
            
            # Process 12 house cusps
            for i in range(12):
                house_num = i + 1
                cusp_longitude = house_cusps[i]
                
                # Determine sign and degree
                sign_num = int(cusp_longitude // 30)
                degree_in_sign = cusp_longitude % 30
                sign_name = SIGN_NAMES[sign_num]
                
                houses[f'house_{house_num}'] = {
                    'longitude': round(cusp_longitude, 6),
                    'sign': sign_name,
                    'sign_number': sign_num,
                    'degree': round(degree_in_sign, 6),
                    'degree_absolute': round(cusp_longitude, 6)
                }
            
            # Add special points
            houses['ascendant'] = {
                'longitude': round(ascendant, 6),
                'sign': SIGN_NAMES[int(ascendant // 30)],
                'sign_number': int(ascendant // 30),
                'degree': round(ascendant % 30, 6),
                'degree_absolute': round(ascendant, 6)
            }
            
            houses['midheaven'] = {
                'longitude': round(mc, 6),
                'sign': SIGN_NAMES[int(mc // 30)],
                'sign_number': int(mc // 30),
                'degree': round(mc % 30, 6),
                'degree_absolute': round(mc, 6)
            }
            
            houses['vertex'] = {
                'longitude': round(vertex, 6),
                'sign': SIGN_NAMES[int(vertex // 30)],
                'sign_number': int(vertex // 30),
                'degree': round(vertex % 30, 6),
                'degree_absolute': round(vertex, 6)
            }
            
        except Exception as e:
            print(f"Error calculating houses: {e}")
            # Return empty houses with error info
            for i in range(1, 13):
                houses[f'house_{i}'] = {
                    'longitude': 0, 'sign': 'Aries', 'sign_number': 0,
                    'degree': 0, 'degree_absolute': 0, 'error': str(e)
                }
        
        return houses
    
    def assign_planets_to_houses(self, planets: Dict, houses: Dict) -> Dict:
        """
        Assign each planet to its house based on house cusps.
        
        Args:
            planets: Planet position data
            houses: House cusp data
            
        Returns:
            Updated planets dictionary with house assignments
        """
        if not houses or 'house_1' not in houses:
            return planets
        
        # Extract house cusp longitudes
        house_cusps = []
        for i in range(1, 13):
            house_key = f'house_{i}'
            if house_key in houses:
                house_cusps.append(houses[house_key]['longitude'])
        
        if len(house_cusps) != 12:
            return planets
        
        # Assign each planet to a house
        for planet_name, planet_data in planets.items():
            if planet_data is None:
                continue
                
            planet_longitude = planet_data['longitude']
            house_number = self._find_house_for_longitude(planet_longitude, house_cusps)
            planet_data['house'] = house_number
        
        return planets
    
    def _find_house_for_longitude(self, longitude: float, house_cusps: List[float]) -> int:
        """
        Find which house a given longitude falls into.
        
        Args:
            longitude: Planet longitude (0-360)
            house_cusps: List of 12 house cusp longitudes
            
        Returns:
            House number (1-12)
        """
        # Normalize longitude to 0-360
        longitude = longitude % 360
        
        for i in range(12):
            current_cusp = house_cusps[i]
            next_cusp = house_cusps[(i + 1) % 12]
            
            # Handle wrap-around at 0/360 degrees
            if current_cusp <= next_cusp:
                # Normal case: cusps don't cross 0°
                if current_cusp <= longitude < next_cusp:
                    return i + 1
            else:
                # Special case: cusps cross 0° (e.g., 350° to 30°)
                if longitude >= current_cusp or longitude < next_cusp:
                    return i + 1
        
        # Fallback (should rarely happen)
        return 1
    
    def calculate_chart(self, year: int, month: int, day: int, hour: int, minute: int,
                       latitude: float, longitude: float, house_system: str = 'P') -> Dict[str, Any]:
        """
        Calculate complete astrological chart.
        
        Args:
            year, month, day: Birth date
            hour, minute: Birth time
            latitude, longitude: Birth location
            house_system: House system to use
            
        Returns:
            Complete chart data with planets, houses, and metadata
        """
        try:
            # Calculate Julian Day
            jd = self.julian_day(year, month, day, hour, minute)
            
            # Calculate planetary positions
            planets = self.calculate_planetary_positions(jd)
            
            # Calculate houses
            houses = self.calculate_houses(jd, latitude, longitude, house_system)
            
            # Assign planets to houses
            planets = self.assign_planets_to_houses(planets, houses)
            
            # Create chart metadata
            chart_data = {
                'planets': planets,
                'houses': houses,
                'metadata': {
                    'julian_day': jd,
                    'zodiac_type': self.zodiac_type,
                    'ayanamsa': self.ayanamsa if self.zodiac_type == 'sidereal' else None,
                    'house_system': house_system,
                    'birth_data': {
                        'year': year, 'month': month, 'day': day,
                        'hour': hour, 'minute': minute,
                        'latitude': latitude, 'longitude': longitude
                    },
                    'calculation_timestamp': datetime.now(timezone.utc).isoformat()
                }
            }
            
            return chart_data
            
        except Exception as e:
            print(f"Error in chart calculation: {e}")
            return {
                'error': str(e),
                'planets': {},
                'houses': {},
                'metadata': {
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            }
    
    def generate_chart(self, birth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate chart from birth data dictionary (for API compatibility).
        
        Args:
            birth_data: Dictionary containing birth information
            
        Returns:
            Complete chart data
        """
        required_fields = ['year', 'month', 'day', 'hour', 'minute', 'latitude', 'longitude']
        
        for field in required_fields:
            if field not in birth_data:
                raise ValueError(f"Missing required field: {field}")
        
        house_system = birth_data.get('house_system', 'P')
        
        return self.calculate_chart(
            year=int(birth_data['year']),
            month=int(birth_data['month']),
            day=int(birth_data['day']),
            hour=int(birth_data['hour']),
            minute=int(birth_data['minute']),
            latitude=float(birth_data['latitude']),
            longitude=float(birth_data['longitude']),
            house_system=house_system
        )
    
    def get_chart_summary(self, chart_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the chart.
        
        Args:
            chart_data: Complete chart data
            
        Returns:
            Summary string
        """
        if 'error' in chart_data:
            return f"Chart calculation error: {chart_data['error']}"
        
        planets = chart_data.get('planets', {})
        houses = chart_data.get('houses', {})
        
        summary_parts = []
        
        # Sun, Moon, Rising summary
        if 'Sun' in planets and planets['Sun']:
            sun = planets['Sun']
            summary_parts.append(f"Sun in {sun['sign']} {sun['degree']:.1f}° (House {sun['house']})")
        
        if 'Moon' in planets and planets['Moon']:
            moon = planets['Moon']
            summary_parts.append(f"Moon in {moon['sign']} {moon['degree']:.1f}° (House {moon['house']})")
        
        if 'ascendant' in houses:
            asc = houses['ascendant']
            summary_parts.append(f"Ascendant in {asc['sign']} {asc['degree']:.1f}°")
        
        # Retrograde planets
        retrograde_planets = []
        for planet_name, planet_data in planets.items():
            if planet_data and planet_data.get('retrograde', False):
                retrograde_planets.append(planet_name)
        
        if retrograde_planets:
            summary_parts.append(f"Retrograde: {', '.join(retrograde_planets)}")
        
        # Zodiac type
        zodiac_info = chart_data.get('metadata', {}).get('zodiac_type', 'tropical')
        summary_parts.append(f"Zodiac: {zodiac_info}")
        
        return " | ".join(summary_parts) if summary_parts else "Chart data incomplete"


# Utility functions for external use
def quick_chart_calculation(year: int, month: int, day: int, hour: int, minute: int,
                          latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Quick chart calculation with default settings.
    
    Returns:
        Basic chart data
    """
    calculator = ChartCalculator()
    return calculator.calculate_chart(year, month, day, hour, minute, latitude, longitude)


def validate_birth_data(birth_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate birth data for chart calculation.
    
    Args:
        birth_data: Birth data dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['year', 'month', 'day', 'hour', 'minute', 'latitude', 'longitude']
    
    for field in required_fields:
        if field not in birth_data:
            return False, f"Missing required field: {field}"
    
    # Validate ranges
    try:
        year = int(birth_data['year'])
        month = int(birth_data['month'])
        day = int(birth_data['day'])
        hour = int(birth_data['hour'])
        minute = int(birth_data['minute'])
        latitude = float(birth_data['latitude'])
        longitude = float(birth_data['longitude'])
        
        if not (1800 <= year <= 2200):
            return False, f"Year {year} out of supported range (1800-2200)"
        
        if not (1 <= month <= 12):
            return False, f"Month {month} out of valid range (1-12)"
        
        if not (1 <= day <= 31):
            return False, f"Day {day} out of valid range (1-31)"
        
        if not (0 <= hour <= 23):
            return False, f"Hour {hour} out of valid range (0-23)"
        
        if not (0 <= minute <= 59):
            return False, f"Minute {minute} out of valid range (0-59)"
        
        if not (-90 <= latitude <= 90):
            return False, f"Latitude {latitude} out of valid range (-90 to 90)"
        
        if not (-180 <= longitude <= 180):
            return False, f"Longitude {longitude} out of valid range (-180 to 180)"
        
        return True, "Valid"
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid data type: {e}"


# Swiss Ephemeris status check
def check_ephemeris_status() -> Dict[str, Any]:
    """
    Check if Swiss Ephemeris is properly configured.
    
    Returns:
        Status information
    """
    try:
        # Test calculation with a known date
        test_jd = swe.julday(2000, 1, 1, 12.0)
        result = swe.calc_ut(test_jd, swe.SUN, swe.FLG_SWIEPH)
        
        return {
            'status': 'operational',
            'ephemeris_path': swe.get_library_path(),
            'test_calculation': f"Sun at {result[0][0]:.6f}° on 2000-01-01",
            'available_planets': list(PLANET_NUMBERS.keys()),
            'supported_house_systems': list(HOUSE_SYSTEMS.keys())
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'ephemeris_path': 'unknown',
            'test_calculation': 'failed'
        }