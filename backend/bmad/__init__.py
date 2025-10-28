"""
BMAD - Behavioral Model and Data
Astrological personality and behavioral analysis framework.

This module provides comprehensive tools for analyzing personality traits
and behavioral patterns based on astrological chart data.
"""

from .models import *
from .services import PersonalityAnalyzer, BehaviorPredictor
from .config import BMADConfig, get_config

__version__ = "1.0.0"

# Conditionally import API components (requires Flask)
try:
    from .api import bmad_bp
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
except ImportError:
    # Flask not available, API disabled
    __all__ = [
        # Main classes
        'PersonalityAnalyzer',
        'BehaviorPredictor',
        'BMADConfig',
        
        # Configuration
        'get_config',
        
        # Version
        '__version__'
    ]