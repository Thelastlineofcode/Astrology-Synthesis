"""
BMAD Personality Model
Defines behavioral and personality traits derived from astrological data.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from enum import Enum


class PersonalityDimension(Enum):
    """Core personality dimensions for behavioral analysis."""
    EXTRAVERSION = "extraversion"
    AGREEABLENESS = "agreeableness"
    CONSCIENTIOUSNESS = "conscientiousness"
    NEUROTICISM = "neuroticism"
    OPENNESS = "openness"
    ASSERTIVENESS = "assertiveness"
    EMOTIONAL_STABILITY = "emotional_stability"
    CREATIVITY = "creativity"
    LEADERSHIP = "leadership"
    COMMUNICATION = "communication"


class IntensityLevel(Enum):
    """Intensity levels for traits and behaviors."""
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5


@dataclass
class Trait:
    """Individual personality trait with intensity and astrological influence."""
    name: str
    dimension: PersonalityDimension
    intensity: IntensityLevel
    description: str
    astrological_source: Dict[str, Union[str, float]]  # planet, aspect, house, etc.
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert trait to dictionary format."""
        return {
            'name': self.name,
            'dimension': self.dimension.value,
            'intensity': self.intensity.value,
            'description': self.description,
            'astrological_source': self.astrological_source,
            'keywords': self.keywords
        }


@dataclass
class BehavioralPattern:
    """Behavioral pattern derived from multiple astrological factors."""
    pattern_id: str
    name: str
    description: str
    probability: float  # 0.0 to 1.0
    triggers: List[Dict[str, str]]  # astrological conditions that trigger this pattern
    manifestations: List[str]  # how this pattern shows up in behavior
    related_traits: List[str]  # trait names that relate to this pattern
    
    def to_dict(self) -> Dict:
        """Convert behavioral pattern to dictionary format."""
        return {
            'pattern_id': self.pattern_id,
            'name': self.name,
            'description': self.description,
            'probability': self.probability,
            'triggers': self.triggers,
            'manifestations': self.manifestations,
            'related_traits': self.related_traits
        }


@dataclass
class PersonalityProfile:
    """Complete personality profile containing traits and behavioral patterns."""
    profile_id: str
    name: str
    birth_data: Dict[str, Union[str, int, float]]
    traits: List[Trait]
    behavioral_patterns: List[BehavioralPattern]
    dominant_dimensions: List[PersonalityDimension]
    summary: str
    created_timestamp: str
    chart_data_reference: Optional[Dict] = None
    
    def get_trait_by_dimension(self, dimension: PersonalityDimension) -> List[Trait]:
        """Get all traits for a specific personality dimension."""
        return [trait for trait in self.traits if trait.dimension == dimension]
    
    def get_dominant_trait_intensity(self) -> Dict[PersonalityDimension, IntensityLevel]:
        """Get the dominant intensity level for each personality dimension."""
        dimension_intensities = {}
        for dimension in PersonalityDimension:
            traits = self.get_trait_by_dimension(dimension)
            if traits:
                max_intensity = max(trait.intensity for trait in traits)
                dimension_intensities[dimension] = max_intensity
        return dimension_intensities
    
    def to_dict(self) -> Dict:
        """Convert personality profile to dictionary format."""
        return {
            'profile_id': self.profile_id,
            'name': self.name,
            'birth_data': self.birth_data,
            'traits': [trait.to_dict() for trait in self.traits],
            'behavioral_patterns': [pattern.to_dict() for pattern in self.behavioral_patterns],
            'dominant_dimensions': [dim.value for dim in self.dominant_dimensions],
            'summary': self.summary,
            'created_timestamp': self.created_timestamp,
            'chart_data_reference': self.chart_data_reference
        }


@dataclass
class CompatibilityAnalysis:
    """Compatibility analysis between two personality profiles."""
    profile1_id: str
    profile2_id: str
    overall_compatibility: float  # 0.0 to 1.0
    dimension_compatibility: Dict[PersonalityDimension, float]
    strengths: List[str]
    challenges: List[str]
    recommendations: List[str]
    synastry_influences: List[Dict[str, Union[str, float]]]
    
    def to_dict(self) -> Dict:
        """Convert compatibility analysis to dictionary format."""
        return {
            'profile1_id': self.profile1_id,
            'profile2_id': self.profile2_id,
            'overall_compatibility': self.overall_compatibility,
            'dimension_compatibility': {dim.value: score for dim, score in self.dimension_compatibility.items()},
            'strengths': self.strengths,
            'challenges': self.challenges,
            'recommendations': self.recommendations,
            'synastry_influences': self.synastry_influences
        }