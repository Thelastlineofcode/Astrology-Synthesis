"""
BMAD Models Package
Behavioral Model and Data models for astrological personality and behavior analysis.
"""

from .personality import (
    PersonalityDimension,
    IntensityLevel,
    Trait,
    BehavioralPattern,
    PersonalityProfile,
    CompatibilityAnalysis
)

from .behavior import (
    BehaviorCategory,
    PredictionConfidence,
    LifePhase,
    BehaviorIndicator,
    BehaviorPrediction,
    BehaviorEvolution,
    BehaviorTrigger,
    BehaviorProfile
)

__all__ = [
    # Personality models
    'PersonalityDimension',
    'IntensityLevel',
    'Trait',
    'BehavioralPattern',
    'PersonalityProfile',
    'CompatibilityAnalysis',
    
    # Behavior models
    'BehaviorCategory',
    'PredictionConfidence',
    'LifePhase',
    'BehaviorIndicator',
    'BehaviorPrediction',
    'BehaviorEvolution',
    'BehaviorTrigger',
    'BehaviorProfile'
]