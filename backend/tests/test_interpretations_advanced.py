"""
Advanced Test Suite for Unified Interpretation System
"""

import pytest
from backend.interpretations import InterpretationEngine
from backend.interpretations.core import PlanetInterpreter, HouseInterpreter, AspectInterpreter
from backend.interpretations.synastry import (
    InterAspectInterpreter,
    HouseOverlayInterpreter,
    LunarMansionSynastryInterpreter
)


def test_engine_comprehensive_integration():
    """Test full engine integration with mock chart data"""
    engine = InterpretationEngine()
    chart_data = {
        "planets": [
            {"name": "Sun", "sign": "Aries", "house": 1},
            {"name": "Moon", "sign": "Taurus", "house": 4}
        ],
        "aspects": [
            {"planet1": "Sun", "planet2": "Moon", "type": "trine"}
        ]
    }
    result = engine.interpret_birth_chart(chart_data)
    assert isinstance(result, dict)
    assert len(result["planets"]) == 2
    assert len(result["aspects"]) == 1
    assert "title" in result["planets"][0]["sign_interpretation"]
    assert "description" in result["aspects"][0]


def test_synastry_engine_comprehensive():
    """Test synastry engine with mock chart data and Nakshatra compatibility"""
    engine = InterpretationEngine()
    chart1 = {"moon_nakshatra": "Ashwini"}
    chart2 = {"moon_nakshatra": "Rohini"}
    result = engine.interpret_synastry(chart1, chart2)
    assert isinstance(result, dict)
    assert "nakshatra_compatibility" in result
    compat = result["nakshatra_compatibility"]
    assert "compatibility_score" in compat
    assert 0.0 <= compat["compatibility_score"] <= 1.0
    assert compat["category"] in ["excellent", "good", "neutral", "challenging"]


def test_planet_interpreter_edge_cases():
    """Test planet interpreter with unknown planet/sign"""
    interpreter = PlanetInterpreter()
    result = interpreter.interpret_planet_in_sign("Unknown", "UnknownSign")
    assert result["description"].startswith("Interpretation pending")


def test_house_interpreter_edge_cases():
    """Test house interpreter with invalid house number"""
    interpreter = HouseInterpreter()
    result = interpreter.interpret_planet_in_house("Sun", 99)
    assert result["description"].startswith("Interpretation pending")


def test_aspect_interpreter_all_major_aspects():
    """Test aspect interpreter for all major aspects"""
    interpreter = AspectInterpreter()
    for aspect in interpreter.MAJOR_ASPECTS.keys():
        result = interpreter.interpret_aspect("Sun", "Moon", aspect)
        assert "title" in result
        assert result["nature"] in ["harmonious", "challenging", "neutral"]


def test_inter_aspect_interpreter_edge_case():
    """Test inter-aspect interpreter with unknown aspect"""
    interpreter = InterAspectInterpreter()
    result = interpreter.interpret_inter_aspect("Foo", "Bar", "baz")
    assert result["description"].startswith("Interpretation pending")


def test_house_overlay_interpreter_edge_case():
    """Test house overlay interpreter with invalid house"""
    interpreter = HouseOverlayInterpreter()
    result = interpreter.interpret_house_overlay("Sun", 99)
    assert result["description"].startswith("Interpretation pending")


def test_lunar_mansion_synastry_edge_case():
    """Test Nakshatra synastry with unknown nakshatras"""
    interpreter = LunarMansionSynastryInterpreter()
    result = interpreter.interpret_nakshatra_compatibility("Unknown1", "Unknown2")
    assert result["description"].startswith("Interpretation pending")
