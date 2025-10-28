"""
BMAD Behavior Models
Defines behavioral analysis models and prediction structures.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime


class BehaviorCategory(Enum):
    """Categories of behavior for analysis."""
    SOCIAL = "social"
    PROFESSIONAL = "professional"
    ROMANTIC = "romantic"
    FAMILY = "family"
    CREATIVE = "creative"
    SPIRITUAL = "spiritual"
    FINANCIAL = "financial"
    HEALTH = "health"
    COMMUNICATION = "communication"
    DECISION_MAKING = "decision_making"


class PredictionConfidence(Enum):
    """Confidence levels for behavioral predictions."""
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    VERY_HIGH = 5


class LifePhase(Enum):
    """Life phases for behavioral evolution tracking."""
    CHILDHOOD = "childhood"
    ADOLESCENCE = "adolescence"
    YOUNG_ADULT = "young_adult"
    ADULT = "adult"
    MIDDLE_AGE = "middle_age"
    SENIOR = "senior"


@dataclass
class BehaviorIndicator:
    """Individual behavioral indicator derived from astrological factors."""
    indicator_id: str
    name: str
    category: BehaviorCategory
    description: str
    intensity: float  # 0.0 to 1.0
    astrological_basis: Dict[str, str]  # source planets, aspects, houses
    manifestation_age: Optional[Tuple[int, int]] = None  # age range when most prominent
    life_phases: List[LifePhase] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert behavior indicator to dictionary format."""
        return {
            'indicator_id': self.indicator_id,
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'intensity': self.intensity,
            'astrological_basis': self.astrological_basis,
            'manifestation_age': self.manifestation_age,
            'life_phases': [phase.value for phase in self.life_phases]
        }


@dataclass
class BehaviorPrediction:
    """Prediction of future behavioral patterns."""
    prediction_id: str
    target_date: str  # ISO format date
    category: BehaviorCategory
    predicted_behaviors: List[str]
    confidence: PredictionConfidence
    astrological_transits: List[Dict[str, str]]  # transit data causing prediction
    duration_days: int
    intensity_curve: List[Tuple[str, float]]  # date, intensity pairs
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        """Convert behavior prediction to dictionary format."""
        return {
            'prediction_id': self.prediction_id,
            'target_date': self.target_date,
            'category': self.category.value,
            'predicted_behaviors': self.predicted_behaviors,
            'confidence': self.confidence.value,
            'astrological_transits': self.astrological_transits,
            'duration_days': self.duration_days,
            'intensity_curve': self.intensity_curve,
            'recommendations': self.recommendations
        }


@dataclass
class BehaviorEvolution:
    """Tracks how behaviors evolve over time."""
    evolution_id: str
    person_id: str
    start_date: str
    end_date: str
    category: BehaviorCategory
    baseline_indicators: List[BehaviorIndicator]
    evolved_indicators: List[BehaviorIndicator]
    key_transits: List[Dict[str, str]]  # major transits during this period
    milestones: List[Dict[str, str]]  # significant behavioral changes
    evolution_summary: str
    
    def to_dict(self) -> Dict:
        """Convert behavior evolution to dictionary format."""
        return {
            'evolution_id': self.evolution_id,
            'person_id': self.person_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'category': self.category.value,
            'baseline_indicators': [ind.to_dict() for ind in self.baseline_indicators],
            'evolved_indicators': [ind.to_dict() for ind in self.evolved_indicators],
            'key_transits': self.key_transits,
            'milestones': self.milestones,
            'evolution_summary': self.evolution_summary
        }


@dataclass
class BehaviorTrigger:
    """Astrological triggers that activate specific behaviors."""
    trigger_id: str
    name: str
    astrological_condition: Dict[str, str]  # specific aspect, transit, or progression
    triggered_behaviors: List[str]
    activation_probability: float  # 0.0 to 1.0
    duration_hours: int
    intensity_pattern: str  # gradual, immediate, wave, etc.
    historical_activations: List[str]  # dates when this trigger was active
    
    def to_dict(self) -> Dict:
        """Convert behavior trigger to dictionary format."""
        return {
            'trigger_id': self.trigger_id,
            'name': self.name,
            'astrological_condition': self.astrological_condition,
            'triggered_behaviors': self.triggered_behaviors,
            'activation_probability': self.activation_probability,
            'duration_hours': self.duration_hours,
            'intensity_pattern': self.intensity_pattern,
            'historical_activations': self.historical_activations
        }


@dataclass
class BehaviorProfile:
    """Complete behavioral profile for an individual."""
    profile_id: str
    person_name: str
    birth_data: Dict[str, any]
    current_indicators: List[BehaviorIndicator]
    behavior_triggers: List[BehaviorTrigger]
    future_predictions: List[BehaviorPrediction]
    evolution_history: List[BehaviorEvolution]
    dominant_categories: List[BehaviorCategory]
    behavioral_summary: str
    last_updated: str
    
    def get_indicators_by_category(self, category: BehaviorCategory) -> List[BehaviorIndicator]:
        """Get all behavior indicators for a specific category."""
        return [ind for ind in self.current_indicators if ind.category == category]
    
    def get_active_triggers(self, current_date: str) -> List[BehaviorTrigger]:
        """Get triggers that might be active around the current date."""
        # This would need to be implemented with actual transit calculations
        return self.behavior_triggers
    
    def to_dict(self) -> Dict:
        """Convert behavior profile to dictionary format."""
        return {
            'profile_id': self.profile_id,
            'person_name': self.person_name,
            'birth_data': self.birth_data,
            'current_indicators': [ind.to_dict() for ind in self.current_indicators],
            'behavior_triggers': [trigger.to_dict() for trigger in self.behavior_triggers],
            'future_predictions': [pred.to_dict() for pred in self.future_predictions],
            'evolution_history': [evo.to_dict() for evo in self.evolution_history],
            'dominant_categories': [cat.value for cat in self.dominant_categories],
            'behavioral_summary': self.behavioral_summary,
            'last_updated': self.last_updated
        }