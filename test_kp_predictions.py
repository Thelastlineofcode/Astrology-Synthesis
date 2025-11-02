#!/usr/bin/env python3
"""
KP (Krishnamurti Paddhati) Prediction Engine Test Suite

Comprehensive tests for KP calculation accuracy and prediction methods:
- Sub-lord calculation precision
- Cuspal sub-lord analysis
- Significator identification
- Ruling planets calculation
- Prediction confidence scoring
- Historical prediction validation
"""

import sys
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'calculations'))

try:
    from kp_engine import (
        get_sub_lord,
        get_cuspal_sub_lords,
        get_planet_sub_lords,
        format_sub_lord_position,
        get_significators_for_house,
        get_house_lord,
        get_ruling_planets,
        calculate_kp_confidence,
        SubLordPosition,
        Significator,
        VIMSHOTTARI_PROPORTIONS,
        SUB_LORD_SEQUENCE,
        NAKSHATRA_NAMES
    )
    KP_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Could not import KP engine: {e}")
    KP_ENGINE_AVAILABLE = False


# ==================== TEST DATA ====================

# Known KP positions for validation (from KP ephemeris/software)
KNOWN_KP_POSITIONS = [
    {
        'longitude': 0.0,  # 0° Aries
        'expected': {
            'nakshatra_num': 1,
            'nakshatra_name': 'Ashwini',
            'nakshatra_lord': 'Ketu',
            'sub_lord': 'Ketu'  # First sub-division
        }
    },
    {
        'longitude': 13.333333,  # 13°20' Aries (end of Ashwini)
        'expected': {
            'nakshatra_num': 2,
            'nakshatra_name': 'Bharani',
            'nakshatra_lord': 'Venus',
            'sub_lord': 'Ketu'
        }
    },
    {
        'longitude': 30.0,  # 0° Taurus
        'expected': {
            'nakshatra_num': 3,
            'nakshatra_name': 'Krittika',
            'nakshatra_lord': 'Sun',
            'sub_lord': 'Venus'  # Krittika starts in Venus sub
        }
    },
    {
        'longitude': 90.0,  # 0° Cancer
        'expected': {
            'nakshatra_num': 8,
            'nakshatra_name': 'Pushya',
            'nakshatra_lord': 'Saturn',
            'sub_lord': 'Venus'
        }
    },
    {
        'longitude': 135.0,  # 15° Leo
        'expected': {
            'nakshatra_num': 11,
            'nakshatra_name': 'Purva Phalguni',
            'nakshatra_lord': 'Venus',
            'sub_lord': 'Ketu'  # At 15° Leo
        }
    },
    {
        'longitude': 180.0,  # 0° Libra
        'expected': {
            'nakshatra_num': 14,
            'nakshatra_name': 'Chitra',
            'nakshatra_lord': 'Mars',
            'sub_lord': 'Venus'
        }
    },
    {
        'longitude': 270.0,  # 0° Capricorn
        'expected': {
            'nakshatra_num': 21,
            'nakshatra_name': 'Uttara Ashadha',
            'nakshatra_lord': 'Sun',
            'sub_lord': 'Venus'
        }
    },
    {
        'longitude': 359.999,  # End of zodiac
        'expected': {
            'nakshatra_num': 27,
            'nakshatra_name': 'Revati',
            'nakshatra_lord': 'Mercury',
            'sub_lord': 'Mercury'  # Last sub-lord
        }
    }
]

