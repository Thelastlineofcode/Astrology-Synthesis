"""
Synastry Calculation Engine

Analyzes relationship compatibility by comparing two birth charts.
Provides inter-chart aspects, house overlays, composite charts, and compatibility scores.

Based on:
- Western synastry techniques
- Vedic relationship analysis (Kuta system)
- KP significator matching
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import math

from backend.calculations.ephemeris import EphemerisCalculator
from backend.calculations.kp_engine import get_sub_lord, get_significators_for_house
from backend.calculations.exceptions import CalculationError

logger = logging.getLogger(__name__)


# Synastry aspect orbs (degrees)
SYNASTRY_ORBS = {
    "Conjunction": 8.0,
    "Opposition": 8.0,
    "Trine": 6.0,
    "Square": 6.0,
    "Sextile": 4.0,
    "Quincunx": 3.0,
}

# Aspect scores for compatibility
ASPECT_SCORES = {
    "Conjunction": {"harmonious": 0.8, "challenging": 0.4},
    "Trine": {"harmonious": 1.0, "challenging": 0.0},
    "Sextile": {"harmonious": 0.7, "challenging": 0.0},
    "Opposition": {"harmonious": 0.3, "challenging": 0.8},
    "Square": {"harmonious": 0.2, "challenging": 1.0},
    "Quincunx": {"harmonious": 0.3, "challenging": 0.5},
}

# Planet compatibility weights
PLANET_WEIGHTS = {
    "Sun": 1.5,      # Core identity
    "Moon": 2.0,     # Emotions (most important)
    "Venus": 1.8,    # Love and attraction
    "Mars": 1.3,     # Passion and conflict
    "Mercury": 1.0,  # Communication
    "Jupiter": 0.8,  # Growth and expansion
    "Saturn": 1.2,   # Commitment and challenges
    "Ascendant": 1.5,  # First impressions
}


@dataclass
class SynastryAspect:
    """Represents an aspect between two charts."""
    person1_planet: str
    person2_planet: str
    aspect_type: str
    orb: float
    angle: float
    is_applying: bool
    is_harmonious: bool
    strength: float  # 0-1
    interpretation: str


@dataclass
class HouseOverlay:
    """Represents a planet from one chart falling in another's house."""
    person: str  # "Person1" or "Person2"
    planet: str
    falls_in_house: int
    house_owner: str  # "Person1" or "Person2"
    interpretation: str


@dataclass
class CompositeChart:
    """Midpoint composite chart for the relationship."""
    composite_sun: float
    composite_moon: float
    composite_ascendant: float
    composite_planets: Dict[str, float]
    chart_date: datetime


@dataclass
class CompatibilityScore:
    """Overall compatibility analysis."""
    overall_score: float  # 0-100
    emotional_compatibility: float
    romantic_compatibility: float
    communication_compatibility: float
    long_term_compatibility: float
    sexual_compatibility: float

    harmonious_aspects: int
    challenging_aspects: int

    strengths: List[str]
    challenges: List[str]
    advice: List[str]


@dataclass
class SynastryResult:
    """Complete synastry analysis."""
    person1_name: str
    person2_name: str

    inter_aspects: List[SynastryAspect]
    house_overlays: List[HouseOverlay]
    composite_chart: Optional[CompositeChart]

    compatibility_score: CompatibilityScore

    calculation_time_ms: float


