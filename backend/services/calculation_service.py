"""
Calculation orchestration service.
Wraps all Phase 2 calculation engines (KP, Dasha, Transit, Ephemeris).
Implements the syncretic synthesis formula and data transformation.
Integrates UnifiedInterpreter for multi-tradition interpretations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from backend.calculations.kp_engine import (
    get_significators_for_house,
    get_sub_lord,
    get_ruling_planets,
)
from backend.calculations.dasha_engine import DashaCalculator
from backend.calculations.transit_engine import TransitAnalyzer
from backend.calculations.ephemeris import EphemerisCalculator
from backend.calculations.unified_interpreter import UnifiedInterpreter
from backend.calculations.exceptions import (
    InvalidPredictionWindowError,
    InvalidBirthDataError,
    CalculationError
)
from backend.schemas import BirthDataInput, PredictionEventData
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Constants for validation
MAX_PREDICTION_WINDOW_DAYS = 365
MIN_PREDICTION_WINDOW_DAYS = 1

# Calculation constants
NAKSHATRA_LENGTH_DEGREES = 13.333333  # 13°20' = 13.333333 degrees
PADA_LENGTH_DEGREES = 3.333333  # Each nakshatra divided into 4 padas
DEGREES_PER_SIGN = 30.0  # Zodiac sign length

# Synthesis formula weights
KP_WEIGHT = 0.6
DASHA_WEIGHT = 0.4


@dataclass
class SyntheticPredictionResult:
    """Result from syncretic prediction synthesis."""
    
    events: List[PredictionEventData]
    confidence_score: float
    kp_contribution: float
    dasha_contribution: float
    transit_contribution: float
    calculation_time_ms: float


class CalculationService:
    """Service for orchestrating all calculation engines."""
    
    def __init__(self):
        """Initialize calculation service."""
        self.ephemeris = EphemerisCalculator()
        self.interpreter = UnifiedInterpreter()
    
    def generate_birth_chart(self, birth_data: BirthDataInput) -> Dict[str, Any]:
        """
        Generate a complete birth chart using Swiss Ephemeris.
        
        Args:
            birth_data: Birth data (date, time, location)
            
        Returns:
            Dictionary containing all chart data
        """
        try:
            import pytz
            from datetime import datetime as dt
            
            # Parse birth data
            birth_date_str = f"{birth_data.date} {birth_data.time}"
            tz = pytz.timezone(birth_data.timezone)
            birth_datetime = dt.strptime(birth_date_str, "%Y-%m-%d %H:%M:%S")
            birth_datetime = tz.localize(birth_datetime)
            # Convert to UTC
            birth_datetime_utc = birth_datetime.astimezone(pytz.UTC)
            
            # Get all planetary positions
            planets = self.ephemeris.get_all_planets(birth_datetime_utc, tropical=False)
            
            # Get house cusps
            house_cusps = self.ephemeris.get_house_cusps(
                birth_datetime_utc,
                birth_data.latitude,
                birth_data.longitude
            )
            
            # Format planet positions for consistency
            planet_positions = []
            for planet_name, position in planets.items():
                degree, minutes, seconds = self._degree_to_dms(position.longitude)
                house_num = self._get_planet_house(position.longitude, house_cusps)
                
                # Calculate pada (1-4) from degree in nakshatra
                # Each nakshatra is 13°20', divided into 4 padas of 3°20' each
                nakshatra_degree = position.degree_in_sign % NAKSHATRA_LENGTH_DEGREES
                pada = int(nakshatra_degree / PADA_LENGTH_DEGREES) + 1
                
                planet_positions.append({
                    "planet": planet_name,
                    "degree": degree,
                    "minutes": minutes,
                    "seconds": seconds,
                    "house": house_num,
                    "zodiac_sign": self._get_zodiac_sign(position.longitude),
                    "zodiac_degree": self._get_zodiac_degree(position.longitude),
                    "longitude": position.longitude,
                    "latitude": position.latitude,
                    "sign": position.sign,
                    "degree_in_sign": position.degree_in_sign,
                    "retrograde": position.is_retrograde,
                    "nakshatra": position.nakshatra,
                    "pada": pada,
                })
            
            # Format house cusps as a list of 12 houses
            houses_list = []
            for i in range(12):
                degree, minutes, seconds = self._degree_to_dms(house_cusps.cusps[i])
                houses_list.append({
                    "house": i + 1,
                    "degree": degree,
                    "minutes": minutes,
                    "seconds": seconds,
                    "zodiac_sign": self._get_zodiac_sign(house_cusps.cusps[i]),
                    "zodiac_degree": self._get_zodiac_degree(house_cusps.cusps[i]),
                    "cusp": house_cusps.cusps[i],
                    "longitude": house_cusps.cusps[i],
                })
            
            chart_data = {
                "planet_positions": planet_positions,
                "house_cusps": houses_list,
                "ascendant": {
                    "degree": house_cusps.ascendant,
                    "zodiac_sign": self._get_zodiac_sign(house_cusps.ascendant),
                    "zodiac_degree": self._get_zodiac_degree(house_cusps.ascendant),
                },
                "midheaven": {
                    "degree": house_cusps.midheaven,
                    "zodiac_sign": self._get_zodiac_sign(house_cusps.midheaven),
                    "zodiac_degree": self._get_zodiac_degree(house_cusps.midheaven),
                },
                "timezone": birth_data.timezone,
                "latitude": birth_data.latitude,
                "longitude": birth_data.longitude,
                "aspects": self._calculate_aspects(planets),
            }
            
            logger.info(f"✅ Birth chart generated for {birth_data.location_name}")
            return chart_data
            
        except Exception as e:
            logger.error(f"❌ Birth chart generation failed: {str(e)}")
            raise
    
    def _calculate_aspects(self, planets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculate major aspects between planets.
        
        Args:
            planets: Dictionary of planet positions
            
        Returns:
            List of aspect data
        """
        aspects = []
        aspect_types = {
            0: {"name": "Conjunction", "orb": 8},
            60: {"name": "Sextile", "orb": 6},
            90: {"name": "Square", "orb": 8},
            120: {"name": "Trine", "orb": 8},
            180: {"name": "Opposition", "orb": 8},
        }
        
        planet_list = list(planets.items())
        for i in range(len(planet_list)):
            for j in range(i + 1, len(planet_list)):
                name1, pos1 = planet_list[i]
                name2, pos2 = planet_list[j]
                
                # Calculate angular distance
                diff = abs(pos1.longitude - pos2.longitude)
                if diff > 180:
                    diff = 360 - diff
                
                # Check against known aspects
                for aspect_angle, aspect_info in aspect_types.items():
                    orb = aspect_info["orb"]
                    if abs(diff - aspect_angle) <= orb:
                        orb_diff = abs(diff - aspect_angle)
                        aspects.append({
                            "planet1": name1,
                            "planet2": name2,
                            "aspect_type": aspect_info["name"],
                            "angle": diff,
                            "orb": orb_diff,
                            "is_exact": orb_diff < 1.0,
                        })
                        break
        
        return aspects
    
    def get_syncretic_prediction(
        self,
        birth_data: BirthDataInput,
        query: str,
        prediction_window_days: int = 30,
    ) -> SyntheticPredictionResult:
        """
        Generate comprehensive syncretic prediction combining KP, Dasha, and Transit.

        Synthesis Formula: (KP × 0.6) + (Dasha × 0.4)

        Args:
            birth_data: Birth data
            query: User's prediction query
            prediction_window_days: Days to look ahead (max 365)

        Returns:
            SyntheticPredictionResult with all analysis

        Raises:
            InvalidPredictionWindowError: If prediction_window_days is out of valid range
            InvalidBirthDataError: If birth data is incomplete or invalid
            CalculationError: If calculation fails
        """
        import time
        start_time = time.time()

        # Validate input parameters
        if prediction_window_days < MIN_PREDICTION_WINDOW_DAYS:
            raise InvalidPredictionWindowError(
                f"Prediction window must be at least {MIN_PREDICTION_WINDOW_DAYS} day(s)"
            )
        if prediction_window_days > MAX_PREDICTION_WINDOW_DAYS:
            raise InvalidPredictionWindowError(
                f"Prediction window cannot exceed {MAX_PREDICTION_WINDOW_DAYS} days"
            )

        try:
            import pytz
            from datetime import datetime as dt
            
            # Parse birth data
            birth_date_str = f"{birth_data.date} {birth_data.time}"
            tz = pytz.timezone(birth_data.timezone)
            birth_datetime = dt.strptime(birth_date_str, "%Y-%m-%d %H:%M:%S")
            birth_datetime = tz.localize(birth_datetime)
            
            # Convert to UTC for calculations
            birth_datetime_utc = birth_datetime.astimezone(pytz.UTC)
            
            # Get birth chart for moon position (required for dasha)
            birth_chart = self.generate_birth_chart(birth_data)
            moon_position = next(
                (p for p in birth_chart["planet_positions"] if p["planet"] == "Moon"),
                None
            )
            
            if not moon_position:
                raise InvalidBirthDataError("Moon position not found in birth chart")

            # Use the pre-calculated longitude directly (0-360 degrees)
            moon_longitude = moon_position["longitude"]
            
            # Calculate prediction window (timezone-aware UTC)
            prediction_start = datetime.now(pytz.UTC)
            prediction_end = prediction_start + timedelta(days=prediction_window_days)
            
            # Initialize calculators
            dasha_calc = DashaCalculator()
            transit_analyzer = TransitAnalyzer()
            
            # Collect all events
            all_events: List[PredictionEventData] = []
            
            # 1. KP System analysis
            kp_score = 0.0
            kp_events = self._analyze_kp_system(
                birth_chart, prediction_start, prediction_end
            )
            all_events.extend(kp_events)
            kp_score = sum(e.strength_score for e in kp_events) / len(kp_events) if kp_events else 0.5
            
            # 2. Dasha System analysis
            dasha_score = 0.0
            dasha_events = self._analyze_dasha_system(
                dasha_calc, prediction_start, prediction_end, birth_datetime_utc
            )
            all_events.extend(dasha_events)
            dasha_score = sum(e.strength_score for e in dasha_events) / len(dasha_events) if dasha_events else 0.5
            
            # 3. Transit analysis
            transit_score = 0.0
            transit_events = self._analyze_transits(
                transit_analyzer, birth_chart, prediction_start, prediction_end
            )
            all_events.extend(transit_events)
            transit_score = sum(e.strength_score for e in transit_events) / len(transit_events) if transit_events else 0.5
            
            # Compute syncretic confidence using weighted formula
            confidence_score = (kp_score * KP_WEIGHT) + (dasha_score * DASHA_WEIGHT)
            
            # Sort events by date
            all_events.sort(key=lambda e: e.event_date)
            
            # Enrich events with unified interpretations
            all_events = self._enrich_events_with_interpretations(all_events, birth_chart)
            
            calculation_time = (time.time() - start_time) * 1000  # Convert to ms
            
            result = SyntheticPredictionResult(
                events=all_events,
                confidence_score=min(confidence_score, 1.0),  # Cap at 1.0
                kp_contribution=kp_score,
                dasha_contribution=dasha_score,
                transit_contribution=transit_score,
                calculation_time_ms=calculation_time,
            )
            
            logger.info(f"✅ Syncretic prediction generated (confidence: {confidence_score:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Prediction generation failed: {str(e)}")
            raise
    
    def _analyze_kp_system(
        self,
        birth_chart: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
    ) -> List[PredictionEventData]:
        """Analyze KP system for prediction events."""
        events = []
        
        try:
            # Extract planets dict for KP analysis
            planets_dict = {}
            for planet_data in birth_chart.get("planet_positions", []):
                planets_dict[planet_data["planet"]] = {
                    "longitude": planet_data["longitude"],
                    "house": planet_data["house"],
                    "sign": planet_data["sign"],
                    "degree_in_sign": planet_data["degree_in_sign"],
                }
            
            # Extract house cusps as list of longitudes
            house_cusps = [house["cusp"] for house in birth_chart.get("house_cusps", [])]
            
            # Get significators for houses
            for house_num in range(1, 13):
                significators = get_significators_for_house(house_num, planets_dict, house_cusps)
                
                if significators:
                    # Extract planet names from Significator objects
                    primary = significators[0].planet if significators else None
                    secondary = significators[1].planet if len(significators) > 1 else None
                    
                    event = PredictionEventData(
                        event_type="kp_significator",
                        event_date=start_date + timedelta(days=house_num * 3),
                        event_window_start=start_date,
                        event_window_end=end_date,
                        primary_planet=primary,
                        secondary_planet=secondary,
                        strength_score=significators[0].strength if significators else 0.6,
                        influence_area=self._get_house_influence(house_num),
                        description=f"KP House {house_num}: {significators[0].reason if significators else 'Active'}",
                        recommendation="Monitor planetary transits"
                    )
                    events.append(event)
            
            logger.info(f"✅ KP analysis complete: {len(events)} events identified")
            return events
            
        except Exception as e:
            logger.error(f"❌ KP analysis failed: {str(e)}")
            return []
    
    def _analyze_dasha_system(
        self,
        dasha_calc: DashaCalculator,
        start_date: datetime,
        end_date: datetime,
        birth_date: datetime,
    ) -> List[PredictionEventData]:
        """Analyze Dasha system for prediction events."""
        events = []
        
        try:
            # Calculate years forward from birth to end_date
            years_forward = max(2, int((end_date - birth_date).days / 365.25) + 1)
            
            # Get dasha timeline
            timeline = dasha_calc.get_dasha_timeline(birth_date, years_forward)
            
            for dasha_phase in timeline:
                # Only include periods within our prediction window
                if dasha_phase.start_date > end_date:
                    continue
                if dasha_phase.end_date < start_date:
                    continue
                    
                event = PredictionEventData(
                    event_type="dasha_change",
                    event_date=dasha_phase.start_date,
                    event_window_start=dasha_phase.start_date,
                    event_window_end=dasha_phase.end_date,
                    primary_planet=dasha_phase.planet,
                    secondary_planet=None,
                    strength_score=0.75,
                    influence_area="Overall life",
                    description=f"Mahadasha period: {dasha_phase.planet}",
                    recommendation=f"Leverage {dasha_phase.planet} energies for major life decisions"
                )
                events.append(event)
            
            logger.info(f"✅ Dasha analysis complete: {len(events)} periods identified")
            return events
            
        except Exception as e:
            logger.error(f"❌ Dasha analysis failed: {str(e)}")
            return []
    
    def _analyze_transits(
        self,
        transit_analyzer: TransitAnalyzer,
        birth_chart: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
    ) -> List[PredictionEventData]:
        """Analyze transits for prediction events."""
        events = []
        
        try:
            # Get transit windows (returns ActivationWindow dataclass objects)
            windows = transit_analyzer.get_favorable_windows(
                birth_chart, start_date, end_date
            )
            
            for window in windows:
                # Extract primary planet from key_planets list
                primary_planet = window.key_planets[0] if window.key_planets else None
                
                event = PredictionEventData(
                    event_type="transit_window",
                    event_date=window.peak_date,
                    event_window_start=window.start_date,
                    event_window_end=window.end_date,
                    primary_planet=primary_planet,
                    strength_score=window.peak_confidence,
                    influence_area=window.event_type,
                    description=f"Transit window for {window.event_type}: {window.favorable_days} favorable days",
                    recommendation=f"Peak activation on {window.peak_date.strftime('%Y-%m-%d')}"
                )
                events.append(event)
            
            logger.info(f"✅ Transit analysis complete: {len(events)} windows identified")
            return events
            
        except Exception as e:
            logger.error(f"❌ Transit analysis failed: {str(e)}")
            return []
    
    def _enrich_events_with_interpretations(
        self,
        events: List[PredictionEventData],
        birth_chart: Dict[str, Any],
    ) -> List[PredictionEventData]:
        """
        Enrich prediction events with unified multi-tradition interpretations.
        
        This is the proprietary system - weaves Vedic, Western, Voodoo, 
        Mysticism, and Lunar Mansions into single unified interpretations.
        """
        enriched_events = []
        
        for event in events:
            try:
                # Get planet data from birth chart
                planet_data = None
                if event.primary_planet:
                    planet_data = next(
                        (p for p in birth_chart.get("planet_positions", [])
                         if p["planet"] == event.primary_planet),
                        None
                    )
                
                if planet_data:
                    # Generate unified interpretation
                    interpretation = self.interpreter.interpret_event(
                        event_type=event.event_type,
                        primary_planet=event.primary_planet,
                        secondary_planet=event.secondary_planet,
                        planet_sign=planet_data.get("sign"),
                        planet_house=planet_data.get("house"),
                        planet_nakshatra=planet_data.get("nakshatra"),
                        event_date=event.event_date,
                        strength_score=event.strength_score,
                    )
                    
                    # Update event with interpretation
                    event.description = interpretation.get("description", event.description)
                    event.recommendation = interpretation.get("recommendation", event.recommendation)
                    
                    # Add interpretation details if available
                    if hasattr(event, 'interpretation_details'):
                        event.interpretation_details = interpretation.get("details", {})
                
                enriched_events.append(event)
                
            except Exception as e:
                logger.warning(f"⚠️ Failed to interpret event: {str(e)}")
                enriched_events.append(event)  # Keep original event
        
        logger.info(f"✅ Enriched {len(enriched_events)} events with unified interpretations")
        return enriched_events
    
    @staticmethod
    def _get_house_influence(house_number: int) -> str:
        """Get the life area influenced by a house."""
        house_influences = {
            1: "Self & Personality",
            2: "Finance & Family",
            3: "Communication & Siblings",
            4: "Home & Mother",
            5: "Creativity & Children",
            6: "Health & Work",
            7: "Relationships & Marriage",
            8: "Transformation & Legacy",
            9: "Spirituality & Travel",
            10: "Career & Status",
            11: "Friendships & Goals",
            12: "Spirituality & Endings",
        }
        return house_influences.get(house_number, "General Life Area")
    
    @staticmethod
    def _degree_to_dms(degree: float) -> tuple:
        """Convert decimal degree to degree, minutes, seconds."""
        d = int(degree)
        m = int((degree - d) * 60)
        s = ((degree - d) * 60 - m) * 60
        return d, m, s
    
    @staticmethod
    def _get_zodiac_sign(degree: float) -> str:
        """Get zodiac sign from ecliptic degree (0-360)."""
        zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        sign_index = int(degree / DEGREES_PER_SIGN)
        return zodiac_signs[min(sign_index, 11)]

    @staticmethod
    def _get_zodiac_degree(degree: float) -> float:
        """Get degree within zodiac sign (0-30)."""
        return degree % DEGREES_PER_SIGN
    
    @staticmethod
    def _get_planet_house(planet_degree: float, house_cusps) -> int:
        """Determine which house a planet is in based on its degree."""
        # house_cusps.cusps already contains 12 cusps, with cusps[0] being the ascendant
        cusps = house_cusps.cusps
        for i in range(12):
            cusp1 = cusps[i]
            cusp2 = cusps[(i + 1) % 12]

            # Handle the wrap-around at 360/0
            if cusp1 <= cusp2:
                if cusp1 <= planet_degree < cusp2:
                    return i + 1
            else:  # wrap-around
                if planet_degree >= cusp1 or planet_degree < cusp2:
                    return i + 1

        return 1  # default to house 1