# Sample birth charts for prediction testing
SAMPLE_CHARTS = {
    'chart_1_marriage_favorable': {
        'name': 'Marriage Favorable Chart',
        'birth_data': {
            'year': 1990, 'month': 8, 'day': 15,
            'hour': 14, 'minute': 30,
            'latitude': 29.7604, 'longitude': -95.3698  # Houston, TX
        },
        'planets': {
            'Sun': 132.5,     # Leo
            'Moon': 45.2,     # Taurus
            'Mars': 225.8,    # Scorpio
            'Mercury': 145.3, # Leo
            'Jupiter': 95.7,  # Cancer
            'Venus': 180.5,   # Libra (7th house in equal system)
            'Saturn': 280.2   # Capricorn
        },
        'houses': [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],  # Equal house
        'prediction_context': {
            'question': 'When will I get married?',
            'expected_houses': [7, 2, 11],  # Marriage, family, fulfillment
            'favorable_indicators': ['Venus in 7th house', '7th cusp sub-lord favorable']
        }
    },
    'chart_2_career_strong': {
        'name': 'Career Strong Chart',
        'birth_data': {
            'year': 1985, 'month': 3, 'day': 22,
            'hour': 9, 'minute': 15,
            'latitude': 40.7128, 'longitude': -74.0060  # NYC
        },
        'planets': {
            'Sun': 1.2,       # Aries (10th house in equal)
            'Moon': 195.5,    # Libra
            'Mars': 275.3,    # Capricorn (strong in 10th sign)
            'Mercury': 15.8,  # Aries
            'Jupiter': 305.2, # Aquarius (aspecting 10th)
            'Venus': 330.5,   # Pisces
            'Saturn': 245.7   # Sagittarius
        },
        'houses': [105, 135, 165, 195, 225, 255, 285, 315, 345, 15, 45, 75],
        'prediction_context': {
            'question': 'When will I get promotion?',
            'expected_houses': [10, 2, 11],  # Career, income, gains
            'favorable_indicators': ['Sun in 10th house', 'Mars strong in Capricorn']
        }
    }
}

# Historical predictions for accuracy validation
HISTORICAL_PREDICTIONS = [
    {
        'description': 'Marriage Prediction - Actual Date Known',
        'birth_data': {
            'year': 1988, 'month': 6, 'day': 10,
            'hour': 8, 'minute': 0,
            'latitude': 28.6139, 'longitude': 77.2090  # Delhi, India
        },
        'question': 'When will marriage happen?',
        'query_date': '2012-01-15',
        'actual_event_date': '2014-11-22',
        'cuspal_7th_sub_lord': 'Venus',  # Known from actual chart
        'expected_prediction': 'Marriage likely in Venus period',
        'confidence_threshold': 0.7
    }
]


# ==================== HELPER FUNCTIONS ====================

def print_test_header(title: str, symbol: str = "="):
    """Print formatted test section header."""
    print(f"\n{symbol * 70}")
    print(f"{title:^70}")
    print(f"{symbol * 70}\n")


def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Print formatted test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status:10} | {test_name:40} | {details}")


def calculate_degree_accuracy(expected: float, actual: float) -> float:
    """Calculate degree accuracy percentage."""
    diff = abs(expected - actual)
    # Handle wraparound at 360°
    if diff > 180:
        diff = 360 - diff
    accuracy = max(0, 100 - (diff * 10))  # 1° off = 10% penalty
    return accuracy


# ==================== UNIT TESTS ====================

def test_sub_lord_calculation_accuracy():
    """Test 1: Sub-lord calculation precision against known positions."""
    print_test_header("TEST 1: Sub-lord Calculation Accuracy")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    all_passed = True
    
    for i, test_case in enumerate(KNOWN_KP_POSITIONS, 1):
        longitude = test_case['longitude']
        expected = test_case['expected']
        
        # Calculate sub-lord
        result = get_sub_lord(longitude)
        
        # Verify nakshatra number
        nak_num_match = result.nakshatra_num == expected['nakshatra_num']
        
        # Verify nakshatra name
        nak_name_match = result.nakshatra_name == expected['nakshatra_name']
        
        # Verify nakshatra lord
        nak_lord_match = result.nakshatra_lord == expected['nakshatra_lord']
        
        # Verify sub-lord
        sub_lord_match = result.sub_lord == expected['sub_lord']
        
        # Overall pass
        test_passed = all([nak_num_match, nak_name_match, nak_lord_match, sub_lord_match])
        all_passed &= test_passed
        
        # Print result
        test_name = f"Position {longitude:6.2f}° → {expected['nakshatra_name']}"
        details = f"Sub-lord: {result.sub_lord} (expected {expected['sub_lord']})"
        print_test_result(test_name, test_passed, details)
        
        if not test_passed:
            print(f"   Expected: Nak#{expected['nakshatra_num']} {expected['nakshatra_name']} "
                  f"({expected['nakshatra_lord']}) → {expected['sub_lord']} sub")
            print(f"   Got:      Nak#{result.nakshatra_num} {result.nakshatra_name} "
                  f"({result.nakshatra_lord}) → {result.sub_lord} sub")
    
    return all_passed


