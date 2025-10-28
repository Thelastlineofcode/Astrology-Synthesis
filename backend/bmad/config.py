"""
BMAD Configuration
Configuration settings and parameters for Behavioral Model and Data analysis.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import os


@dataclass
class PersonalityConfig:
    """Configuration for personality analysis."""
    default_intensity_threshold: float = 0.5
    trait_calculation_precision: int = 3
    enable_aspect_traits: bool = True
    enable_house_traits: bool = True
    enable_sign_traits: bool = True
    compatibility_algorithm: str = "dimensional_weighted"
    max_traits_per_dimension: int = 10


@dataclass
class BehaviorConfig:
    """Configuration for behavioral analysis."""
    prediction_confidence_threshold: float = 0.3
    default_prediction_days: int = 30
    max_prediction_days: int = 365
    behavior_intensity_scale: str = "logarithmic"  # linear, logarithmic, exponential
    enable_trigger_analysis: bool = True
    trigger_sensitivity: float = 0.6
    evolution_analysis_granularity: str = "monthly"  # daily, weekly, monthly


@dataclass
class AnalysisConfig:
    """Configuration for analysis algorithms."""
    orb_precision: float = 0.1
    aspect_orb_multiplier: float = 1.0
    house_cusp_sensitivity: float = 2.0  # degrees
    planetary_strength_weights: Dict[str, float] = None
    sign_element_weights: Dict[str, float] = None
    house_angular_bonus: float = 1.2


@dataclass
class APIConfig:
    """Configuration for BMAD API behavior."""
    enable_debug_mode: bool = False
    max_request_size_mb: int = 10
    rate_limit_per_minute: int = 60
    cache_analysis_results: bool = True
    cache_expiry_hours: int = 24
    enable_request_logging: bool = True


class BMADConfig:
    """Main BMAD configuration class."""
    
    def __init__(self):
        self.personality = PersonalityConfig()
        self.behavior = BehaviorConfig()
        self.analysis = AnalysisConfig()
        self.api = APIConfig()
        
        # Initialize default planetary weights
        self.analysis.planetary_strength_weights = self._get_default_planetary_weights()
        self.analysis.sign_element_weights = self._get_default_element_weights()
        
        # Load configuration from environment variables if available
        self._load_from_environment()
    
    def _get_default_planetary_weights(self) -> Dict[str, float]:
        """Get default planetary strength weights for analysis."""
        return {
            'Sun': 1.0,
            'Moon': 0.9,
            'Mercury': 0.7,
            'Venus': 0.7,
            'Mars': 0.8,
            'Jupiter': 0.8,
            'Saturn': 0.8,
            'Uranus': 0.6,
            'Neptune': 0.5,
            'Pluto': 0.6,
            'North Node': 0.4,
            'South Node': 0.4,
            'Chiron': 0.3
        }
    
    def _get_default_element_weights(self) -> Dict[str, float]:
        """Get default element weights for analysis."""
        return {
            'Fire': 1.0,
            'Earth': 1.0,
            'Air': 1.0,
            'Water': 1.0
        }
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        # Personality config
        if os.getenv('BMAD_PERSONALITY_INTENSITY_THRESHOLD'):
            self.personality.default_intensity_threshold = float(
                os.getenv('BMAD_PERSONALITY_INTENSITY_THRESHOLD')
            )
        
        if os.getenv('BMAD_PERSONALITY_PRECISION'):
            self.personality.trait_calculation_precision = int(
                os.getenv('BMAD_PERSONALITY_PRECISION')
            )
        
        # Behavior config
        if os.getenv('BMAD_BEHAVIOR_CONFIDENCE_THRESHOLD'):
            self.behavior.prediction_confidence_threshold = float(
                os.getenv('BMAD_BEHAVIOR_CONFIDENCE_THRESHOLD')
            )
        
        if os.getenv('BMAD_BEHAVIOR_DEFAULT_DAYS'):
            self.behavior.default_prediction_days = int(
                os.getenv('BMAD_BEHAVIOR_DEFAULT_DAYS')
            )
        
        # Analysis config
        if os.getenv('BMAD_ANALYSIS_ORB_PRECISION'):
            self.analysis.orb_precision = float(
                os.getenv('BMAD_ANALYSIS_ORB_PRECISION')
            )
        
        # API config
        if os.getenv('BMAD_API_DEBUG_MODE'):
            self.api.enable_debug_mode = os.getenv('BMAD_API_DEBUG_MODE').lower() == 'true'
        
        if os.getenv('BMAD_API_RATE_LIMIT'):
            self.api.rate_limit_per_minute = int(
                os.getenv('BMAD_API_RATE_LIMIT')
            )
    
    def get_trait_rules_path(self) -> str:
        """Get the path to trait analysis rules file."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_dir, 'content', 'trait_rules.json')
    
    def get_behavior_rules_path(self) -> str:
        """Get the path to behavior analysis rules file."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_dir, 'content', 'behavior_rules.json')
    
    def get_pattern_rules_path(self) -> str:
        """Get the path to pattern analysis rules file."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_dir, 'content', 'pattern_rules.json')
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary format."""
        return {
            'personality': {
                'default_intensity_threshold': self.personality.default_intensity_threshold,
                'trait_calculation_precision': self.personality.trait_calculation_precision,
                'enable_aspect_traits': self.personality.enable_aspect_traits,
                'enable_house_traits': self.personality.enable_house_traits,
                'enable_sign_traits': self.personality.enable_sign_traits,
                'compatibility_algorithm': self.personality.compatibility_algorithm,
                'max_traits_per_dimension': self.personality.max_traits_per_dimension
            },
            'behavior': {
                'prediction_confidence_threshold': self.behavior.prediction_confidence_threshold,
                'default_prediction_days': self.behavior.default_prediction_days,
                'max_prediction_days': self.behavior.max_prediction_days,
                'behavior_intensity_scale': self.behavior.behavior_intensity_scale,
                'enable_trigger_analysis': self.behavior.enable_trigger_analysis,
                'trigger_sensitivity': self.behavior.trigger_sensitivity,
                'evolution_analysis_granularity': self.behavior.evolution_analysis_granularity
            },
            'analysis': {
                'orb_precision': self.analysis.orb_precision,
                'aspect_orb_multiplier': self.analysis.aspect_orb_multiplier,
                'house_cusp_sensitivity': self.analysis.house_cusp_sensitivity,
                'planetary_strength_weights': self.analysis.planetary_strength_weights,
                'sign_element_weights': self.analysis.sign_element_weights,
                'house_angular_bonus': self.analysis.house_angular_bonus
            },
            'api': {
                'enable_debug_mode': self.api.enable_debug_mode,
                'max_request_size_mb': self.api.max_request_size_mb,
                'rate_limit_per_minute': self.api.rate_limit_per_minute,
                'cache_analysis_results': self.api.cache_analysis_results,
                'cache_expiry_hours': self.api.cache_expiry_hours,
                'enable_request_logging': self.api.enable_request_logging
            }
        }


# Global configuration instance
bmad_config = BMADConfig()


def get_config() -> BMADConfig:
    """Get the global BMAD configuration instance."""
    return bmad_config


def update_config(**kwargs):
    """Update configuration values dynamically."""
    config = get_config()
    
    for section, values in kwargs.items():
        if hasattr(config, section):
            section_config = getattr(config, section)
            for key, value in values.items():
                if hasattr(section_config, key):
                    setattr(section_config, key, value)


# Configuration validation functions
def validate_personality_config(config: PersonalityConfig) -> List[str]:
    """Validate personality configuration and return any errors."""
    errors = []
    
    if not 0 <= config.default_intensity_threshold <= 1:
        errors.append("default_intensity_threshold must be between 0 and 1")
    
    if config.trait_calculation_precision < 1:
        errors.append("trait_calculation_precision must be at least 1")
    
    if config.max_traits_per_dimension < 1:
        errors.append("max_traits_per_dimension must be at least 1")
    
    return errors


def validate_behavior_config(config: BehaviorConfig) -> List[str]:
    """Validate behavior configuration and return any errors."""
    errors = []
    
    if not 0 <= config.prediction_confidence_threshold <= 1:
        errors.append("prediction_confidence_threshold must be between 0 and 1")
    
    if config.default_prediction_days < 1:
        errors.append("default_prediction_days must be at least 1")
    
    if config.max_prediction_days < config.default_prediction_days:
        errors.append("max_prediction_days must be >= default_prediction_days")
    
    if not 0 <= config.trigger_sensitivity <= 1:
        errors.append("trigger_sensitivity must be between 0 and 1")
    
    valid_scales = ['linear', 'logarithmic', 'exponential']
    if config.behavior_intensity_scale not in valid_scales:
        errors.append(f"behavior_intensity_scale must be one of: {valid_scales}")
    
    valid_granularities = ['daily', 'weekly', 'monthly']
    if config.evolution_analysis_granularity not in valid_granularities:
        errors.append(f"evolution_analysis_granularity must be one of: {valid_granularities}")
    
    return errors


def validate_analysis_config(config: AnalysisConfig) -> List[str]:
    """Validate analysis configuration and return any errors."""
    errors = []
    
    if config.orb_precision <= 0:
        errors.append("orb_precision must be greater than 0")
    
    if config.aspect_orb_multiplier <= 0:
        errors.append("aspect_orb_multiplier must be greater than 0")
    
    if config.house_cusp_sensitivity <= 0:
        errors.append("house_cusp_sensitivity must be greater than 0")
    
    if config.house_angular_bonus < 1:
        errors.append("house_angular_bonus should be >= 1 to provide actual bonus")
    
    return errors


def validate_api_config(config: APIConfig) -> List[str]:
    """Validate API configuration and return any errors."""
    errors = []
    
    if config.max_request_size_mb < 1:
        errors.append("max_request_size_mb must be at least 1")
    
    if config.rate_limit_per_minute < 1:
        errors.append("rate_limit_per_minute must be at least 1")
    
    if config.cache_expiry_hours < 1:
        errors.append("cache_expiry_hours must be at least 1")
    
    return errors


def validate_full_config(config: BMADConfig) -> Dict[str, List[str]]:
    """Validate entire BMAD configuration and return errors by section."""
    validation_results = {}
    
    personality_errors = validate_personality_config(config.personality)
    if personality_errors:
        validation_results['personality'] = personality_errors
    
    behavior_errors = validate_behavior_config(config.behavior)
    if behavior_errors:
        validation_results['behavior'] = behavior_errors
    
    analysis_errors = validate_analysis_config(config.analysis)
    if analysis_errors:
        validation_results['analysis'] = analysis_errors
    
    api_errors = validate_api_config(config.api)
    if api_errors:
        validation_results['api'] = api_errors
    
    return validation_results