class SynastryCalculator:
    """
    Main synastry calculation engine.

    Analyzes relationship compatibility between two birth charts.
    """

    def __init__(self):
        """Initialize synastry calculator."""
        self.ephemeris = EphemerisCalculator()
        logger.info("SynastryCalculator initialized")

    def calculate_synastry(
        self,
        chart1: Dict[str, Any],
        chart2: Dict[str, Any],
        person1_name: str = "Person 1",
        person2_name: str = "Person 2",
        include_composite: bool = True,
    ) -> SynastryResult:
        """
        Calculate complete synastry analysis.

        Args:
            chart1: First person's birth chart
            chart2: Second person's birth chart
            person1_name: Name for person 1
            person2_name: Name for person 2
            include_composite: Calculate composite chart

        Returns:
            Complete synastry analysis
        """
        import time
        start_time = time.time()

        try:
            logger.info(f"Calculating synastry: {person1_name} + {person2_name}")

            # Calculate inter-chart aspects
            inter_aspects = self._calculate_inter_aspects(chart1, chart2)

            # Calculate house overlays
            house_overlays = self._calculate_house_overlays(
                chart1, chart2, person1_name, person2_name
            )

            # Calculate composite chart if requested
            composite_chart = None
            if include_composite:
                composite_chart = self._calculate_composite_chart(chart1, chart2)

            # Calculate compatibility score
            compatibility_score = self._calculate_compatibility(
                inter_aspects,
                house_overlays,
                chart1,
                chart2,
            )

            calculation_time = (time.time() - start_time) * 1000

            result = SynastryResult(
                person1_name=person1_name,
                person2_name=person2_name,
                inter_aspects=inter_aspects,
                house_overlays=house_overlays,
                composite_chart=composite_chart,
                compatibility_score=compatibility_score,
                calculation_time_ms=calculation_time,
            )

            logger.info(
                f"Synastry calculated: {len(inter_aspects)} aspects, "
                f"score={compatibility_score.overall_score:.1f}/100, "
                f"time={calculation_time:.1f}ms"
            )

            return result

        except Exception as e:
            logger.error(f"Synastry calculation failed: {str(e)}")
            raise CalculationError(f"Synastry calculation error: {str(e)}")

    def _calculate_inter_aspects(
        self,
        chart1: Dict[str, Any],
        chart2: Dict[str, Any],
    ) -> List[SynastryAspect]:
        """
        Calculate aspects between planets in two charts.

        Args:
            chart1: First chart
            chart2: Second chart

        Returns:
            List of synastry aspects
        """
        aspects = []

        # Get planet positions from both charts
        planets1 = chart1.get("planet_positions", [])
        planets2 = chart2.get("planet_positions", [])

        # Consider these planets for synastry
        synastry_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars",
                           "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

        # Also include Ascendant
        planets1_dict = {p["planet"]: p["longitude"] for p in planets1
                        if p["planet"] in synastry_planets}
        planets2_dict = {p["planet"]: p["longitude"] for p in planets2
                        if p["planet"] in synastry_planets}

        # Add Ascendant
        if chart1.get("ascendant"):
            planets1_dict["Ascendant"] = chart1["ascendant"]["degree"]
        if chart2.get("ascendant"):
            planets2_dict["Ascendant"] = chart2["ascendant"]["degree"]

        # Calculate aspects between all planet pairs
        for planet1, long1 in planets1_dict.items():
            for planet2, long2 in planets2_dict.items():
                aspect = self._check_aspect(planet1, long1, planet2, long2)
                if aspect:
                    aspects.append(aspect)

        # Sort by importance (harmonious aspects first, then by strength)
        aspects.sort(key=lambda a: (-int(a.is_harmonious), -a.strength))

        return aspects

    def _check_aspect(
        self,
        planet1: str,
        long1: float,
        planet2: str,
        long2: float,
    ) -> Optional[SynastryAspect]:
        """Check if two planets form an aspect."""
        # Calculate angular distance
        diff = abs(long1 - long2)
        if diff > 180:
            diff = 360 - diff

        # Check each aspect type
        for aspect_type, max_orb in SYNASTRY_ORBS.items():
            target_angle = self._get_aspect_angle(aspect_type)
            orb = abs(diff - target_angle)

            if orb <= max_orb:
                # Determine if harmonious or challenging
                is_harmonious = self._is_harmonious_aspect(aspect_type, planet1, planet2)

                # Calculate strength (closer = stronger)
                strength = 1.0 - (orb / max_orb)

                # Apply planet weight
                weight = min(
                    PLANET_WEIGHTS.get(planet1, 0.5),
                    PLANET_WEIGHTS.get(planet2, 0.5),
                )
                strength *= weight

                # Generate interpretation
                interpretation = self._interpret_aspect(
                    planet1, planet2, aspect_type, is_harmonious
                )

                return SynastryAspect(
                    person1_planet=planet1,
                    person2_planet=planet2,
                    aspect_type=aspect_type,
                    orb=orb,
                    angle=diff,
                    is_applying=False,  # Would need planet speeds to determine
                    is_harmonious=is_harmonious,
                    strength=strength,
                    interpretation=interpretation,
                )

        return None

    def _get_aspect_angle(self, aspect_type: str) -> float:
        """Get the angle for an aspect type."""
        angles = {
            "Conjunction": 0,
            "Sextile": 60,
            "Square": 90,
            "Trine": 120,
            "Quincunx": 150,
            "Opposition": 180,
        }
        return angles.get(aspect_type, 0)

    def _is_harmonious_aspect(
        self,
        aspect_type: str,
        planet1: str,
        planet2: str,
    ) -> bool:
        """Determine if aspect is harmonious or challenging."""
        # Base harmonious aspects
        harmonious = aspect_type in ["Trine", "Sextile"]

        # Conjunction depends on planets involved
        if aspect_type == "Conjunction":
            # Beneficial planets in conjunction are harmonious
            beneficial = ["Venus", "Jupiter", "Sun", "Moon"]
            if planet1 in beneficial and planet2 in beneficial:
                return True
            # Mars-Mars or Saturn-Saturn can be challenging
            if planet1 == planet2 and planet1 in ["Mars", "Saturn"]:
                return False
            return True  # Most conjunctions are neutral to positive

        return harmonious

    def _interpret_aspect(
        self,
        planet1: str,
        planet2: str,
        aspect_type: str,
        is_harmonious: bool,
    ) -> str:
        """Generate interpretation for synastry aspect."""
        # Simplified interpretation - would expand in production
        quality = "harmonious" if is_harmonious else "challenging"

        descriptions = {
            ("Sun", "Moon"): {
                "harmonious": "Deep emotional understanding and mutual support",
                "challenging": "Tension between ego needs and emotional security",
            },
            ("Venus", "Mars"): {
                "harmonious": "Strong romantic and sexual attraction",
                "challenging": "Passion mixed with friction and desire",
            },
            ("Moon", "Moon"): {
                "harmonious": "Emotional wavelength compatibility",
                "challenging": "Different emotional needs and responses",
            },
            ("Mercury", "Mercury"): {
                "harmonious": "Easy communication and mental rapport",
                "challenging": "Communication misunderstandings",
            },
        }

        key = (planet1, planet2)
        if key in descriptions:
            return descriptions[key][quality]

        return f"{planet1}-{planet2} {aspect_type} creates {quality} energy in the relationship"

    def _calculate_house_overlays(
        self,
        chart1: Dict[str, Any],
        chart2: Dict[str, Any],
        person1_name: str,
        person2_name: str,
    ) -> List[HouseOverlay]:
        """Calculate house overlays between two charts."""
        overlays = []

        # Person 1's planets in Person 2's houses
        planets1 = chart1.get("planet_positions", [])
        houses2 = chart2.get("house_cusps", [])

        for planet_data in planets1:
            planet = planet_data["planet"]
            planet_long = planet_data["longitude"]

            # Find which house in chart2 this planet falls into
            house_num = self._find_house(planet_long, houses2)

            interpretation = self._interpret_house_overlay(
                planet, house_num, person1_name, person2_name
            )

            overlays.append(HouseOverlay(
                person=person1_name,
                planet=planet,
                falls_in_house=house_num,
                house_owner=person2_name,
                interpretation=interpretation,
            ))

        # Person 2's planets in Person 1's houses
        planets2 = chart2.get("planet_positions", [])
        houses1 = chart1.get("house_cusps", [])

        for planet_data in planets2:
            planet = planet_data["planet"]
            planet_long = planet_data["longitude"]

            house_num = self._find_house(planet_long, houses1)

            interpretation = self._interpret_house_overlay(
                planet, house_num, person2_name, person1_name
            )

            overlays.append(HouseOverlay(
                person=person2_name,
                planet=planet,
                falls_in_house=house_num,
                house_owner=person1_name,
                interpretation=interpretation,
            ))

        return overlays

    def _find_house(self, planet_long: float, house_cusps: List[Dict]) -> int:
        """Find which house a planet falls into."""
        cusps = [h.get("cusp", h.get("longitude", 0)) for h in house_cusps]

        for i in range(12):
            cusp1 = cusps[i]
            cusp2 = cusps[(i + 1) % 12]

            if cusp1 <= cusp2:
                if cusp1 <= planet_long < cusp2:
                    return i + 1
            else:  # wrap-around
                if planet_long >= cusp1 or planet_long < cusp2:
                    return i + 1

        return 1

    def _interpret_house_overlay(
        self,
        planet: str,
        house: int,
        planet_owner: str,
        house_owner: str,
    ) -> str:
        """Interpret a planet in another person's house."""
        house_meanings = {
            1: "identity and self-expression",
            2: "values and resources",
            3: "communication and mind",
            4: "home and emotional security",
            5: "romance and creativity",
            6: "daily routines and service",
            7: "partnerships and commitment",
            8: "intimacy and transformation",
            9: "beliefs and growth",
            10: "career and reputation",
            11: "friendships and ideals",
            12: "spirituality and hidden matters",
        }

        meaning = house_meanings.get(house, "life area")
        return f"{planet_owner}'s {planet} activates {house_owner}'s {meaning}"

    def _calculate_composite_chart(
        self,
        chart1: Dict[str, Any],
        chart2: Dict[str, Any],
    ) -> CompositeChart:
        """Calculate midpoint composite chart."""
        # Get planets from both charts
        planets1 = {p["planet"]: p["longitude"]
                   for p in chart1.get("planet_positions", [])}
        planets2 = {p["planet"]: p["longitude"]
                   for p in chart2.get("planet_positions", [])}

        # Calculate midpoints
        composite_planets = {}
        for planet in planets1:
            if planet in planets2:
                midpoint = self._calculate_midpoint(
                    planets1[planet], planets2[planet]
                )
                composite_planets[planet] = midpoint

        # Composite Ascendant
        asc1 = chart1.get("ascendant", {}).get("degree", 0)
        asc2 = chart2.get("ascendant", {}).get("degree", 0)
        composite_asc = self._calculate_midpoint(asc1, asc2)

        return CompositeChart(
            composite_sun=composite_planets.get("Sun", 0),
            composite_moon=composite_planets.get("Moon", 0),
            composite_ascendant=composite_asc,
            composite_planets=composite_planets,
            chart_date=datetime.now(),
        )

    def _calculate_midpoint(self, long1: float, long2: float) -> float:
        """Calculate midpoint between two longitudes."""
        diff = abs(long1 - long2)

        if diff <= 180:
            # Direct midpoint
            midpoint = (long1 + long2) / 2
        else:
            # Use the short way around
            midpoint = ((long1 + long2) / 2 + 180) % 360

        return midpoint % 360

    def _calculate_compatibility(
        self,
        aspects: List[SynastryAspect],
        overlays: List[HouseOverlay],
        chart1: Dict[str, Any],
        chart2: Dict[str, Any],
    ) -> CompatibilityScore:
        """Calculate overall compatibility score."""
        # Count aspect types
        harmonious = [a for a in aspects if a.is_harmonious]
        challenging = [a for a in aspects if not a.is_harmonious]

        # Calculate sub-scores
        emotional = self._calculate_emotional_compatibility(aspects, chart1, chart2)
        romantic = self._calculate_romantic_compatibility(aspects, chart1, chart2)
        communication = self._calculate_communication_compatibility(aspects)
        long_term = self._calculate_long_term_compatibility(aspects)
        sexual = self._calculate_sexual_compatibility(aspects)

        # Overall score (weighted average)
        overall = (
            emotional * 0.25 +
            romantic * 0.25 +
            communication * 0.20 +
            long_term * 0.20 +
            sexual * 0.10
        )

        # Generate insights
        strengths = self._identify_strengths(aspects, overlays)
        challenges_list = self._identify_challenges(aspects, overlays)
        advice = self._generate_advice(aspects, overall)

        return CompatibilityScore(
            overall_score=overall,
            emotional_compatibility=emotional,
            romantic_compatibility=romantic,
            communication_compatibility=communication,
            long_term_compatibility=long_term,
            sexual_compatibility=sexual,
            harmonious_aspects=len(harmonious),
            challenging_aspects=len(challenging),
            strengths=strengths,
            challenges=challenges_list,
            advice=advice,
        )

    def _calculate_emotional_compatibility(
        self,
        aspects: List[SynastryAspect],
        chart1: Dict,
        chart2: Dict,
    ) -> float:
        """Calculate emotional compatibility (Moon-Moon, Moon-Venus, Sun-Moon)."""
        score = 50.0  # Base score

        emotional_aspects = [
            a for a in aspects
            if ("Moon" in [a.person1_planet, a.person2_planet] or
                "Sun" in [a.person1_planet, a.person2_planet])
        ]

        for aspect in emotional_aspects:
            if aspect.is_harmonious:
                score += aspect.strength * 10
            else:
                score -= aspect.strength * 5

        return min(100, max(0, score))

    def _calculate_romantic_compatibility(
        self,
        aspects: List[SynastryAspect],
        chart1: Dict,
        chart2: Dict,
    ) -> float:
        """Calculate romantic compatibility (Venus-Mars, Venus-Venus)."""
        score = 50.0

        romantic_aspects = [
            a for a in aspects
            if ("Venus" in [a.person1_planet, a.person2_planet] or
                "Mars" in [a.person1_planet, a.person2_planet])
        ]

        for aspect in romantic_aspects:
            if aspect.is_harmonious:
                score += aspect.strength * 12
            else:
                score += aspect.strength * 5  # Even challenging aspects show attraction

        return min(100, max(0, score))

    def _calculate_communication_compatibility(
        self,
        aspects: List[SynastryAspect],
    ) -> float:
        """Calculate communication compatibility (Mercury aspects)."""
        score = 50.0

        mercury_aspects = [
            a for a in aspects
            if "Mercury" in [a.person1_planet, a.person2_planet]
        ]

        for aspect in mercury_aspects:
            if aspect.is_harmonious:
                score += aspect.strength * 10
            else:
                score -= aspect.strength * 8

        return min(100, max(0, score))

    def _calculate_long_term_compatibility(
        self,
        aspects: List[SynastryAspect],
    ) -> float:
        """Calculate long-term compatibility (Saturn, Jupiter aspects)."""
        score = 50.0

        long_term_aspects = [
            a for a in aspects
            if ("Saturn" in [a.person1_planet, a.person2_planet] or
                "Jupiter" in [a.person1_planet, a.person2_planet])
        ]

        for aspect in long_term_aspects:
            if aspect.is_harmonious:
                score += aspect.strength * 8
            else:
                score -= aspect.strength * 6

        return min(100, max(0, score))

    def _calculate_sexual_compatibility(
        self,
        aspects: List[SynastryAspect],
    ) -> float:
        """Calculate sexual compatibility (Mars-Venus, Mars-Mars aspects)."""
        score = 50.0

        sexual_aspects = [
            a for a in aspects
            if (set([a.person1_planet, a.person2_planet]) & {"Mars", "Venus", "Pluto"})
        ]

        for aspect in sexual_aspects:
            # Both harmonious and challenging aspects indicate attraction
            score += aspect.strength * 10

        return min(100, max(0, score))

    def _identify_strengths(
        self,
        aspects: List[SynastryAspect],
        overlays: List[HouseOverlay],
    ) -> List[str]:
        """Identify relationship strengths."""
        strengths = []

        # Check for strong harmonious aspects
        harmonious = [a for a in aspects if a.is_harmonious and a.strength > 0.7]

        if any(a.person1_planet == "Moon" and a.person2_planet == "Moon" for a in harmonious):
            strengths.append("Deep emotional understanding")

        if any(set([a.person1_planet, a.person2_planet]) == {"Venus", "Mars"} for a in harmonious):
            strengths.append("Strong romantic and physical attraction")

        if any("Jupiter" in [a.person1_planet, a.person2_planet] for a in harmonious):
            strengths.append("Growth and expansion together")

        if not strengths:
            strengths.append("Potential for growth through challenges")

        return strengths[:5]  # Top 5 strengths

    def _identify_challenges(
        self,
        aspects: List[SynastryAspect],
        overlays: List[HouseOverlay],
    ) -> List[str]:
        """Identify relationship challenges."""
        challenges = []

        challenging = [a for a in aspects if not a.is_harmonious and a.strength > 0.6]

        if any(a.person1_planet == "Moon" and a.person2_planet == "Moon" for a in challenging):
            challenges.append("Different emotional needs require understanding")

        if any("Saturn" in [a.person1_planet, a.person2_planet] for a in challenging):
            challenges.append("Patience needed for long-term commitment")

        if any(set([a.person1_planet, a.person2_planet]) == {"Mars", "Mars"} for a in challenging):
            challenges.append("Potential for conflict and competition")

        if not challenges:
            challenges.append("Minor adjustments needed in daily life")

        return challenges[:5]  # Top 5 challenges

    def _generate_advice(
        self,
        aspects: List[SynastryAspect],
        overall_score: float,
    ) -> List[str]:
        """Generate relationship advice."""
        advice = []

        if overall_score >= 75:
            advice.append("Nurture your strong connection through quality time together")
        elif overall_score >= 60:
            advice.append("Focus on your strengths while working through challenges")
        else:
            advice.append("Open communication is essential for this relationship")

        advice.append("Respect each other's individual needs and growth")
        advice.append("Use challenges as opportunities to deepen understanding")

        return advice
