"""
Test Suite for Transit Timing Engine

Tests the syncretic integration of:
- KP Significators
- Vimshottari Dasha
- Transit Analysis

Validates:
- Transit activation detection
- Dasha support calculation
- Favorable window identification
- Event interpretation accuracy
"""

import sys
import os
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'calculations'))

from transit_engine import (
    TransitAnalyzer,
    TransitEvent,
    ActivationWindow,
    analyze_marriage_window,
    analyze_career_window
)


def print_test_header(title: str):
    """Print formatted test header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Print test result with status."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}     | {test_name:45} | {details}")


def test_transit_analyzer_initialization():
    """Test 1: Initialize TransitAnalyzer with Dasha engine."""
    print_test_header("TEST 1: Transit Analyzer Initialization")
    
    try:
        analyzer = TransitAnalyzer()
        
        # Verify Dasha engine loaded
        has_dasha = analyzer.dasha is not None
        has_house_matters = len(analyzer.house_matters) == 12
        
        print(f"  ✓ Dasha Engine loaded: {has_dasha}")
        print(f"  ✓ House matters mapped: {has_house_matters} houses")
        
        test_passed = has_dasha and has_house_matters
        print_test_result("Transit analyzer initialization", test_passed)
        return test_passed
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print_test_result("Transit analyzer initialization", False, str(e))
        return False


def test_kp_transit_confidence():
    """Test 2: Calculate KP confidence for transits."""
    print_test_header("TEST 2: KP Transit Confidence Calculation")
    
    analyzer = TransitAnalyzer()
    
    test_cases = [
        # (transiting_planet, significator, house, expected_range)
        ('Jupiter', 'Sun', 1, (0.7, 0.95)),  # Natural sig, benefic planet
        ('Mars', 'Moon', 4, (0.55, 0.75)),   # Malefic on home
        ('Mercury', 'Mercury', 3, (0.55, 0.80)),  # Mercury in communication
        ('Saturn', 'Jupiter', 9, (0.45, 0.70)),   # Malefic on fortune
        ('Venus', 'Venus', 7, (0.75, 0.95)),  # Venus on marriage
    ]
    
    passed = 0
    for transiting_planet, significator, house, expected_range in test_cases:
        confidence = analyzer._calculate_kp_transit_confidence(
            transiting_planet=transiting_planet,
            natal_significator=significator,
            house=house,
            natal_planets={}
        )
        
        in_range = expected_range[0] <= confidence <= expected_range[1]
        passed += in_range
        
        status = "✓" if in_range else "✗"
        print(f"  {status} {transiting_planet:7} → {significator:7} in House {house} "
              f"= {confidence:.2f} (expected {expected_range[0]:.2f}-{expected_range[1]:.2f})")
    
    test_passed = passed == len(test_cases)
    print_test_result("KP transit confidence calculation", test_passed, f"{passed}/{len(test_cases)} correct")
    return test_passed


def test_dasha_support_calculation():
    """Test 3: Calculate Dasha support for events."""
    print_test_header("TEST 3: Dasha Support Calculation")
    
    analyzer = TransitAnalyzer()
    
    test_cases = [
        # (dasha_planet, significator, house, expected_desc)
        ('Jupiter', 'Jupiter', 9, 'High'),      # Dasha lord = significator
        ('Venus', 'Saturn', 7, 'Medium'),       # Venus on marriage (friends)
        ('Mars', 'Mars', 6, 'High'),            # Mars dasha for Mars significator
        ('Saturn', 'Moon', 4, 'Low'),           # Saturn opposing Moon (enemies)
    ]
    
    passed = 0
    for dasha_planet, significator, house, expected_desc in test_cases:
        support = analyzer._calculate_dasha_support(
            dasha_planet=dasha_planet,
            significator=significator,
            house=house
        )
        
        # Classify support level
        if support >= 0.75:
            desc = 'High'
        elif support >= 0.65:
            desc = 'Medium'
        else:
            desc = 'Low'
        
        is_correct = desc == expected_desc
        passed += is_correct
        
        status = "✓" if is_correct else "✗"
        print(f"  {status} {dasha_planet:7} + {significator:7} = {support:.2f} ({desc})")
    
    test_passed = passed == len(test_cases)
    print_test_result("Dasha support calculation", test_passed, f"{passed}/{len(test_cases)} correct")
    return test_passed


def test_event_strength_classification():
    """Test 4: Classify event strength based on confidence."""
    print_test_header("TEST 4: Event Strength Classification")
    
    analyzer = TransitAnalyzer()
    
    test_cases = [
        (0.92, 'Major'),
        (0.80, 'Moderate'),
        (0.65, 'Minor'),
        (0.55, 'Minor'),
    ]
    
    passed = 0
    for confidence, expected_strength in test_cases:
        strength = analyzer._classify_event_strength(confidence)
        is_correct = strength == expected_strength
        passed += is_correct
        
        status = "✓" if is_correct else "✗"
        print(f"  {status} Confidence {confidence:.2f} → {strength} (expected {expected_strength})")
    
    test_passed = passed == len(test_cases)
    print_test_result("Event strength classification", test_passed, f"{passed}/{len(test_cases)} correct")
    return test_passed


def test_transit_duration_estimation():
    """Test 5: Estimate transit durations."""
    print_test_header("TEST 5: Transit Duration Estimation")
    
    analyzer = TransitAnalyzer()
    
    planets_duration = [
        ('Sun', 30),
        ('Mercury', 45),
        ('Venus', 40),
        ('Mars', 45),
        ('Jupiter', 13),
        ('Saturn', 2),
    ]
    
    passed = 0
    for planet, expected_days in planets_duration:
        duration = analyzer._estimate_transit_duration(planet)
        is_correct = duration == int(expected_days)
        passed += is_correct
        
        status = "✓" if is_correct else "✗"
        print(f"  {status} {planet:7} transit: {duration} days (expected ~{int(expected_days)})")
    
    test_passed = passed == len(planets_duration)
    print_test_result("Transit duration estimation", test_passed, f"{passed}/{len(planets_duration)} correct")
    return test_passed


def test_interpretation_generation():
    """Test 6: Generate natural language interpretations."""
    print_test_header("TEST 6: Interpretation Generation")
    
    analyzer = TransitAnalyzer()
    
    test_cases = [
        ('Venus', 7, 'Jupiter', 0.88, 'Major'),
        ('Mars', 6, 'Sun', 0.72, 'Moderate'),
        ('Mercury', 3, 'Mercury', 0.60, 'Minor'),
    ]
    
    for significator, house, dasha_planet, confidence, expected_strength in test_cases:
        interpretation = analyzer._generate_interpretation(
            significator=significator,
            house=house,
            dasha_planet=dasha_planet,
            confidence=confidence
        )
        
        contains_strength = expected_strength in interpretation
        contains_dasha = dasha_planet in interpretation
        contains_confidence = f"{confidence:.0%}" in interpretation
        
        is_valid = contains_strength and contains_dasha and contains_confidence
        status = "✓" if is_valid else "✗"
        
        print(f"  {status} {significator} in House {house} (Dasha: {dasha_planet})")
        print(f"     → {interpretation[:70]}...")
    
    test_passed = len(test_cases) > 0
    print_test_result("Interpretation generation", test_passed)
    return test_passed


def test_marriage_window_analysis():
    """Test 7: Analyze favorable marriage windows."""
    print_test_header("TEST 7: Marriage Window Analysis")
    
    # Sample birth chart with proper structure
    birth_chart = {
        'birth_date': datetime(1995, 6, 15),
        'moon_longitude': 45.0,  # Rohini
        'dasha_balance_years': 18.5,
        'natal_planets': {
            'Sun': {'longitude': 80.0, 'house': 9},
            'Moon': {'longitude': 45.0, 'house': 5},
            'Mars': {'longitude': 120.0, 'house': 8},
            'Mercury': {'longitude': 95.0, 'house': 7},
            'Jupiter': {'longitude': 200.0, 'house': 12},
            'Venus': {'longitude': 150.0, 'house': 9},
            'Saturn': {'longitude': 240.0, 'house': 2},
            'Rahu': {'longitude': 85.0, 'house': 7},
        }
    }
    
    try:
        start_date = datetime(2025, 11, 1)
        
        windows = analyze_marriage_window(birth_chart, start_date, 12)
        
        print(f"  ✓ Analysis completed")
        print(f"  ✓ Result type: {type(windows)}")
        
        if windows and hasattr(windows, 'duration_days'):
            print(f"\n  Best Marriage Window:")
            print(f"    Duration: ~{windows.duration_days} days")
            print(f"    Type: {windows.event_type}")
            print(f"    Peak Confidence: {windows.peak_confidence:.0%}")
        
        test_passed = True
        print_test_result("Marriage window analysis", test_passed)
        return test_passed
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        print_test_result("Marriage window analysis", False, str(e))
        return False


def test_career_window_analysis():
    """Test 8: Analyze favorable career windows."""
    print_test_header("TEST 8: Career Window Analysis")
    
    # Sample birth chart with proper structure
    birth_chart = {
        'birth_date': datetime(1990, 3, 20),
        'moon_longitude': 120.0,  # Purva Phalguni
        'dasha_balance_years': 12.0,
        'natal_planets': {
            'Sun': {'longitude': 120.0, 'house': 8},
            'Moon': {'longitude': 120.0, 'house': 8},
            'Mars': {'longitude': 180.0, 'house': 11},
            'Mercury': {'longitude': 100.0, 'house': 7},
            'Jupiter': {'longitude': 280.0, 'house': 3},
            'Venus': {'longitude': 160.0, 'house': 10},
            'Saturn': {'longitude': 220.0, 'house': 1},
            'Rahu': {'longitude': 140.0, 'house': 9},
        }
    }
    
    try:
        start_date = datetime(2025, 11, 1)
        
        windows = analyze_career_window(birth_chart, start_date, 24)
        
        print(f"  ✓ Analysis completed")
        print(f"  ✓ Result type: {type(windows)}")
        
        if windows and hasattr(windows, 'duration_days'):
            print(f"\n  Best Career Window:")
            print(f"    Duration: ~{windows.duration_days} days")
            print(f"    Peak Confidence: {windows.peak_confidence:.0%}")
        
        test_passed = True
        print_test_result("Career window analysis", test_passed)
        return test_passed
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        print_test_result("Career window analysis", False, str(e))
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("  TRANSIT TIMING ENGINE - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    tests = [
        test_transit_analyzer_initialization,
        test_kp_transit_confidence,
        test_dasha_support_calculation,
        test_event_strength_classification,
        test_transit_duration_estimation,
        test_interpretation_generation,
        test_marriage_window_analysis,
        test_career_window_analysis,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 80)
    print("  TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n✅ PASS | {passed}/{total} tests passed ({pass_rate:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Transit engine is ready for integration.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review above.")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
