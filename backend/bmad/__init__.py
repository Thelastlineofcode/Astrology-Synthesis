"""
BMAD - Behavioral Model and Data
Astrological personality and behavioral analysis framework.

This module provides comprehensive tools for analyzing personality traits
and behavioral patterns based on astrological chart data.
"""

from .models import *
from .services import PersonalityAnalyzer, BehaviorPredictor
from .api import bmad_bp
from .config import BMADConfig, get_config

__version__ = "1.0.0"

__all__ = [
    # Main classes
    'PersonalityAnalyzer',
    'BehaviorPredictor',
    'BMADConfig',
    
    # API
    'bmad_bp',
    
    # Configuration
    'get_config',
    
    # Version
    '__version__'
]