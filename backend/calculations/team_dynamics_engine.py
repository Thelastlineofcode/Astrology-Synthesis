"""
Team Dynamics and Compatibility Engine

Analyzes team composition using numerology and astrology for personal development
and team building purposes.

IMPORTANT DISCLAIMER:
This tool is designed for team building, coaching, and wellness programs.
It is NOT intended for hiring, promotion, or employment decisions.
It is NOT scientifically validated and should not be used for employee evaluation.

Strategic Use Cases:
- Team composition insights for existing teams
- Communication style mapping
- Strengths synergy identification
- Trust-building conversations
- Team retreat activities
- Leadership development coaching
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import date
import logging

from .personal_development_engine import (
    FlexibleBirthData,
    PersonalDevelopmentReading,
    FlexibleInsightsEngine,
    DataCompleteness,
)

logger = logging.getLogger(__name__)


@dataclass
class TeamMember:
    """
    Team member with personal development profile.

    Only stores minimal information needed for team insights.
    """
    member_id: str
    name: str
    birth_data: FlexibleBirthData
    reading: Optional[PersonalDevelopmentReading] = None

    # Metadata
    role: Optional[str] = None  # Optional: for role-based insights
    department: Optional[str] = None


@dataclass
class TeamCompatibilityScore:
    """Team-wide compatibility and synergy metrics."""
    overall_synergy: float  # 0-100
    communication_compatibility: float
    strengths_diversity: float
    complementary_skills: float

    # Insights
    team_strengths: List[str]
    growth_areas: List[str]
    communication_tips: List[str]
    collaboration_opportunities: List[str]


@dataclass
class TeamDynamicsAnalysis:
    """
    Complete team dynamics analysis.

    Focuses on strengths, communication, and collaboration opportunities.
    """
    team_name: str
    member_count: int
    members: List[TeamMember]

    # Aggregate insights
    compatibility_score: TeamCompatibilityScore

    # Element distribution (if astrology data available)
    element_balance: Optional[Dict[str, int]] = None  # Fire, Earth, Air, Water

    # Life path distribution
    life_path_distribution: Dict[int, int] = None

    # Communication styles
    communication_matrix: Optional[List[Dict[str, Any]]] = None

    # Pairwise synergies (top 5 strongest pairs)
    strongest_synergies: List[Tuple[str, str, float]] = None

    # Growth opportunities
    team_coaching_prompts: List[str] = None

    # Disclaimer
    disclaimer: str = (
        "This team analysis is for personal development, coaching, and team building only. "
        "It is not a scientific assessment and should not be used for hiring, promotion, "
        "performance evaluation, or any employment decisions. Results are meant to inspire "
        "team conversations, build trust, and facilitate collaborative growth."
    )

    def __post_init__(self):
        """Initialize default values."""
        if self.life_path_distribution is None:
            self.life_path_distribution = {}
        if self.strongest_synergies is None:
            self.strongest_synergies = []
        if self.team_coaching_prompts is None:
            self.team_coaching_prompts = []


class TeamDynamicsEngine:
    """
    Analyzes team composition and dynamics for personal development.

    Provides:
    - Team-wide compatibility scoring
    - Communication style mapping
    - Strengths synergy identification
    - Collaboration opportunity discovery
    - Coaching conversation prompts
    """

    def __init__(self):
        """Initialize team dynamics engine."""
        self.insights_engine = FlexibleInsightsEngine()
        logger.info("TeamDynamicsEngine initialized (Team Building Tool - Not for HR Decisions)")

    def analyze_team(
        self,
        team_members: List[Dict[str, Any]],
        team_name: str = "Team",
        include_pairwise_analysis: bool = True,
    ) -> TeamDynamicsAnalysis:
        """
        Analyze team dynamics based on member birth data.

        Args:
            team_members: List of dicts with member info (name, birth_date, etc.)
            team_name: Name of the team
            include_pairwise_analysis: Calculate pairwise compatibilities

        Returns:
            TeamDynamicsAnalysis with comprehensive insights
        """
        logger.info(f"Analyzing team '{team_name}' with {len(team_members)} members")

        # Generate individual readings
        members = []
        for member_data in team_members:
            birth_data = self._parse_birth_data(member_data)
            reading = self.insights_engine.generate_reading(birth_data)

            member = TeamMember(
                member_id=member_data.get("id", f"member_{len(members)}"),
                name=member_data.get("name", f"Member {len(members) + 1}"),
                birth_data=birth_data,
                reading=reading,
                role=member_data.get("role"),
                department=member_data.get("department"),
            )
            members.append(member)

        # Analyze team composition
        life_path_dist = self._calculate_life_path_distribution(members)
        element_balance = self._calculate_element_balance(members)

        # Calculate team compatibility
        compatibility_score = self._calculate_team_compatibility(members)

        # Pairwise synergies
        strongest_synergies = []
        if include_pairwise_analysis and len(members) >= 2:
            strongest_synergies = self._find_strongest_synergies(members, top_n=5)

        # Communication matrix
        communication_matrix = self._build_communication_matrix(members)

        # Team coaching prompts
        coaching_prompts = self._generate_team_coaching_prompts(
            members, compatibility_score
        )

        return TeamDynamicsAnalysis(
            team_name=team_name,
            member_count=len(members),
            members=members,
            compatibility_score=compatibility_score,
            element_balance=element_balance,
            life_path_distribution=life_path_dist,
            communication_matrix=communication_matrix,
            strongest_synergies=strongest_synergies,
            team_coaching_prompts=coaching_prompts,
        )

    def _parse_birth_data(self, member_data: Dict[str, Any]) -> FlexibleBirthData:
        """Parse member data into FlexibleBirthData."""
        birth_date_str = member_data.get("birth_date")
        if isinstance(birth_date_str, str):
            from datetime import datetime
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        else:
            birth_date = birth_date_str

        return FlexibleBirthData(
            birth_date=birth_date,
            birth_time=member_data.get("birth_time"),
            birth_location=member_data.get("birth_location"),
            latitude=member_data.get("latitude"),
            longitude=member_data.get("longitude"),
            timezone=member_data.get("timezone"),
            full_name=member_data.get("full_name"),
        )

    def _calculate_life_path_distribution(
        self, members: List[TeamMember]
    ) -> Dict[int, int]:
        """Calculate distribution of life path numbers in team."""
        distribution = {}
        for member in members:
            if member.reading and member.reading.life_path_number:
                lp = member.reading.life_path_number
                distribution[lp] = distribution.get(lp, 0) + 1
        return distribution

    def _calculate_element_balance(
        self, members: List[TeamMember]
    ) -> Optional[Dict[str, int]]:
        """
        Calculate distribution of astrological elements.

        Only if astrology data is available for members.
        """
        element_count = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}

        fire_signs = ["Aries", "Leo", "Sagittarius"]
        earth_signs = ["Taurus", "Virgo", "Capricorn"]
        air_signs = ["Gemini", "Libra", "Aquarius"]
        water_signs = ["Cancer", "Scorpio", "Pisces"]

        has_data = False
        for member in members:
            if member.reading and member.reading.sun_sign:
                has_data = True
                sign = member.reading.sun_sign
                if sign in fire_signs:
                    element_count["Fire"] += 1
                elif sign in earth_signs:
                    element_count["Earth"] += 1
                elif sign in air_signs:
                    element_count["Air"] += 1
                elif sign in water_signs:
                    element_count["Water"] += 1

        return element_count if has_data else None

    def _calculate_team_compatibility(
        self, members: List[TeamMember]
    ) -> TeamCompatibilityScore:
        """
        Calculate overall team compatibility metrics.

        Based on diversity of strengths, complementary life paths,
        and communication compatibility.
        """
        # Collect all life path numbers
        life_paths = [
            m.reading.life_path_number
            for m in members
            if m.reading and m.reading.life_path_number
        ]

        # Diversity score (more diverse = better for teams)
        unique_life_paths = len(set(life_paths))
        diversity_ratio = unique_life_paths / len(life_paths) if life_paths else 0
        strengths_diversity = min(diversity_ratio * 100, 100)

        # Communication compatibility (based on life path patterns)
        communication_score = self._calculate_communication_compatibility(life_paths)

        # Complementary skills (presence of different archetypal energies)
        complementary_score = self._calculate_complementary_skills(life_paths)

        # Overall synergy (weighted average)
        overall_synergy = (
            communication_score * 0.4
            + strengths_diversity * 0.3
            + complementary_score * 0.3
        )

        # Generate insights
        team_strengths = self._identify_team_strengths(members)
        growth_areas = self._identify_growth_areas(members, life_paths)
        communication_tips = self._generate_communication_tips(members)
        collaboration_opportunities = self._identify_collaboration_opportunities(members)

        return TeamCompatibilityScore(
            overall_synergy=round(overall_synergy, 1),
            communication_compatibility=round(communication_score, 1),
            strengths_diversity=round(strengths_diversity, 1),
            complementary_skills=round(complementary_score, 1),
            team_strengths=team_strengths,
            growth_areas=growth_areas,
            communication_tips=communication_tips,
            collaboration_opportunities=collaboration_opportunities,
        )

    def _calculate_communication_compatibility(self, life_paths: List[int]) -> float:
        """Calculate how well the team communicates based on life paths."""
        if not life_paths:
            return 70.0  # Default

        # Check for balance between different communication styles
        # 1, 3, 5: Direct, expressive communicators
        # 2, 6, 9: Empathetic, relational communicators
        # 4, 7, 8: Analytical, structured communicators

        direct = sum(1 for lp in life_paths if lp in [1, 3, 5])
        empathetic = sum(1 for lp in life_paths if lp in [2, 6, 9])
        analytical = sum(1 for lp in life_paths if lp in [4, 7, 8])

        total = len(life_paths)

        # Balanced teams communicate better
        balance_score = 100 - (
            abs(direct - empathetic) / total * 50
            + abs(empathetic - analytical) / total * 50
            + abs(analytical - direct) / total * 50
        ) / 3

        return max(50, min(balance_score, 95))

    def _calculate_complementary_skills(self, life_paths: List[int]) -> float:
        """Calculate complementary skills score."""
        if not life_paths:
            return 70.0

        # Ideal teams have mix of:
        # Leaders (1, 8)
        # Collaborators (2, 6)
        # Creatives (3, 5)
        # Organizers (4)
        # Thinkers (7)
        # Visionaries (9, 11, 22, 33)

        has_leaders = any(lp in [1, 8] for lp in life_paths)
        has_collaborators = any(lp in [2, 6] for lp in life_paths)
        has_creatives = any(lp in [3, 5] for lp in life_paths)
        has_organizers = any(lp == 4 for lp in life_paths)
        has_thinkers = any(lp == 7 for lp in life_paths)
        has_visionaries = any(lp in [9, 11, 22, 33] for lp in life_paths)

        archetypes_present = sum([
            has_leaders,
            has_collaborators,
            has_creatives,
            has_organizers,
            has_thinkers,
            has_visionaries,
        ])

        # More archetypes = more complementary skills
        return (archetypes_present / 6) * 100

    def _identify_team_strengths(self, members: List[TeamMember]) -> List[str]:
        """Identify collective team strengths."""
        strengths = []

        # Collect all individual strengths
        all_strengths = []
        for member in members:
            if member.reading and member.reading.strengths_themes:
                all_strengths.extend(member.reading.strengths_themes)

        # Find common themes
        if "creativity" in " ".join(all_strengths).lower() or "innovation" in " ".join(all_strengths).lower():
            strengths.append("Strong creative and innovative capacity")

        if "empathy" in " ".join(all_strengths).lower() or "collaboration" in " ".join(all_strengths).lower():
            strengths.append("Excellent team collaboration and empathy")

        if "leadership" in " ".join(all_strengths).lower() or "organizational" in " ".join(all_strengths).lower():
            strengths.append("Natural leadership and organizational abilities")

        if not strengths:
            strengths.append("Diverse strengths creating unique team dynamic")

        return strengths

    def _identify_growth_areas(
        self, members: List[TeamMember], life_paths: List[int]
    ) -> List[str]:
        """Identify team-wide growth opportunities."""
        growth = []

        # Check for overrepresentation
        from collections import Counter
        lp_counts = Counter(life_paths)
        most_common = lp_counts.most_common(1)

        if most_common and most_common[0][1] > len(life_paths) * 0.5:
            growth.append(
                "Consider bringing in diverse perspectives to balance team strengths"
            )

        # Check for missing archetypes
        has_collaborators = any(lp in [2, 6] for lp in life_paths)
        has_organizers = any(lp == 4 for lp in life_paths)

        if not has_collaborators:
            growth.append("Building collaborative and empathetic communication patterns")

        if not has_organizers:
            growth.append("Strengthening processes and organizational structure")

        if not growth:
            growth.append("Continuous learning and team trust-building")

        return growth

    def _generate_communication_tips(self, members: List[TeamMember]) -> List[str]:
        """Generate team communication tips."""
        tips = [
            "Create space for different communication styles (direct, empathetic, analytical)",
            "Use team strengths mapping as a trust-building conversation starter",
            "Recognize that each member brings unique gifts to the team",
        ]

        # Check for specific patterns
        life_paths = [
            m.reading.life_path_number
            for m in members
            if m.reading and m.reading.life_path_number
        ]

        if any(lp in [1, 8] for lp in life_paths) and any(lp in [2, 6] for lp in life_paths):
            tips.append(
                "Balance between decisive leadership and collaborative consensus-building"
            )

        return tips

    def _identify_collaboration_opportunities(
        self, members: List[TeamMember]
    ) -> List[str]:
        """Identify specific collaboration opportunities."""
        opportunities = [
            "Pair complementary strengths for project partnerships",
            "Rotate leadership roles to leverage different styles",
            "Create cross-functional teams based on diverse approaches",
        ]

        return opportunities

    def _find_strongest_synergies(
        self, members: List[TeamMember], top_n: int = 5
    ) -> List[Tuple[str, str, float]]:
        """
        Find strongest pairwise synergies in team.

        Returns list of (name1, name2, synergy_score) tuples.
        """
        synergies = []

        for i, member1 in enumerate(members):
            for member2 in members[i + 1:]:
                if not (member1.reading and member2.reading):
                    continue

                score = self._calculate_pairwise_synergy(
                    member1.reading, member2.reading
                )
                synergies.append((member1.name, member2.name, score))

        # Sort by score and return top N
        synergies.sort(key=lambda x: x[2], reverse=True)
        return synergies[:top_n]

    def _calculate_pairwise_synergy(
        self,
        reading1: PersonalDevelopmentReading,
        reading2: PersonalDevelopmentReading,
    ) -> float:
        """Calculate synergy score between two individuals."""
        score = 70.0  # Base score

        # Life path compatibility
        if reading1.life_path_number and reading2.life_path_number:
            lp1 = reading1.life_path_number
            lp2 = reading2.life_path_number

            # Complementary pairs
            if (lp1, lp2) in [(1, 2), (2, 1), (3, 4), (4, 3), (5, 6), (6, 5), (7, 8), (8, 7)]:
                score += 15

            # Similar energy
            if lp1 == lp2:
                score += 10

        # Sun sign compatibility (if available)
        if reading1.sun_sign and reading2.sun_sign:
            # Simplified element compatibility
            fire_signs = ["Aries", "Leo", "Sagittarius"]
            earth_signs = ["Taurus", "Virgo", "Capricorn"]
            air_signs = ["Gemini", "Libra", "Aquarius"]
            water_signs = ["Cancer", "Scorpio", "Pisces"]

            sign1_element = None
            sign2_element = None

            for element, signs in [
                ("Fire", fire_signs),
                ("Earth", earth_signs),
                ("Air", air_signs),
                ("Water", water_signs),
            ]:
                if reading1.sun_sign in signs:
                    sign1_element = element
                if reading2.sun_sign in signs:
                    sign2_element = element

            # Fire/Air and Earth/Water are compatible
            if (sign1_element == "Fire" and sign2_element == "Air") or \
               (sign1_element == "Air" and sign2_element == "Fire") or \
               (sign1_element == "Earth" and sign2_element == "Water") or \
               (sign1_element == "Water" and sign2_element == "Earth"):
                score += 10

        return min(score, 100)

    def _build_communication_matrix(
        self, members: List[TeamMember]
    ) -> List[Dict[str, Any]]:
        """Build matrix of communication styles."""
        matrix = []

        for member in members:
            if not member.reading:
                continue

            style = "Balanced"
            if member.reading.life_path_number:
                lp = member.reading.life_path_number
                if lp in [1, 3, 5]:
                    style = "Direct & Expressive"
                elif lp in [2, 6, 9]:
                    style = "Empathetic & Relational"
                elif lp in [4, 7, 8]:
                    style = "Analytical & Structured"

            matrix.append({
                "name": member.name,
                "communication_style": style,
                "life_path": member.reading.life_path_number,
            })

        return matrix

    def _generate_team_coaching_prompts(
        self,
        members: List[TeamMember],
        compatibility: TeamCompatibilityScore,
    ) -> List[str]:
        """Generate coaching prompts for team development."""
        prompts = [
            "How do your individual strengths complement each other on this team?",
            "What communication patterns have you noticed in team interactions?",
            "Where do you see opportunities for deeper collaboration?",
            f"With {len(members)} different perspectives, how can you leverage this diversity?",
        ]

        if compatibility.overall_synergy < 70:
            prompts.append(
                "What can the team do to build more trust and understanding?"
            )
        else:
            prompts.append(
                "How can you build on your existing team synergy to achieve bigger goals?"
            )

        return prompts
