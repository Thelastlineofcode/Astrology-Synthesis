#!/usr/bin/env python3
"""
Standalone Chart Validation Test Runner
Runs without pytest to avoid import issues
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.calculation_service import CalculationService
from schemas import BirthDataInput


def test_sun_position():
    """Test Sun position calculation"""
    print("\n=== Testing Sun Position ===")
    calc_service = CalculationService()
    
    birth_data = BirthDataInput(
        date="1984-12-19",
        time="12:00:00",
        timezone="America/Chicago",
        latitude=29.9844,
        longitude=-90.1547,
        location_name="Metairie, LA"
    )
    
    chart = calc_service.generate_birth_chart(birth_data)
    sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
    
    print(f"Sun Position: {sun['longitude']:.2f}°")
    print(f"Zodiac Sign: {sun['zodiac_sign']}")
    print(f"House: {sun['house']}")
    print(f"Nakshatra: {sun['nakshatra']}, Pada {sun['pada']}")
    print(f"Retrograde: {sun['retrograde']}")
    
    assert sun["zodiac_sign"] == "Sagittarius", f"Expected Sagittarius, got {sun['zodiac_sign']}"
    assert 240 <= sun["longitude"] < 270, f"Sun at {sun['longitude']}° not in Sagittarius range"
    print("✅ Sun position test PASSED")
    

def test_all_planets():
    """Test that all planets are present"""
    print("\n=== Testing All Planets Present ===")
    calc_service = CalculationService()
    
    birth_data = BirthDataInput(
        date="1984-12-19",
        time="12:00:00",
        timezone="America/Chicago",
        latitude=29.9844,
        longitude=-90.1547,
        location_name="Metairie, LA"
    )
    
    chart = calc_service.generate_birth_chart(birth_data)
    planets = [p["planet"] for p in chart["planet_positions"]]
    
    expected = ["Sun", "Moon", "Mercury", "Venus", "Mars", 
               "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
               "Rahu", "Ketu"]
    
    for planet in expected:
        assert planet in planets, f"{planet} missing"
        print(f"✓ {planet} present")
    
    print(f"✅ All {len(planets)} planets test PASSED")


def test_house_cusps():
    """Test house cusp calculations"""
    print("\n=== Testing House Cusps ===")
    calc_service = CalculationService()
    
    birth_data = BirthDataInput(
        date="1984-12-19",
        time="12:00:00",
        timezone="America/Chicago",
        latitude=29.9844,
        longitude=-90.1547,
        location_name="Metairie, LA"
    )
    
    chart = calc_service.generate_birth_chart(birth_data)
    
    assert len(chart["house_cusps"]) == 12, f"Expected 12 houses, got {len(chart['house_cusps'])}"
    
    for cusp in chart["house_cusps"]:
        print(f"House {cusp['house']}: {cusp['longitude']:.2f}° ({cusp['zodiac_sign']})")
        assert "house" in cusp
        assert "longitude" in cusp
        assert "zodiac_sign" in cusp
        assert 0 <= cusp["longitude"] < 360
    
    print("✅ House cusps test PASSED")


def test_nakshatras():
    """Test nakshatra assignments"""
    print("\n=== Testing Nakshatras ===")
    calc_service = CalculationService()
    
    birth_data = BirthDataInput(
        date="1984-12-19",
        time="12:00:00",
        timezone="America/Chicago",
        latitude=29.9844,
        longitude=-90.1547,
        location_name="Metairie, LA"
    )
    
    chart = calc_service.generate_birth_chart(birth_data)
    
    for planet in chart["planet_positions"]:
        if planet["planet"] not in ["Rahu", "Ketu"]:
            assert "nakshatra" in planet
            assert "pada" in planet
            assert 1 <= planet["pada"] <= 4
            print(f"{planet['planet']}: {planet['nakshatra']} Pada {planet['pada']}")
    
    print("✅ Nakshatra test PASSED")


def test_aspects():
    """Test aspect calculations"""
    print("\n=== Testing Aspects ===")
    calc_service = CalculationService()
    
    birth_data = BirthDataInput(
        date="1984-12-19",
        time="12:00:00",
        timezone="America/Chicago",
        latitude=29.9844,
        longitude=-90.1547,
        location_name="Metairie, LA"
    )
    
    chart = calc_service.generate_birth_chart(birth_data)
    
    assert "aspects" in chart
    print(f"Found {len(chart['aspects'])} aspects")
    
    for aspect in chart["aspects"][:5]:  # Show first 5
        print(f"{aspect['planet1']} {aspect['aspect_type']} {aspect['planet2']} (orb: {aspect['orb']:.2f}°)")
    
    print("✅ Aspects test PASSED")


def test_retrograde_detection():
    """Test retrograde detection"""
    print("\n=== Testing Retrograde Detection ===")
    calc_service = CalculationService()
    
    birth_data = BirthDataInput(
        date="1984-12-19",
        time="12:00:00",
        timezone="America/Chicago",
        latitude=29.9844,
        longitude=-90.1547,
        location_name="Metairie, LA"
    )
    
    chart = calc_service.generate_birth_chart(birth_data)
    
    retrograde_planets = [p["planet"] for p in chart["planet_positions"] if p.get("retrograde")]
    
    print(f"Retrograde planets: {', '.join(retrograde_planets) if retrograde_planets else 'None'}")
    
    for planet in chart["planet_positions"]:
        assert "retrograde" in planet
        assert isinstance(planet["retrograde"], bool)
    
    print("✅ Retrograde detection test PASSED")


def run_all_tests():
    """Run all validation tests"""
    print("=" * 60)
    print("CHART CALCULATION VALIDATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_sun_position,
        test_all_planets,
        test_house_cusps,
        test_nakshatras,
        test_aspects,
        test_retrograde_detection,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
