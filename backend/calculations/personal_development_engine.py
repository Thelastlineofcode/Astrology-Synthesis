"""
Flexible Personal Development Insights Engine

A coaching-focused tool that provides astrological and numerological insights
for personal development, team dynamics, and wellness programs.

IMPORTANT DISCLAIMER:
This tool is designed for personal development, coaching, and team building.
It is NOT intended for hiring, promotion, or employment decisions.
It is NOT scientifically validated and should not be used for employee evaluation.

Strategic Positioning:
- Personal development coaching tool
- Team dynamics and trust-building
- Self-awareness and wellness integration
- Conversation starter for coaching relationships

Privacy-First Design:
- All data encrypted
- User consent required
- No HRIS integration by default
- Results visible only to user (unless explicitly shared)
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DataCompleteness(Enum):
    """Level of birth data completeness."""
    DATE_ONLY = "date_only"  # Just birth date
    DATE_AND_TIME = "date_and_time"  # Date and time, no location
    FULL_DATA = "full_data"  # Date, time, and location


@dataclass
class FlexibleBirthData:
    """
    Flexible birth data structure that works with partial information.

    Supports three levels of completeness:
    1. DATE_ONLY: Just birth date (numerology only)
    2. DATE_AND_TIME: Date and time (numerology + partial astrology)
    3. FULL_DATA: Complete data (full numerology + astrology)
    """

    # Always required
    birth_date: date

    # Optional fields
    birth_time: Optional[str] = None  # HH:MM:SS format
    birth_location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None

    # Personal information (optional, for numerology)
    full_name: Optional[str] = None

    # Metadata
    completeness: DataCompleteness = DataCompleteness.DATE_ONLY

    def __post_init__(self):
        """Determine data completeness level."""
        if self.birth_time and self.latitude and self.longitude:
            self.completeness = DataCompleteness.FULL_DATA
        elif self.birth_time:
            self.completeness = DataCompleteness.DATE_AND_TIME
        else:
            self.completeness = DataCompleteness.DATE_ONLY

    def has_full_astrology_data(self) -> bool:
        """Check if we have enough data for full astrological chart."""
        return self.completeness == DataCompleteness.FULL_DATA

    def has_time_data(self) -> bool:
        """Check if we have birth time."""
        return self.birth_time is not None

    def has_name_data(self) -> bool:
        """Check if we have name for numerology."""
        return self.full_name is not None

    def get_available_analyses(self) -> List[str]:
        """Get list of possible analyses based on available data."""
        analyses = ["life_path_number", "day_of_week_insights"]

        if self.has_name_data():
            analyses.extend([
                "destiny_number",
                "soul_urge_number",
                "personality_number",
            ])

        if self.has_time_data():
            analyses.extend([
                "sun_sign",
                "moon_phase",
            ])

        if self.has_full_astrology_data():
            analyses.extend([
                "rising_sign",
                "moon_sign",
                "planetary_positions",
                "house_positions",
                "full_birth_chart",
            ])

        return analyses


@dataclass
class PersonalDevelopmentReading:
    """
    Personal development insights based on available birth data.

    Explicitly NOT an assessment or evaluation tool.
    For coaching, self-reflection, and personal growth only.
    """

    # Metadata
    data_completeness: DataCompleteness
    available_analyses: List[str]

    # Numerology insights (always available with birth date)
    life_path_number: Optional[int] = None
    life_path_interpretation: Optional[str] = None

    day_of_week: Optional[str] = None
    day_of_week_insights: Optional[str] = None

    # Name-based numerology (if name provided)
    destiny_number: Optional[int] = None
    destiny_interpretation: Optional[str] = None

    soul_urge_number: Optional[int] = None
    soul_urge_interpretation: Optional[str] = None

    personality_number: Optional[int] = None
    personality_interpretation: Optional[str] = None

    # Astrology insights (if time/location provided)
    sun_sign: Optional[str] = None
    sun_sign_interpretation: Optional[str] = None

    moon_sign: Optional[str] = None
    moon_sign_interpretation: Optional[str] = None

    rising_sign: Optional[str] = None
    rising_sign_interpretation: Optional[str] = None

    # Synthesis and coaching prompts
    strengths_themes: List[str] = None
    growth_opportunities: List[str] = None
    communication_style: Optional[str] = None
    work_style_insights: Optional[str] = None

    # Coaching conversation starters
    reflection_prompts: List[str] = None

    # Disclaimer
    disclaimer: str = (
        "This reading is for personal development and self-reflection purposes only. "
        "It is not a scientific assessment and should not be used for employment decisions, "
        "hiring, promotion, or employee evaluation. Results are meant to inspire "
        "self-awareness and facilitate coaching conversations."
    )

    def __post_init__(self):
        """Initialize default values."""
        if self.strengths_themes is None:
            self.strengths_themes = []
        if self.growth_opportunities is None:
            self.growth_opportunities = []
        if self.reflection_prompts is None:
            self.reflection_prompts = []


class FlexibleInsightsEngine:
    """
    Main engine for generating personal development insights.

    Adapts to available data and provides appropriate level of analysis.
    """

    def __init__(self):
        """Initialize the insights engine."""
        logger.info("FlexibleInsightsEngine initialized (Coaching Tool - Not for Employment Decisions)")

    def generate_reading(
        self,
        birth_data: FlexibleBirthData,
        include_coaching_prompts: bool = True,
    ) -> PersonalDevelopmentReading:
        """
        Generate personal development reading based on available data.

        Args:
            birth_data: Flexible birth data (any completeness level)
            include_coaching_prompts: Include coaching conversation prompts

        Returns:
            PersonalDevelopmentReading with insights based on available data
        """
        logger.info(
            f"Generating reading with {birth_data.completeness.value} data completeness"
        )

        reading = PersonalDevelopmentReading(
            data_completeness=birth_data.completeness,
            available_analyses=birth_data.get_available_analyses(),
        )

        # Always calculate numerology from birth date
        self._add_date_numerology(birth_data, reading)

        # Add name numerology if available
        if birth_data.has_name_data():
            self._add_name_numerology(birth_data, reading)

        # Add basic astrology if time available
        if birth_data.has_time_data():
            self._add_time_based_astrology(birth_data, reading)

        # Add full astrology if complete data available
        if birth_data.has_full_astrology_data():
            self._add_full_astrology(birth_data, reading)

        # Generate synthesis and coaching prompts
        self._synthesize_insights(reading)

        if include_coaching_prompts:
            self._generate_coaching_prompts(reading)

        return reading

    def _add_date_numerology(
        self,
        birth_data: FlexibleBirthData,
        reading: PersonalDevelopmentReading,
    ) -> None:
        """Add numerology based on birth date."""
        from backend.calculations.numerology_engine import NumerologyCalculator

        calc = NumerologyCalculator()

        # Life path number
        life_path = calc.calculate_life_path_number(birth_data.birth_date)
        reading.life_path_number = life_path
        reading.life_path_interpretation = calc.interpret_life_path_number(life_path)

        # Day of week insights
        day_name = birth_data.birth_date.strftime("%A")
        reading.day_of_week = day_name
        reading.day_of_week_insights = calc.interpret_day_of_week(day_name)

    def _add_name_numerology(
        self,
        birth_data: FlexibleBirthData,
        reading: PersonalDevelopmentReading,
    ) -> None:
        """Add numerology based on name."""
        from backend.calculations.numerology_engine import NumerologyCalculator

        calc = NumerologyCalculator()
        name = birth_data.full_name

        # Destiny number
        destiny = calc.calculate_destiny_number(name)
        reading.destiny_number = destiny
        reading.destiny_interpretation = calc.interpret_destiny_number(destiny)

        # Soul urge number
        soul_urge = calc.calculate_soul_urge_number(name)
        reading.soul_urge_number = soul_urge
        reading.soul_urge_interpretation = calc.interpret_soul_urge_number(soul_urge)

        # Personality number
        personality = calc.calculate_personality_number(name)
        reading.personality_number = personality
        reading.personality_interpretation = calc.interpret_personality_number(personality)

    def _add_time_based_astrology(
        self,
        birth_data: FlexibleBirthData,
        reading: PersonalDevelopmentReading,
    ) -> None:
        """Add astrology that only requires date and time."""
        # Sun sign (only needs date)
        reading.sun_sign = self._calculate_sun_sign(birth_data.birth_date)
        reading.sun_sign_interpretation = self._interpret_sun_sign(reading.sun_sign)

    def _add_full_astrology(
        self,
        birth_data: FlexibleBirthData,
        reading: PersonalDevelopmentReading,
    ) -> None:
        """Add full astrological analysis."""
        from backend.services.calculation_service import CalculationService
        from backend.schemas import BirthDataInput

        # Generate full birth chart
        calc_service = CalculationService()

        birth_input = BirthDataInput(
            date=birth_data.birth_date.isoformat(),
            time=birth_data.birth_time,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone,
            location_name=birth_data.birth_location or "",
        )

        try:
            chart = calc_service.generate_birth_chart(birth_input)

            # Extract key placements
            planets = chart.get("planet_positions", [])

            # Sun sign (already have it, but get interpretation)
            sun = next((p for p in planets if p["planet"] == "Sun"), None)
            if sun:
                reading.sun_sign = sun["sign"]
                reading.sun_sign_interpretation = self._interpret_sun_sign(sun["sign"])

            # Moon sign
            moon = next((p for p in planets if p["planet"] == "Moon"), None)
            if moon:
                reading.moon_sign = moon["sign"]
                reading.moon_sign_interpretation = self._interpret_moon_sign(moon["sign"])

            # Rising sign (Ascendant)
            asc = chart.get("ascendant", {})
            if asc:
                reading.rising_sign = asc.get("zodiac_sign")
                reading.rising_sign_interpretation = self._interpret_rising_sign(
                    reading.rising_sign
                )

        except Exception as e:
            logger.warning(f"Could not generate full astrology: {str(e)}")

    def _synthesize_insights(self, reading: PersonalDevelopmentReading) -> None:
        """Synthesize insights into strengths and growth themes."""
        strengths = []
        growth = []

        # Based on life path number
        if reading.life_path_number:
            if reading.life_path_number in [1, 3, 5]:
                strengths.append("Natural creativity and innovation")
            if reading.life_path_number in [2, 6, 9]:
                strengths.append("Strong empathy and collaboration skills")
            if reading.life_path_number in [4, 8]:
                strengths.append("Organizational and leadership abilities")

        # Based on sun sign (if available)
        if reading.sun_sign:
            fire_signs = ["Aries", "Leo", "Sagittarius"]
            earth_signs = ["Taurus", "Virgo", "Capricorn"]
            air_signs = ["Gemini", "Libra", "Aquarius"]
            water_signs = ["Cancer", "Scorpio", "Pisces"]

            if reading.sun_sign in fire_signs:
                strengths.append("Enthusiastic and action-oriented")
                growth.append("Developing patience and listening skills")
            elif reading.sun_sign in earth_signs:
                strengths.append("Practical and reliable")
                growth.append("Embracing flexibility and change")
            elif reading.sun_sign in air_signs:
                strengths.append("Excellent communicator and networker")
                growth.append("Connecting ideas to action")
            elif reading.sun_sign in water_signs:
                strengths.append("Emotionally intelligent and intuitive")
                growth.append("Setting healthy boundaries")

        reading.strengths_themes = strengths if strengths else [
            "Unique personal strengths to discover through self-reflection"
        ]
        reading.growth_opportunities = growth if growth else [
            "Growth opportunities to explore with coaching support"
        ]

    def _generate_coaching_prompts(self, reading: PersonalDevelopmentReading) -> None:
        """Generate coaching conversation starters."""
        prompts = [
            "What patterns in your work style resonate with your numerological insights?",
            "How do your natural strengths show up in your daily interactions?",
        ]

        if reading.life_path_number:
            prompts.append(
                f"Your life path number {reading.life_path_number} suggests certain tendencies. "
                "How have you seen these manifest in your career choices?"
            )

        if reading.sun_sign:
            prompts.append(
                f"As a {reading.sun_sign}, how do you approach challenges and collaboration?"
            )

        if reading.destiny_number:
            prompts.append(
                "What aspects of your name's numerology align with your life purpose?"
            )

        reading.reflection_prompts = prompts

    def _calculate_sun_sign(self, birth_date: date) -> str:
        """Calculate sun sign from date."""
        month = birth_date.month
        day = birth_date.day

        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        else:
            return "Pisces"

    def _interpret_sun_sign(self, sign: str) -> str:
        """Get sun sign interpretation for personal development."""
        interpretations = {
            "Aries": "Natural leadership and initiative; thrives in dynamic environments",
            "Taurus": "Steady and reliable; excels in building sustainable systems",
            "Gemini": "Versatile communicator; brings fresh perspectives to teams",
            "Cancer": "Nurturing team player; creates supportive work environments",
            "Leo": "Confident and inspiring; motivates others through enthusiasm",
            "Virgo": "Detail-oriented problem solver; improves processes through analysis",
            "Libra": "Diplomatic collaborator; builds bridges and finds balance",
            "Scorpio": "Intense and transformative; drives deep organizational change",
            "Sagittarius": "Visionary explorer; brings optimism and big-picture thinking",
            "Capricorn": "Strategic planner; achieves long-term goals through discipline",
            "Aquarius": "Innovative thinker; challenges status quo with unique ideas",
            "Pisces": "Empathetic connector; understands unspoken team dynamics",
        }
        return interpretations.get(sign, "Unique strengths to explore")

    def _interpret_moon_sign(self, sign: str) -> str:
        """Get moon sign interpretation."""
        return f"Emotional style and inner needs reflected through {sign} energy"

    def _interpret_rising_sign(self, sign: str) -> str:
        """Get rising sign interpretation."""
        return f"First impression and approach to new situations through {sign} lens"