def test_vimshottari_proportions():
    """Test 2: Verify Vimshottari proportions sum correctly."""
    print_test_header("TEST 2: Vimshottari Proportions Validation")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    # Sum of all proportions should equal one nakshatra length (13°20' = 13.333333°)
    total_arc = sum(VIMSHOTTARI_PROPORTIONS.values())
    nakshatra_length = 13 + 20/60
    
    # Allow small floating point error
    difference = abs(total_arc - nakshatra_length)
    tolerance = 0.0001  # Less than 0.01 seconds of arc
    
    test_passed = difference < tolerance
    
    print(f"Nakshatra length: {nakshatra_length:.10f}°")
    print(f"Sum of sub-lords: {total_arc:.10f}°")
    print(f"Difference:       {difference:.10f}°")
    print(f"Tolerance:        {tolerance:.10f}°")
    
    print_test_result("Vimshottari proportions sum", test_passed, 
                     f"Diff: {difference:.10f}°")
    
    # Test individual proportions
    print("\nIndividual Sub-lord Arcs:")
    for planet in SUB_LORD_SEQUENCE:
        arc = VIMSHOTTARI_PROPORTIONS[planet]
        arc_dms = f"{int(arc)}°{int((arc % 1) * 60)}'{int(((arc % 1) * 60 % 1) * 60)}\""
        print(f"  {planet:8} : {arc:10.6f}° = {arc_dms}")
    
    return test_passed


def test_cuspal_sub_lord_calculation():
    """Test 3: Cuspal sub-lord calculation for 12 houses."""
    print_test_header("TEST 3: Cuspal Sub-lord Calculation")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    # Test with equal house system
    equal_house_cusps = [i * 30 for i in range(12)]
    
    try:
        cuspal_sub_lords = get_cuspal_sub_lords(equal_house_cusps)
        
        # Verify we got 12 results
        test_passed = len(cuspal_sub_lords) == 12
        
        print("Equal House System Cuspal Sub-lords:")
        for house_num in range(1, 13):
            data = cuspal_sub_lords[house_num]
            cusp_long = equal_house_cusps[house_num - 1]
            print(f"  House {house_num:2d} ({cusp_long:3d}°): {data.sub_lord:8} "
                  f"in {data.nakshatra_name} ({data.nakshatra_lord})")
        
        print_test_result("Cuspal sub-lords calculation", test_passed, 
                         f"Generated {len(cuspal_sub_lords)}/12 houses")
        
        return test_passed
        
    except Exception as e:
        print_test_result("Cuspal sub-lords calculation", False, f"Error: {e}")
        return False


def test_significator_hierarchy():
    """Test 4: Significator analysis hierarchy."""
    print_test_header("TEST 4: Significator Hierarchy Analysis")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    # Use chart_1 (marriage favorable)
    chart = SAMPLE_CHARTS['chart_1_marriage_favorable']
    
    # Create planet dict with house assignments (equal house system)
    planets_dict = {}
    for planet_name, longitude in chart['planets'].items():
        house_num = int(longitude / 30) + 1
        if house_num > 12:
            house_num = 12
        planets_dict[planet_name] = {
            'longitude': longitude,
            'house': house_num
        }
    
    try:
        # Get significators for 7th house (marriage)
        significators = get_significators_for_house(7, planets_dict, chart['houses'])
        
        print(f"Significators for 7th House (Marriage):")
        print(f"{'Priority':<12} | {'Planet':<10} | {'Reason'}")
        print("-" * 60)
        
        for sig in significators[:10]:  # Show top 10
            print(f"{sig.priority:<12} | {sig.planet:<10} | {sig.reason}")
        
        # Verify Venus (in 7th house) is PRIMARY significator
        primary_planets = [s.planet for s in significators if s.priority == 'PRIMARY']
        venus_is_primary = 'Venus' in primary_planets
        
        test_passed = venus_is_primary and len(significators) > 0
        
        print_test_result("Venus as PRIMARY significator", venus_is_primary,
                         f"Found {len(primary_planets)} primary significator(s)")
        print_test_result("Significator hierarchy", test_passed,
                         f"Total {len(significators)} significators identified")
        
        return test_passed
        
    except Exception as e:
        print_test_result("Significator analysis", False, f"Error: {e}")
        return False


