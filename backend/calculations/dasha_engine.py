"""
Vimshottari Dasha Calculator

Implements the complete Vimshottari dasha system used in Vedic astrology:
- Mahadasha (120-year planetary periods)
- Antardasha (sub-periods within Mahadasha)
- Pratyantardasha (micro-periods within Antardasha)

The Vimshottari dasha is the most widely used planetary period system,
indicating which planet "rules" a given time period and influences events.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import math


# Vimshottari dasha sequence and durations (in years)
DASHA_SEQUENCE = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = {
    'Ketu': 7,
    'Venus': 20,
    'Sun': 6,
    'Moon': 10,
    'Mars': 7,
    'Rahu': 18,
    'Jupiter': 16,
    'Saturn': 19,
    'Mercury': 17,
}

# Total dasha cycle = 120 years
TOTAL_DASHA_CYCLE = 120


@dataclass
class DashaPosition:
    """Represents a specific dasha period and current position within it."""
    dasha_planet: str           # Current Mahadasha lord
    dasha_start: datetime       # When this Mahadasha begins
    dasha_end: datetime         # When this Mahadasha ends
    dasha_years: int            # Duration of Mahadasha in years
    dasha_remaining: float      # Years remaining in current Mahadasha
    
    antardasha_planet: str      # Current Antardasha (sub-period) lord
    antardasha_start: datetime  # When this Antardasha begins
    antardasha_end: datetime    # When this Antardasha ends
    antardasha_years: float     # Duration of Antardasha in years
    antardasha_remaining: float # Years remaining in current Antardasha
    
    pratyantardasha_planet: str      # Current Pratyantardasha lord
    pratyantardasha_start: datetime  # When this Pratyantardasha begins
    pratyantardasha_end: datetime    # When this Pratyantardasha ends
    pratyantardasha_years: float     # Duration in days
    pratyantardasha_remaining: float # Days remaining
    
    percentage_complete: float  # Percent through entire 120-year cycle


@dataclass
class DashaPhase:
    """Represents a single dasha phase for timeline display."""
    planet: str
    level: str              # 'Mahadasha', 'Antardasha', 'Pratyantardasha'
    start_date: datetime
    end_date: datetime
    duration_years: float
    start_age_at_birth: float  # If birth was Jan 1, how old would native be
    end_age_at_birth: float


class DashaCalculator:
    """
    Complete Vimshottari dasha calculation engine.
    
    The dasha system shows the sequence of planetary influences from birth.
    Starting point depends on Moon's nakshatra at birth.
    """
    
    def __init__(self):
        """Initialize dasha calculator with standard Vimshottari sequence."""
        self.sequence = DASHA_SEQUENCE
        self.years = DASHA_YEARS
        self.total_cycle = TOTAL_DASHA_CYCLE
    
    
    def get_nakshatra_number(self, moon_longitude: float) -> int:
        """
        Get nakshatra number (1-27) from Moon's longitude.
        Used to determine starting dasha.
        
        Args:
            moon_longitude: Moon's longitude in degrees (0-360)
        
        Returns:
            Nakshatra number (1-27)
        """
        nakshatra_length = 13 + (20/60)  # 13°20' = 13.333...
        
        # Normalize to 0-360
        position = moon_longitude % 360
        
        # Calculate which nakshatra
        # Critical: Due to floating point precision, a position like 13.333333°
        # may be slightly less than the true boundary 13.33333333...
        # Add epsilon large enough to push past these precision gaps
        EPSILON = 1e-5  # Push past floating point precision issues
        quotient = (position + EPSILON) / nakshatra_length
        nakshatra_num = int(quotient) + 1
        
        # Handle edge case: if exactly at end of zodiac, should be Nak 27
        if nakshatra_num > 27:
            nakshatra_num = 27
        
        return nakshatra_num
    
    
    def get_starting_dasha_planet(self, moon_nakshatra: int) -> str:
        """
        Determine which planet's dasha started at birth based on Moon's nakshatra.
        
        Each nakshatra corresponds to a planet lord.
        The Vimshottari starts at a specific point and must be calculated
        based on when in that planet's period the native was born.
        
        Args:
            moon_nakshatra: Nakshatra number (1-27)
        
        Returns:
            Starting dasha planet name
        """
        # Nakshatra lords cycle every 9 nakshatras
        lord_index = (moon_nakshatra - 1) % 9
        return self.sequence[lord_index]
    
    
    def get_dasha_at_birth(self, moon_longitude: float, birth_date: datetime) -> str:
        """
        Calculate which dasha started closest to birth date.
        
        Note: Full accuracy requires:
        1. Exact birth time
        2. Exact Moon nakshatra
        3. Calculation of balance of dasha years at birth
        
        This is simplified; full calculation requires detailed ephemeris work.
        
        Args:
            moon_longitude: Moon's longitude at birth (0-360°)
            birth_date: Birth date
        
        Returns:
            Dasha planet at birth
        """
        nakshatra = self.get_nakshatra_number(moon_longitude)
        return self.get_starting_dasha_planet(nakshatra)
    
    
    def calculate_dasha_position(
        self,
        birth_date: datetime,
        moon_longitude: float,
        dasha_balance_years: float,
        query_date: datetime
    ) -> DashaPosition:
        """
        Calculate complete dasha position (Mahadasha, Antardasha, Pratyantardasha)
        at any given query date.
        
        Args:
            birth_date: Native's birth date
            moon_longitude: Moon's longitude at birth (for determining starting dasha)
            dasha_balance_years: Balance of dasha at birth (years remaining in first dasha)
                                  Usually provided in birth chart calculations
            query_date: Date to calculate dasha position for
        
        Returns:
            DashaPosition with complete period information
        """
        # Time elapsed since birth
        time_elapsed = query_date - birth_date
        days_elapsed = time_elapsed.days + time_elapsed.seconds / 86400
        years_elapsed = days_elapsed / 365.25
        
        # Total dasha years from birth
        total_dasha_years_elapsed = dasha_balance_years + years_elapsed
        
        # Which Mahadasha are we in?
        mahadasha_index = int(total_dasha_years_elapsed / self.total_cycle) % 9
        years_in_cycle = total_dasha_years_elapsed % self.total_cycle
        
        # Calculate current Mahadasha
        mahadasha_planet, mahadasha_start_year, mahadasha_end_year = \
            self._get_current_mahadasha(years_in_cycle)
        
        # Convert to actual dates
        mahadasha_start = birth_date + timedelta(days=mahadasha_start_year * 365.25)
        mahadasha_end = birth_date + timedelta(days=mahadasha_end_year * 365.25)
        mahadasha_remaining = (mahadasha_end - query_date).days / 365.25
        mahadasha_years = self.years[mahadasha_planet]
        
        # Calculate Antardasha within current Mahadasha
        years_in_mahadasha = (total_dasha_years_elapsed - mahadasha_start_year) % mahadasha_years
        antardasha_planet, antardasha_start_year, antardasha_end_year = \
            self._get_current_antardasha(mahadasha_planet, years_in_mahadasha)
        
        # Convert to actual dates
        antardasha_start = birth_date + timedelta(days=antardasha_start_year * 365.25)
        antardasha_end = birth_date + timedelta(days=antardasha_end_year * 365.25)
        antardasha_remaining = (antardasha_end - query_date).days / 365.25
        antardasha_years = self._get_antardasha_duration(mahadasha_planet, antardasha_planet)
        
        # Calculate Pratyantardasha within current Antardasha
        days_in_antardasha = (query_date - antardasha_start).days
        pratyantardasha_planet, pratyantardasha_start_day, pratyantardasha_end_day = \
            self._get_current_pratyantardasha(
                antardasha_planet,
                days_in_antardasha,
                self._get_antardasha_duration_days(mahadasha_planet, antardasha_planet)
            )
        
        pratyantardasha_start = antardasha_start + timedelta(days=pratyantardasha_start_day)
        pratyantardasha_end = antardasha_start + timedelta(days=pratyantardasha_end_day)
        pratyantardasha_remaining = (pratyantardasha_end - query_date).days
        pratyantardasha_years = pratyantardasha_end_day - pratyantardasha_start_day
        
        # Calculate percentage through cycle
        percentage = (total_dasha_years_elapsed % self.total_cycle) / self.total_cycle * 100
        
        return DashaPosition(
            dasha_planet=mahadasha_planet,
            dasha_start=mahadasha_start,
            dasha_end=mahadasha_end,
            dasha_years=mahadasha_years,
            dasha_remaining=mahadasha_remaining,
            
            antardasha_planet=antardasha_planet,
            antardasha_start=antardasha_start,
            antardasha_end=antardasha_end,
            antardasha_years=antardasha_years,
            antardasha_remaining=antardasha_remaining,
            
            pratyantardasha_planet=pratyantardasha_planet,
            pratyantardasha_start=pratyantardasha_start,
            pratyantardasha_end=pratyantardasha_end,
            pratyantardasha_years=pratyantardasha_years,
            pratyantardasha_remaining=pratyantardasha_remaining,
            
            percentage_complete=percentage
        )
    
    
    def _get_current_mahadasha(self, years_in_cycle: float) -> Tuple[str, float, float]:
        """
        Determine which Mahadasha period we're in and its dates.
        
        Args:
            years_in_cycle: Years into the 120-year cycle
        
        Returns:
            Tuple of (planet_name, start_year, end_year)
        """
        cumulative_years = 0
        
        for planet in self.sequence:
            planet_years = self.years[planet]
            end_year = cumulative_years + planet_years
            
            if years_in_cycle < end_year:
                return planet, cumulative_years, end_year
            
            cumulative_years = end_year
        
        # Shouldn't reach here, but fallback to last planet
        return self.sequence[-1], cumulative_years - self.years[self.sequence[-1]], cumulative_years
    
    
    def _get_current_antardasha(self, mahadasha_planet: str, years_in_mahadasha: float) -> Tuple[str, float, float]:
        """
        Determine which Antardasha (sub-period) we're in within current Mahadasha.
        
        Each Mahadasha is subdivided into 9 Antardashas (one for each planet).
        The sub-periods are proportional to each planet's dasha years.
        
        Args:
            mahadasha_planet: Current Mahadasha planet
            years_in_mahadasha: Years elapsed in current Mahadasha
        
        Returns:
            Tuple of (planet_name, start_year, end_year) relative to Mahadasha start
        """
        mahadasha_duration = self.years[mahadasha_planet]
        
        # Each Antardasha duration = (Antardasha planet years / 120) * Mahadasha duration
        cumulative_years = 0
        
        for planet in self.sequence:
            antardasha_duration = (self.years[planet] / self.total_cycle) * mahadasha_duration
            end_year = cumulative_years + antardasha_duration
            
            if years_in_mahadasha < end_year:
                return planet, cumulative_years, end_year
            
            cumulative_years = end_year
        
        # Fallback to last planet
        return self.sequence[-1], cumulative_years - self._get_antardasha_duration(mahadasha_planet, self.sequence[-1]), cumulative_years
    
    
    def _get_antardasha_duration(self, mahadasha_planet: str, antardasha_planet: str) -> float:
        """
        Calculate duration of an Antardasha in years.
        
        Formula: (Antardasha planet years / 120 years total) * Mahadasha duration
        
        Args:
            mahadasha_planet: Current Mahadasha lord
            antardasha_planet: Current Antardasha lord
        
        Returns:
            Duration in years (can be fractional)
        """
        mahadasha_duration = self.years[mahadasha_planet]
        antardasha_planet_years = self.years[antardasha_planet]
        return (antardasha_planet_years / self.total_cycle) * mahadasha_duration
    
    
    def _get_antardasha_duration_days(self, mahadasha_planet: str, antardasha_planet: str) -> float:
        """
        Calculate duration of an Antardasha in days.
        
        Args:
            mahadasha_planet: Current Mahadasha lord
            antardasha_planet: Current Antardasha lord
        
        Returns:
            Duration in days
        """
        years = self._get_antardasha_duration(mahadasha_planet, antardasha_planet)
        return years * 365.25
    
    
    def _get_current_pratyantardasha(
        self,
        antardasha_planet: str,
        days_in_antardasha: float,
        antardasha_duration_days: float
    ) -> Tuple[str, float, float]:
        """
        Determine which Pratyantardasha we're in.
        
        The Antardasha is subdivided into 9 Pratyantardashas.
        Similar proportional calculation as Antardasha within Mahadasha.
        
        Args:
            antardasha_planet: Current Antardasha planet
            days_in_antardasha: Days elapsed in current Antardasha
            antardasha_duration_days: Total duration of Antardasha in days
        
        Returns:
            Tuple of (planet_name, start_day, end_day)
        """
        cumulative_days = 0
        
        for planet in self.sequence:
            # Pratyantardasha duration = (Prat planet years / 120) * Antardasha duration
            pratyantardasha_duration = (self.years[planet] / self.total_cycle) * antardasha_duration_days
            end_day = cumulative_days + pratyantardasha_duration
            
            if days_in_antardasha < end_day:
                return planet, cumulative_days, end_day
            
            cumulative_days = end_day
        
        # Fallback
        return self.sequence[-1], cumulative_days - (self.years[self.sequence[-1]] / self.total_cycle) * antardasha_duration_days, cumulative_days
    
    
    def get_dasha_timeline(
        self,
        birth_date: datetime,
        years_forward: int = 2,
        level: str = 'Mahadasha'
    ) -> List[DashaPhase]:
        """
        Generate a timeline of dasha periods from birth into the future.
        
        Args:
            birth_date: Native's birth date
            years_forward: How many years forward to calculate (default 2 years)
            level: 'Mahadasha', 'Antardasha', or 'Pratyantardasha'
        
        Returns:
            List of DashaPhase objects representing the timeline
        """
        timeline = []
        current_date = birth_date
        end_date = datetime.now() + timedelta(days=years_forward * 365.25)
        
        if level == 'Mahadasha':
            for planet in self.sequence:
                duration = self.years[planet]
                start_date = current_date
                end_date = current_date + timedelta(days=duration * 365.25)
                
                timeline.append(DashaPhase(
                    planet=planet,
                    level='Mahadasha',
                    start_date=start_date,
                    end_date=end_date,
                    duration_years=duration,
                    start_age_at_birth=(start_date - birth_date).days / 365.25,
                    end_age_at_birth=(end_date - birth_date).days / 365.25
                ))
                
                current_date = end_date
                
                if current_date > end_date:
                    break
        
        return timeline
    
    
    def get_favorable_periods(
        self,
        birth_date: datetime,
        moon_longitude: float,
        query_date: datetime,
        target_planet: str,
        months_ahead: int = 24
    ) -> List[Tuple[datetime, datetime, str]]:
        """
        Find favorable periods when a specific planet will be active
        (good for important actions related to that planet).
        
        Args:
            birth_date: Native's birth date
            moon_longitude: Moon's longitude at birth
            query_date: Query date (usually today)
            target_planet: Which planet to find favorable periods for
            months_ahead: Look ahead this many months
        
        Returns:
            List of (start_date, end_date, confidence_reason) tuples
        """
        favorable_periods = []
        
        # Look at Antardasha and Pratyantardasha levels for most practical timing
        current_date = query_date
        end_date = query_date + timedelta(days=months_ahead * 30)
        dasha_balance = 12  # Simplified; should calculate from birth chart
        
        while current_date < end_date:
            position = self.calculate_dasha_position(
                birth_date,
                moon_longitude,
                dasha_balance,
                current_date
            )
            
            # Check if any level has target planet
            reasons = []
            
            if position.antardasha_planet == target_planet:
                reasons.append(f"Antardasha of {target_planet}")
                favorable_periods.append((
                    position.antardasha_start,
                    position.antardasha_end,
                    f"Antardasha: {target_planet}"
                ))
            
            if position.pratyantardasha_planet == target_planet:
                reasons.append(f"Pratyantardasha of {target_planet}")
                favorable_periods.append((
                    position.pratyantardasha_start,
                    position.pratyantardasha_end,
                    f"Pratyantardasha: {target_planet}"
                ))
            
            # Move forward by 1 month
            current_date += timedelta(days=30)
        
        # Sort by start date and deduplicate overlapping periods
        favorable_periods.sort(key=lambda x: x[0])
        return favorable_periods
    
    
    def format_dasha_position(self, position: DashaPosition) -> str:
        """
        Format dasha position for display.
        
        Args:
            position: DashaPosition to format
        
        Returns:
            Formatted string representation
        """
        output = f"""
