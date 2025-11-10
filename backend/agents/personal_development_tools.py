"""
LangChain tools for personal development agents.

Provides tools for numerology, flexible astrology, and team dynamics.
"""

from typing import Optional, Dict, Any, List
from langchain.tools import Tool, StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


# Tool input schemas
class PersonalReadingInput(BaseModel):
    """Input schema for personal development reading."""
    birth_date: str = Field(description="Birth date in YYYY-MM-DD format")
    full_name: Optional[str] = Field(default=None, description="Full birth name (optional)")
    birth_time: Optional[str] = Field(default=None, description="Birth time HH:MM:SS (optional)")
    latitude: Optional[float] = Field(default=None, description="Birth latitude (optional)")
    longitude: Optional[float] = Field(default=None, description="Birth longitude (optional)")
    timezone: Optional[str] = Field(default=None, description="Timezone (optional)")


class NumerologyInput(BaseModel):
    """Input schema for numerology calculation."""
    birth_date: str = Field(description="Birth date in YYYY-MM-DD format")
    full_name: Optional[str] = Field(default=None, description="Full birth name (optional)")


class TeamAnalysisInput(BaseModel):
    """Input schema for team analysis."""
    team_name: str = Field(description="Name of the team")
    # Note: Team members data would be passed separately


# Tool implementations
def _get_personal_development_reading(
    birth_date: str,
    full_name: Optional[str] = None,
    birth_time: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    timezone: Optional[str] = None,
) -> str:
    """
    Generate personal development reading based on available data.

    Adapts to whatever level of data is provided.

    Args:
        birth_date: Birth date (YYYY-MM-DD)
        full_name: Full name (optional)
        birth_time: Birth time (optional)
        latitude: Latitude (optional)
        longitude: Longitude (optional)
        timezone: Timezone (optional)

    Returns:
        Personal development reading summary
    """
    try:
        from backend.calculations.personal_development_engine import (
            FlexibleBirthData,
            FlexibleInsightsEngine,
        )

        logger.info(f"Generating personal development reading for {birth_date}")

        # Parse birth date
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()

        # Create flexible birth data
        birth_data = FlexibleBirthData(
            birth_date=birth_date_obj,
            full_name=full_name,
            birth_time=birth_time,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
        )

        # Generate reading
        engine = FlexibleInsightsEngine()
        reading = engine.generate_reading(birth_data, include_coaching_prompts=True)

        # Format summary
        summary_parts = [
            f"Personal Development Reading (Data level: {reading.data_completeness.value})",
            f"\nLife Path Number: {reading.life_path_number}",
            f"{reading.life_path_interpretation}",
            f"\nDay of Week: {reading.day_of_week}",
            f"{reading.day_of_week_insights}",
        ]

        if reading.destiny_number:
            summary_parts.append(
                f"\nDestiny Number: {reading.destiny_number} - {reading.destiny_interpretation}"
            )

        if reading.sun_sign:
            summary_parts.append(
                f"\nSun Sign: {reading.sun_sign} - {reading.sun_sign_interpretation}"
            )

        if reading.strengths_themes:
            summary_parts.append(
                f"\nStrengths: {', '.join(reading.strengths_themes)}"
            )

        if reading.growth_opportunities:
            summary_parts.append(
                f"\nGrowth Areas: {', '.join(reading.growth_opportunities)}"
            )

        summary_parts.append(
            f"\nAvailable analyses: {', '.join(reading.available_analyses)}"
        )

        return "\n".join(summary_parts)

    except Exception as e:
        logger.error(f"Error generating reading: {str(e)}")
        return f"Error: {str(e)}"


def _calculate_numerology(
    birth_date: str,
    full_name: Optional[str] = None,
) -> str:
    """
    Calculate all numerology numbers.

    Args:
        birth_date: Birth date (YYYY-MM-DD)
        full_name: Full name (optional)

    Returns:
        Numerology summary
    """
    try:
        from backend.calculations.numerology_engine import NumerologyCalculator

        logger.info(f"Calculating numerology for {birth_date}")

        # Parse birth date
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()

        # Calculate
        calc = NumerologyCalculator()
        numbers = calc.get_all_numbers(birth_date_obj, full_name)
        interpretations = calc.get_all_interpretations(birth_date_obj, full_name)

        # Format
        summary = [
            "Numerology Analysis:",
            f"\nLife Path Number: {numbers['life_path']}",
            interpretations["life_path"],
        ]

        if full_name and "destiny" in numbers:
            summary.append(f"\nDestiny Number: {numbers['destiny']}")
            summary.append(interpretations["destiny"])
            summary.append(f"\nSoul Urge Number: {numbers['soul_urge']}")
            summary.append(interpretations["soul_urge"])
            summary.append(f"\nPersonality Number: {numbers['personality']}")
            summary.append(interpretations["personality"])

        return "\n".join(summary)

    except Exception as e:
        logger.error(f"Error calculating numerology: {str(e)}")
        return f"Error: {str(e)}"