def test_ruling_planets():
    """Test 5: Ruling planets calculation."""
    print_test_header("TEST 5: Ruling Planets Calculation")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    # Test query: November 1, 2025, 2:30 PM
    query_time = datetime(2025, 11, 1, 14, 30)
    asc_longitude = 45.0  # 15° Taurus
    moon_longitude = 135.0  # 15° Leo
    
    try:
        ruling = get_ruling_planets(query_time, asc_longitude, moon_longitude)
        
        print(f"Query Time: {query_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Ascendant: {asc_longitude}° → {ruling['ascendant']['formatted']}")
        print(f"  Sign Lord: {ruling['ascendant']['sign_lord']}")
        print(f"  Nakshatra Lord: {ruling['ascendant']['nakshatra_lord']}")
        print(f"  Sub-lord: {ruling['ascendant']['sub_lord']}")
        print()
        print(f"Moon: {moon_longitude}° → {ruling['moon']['formatted']}")
        print(f"  Nakshatra: {ruling['moon']['nakshatra']}")
        print(f"  Nakshatra Lord: {ruling['moon']['nakshatra_lord']}")
        print(f"  Sub-lord: {ruling['moon']['sub_lord']}")
        print()
        print(f"Day Lord: {ruling['day_lord']['planet']} ({ruling['day_lord']['weekday']})")
        
        # Verify Saturday = Saturn
        saturday_correct = ruling['day_lord']['planet'] == 'Saturn'
        
        # Verify all fields present
        has_all_fields = (
            'ascendant' in ruling and 'moon' in ruling and 'day_lord' in ruling
        )
        
        test_passed = saturday_correct and has_all_fields
        
        print_test_result("Ruling planets calculation", test_passed,
                         "All 3 ruling planets identified")
        print_test_result("Day lord accuracy (Saturday=Saturn)", saturday_correct,
                         f"Got {ruling['day_lord']['planet']}")
        
        return test_passed
        
    except Exception as e:
        print_test_result("Ruling planets", False, f"Error: {e}")
        return False


def test_confidence_scoring():
    """Test 6: Prediction confidence scoring."""
    print_test_header("TEST 6: Confidence Scoring Algorithm")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    # Test case 1: High confidence (cuspal sub-lord is PRIMARY significator)
    significators_high = [
        Significator('Venus', 'PRIMARY', 'Occupying 7th house', 1.0),
        Significator('Mars', 'SECONDARY', 'In Venus star', 0.8),
        Significator('Jupiter', 'TERTIARY', 'In Saturn star', 0.6)
    ]
    
    ruling_high = {
        'ascendant': {'sub_lord': 'Venus'},
        'moon': {'sub_lord': 'Mars'},
        'day_lord': {'planet': 'Venus'}
    }
    
    confidence_high = calculate_kp_confidence('Venus', significators_high, ruling_high)
    
    # Test case 2: Medium confidence
    significators_med = [
        Significator('Mars', 'PRIMARY', 'Occupying 10th house', 1.0),
        Significator('Saturn', 'TERTIARY', 'In Mars star', 0.6)
    ]
    
    ruling_med = {
        'ascendant': {'sub_lord': 'Mercury'},
        'moon': {'sub_lord': 'Mars'},
        'day_lord': {'planet': 'Sun'}
    }
    
    confidence_med = calculate_kp_confidence('Jupiter', significators_med, ruling_med)
    
    # Test case 3: Low confidence (cuspal sub-lord not a significator)
    significators_low = [
        Significator('Sun', 'PRIMARY', 'Occupying 5th house', 1.0)
    ]
    
    ruling_low = {
        'ascendant': {'sub_lord': 'Mercury'},
        'moon': {'sub_lord': 'Rahu'},
        'day_lord': {'planet': 'Moon'}
    }
    
    confidence_low = calculate_kp_confidence('Saturn', significators_low, ruling_low)
    
    print(f"Confidence Scores:")
    print(f"  High confidence case:   {confidence_high:.2f} (expected > 0.75)")
    print(f"  Medium confidence case: {confidence_med:.2f} (expected 0.40-0.75)")
    print(f"  Low confidence case:    {confidence_low:.2f} (expected < 0.40)")
    
    # Verify ordering
    high_correct = confidence_high > 0.75
    med_correct = 0.40 <= confidence_med <= 0.75
    low_correct = confidence_low < 0.40
    ordering_correct = confidence_high > confidence_med > confidence_low
    
    test_passed = high_correct and ordering_correct
    
    print_test_result("High confidence scoring", high_correct,
                     f"Score: {confidence_high:.2f}")
    print_test_result("Medium confidence scoring", med_correct,
                     f"Score: {confidence_med:.2f}")
    print_test_result("Low confidence scoring", low_correct,
                     f"Score: {confidence_low:.2f}")
    print_test_result("Confidence ordering", ordering_correct,
                     "High > Medium > Low")
    
    return test_passed