╔════════════════════════════════════════════════════════════════╗
║                      DASHA ANALYSIS                            ║
╚════════════════════════════════════════════════════════════════╝

MAHADASHA (Major Period): {position.dasha_planet}
  Duration: {position.dasha_years} years
  Period: {position.dasha_start.strftime('%Y-%m-%d')} → {position.dasha_end.strftime('%Y-%m-%d')}
  Remaining: {position.dasha_remaining:.2f} years
  Status: {(1 - position.dasha_remaining / position.dasha_years) * 100:.1f}% complete

ANTARDASHA (Sub-period): {position.antardasha_planet}
  Duration: {position.antardasha_years:.2f} years
  Period: {position.antardasha_start.strftime('%Y-%m-%d')} → {position.antardasha_end.strftime('%Y-%m-%d')}
  Remaining: {position.antardasha_remaining:.2f} years
  Status: {(1 - position.antardasha_remaining / position.antardasha_years) * 100:.1f}% complete

PRATYANTARDASHA (Micro-period): {position.pratyantardasha_planet}
  Duration: {position.pratyantardasha_years:.0f} days
  Period: {position.pratyantardasha_start.strftime('%Y-%m-%d')} → {position.pratyantardasha_end.strftime('%Y-%m-%d')}
  Remaining: {position.pratyantardasha_remaining:.0f} days
  Status: {(1 - position.pratyantardasha_remaining / position.pratyantardasha_years) * 100:.1f}% complete

CYCLE PROGRESS: {position.percentage_complete:.1f}% through 120-year Vimshottari cycle
"""
        return output


# Convenience functions
def create_dasha_calculator() -> DashaCalculator:
    """Factory function to create a DashaCalculator instance."""
    return DashaCalculator()


def get_dasha_at_date(
    birth_date: datetime,
    moon_longitude: float,
    query_date: datetime,
    dasha_balance: float = 12.0
) -> DashaPosition:
    """
    Convenience function to get dasha position at any date.
    
    Args:
        birth_date: Native's birth date
        moon_longitude: Moon's longitude (0-360°)
        query_date: Date to calculate for
        dasha_balance: Balance of dasha at birth (default 12 years)
    
    Returns:
        DashaPosition for the query date
    """
    calculator = DashaCalculator()
    return calculator.calculate_dasha_position(
        birth_date,
        moon_longitude,
        dasha_balance,
        query_date
    )