def _interpret_life_path(life_path_number: int) -> str:
    """
    Get detailed life path interpretation.

    Args:
        life_path_number: Life path number (1-9, 11, 22, 33)

    Returns:
        Detailed interpretation
    """
    try:
        from backend.calculations.numerology_engine import NumerologyCalculator

        calc = NumerologyCalculator()
        return calc.interpret_life_path_number(life_path_number)

    except Exception as e:
        logger.error(f"Error interpreting life path: {str(e)}")
        return f"Error: {str(e)}"


def _get_team_dynamics(
    team_data_json: str,
    team_name: str = "Team",
) -> str:
    """
    Analyze team dynamics.

    Args:
        team_data_json: JSON string with team member data
        team_name: Name of the team

    Returns:
        Team dynamics summary
    """
    try:
        import json
        from backend.calculations.team_dynamics_engine import TeamDynamicsEngine

        logger.info(f"Analyzing team dynamics for '{team_name}'")

        # Parse team data
        team_data = json.loads(team_data_json)

        # Analyze
        engine = TeamDynamicsEngine()
        analysis = engine.analyze_team(team_data, team_name)

        # Format summary
        summary = [
            f"Team Dynamics Analysis: {analysis.team_name}",
            f"Members: {analysis.member_count}",
            f"\nOverall Synergy: {analysis.compatibility_score.overall_synergy}/100",
            f"Communication Compatibility: {analysis.compatibility_score.communication_compatibility}/100",
            f"Strengths Diversity: {analysis.compatibility_score.strengths_diversity}/100",
            f"\nTeam Strengths:",
        ]

        for strength in analysis.compatibility_score.team_strengths:
            summary.append(f"  - {strength}")

        summary.append("\nGrowth Areas:")
        for area in analysis.compatibility_score.growth_areas:
            summary.append(f"  - {area}")

        if analysis.life_path_distribution:
            summary.append("\nLife Path Distribution:")
            for lp, count in sorted(analysis.life_path_distribution.items()):
                summary.append(f"  Life Path {lp}: {count} member(s)")

        return "\n".join(summary)

    except Exception as e:
        logger.error(f"Error analyzing team: {str(e)}")
        return f"Error: {str(e)}"


def _get_coaching_prompts(
    birth_date: str,
    focus_area: Optional[str] = None,
) -> str:
    """
    Generate coaching conversation prompts.

    Args:
        birth_date: Birth date (YYYY-MM-DD)
        focus_area: Specific area to focus on (optional)

    Returns:
        Coaching prompts
    """
    try:
        from backend.calculations.personal_development_engine import (
            FlexibleBirthData,
            FlexibleInsightsEngine,
        )

        # Parse birth date
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()

        # Create birth data
        birth_data = FlexibleBirthData(birth_date=birth_date_obj)

        # Generate reading
        engine = FlexibleInsightsEngine()
        reading = engine.generate_reading(birth_data, include_coaching_prompts=True)

        # Format prompts
        prompts = ["Coaching Conversation Starters:"]
        for prompt in reading.reflection_prompts:
            prompts.append(f"\n- {prompt}")

        if focus_area:
            prompts.append(
                f"\nFocus area: {focus_area}"
                f"\nAdditional prompt: How does your natural style support or challenge "
                f"your goals in {focus_area}?"
            )

        return "\n".join(prompts)

    except Exception as e:
        logger.error(f"Error generating prompts: {str(e)}")
        return f"Error: {str(e)}"


# Create LangChain tools
get_personal_reading_tool = StructuredTool.from_function(
    func=_get_personal_development_reading,
    name="get_personal_development_reading",
    description=(
        "Generate flexible personal development reading from birth data. "
        "Works with any level of data completeness (date only, date+time, or full data). "
        "Returns numerology and astrological insights based on available information."
    ),
    args_schema=PersonalReadingInput,
)

calculate_numerology_tool = StructuredTool.from_function(
    func=_calculate_numerology,
    name="calculate_numerology",
    description=(
        "Calculate numerology numbers (life path, destiny, soul urge, personality) "
        "from birth date and optional name. Always available even with minimal data."
    ),
    args_schema=NumerologyInput,
)

interpret_life_path_tool = Tool(
    name="interpret_life_path_number",
    func=lambda lp: _interpret_life_path(int(lp)),
    description=(
        "Get detailed interpretation of a life path number (1-9, 11, 22, 33). "
        "Provides insights on work style, strengths, and growth areas."
    ),
)

get_team_dynamics_tool = Tool(
    name="analyze_team_dynamics",
    func=lambda team_json, name="Team": _get_team_dynamics(team_json, name),
    description=(
        "Analyze team dynamics and compatibility. Requires JSON with team member "
        "birth data. Returns synergy scores, communication styles, and collaboration tips."
    ),
)

get_coaching_prompts_tool = Tool(
    name="get_coaching_prompts",
    func=lambda bd, focus=None: _get_coaching_prompts(bd, focus),
    description=(
        "Generate coaching conversation prompts based on birth date. "
        "Useful for facilitating personal development discussions."
    ),
)


# Tool collections
PERSONAL_DEVELOPMENT_TOOLS = [
    get_personal_reading_tool,
    calculate_numerology_tool,
    interpret_life_path_tool,
    get_team_dynamics_tool,
    get_coaching_prompts_tool,
]

ALL_PERSONAL_DEVELOPMENT_TOOLS = PERSONAL_DEVELOPMENT_TOOLS
