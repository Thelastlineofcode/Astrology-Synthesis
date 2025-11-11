"""
Transit Timing Engine - Syncretic Integration

Synthesizes three core systems:
1. KP Interpretation (Significators, Sub-lords, House matters)
2. Vimshottari Dasha (Running planetary periods)
3. Transit Analysis (Real planetary movements)

The engine identifies activation windows when:
- Transiting planet enters natal significator
- Current Dasha lord supports the event
- Combined confidence score is high

This creates a unified prediction system that answers:
"When will this event manifest for this person?"
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Import required modules
from backend.calculations.dasha_engine import DashaCalculator, DashaPosition
from backend.calculations.kp_engine import (
    get_sub_lord,
    get_significators_for_house,
    get_ruling_planets,
    VIMSHOTTARI_PROPORTIONS
)
from backend.calculations.ephemeris import EphemerisCalculator, PlanetPosition


@dataclass
class TransitEvent:
    """Represents a single transit activation event."""
    event_date: datetime              # When event activates
    transiting_planet: str            # Planet moving into significator
    natal_significator: str           # House/planet being activated
    house_matter: str                 # What it affects (marriage, career, health, etc)
    
    dasha_planet: str                 # Current Mahadasha lord
    dasha_remaining_years: float      # Years left in current Dasha
    
    kp_confidence: float              # KP system confidence (0-1)
    dasha_support: float              # Dasha lord support (0-1)
    combined_confidence: float        # Overall confidence (0-1)
    
    duration_days: int                # How long the transit lasts
    event_strength: str               # Minor/Moderate/Major
    interpretation: str               # Natural language description


@dataclass
class ActivationWindow:
    """Represents a time window when an event can manifest."""
    start_date: datetime
    end_date: datetime
    duration_days: int
    event_type: str                   # 'Marriage', 'Career Change', 'Health Crisis', etc
    key_planets: List[str]            # Planets involved
    
    favorable_days: int               # Days with high combined confidence
    unfavorable_days: int             # Days with low confidence
    peak_date: datetime               # Date of maximum activation
    peak_confidence: float            # Maximum confidence during window


class TransitAnalyzer:
    """
    Comprehensive transit analysis system.
    
    Combines KP significators with Dasha timing and planetary transits
    to identify when events manifest.
    """
    
    def __init__(self):
        """Initialize transit analyzer with Dasha and Ephemeris engines."""
        self.dasha = DashaCalculator()
        self.ephemeris = EphemerisCalculator()  # For real planetary positions
        
        # House matter keywords for interpretation
        self.house_matters = {
            1: ['Self', 'Personality', 'Health', 'Appearance', 'New Beginning'],
            2: ['Finance', 'Family', 'Food', 'Speech', 'Education'],
            3: ['Communication', 'Siblings', 'Travel', 'Courage', 'Writing'],
            4: ['Home', 'Property', 'Mother', 'Vehicle', 'Land', 'Comfort'],
            5: ['Children', 'Creativity', 'Love', 'Education', 'Entertainment'],
            6: ['Health', 'Work', 'Service', 'Enemies', 'Debts', 'Disease'],
            7: ['Marriage', 'Partnership', 'Business', 'Relationships', 'Enemies'],
            8: ['Longevity', 'Crisis', 'Inheritance', 'Transformation', 'Mystery'],
            9: ['Fortune', 'Travel', 'Religion', 'Teacher', 'Prosperity', 'Higher Learning'],
            10: ['Career', 'Status', 'Fame', 'Authority', 'Public', 'Father'],
            11: ['Gains', 'Friendship', 'Hope', 'Wishes', 'Income', 'Aspirations'],
            12: ['Loss', 'Isolation', 'Foreign Land', 'Spirituality', 'Expenditure', 'Release']
        }
    
    
    def get_transit_activations(
        self,
        birth_chart: Dict,
        start_date: datetime,
        end_date: datetime,
        target_houses: Optional[List[int]] = None,
        min_confidence: float = 0.6
    ) -> List[TransitEvent]:
        """
        Find all transit activation events within a date range.
        
        Args:
            birth_chart: Dict with 'planet_positions' (list), 'moon_longitude', 'dasha_balance_years'
            start_date: Beginning of analysis period
            end_date: End of analysis period
            target_houses: Specific houses to focus on (None = all)
            min_confidence: Minimum confidence to include event (0-1)
        
        Returns:
            List of TransitEvent sorted by date
        """
        events = []
        
        # Convert planet_positions list to dict format for get_significators_for_house
        planet_positions = birth_chart.get('planet_positions', [])
        natal_planets = {}
        for p in planet_positions:
            natal_planets[p['planet']] = {
                'longitude': p['longitude'],
                'house': p['house'],
                'latitude': p.get('latitude', 0)
            }
        
        # Extract house cusp longitudes from house_cusps list
        house_cusps_list = birth_chart.get('house_cusps', [])
        house_cusp_longitudes = []
        if isinstance(house_cusps_list, list) and len(house_cusps_list) > 0:
            # If it's a list of dicts, extract 'cusp' or 'longitude'
            if isinstance(house_cusps_list[0], dict):
                house_cusp_longitudes = [h.get('cusp', h.get('longitude', 0)) for h in house_cusps_list]
            else:
                # It's a list of floats
                house_cusp_longitudes = house_cusps_list
        
        moon_longitude = birth_chart.get('moon_longitude', 0)
        dasha_balance = birth_chart.get('dasha_balance_years', 0)
        
        # Get KP significators for all houses
        significators = {}
        for house in range(1, 13):
            sigs = get_significators_for_house(
                house,
                natal_planets,
                house_cusp_longitudes
            )
            # Extract planet names from Significator objects
            sig_planets = [sig.planet for sig in sigs] if sigs else []
            significators[house] = sig_planets
        
        # Ensure start_date is timezone-aware (UTC)
        if start_date.tzinfo is None:
            import pytz
            start_date = pytz.UTC.localize(start_date)
        
        # Get birth date from chart (or use start_date as fallback)
        birth_date = birth_chart.get('birth_date', start_date)
        if birth_date.tzinfo is None:
            import pytz
            birth_date = pytz.UTC.localize(birth_date)
        
        # Current dasha info
        current_dasha = self.dasha.calculate_dasha_position(
            birth_date,
            moon_longitude,
            dasha_balance,
            start_date
        )
        
        # Scan through each day in the period
        current_date = start_date
        while current_date <= end_date:
            # Get dasha position for this date
            dasha_pos = self.dasha.calculate_dasha_position(
                birth_chart.get('birth_date', start_date),
                moon_longitude,
                dasha_balance,
                current_date
            )
            
            # Check each target house for transits
            houses_to_check = target_houses or list(range(1, 13))
            
            for house in houses_to_check:
                sigs = significators.get(house, [])
                
                for sig_planet in sigs[:3]:  # Top 3 significators per house
                    # Calculate KP confidence for this significator
                    kp_conf = self._calculate_kp_transit_confidence(
                        transiting_planet=self._get_transit_planet_at_date(current_date),
                        natal_significator=sig_planet,
                        house=house,
                        natal_planets=natal_planets
                    )
                    
                    if kp_conf < min_confidence:
                        continue
                    
                    # Calculate Dasha support
                    dasha_support = self._calculate_dasha_support(
                        dasha_planet=dasha_pos.dasha_planet,
                        significator=sig_planet,
                        house=house
                    )
                    
                    # Combined confidence
                    combined = (kp_conf * 0.6) + (dasha_support * 0.4)
                    
                    if combined >= min_confidence:
                        # Create transit event
                        event = TransitEvent(
                            event_date=current_date,
                            transiting_planet=self._get_transit_planet_at_date(current_date),
                            natal_significator=sig_planet,
                            house_matter=', '.join(self.house_matters.get(house, [])),
                            dasha_planet=dasha_pos.dasha_planet,
                            dasha_remaining_years=dasha_pos.dasha_remaining,
                            kp_confidence=kp_conf,
                            dasha_support=dasha_support,
                            combined_confidence=combined,
                            duration_days=self._estimate_transit_duration(sig_planet),
                            event_strength=self._classify_event_strength(combined),
                            interpretation=self._generate_interpretation(
                                sig_planet,
                                house,
                                dasha_pos.dasha_planet,
                                combined
                            )
                        )
                        events.append(event)
            
            current_date += timedelta(days=1)
        
        # Sort by combined confidence (highest first)
        events.sort(key=lambda e: e.combined_confidence, reverse=True)
        return events
    
    
    def get_favorable_windows(
        self,
        birth_chart: Dict,
        start_date: datetime,
        end_date: datetime,
        event_type: str = 'Marriage'
    ) -> List[ActivationWindow]:
        """
        Find favorable windows for specific life events.
        
        Args:
            birth_chart: Birth chart data
            start_date: Analysis start
            end_date: Analysis end
            event_type: Type of event to find ('Marriage', 'Career', 'Health', etc)
        
        Returns:
            List of ActivationWindow sorted by strength
        """
        windows = []
        
        # Map event types to houses
        event_house_map = {
            'Marriage': [7],
            'Career': [10, 2, 6],
            'Health': [6, 8, 12],
            'Finance': [2, 11, 8],
            'Travel': [3, 9, 12],
            'Education': [5, 9],
            'Family': [4, 2],
            'Children': [5],
        }
        
        target_houses = event_house_map.get(event_type, list(range(1, 13)))
        
        # Get all transit events for these houses
        events = self.get_transit_activations(
            birth_chart,
            start_date,
            end_date,
            target_houses=target_houses,
            min_confidence=0.5
        )
        
        if not events:
            return windows
        
        # Group events into windows (consecutive high-confidence days)
        current_window = None
        favorable_count = 0
        
        for event in events:
            if current_window is None:
                current_window = {
                    'start': event.event_date,
                    'end': event.event_date,
                    'peak_confidence': event.combined_confidence,
                    'peak_date': event.event_date,
                    'planets': set([event.transiting_planet]),
                }
                favorable_count = 1 if event.combined_confidence >= 0.7 else 0
            else:
                # Check if event is close to window (within 30 days)
                days_diff = (event.event_date - current_window['end']).days
                
                if days_diff <= 30:
                    # Extend window
                    current_window['end'] = event.event_date
                    current_window['planets'].add(event.transiting_planet)
                    
                    if event.combined_confidence > current_window['peak_confidence']:
                        current_window['peak_confidence'] = event.combined_confidence
                        current_window['peak_date'] = event.event_date
                    
                    if event.combined_confidence >= 0.7:
                        favorable_count += 1
                else:
                    # End current window, start new one
                    if current_window and favorable_count > 0:
                        # Calculate duration_days inline
                        duration_days = (current_window['end'] - current_window['start']).days + 1
                        window = ActivationWindow(
                            start_date=current_window['start'],
                            end_date=current_window['end'],
                            duration_days=duration_days,
                            event_type=event_type,
                            key_planets=list(current_window['planets']),
                            favorable_days=favorable_count,
                            unfavorable_days=duration_days - favorable_count,
                            peak_date=current_window['peak_date'],
                            peak_confidence=current_window['peak_confidence']
                        )
                        windows.append(window)
                    
                    current_window = {
                        'start': event.event_date,
                        'end': event.event_date,
                        'peak_confidence': event.combined_confidence,
                        'peak_date': event.event_date,
                        'planets': set([event.transiting_planet]),
                    }
                    favorable_count = 1 if event.combined_confidence >= 0.7 else 0
        
        # Don't forget the last window
        if current_window and favorable_count > 0:
            window = ActivationWindow(
                start_date=current_window['start'],
                end_date=current_window['end'],
                duration_days=(current_window['end'] - current_window['start']).days + 1,
                event_type=event_type,
                key_planets=list(current_window['planets']),
                favorable_days=favorable_count,
                unfavorable_days=0,
                peak_date=current_window['peak_date'],
                peak_confidence=current_window['peak_confidence']
            )
            windows.append(window)
        
        # Sort by peak confidence (highest first)
        windows.sort(key=lambda w: w.peak_confidence, reverse=True)
        return windows
    
    
    def _get_transit_planet_at_date(self, date: datetime) -> str:
        """Get planets transiting at given date using real ephemeris data."""
        # Get all planet positions at this date
        all_planets = self.ephemeris.get_all_planets(date, tropical=False)
        
        # Find the planet with the most significant movement/position
        # Prioritize faster-moving planets which are more likely transiting
        planets_by_speed = sorted(
            all_planets.items(),
            key=lambda x: x[1].speed,
            reverse=True
        )
        
        # Return the fastest-moving planet (Moon most likely to be transiting)
        if planets_by_speed:
            return planets_by_speed[0][0]
        
        # Fallback to a default planet
        return 'Moon'
    
    
    def _calculate_kp_transit_confidence(
        self,
        transiting_planet: str,
        natal_significator: str,
        house: int,
        natal_planets: Dict
    ) -> float:
        """Calculate KP confidence when transiting planet enters significator."""
        confidence = 0.5  # Base confidence
        
        # Significator strength (natural significator = higher confidence)
        natural_significators = {
            1: 'Sun',
            2: 'Jupiter',
            3: 'Mercury',
            4: 'Moon',
            5: 'Sun',
            6: 'Mars',
            7: 'Venus',
            8: 'Saturn',
            9: 'Jupiter',
            10: 'Saturn',
            11: 'Jupiter',
            12: 'Saturn'
        }
        
        if natal_significator == natural_significators.get(house):
            confidence += 0.2
        
        # Transiting planet strength
        if transiting_planet in ['Jupiter', 'Venus']:
            confidence += 0.15
        elif transiting_planet in ['Saturn', 'Mars']:
            confidence += 0.10
        else:
            confidence += 0.05
        
        # Cap at 1.0
        return min(confidence, 1.0)
    
    
    def _calculate_dasha_support(
        self,
        dasha_planet: str,
        significator: str,
        house: int
    ) -> float:
        """Calculate how well current Dasha supports the event."""
        support = 0.5  # Base support
        
        # Dasha lord as significator = strong support
        if dasha_planet == significator:
            support += 0.3
        
        # Friendly relationships boost support
        friendly_pairs = {
            'Sun': ['Moon', 'Mars', 'Jupiter'],
            'Moon': ['Sun', 'Mercury'],
            'Mars': ['Sun', 'Moon', 'Jupiter'],
            'Mercury': ['Sun', 'Venus'],
            'Jupiter': ['Sun', 'Moon', 'Mars'],
            'Venus': ['Mercury', 'Saturn'],
            'Saturn': ['Mercury', 'Venus']
        }
        
        if significator in friendly_pairs.get(dasha_planet, []):
            support += 0.15
        
        # Cap at 1.0
        return min(support, 1.0)
    
    
    def _estimate_transit_duration(self, planet: str) -> int:
        """Estimate how long a transit typically lasts."""
        transit_durations = {
            'Sun': 30,
            'Mercury': 45,
            'Venus': 40,
            'Mars': 45,
            'Jupiter': 13,
            'Saturn': 2.5,
        }
        return int(transit_durations.get(planet, 30))
    
    
    def _classify_event_strength(self, confidence: float) -> str:
        """Classify event strength based on confidence."""
        if confidence >= 0.85:
            return 'Major'
        elif confidence >= 0.75:
            return 'Moderate'
        else:
            return 'Minor'
    
    
    def _generate_interpretation(
        self,
        significator: str,
        house: int,
        dasha_planet: str,
        confidence: float
    ) -> str:
        """Generate natural language interpretation of the transit."""
        house_names = {
            1: 'Self/Personality',
            2: 'Finance/Family',
            3: 'Communication',
            4: 'Home/Property',
            5: 'Children/Creativity',
            6: 'Health/Work',
            7: 'Marriage/Partnership',
            8: 'Crisis/Transformation',
            9: 'Fortune/Travel',
            10: 'Career/Status',
            11: 'Gains/Friendship',
            12: 'Loss/Spirituality'
        }
        
        strength_desc = self._classify_event_strength(confidence)
        
        return (f"{strength_desc} activation in {house_names.get(house, 'House')} "
                f"via {significator}. Current Dasha: {dasha_planet}. "
                f"Confidence: {confidence:.0%}")


def analyze_marriage_window(
    birth_chart: Dict,
    start_date: datetime = None,
    duration_months: int = 12
) -> ActivationWindow:
    """
    Convenience function: Analyze best marriage window.
    
    Args:
        birth_chart: Birth chart with planetary data
        start_date: When to begin analysis (default: today)
        duration_months: How far ahead to look
    
    Returns:
        Best ActivationWindow for marriage
    """
    analyzer = TransitAnalyzer()
    
    if start_date is None:
        start_date = datetime.now()
    
    end_date = start_date + timedelta(days=duration_months * 30)
    
    windows = analyzer.get_favorable_windows(
        birth_chart,
        start_date,
        end_date,
        event_type='Marriage'
    )
    
    return windows[0] if windows else None


def analyze_career_window(
    birth_chart: Dict,
    start_date: datetime = None,
    duration_months: int = 24
) -> ActivationWindow:
    """
    Convenience function: Analyze best career change window.
    """
    analyzer = TransitAnalyzer()
    
    if start_date is None:
        start_date = datetime.now()
    
    end_date = start_date + timedelta(days=duration_months * 30)
    
    windows = analyzer.get_favorable_windows(
        birth_chart,
        start_date,
        end_date,
        event_type='Career'
    )
    
    return windows[0] if windows else None