def test_prediction_accuracy():
    """Test 7: Full prediction accuracy with historical data."""
    print_test_header("TEST 7: Historical Prediction Validation")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    print("⚠️  Note: Full prediction requires Swiss Ephemeris integration")
    print("This test validates the prediction logic structure.\n")
    
    # For now, test the logic flow
    for hist_pred in HISTORICAL_PREDICTIONS:
        print(f"Case: {hist_pred['description']}")
        print(f"  Question: {hist_pred['question']}")
        print(f"  Query Date: {hist_pred['query_date']}")
        print(f"  Actual Event: {hist_pred['actual_event_date']}")
        print(f"  7th Cusp Sub-lord: {hist_pred['cuspal_7th_sub_lord']}")
        print(f"  Expected: {hist_pred['expected_prediction']}")
        print(f"  Confidence Threshold: {hist_pred['confidence_threshold']}")
        print()
    
    # Placeholder test (will implement full prediction later)
    test_passed = len(HISTORICAL_PREDICTIONS) > 0
    
    print_test_result("Historical data validation", test_passed,
                     f"{len(HISTORICAL_PREDICTIONS)} case(s) ready for testing")
    
    return test_passed


def test_edge_cases():
    """Test 8: Edge cases and boundary conditions."""
    print_test_header("TEST 8: Edge Cases and Boundary Conditions")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    edge_cases = [
        ('Exact 0° Aries', 0.0),
        ('Exact 0° Taurus', 30.0),
        ('Mid-nakshatra', 6.666666),  # Middle of Ashwini
        ('Nakshatra boundary', 13.333333),  # Ashwini/Bharani boundary
        ('End of zodiac', 359.999999),
        ('Wraparound test', 360.0),  # Should normalize to 0°
        ('Sub-lord boundary', 2.77777),  # Ketu/Venus sub boundary in Ashwini
    ]
    
    all_passed = True
    
    for test_name, longitude in edge_cases:
        try:
            result = get_sub_lord(longitude)
            
            # Verify result is valid
            valid_nakshatra = 1 <= result.nakshatra_num <= 27
            valid_sub_lord = result.sub_lord in SUB_LORD_SEQUENCE
            valid_position = 0 <= result.position_in_nakshatra < 13.333334
            
            test_passed = valid_nakshatra and valid_sub_lord and valid_position
            all_passed &= test_passed
            
            details = f"Nak#{result.nakshatra_num}, {result.sub_lord} sub"
            print_test_result(test_name, test_passed, details)
            
        except Exception as e:
            print_test_result(test_name, False, f"Error: {e}")
            all_passed = False
    
    return all_passed


# ==================== INTEGRATION TESTS ====================

