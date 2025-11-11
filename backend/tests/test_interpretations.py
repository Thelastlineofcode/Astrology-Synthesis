"""
Test suite for unified interpretation system
"""

import pytest
from backend.interpretations import InterpretationEngine
from backend.interpretations.core import PlanetInterpreter, HouseInterpreter, AspectInterpreter
from backend.interpretations.synastry import (
    InterAspectInterpreter,
    HouseOverlayInterpreter,
    LunarMansionSynastryInterpreter
)


def test_engine_initialization():
    """Test that interpretation engine initializes all subsystems"""
    engine = InterpretationEngine()
    assert engine.planets is not None
    assert engine.houses is not None
    assert engine.aspects is not None
    assert engine.inter_aspects is not None
    assert engine.house_overlays is not None
    assert engine.nakshatra_synastry is not None


def test_planet_interpreter():
    """Test planet interpretation returns expected structure"""
    interpreter = PlanetInterpreter()
    result = interpreter.interpret_planet_in_sign("Sun", "Aries")
    
    assert "title" in result
    assert "keywords" in result
    assert "description" in result
    assert "strengths" in result
    assert "challenges" in result


def test_house_interpreter():
    """Test house interpretation returns expected structure"""
    interpreter = HouseInterpreter()
    result = interpreter.interpret_planet_in_house("Moon", 4)
    
    assert "title" in result
    assert "keywords" in result
    assert "description" in result
    assert "life_areas" in result


def test_aspect_interpreter():
    """Test aspect interpretation returns expected structure"""
    interpreter = AspectInterpreter()
    result = interpreter.interpret_aspect("Venus", "Mars", "trine")
    
    assert "title" in result
    assert "nature" in result
    assert "description" in result
    assert result["nature"] in ["harmonious", "challenging", "neutral"]


def test_inter_aspect_interpreter():
    """Test synastry aspect interpretation"""
    interpreter = InterAspectInterpreter()
    result = interpreter.interpret_inter_aspect("Venus", "Mars", "trine")
    
    assert "title" in result
    assert "compatibility_score" in result
    assert "description" in result
    assert 0.0 <= result["compatibility_score"] <= 1.0


def test_nakshatra_synastry():
    """Test Nakshatra compatibility interpretation"""
    interpreter = LunarMansionSynastryInterpreter()
    result = interpreter.interpret_nakshatra_compatibility("Ashwini", "Rohini")
    
    assert "compatibility_score" in result
    assert "category" in result
    assert "description" in result
    assert result["category"] in ["excellent", "good", "neutral", "challenging"]
