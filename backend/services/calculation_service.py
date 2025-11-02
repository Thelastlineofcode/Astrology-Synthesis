"""
Calculation orchestration service.
Wraps all Phase 2 calculation engines (KP, Dasha, Transit, Ephemeris).
Implements the syncretic synthesis formula and data transformation.
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
from backend.schemas import BirthDataInput, PredictionEventData
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


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
            
            # Get ephemeris calculations
            planet_positions = self.ephemeris.get_planet_positions(
                birth_datetime,
                birth_data.latitude,
                birth_data.longitude
            )
            
            house_cusps = self.ephemeris.get_house_cusps(
                birth_datetime,
                birth_data.latitude,
                birth_data.longitude
            )
            
            ascendant = self.ephemeris.get_ascendant(
                birth_datetime,
                birth_data.latitude,
                birth_data.longitude
            )
            
            aspects = self.ephemeris.get_aspects(planet_positions)
            
            chart_data = {
                "planet_positions": planet_positions,
                "house_cusps": house_cusps,
                "ascendant": ascendant,
                "aspects": aspects,
            }
            
            logger.info(f"✅ Birth chart generated for {birth_data.location_name}")
            return chart_data
            
        except Exception as e:
            logger.error(f"❌ Birth chart generation failed: {str(e)}")
            raise
    
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
            prediction_window_days: Days to look ahead
            
        Returns:
            SyntheticPredictionResult with all analysis
        """
        import time
        start_time = time.time()
        
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
                raise ValueError("Moon position not found in birth chart")
            
            moon_longitude = moon_position["degree"] + moon_position["minutes"]/60 + moon_position["seconds"]/3600
            
            # Calculate prediction window
            prediction_start = datetime.utcnow()
            prediction_end = prediction_start + timedelta(days=prediction_window_days)
            
            # Initialize calculators
            dasha_calc = DashaCalculator(moon_longitude, birth_datetime_utc)
            transit_analyzer = TransitAnalyzer(birth_chart)
            
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
                dasha_calc, prediction_start, prediction_end
            )
            all_events.extend(dasha_events)
            dasha_score = sum(e.strength_score for e in dasha_events) / len(dasha_events) if dasha_events else 0.5
            
            # 3. Transit analysis
            transit_score = 0.0
            transit_events = self._analyze_transits(
                transit_analyzer, prediction_start, prediction_end
            )
            all_events.extend(transit_events)
            transit_score = sum(e.strength_score for e in transit_events) / len(transit_events) if transit_events else 0.5
            
            # Compute syncretic confidence
            confidence_score = (kp_score * 0.6) + (dasha_score * 0.4)
            
            # Sort events by date
            all_events.sort(key=lambda e: e.event_date)
            
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
            # Get significators for houses
            for house_num in range(1, 13):
                significators = get_significators_for_house(house_num, birth_chart)
                
                if significators:
                    event = PredictionEventData(
                        event_type="kp_significator",
                        event_date=start_date + timedelta(days=house_num * 3),
                        event_window_start=start_date,
                        event_window_end=end_date,
                        primary_planet=significators[0] if significators else None,
                        secondary_planet=significators[1] if len(significators) > 1 else None,
                        strength_score=0.6,
                        influence_area=self._get_house_influence(house_num),
                        description=f"KP House {house_num} activations",
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
    ) -> List[PredictionEventData]:
        """Analyze Dasha system for prediction events."""
        events = []
        
        try:
            # Get dasha timeline
            timeline = dasha_calc.get_dasha_timeline(start_date, end_date)
            
            for dasha_info in timeline:
                event = PredictionEventData(
                    event_type="dasha_change",
                    event_date=dasha_info.get("start_date", start_date),
                    event_window_start=dasha_info.get("start_date", start_date),
                    event_window_end=dasha_info.get("end_date", end_date),
                    primary_planet=dasha_info.get("mahadasha_planet"),
                    secondary_planet=dasha_info.get("antardasha_planet"),
                    strength_score=0.75,
                    influence_area="Overall life",
                    description=f"Dasha period: {dasha_info.get('mahadasha_planet', 'Unknown')} "
                                f"→ {dasha_info.get('antardasha_planet', 'Unknown')}",
                    recommendation="Leverage dasha energies for major life decisions"
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
        start_date: datetime,
        end_date: datetime,
    ) -> List[PredictionEventData]:
        """Analyze transits for prediction events."""
        events = []
        
        try:
            # Get transit windows
            windows = transit_analyzer.get_favorable_windows(start_date, end_date)
            
            for window in windows:
                event = PredictionEventData(
                    event_type="transit_window",
                    event_date=window.get("start_date", start_date),
                    event_window_start=window.get("start_date", start_date),
                    event_window_end=window.get("end_date", end_date),
                    primary_planet=window.get("planet"),
                    strength_score=window.get("strength", 0.5),
                    influence_area=window.get("area", "General"),
                    description=f"Transit window: {window.get('description', 'Favorable period')}",
                    recommendation=window.get("recommendation", "Take action during this window")
                )
                events.append(event)
            
            logger.info(f"✅ Transit analysis complete: {len(events)} windows identified")
            return events
            
        except Exception as e:
            logger.error(f"❌ Transit analysis failed: {str(e)}")
            return []
    
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