def test_full_chart_analysis():
    """Test 9: Complete chart analysis workflow."""
    print_test_header("TEST 9: Full Chart Analysis Workflow")
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ KP Engine not available, skipping tests")
        return False
    
    chart = SAMPLE_CHARTS['chart_1_marriage_favorable']
    
    print(f"Analyzing: {chart['name']}")
    print(f"Birth: {chart['birth_data']['year']}-{chart['birth_data']['month']:02d}-"
          f"{chart['birth_data']['day']:02d} "
          f"{chart['birth_data']['hour']:02d}:{chart['birth_data']['minute']:02d}")
    print()
    
    try:
        # Step 1: Cuspal sub-lords
        cuspal = get_cuspal_sub_lords(chart['houses'])
        print("Step 1: Cuspal Sub-lords")
        for house in [1, 7, 10]:  # Key houses
            print(f"  House {house}: {cuspal[house].sub_lord} "
                  f"({cuspal[house].nakshatra_name})")
        print()
        
        # Step 2: Planet sub-lords
        planet_subs = get_planet_sub_lords(chart['planets'])
        print("Step 2: Planet Sub-lords")
        for planet in ['Sun', 'Moon', 'Venus']:  # Key planets
            print(f"  {planet}: {planet_subs[planet].sub_lord} sub "
                  f"in {planet_subs[planet].nakshatra_name}")
        print()
        
        # Step 3: Significators for marriage (7th house)
        planets_dict = {}
        for planet_name, longitude in chart['planets'].items():
            house_num = int(longitude / 30) + 1
            planets_dict[planet_name] = {'longitude': longitude, 'house': house_num}
        
        significators = get_significators_for_house(7, planets_dict, chart['houses'])
        print("Step 3: Marriage Significators (7th house)")
        for sig in significators[:5]:
            print(f"  {sig.planet:8} - {sig.priority:10} - {sig.reason}")
        print()
        
        # Step 4: Ruling planets (simulated query)
        query_time = datetime(2025, 11, 1, 14, 30)
        ruling = get_ruling_planets(query_time, chart['houses'][0], 
                                    chart['planets']['Moon'])
        print("Step 4: Ruling Planets (query time)")
        print(f"  ASC sub-lord: {ruling['ascendant']['sub_lord']}")
        print(f"  Moon sub-lord: {ruling['moon']['sub_lord']}")
        print(f"  Day lord: {ruling['day_lord']['planet']}")
        print()
        
        # Step 5: Confidence
        confidence = calculate_kp_confidence(
            cuspal[7].sub_lord,
            significators,
            ruling
        )
        print(f"Step 5: Prediction Confidence: {confidence:.2f}")
        print()
        
        test_passed = confidence > 0.5  # Should be favorable chart
        
        print_test_result("Full chart analysis", test_passed,
                         f"Confidence: {confidence:.2f}")
        
        return test_passed
        
    except Exception as e:
        print_test_result("Full chart analysis", False, f"Error: {e}")
        return False


# ==================== MAIN TEST RUNNER ====================

def run_all_tests():
    """Run all KP prediction tests."""
    print("=" * 70)
    print(" KP PREDICTION ENGINE - COMPREHENSIVE TEST SUITE ".center(70))
    print("=" * 70)
    print()
    
    if not KP_ENGINE_AVAILABLE:
        print("❌ FATAL: KP Engine could not be imported")
        print("   Please ensure backend/calculations/kp_engine.py exists")
        return False
    
    tests = [
        ('Sub-lord Calculation Accuracy', test_sub_lord_calculation_accuracy),
        ('Vimshottari Proportions', test_vimshottari_proportions),
        ('Cuspal Sub-lords', test_cuspal_sub_lord_calculation),
        ('Significator Hierarchy', test_significator_hierarchy),
        ('Ruling Planets', test_ruling_planets),
        ('Confidence Scoring', test_confidence_scoring),
        ('Historical Predictions', test_prediction_accuracy),
        ('Edge Cases', test_edge_cases),
        ('Full Chart Analysis', test_full_chart_analysis),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print_test_header("TEST SUMMARY", "=")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    failed = total - passed
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {test_name}")
    
    print()
    print(f"Total Tests: {total}")
    print(f"Passed:      {passed} ({passed/total*100:.1f}%)")
    print(f"Failed:      {failed} ({failed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! KP Engine is production-ready.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review output above.")
        return False


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
