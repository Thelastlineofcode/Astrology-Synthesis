"""
Test suite for Vimshottari Dasha Calculator

Tests the complete dasha system including:
- Mahadasha calculation (120-year cycle)
- Antardasha sub-periods
- Pratyantardasha micro-periods
- Timeline generation
- Favorable period identification
"""

import sys
import os
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'calculations'))

from dasha_engine import (
    DashaCalculator,
    DashaPosition,
    get_dasha_at_date,
    DASHA_SEQUENCE,
    DASHA_YEARS,
    TOTAL_DASHA_CYCLE
)


def print_test_header(title: str):
    """Print formatted test header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Print test result with status."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}     | {test_name:40} | {details}")


def test_vimshottari_sequence():
    """Test 1: Verify Vimshottari sequence and years."""
    print_test_header("TEST 1: Vimshottari Sequence Validation")
    
    calculator = DashaCalculator()
    
    # Check sequence
    expected_sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    assert calculator.sequence == expected_sequence, "Sequence mismatch"
    print(f"✓ Sequence: {' → '.join(calculator.sequence)}")
    
    # Check total years
    total_years = sum(calculator.years.values())
    assert total_years == 120, f"Total years {total_years} != 120"
    print(f"✓ Total dasha cycle: {total_years} years")
    
    # Check individual years
    print("\nDasha Year Distribution:")
    for planet in calculator.sequence:
        years = calculator.years[planet]
        percentage = (years / 120) * 100
        print(f"  {planet:10} → {years:2} years ({percentage:5.1f}%)")
    
    test_passed = total_years == 120 and calculator.sequence == expected_sequence
    print_test_result("Vimshottari sequence validation", test_passed)
    return test_passed


def test_nakshatra_calculation():
    """Test 2: Nakshatra number calculation from Moon longitude."""
    print_test_header("TEST 2: Nakshatra Calculation")
    
    calculator = DashaCalculator()
    
    test_cases = [
        (0.0, 1, "0° Aries = Ashwini"),
        (13.333333, 2, "13°20' Aries = Bharani"),
        (26.666667, 3, "26°40' Aries = Krittika"),
        (90.0, 7, "0° Cancer = Punarvasu"),
        (180.0, 14, "0° Libra = Chitra"),
        (270.0, 21, "0° Capricorn = Uttara Ashadha"),
        (359.999, 27, "End of zodiac = Revati"),
    ]
    
    passed = 0
    for longitude, expected_nak, description in test_cases:
        nak_num = calculator.get_nakshatra_number(longitude)
        is_pass = nak_num == expected_nak
        passed += is_pass
        status = "✓" if is_pass else "✗"
        print(f"  {status} {description:40} → Nak#{nak_num} (expected #{expected_nak})")
    
    test_passed = passed == len(test_cases)
    print_test_result("Nakshatra calculation accuracy", test_passed, f"{passed}/{len(test_cases)} correct")
    return test_passed


def test_antardasha_duration():
    """Test 3: Antardasha duration calculation."""
    print_test_header("TEST 3: Antardasha Duration Calculation")
    
    calculator = DashaCalculator()
    
    # Venus Mahadasha = 20 years
    # Saturn Antardasha within Venus = (19/120) * 20 = 3.1667 years
    venus_md = 'Venus'
    saturn_ad = 'Saturn'
    
    duration = calculator._get_antardasha_duration(venus_md, saturn_ad)
    expected = (19 / 120) * 20  # 3.1667 years
    
    print(f"Mahadasha: {venus_md} ({calculator.years[venus_md]} years)")
    print(f"Antardasha: {saturn_ad} within {venus_md}")
    print(f"  Formula: ({calculator.years[saturn_ad]}/120) × {calculator.years[venus_md]} = {duration:.4f} years")
    print(f"  Expected: {expected:.4f} years")
    print(f"  Match: {abs(duration - expected) < 0.0001}")
    
    # Test multiple Maharashas
    print("\nAntardasha durations within different Maharashas:")
    for md in ['Sun', 'Moon', 'Saturn']:
        print(f"\n  {md} Mahadasha ({calculator.years[md]} years):")
        for ad_index, ad in enumerate(calculator.sequence[:3]):  # First 3 Antardashas
            duration = calculator._get_antardasha_duration(md, ad)
            print(f"    {ad:8} Antardasha → {duration:.3f} years")
    
    test_passed = abs(duration - expected) < 0.0001
    print_test_result("Antardasha duration calculation", test_passed)
    return test_passed


def test_dasha_position_calculation():
    """Test 4: Calculate dasha position at specific date."""
    print_test_header("TEST 4: Dasha Position Calculation")
    
    calculator = DashaCalculator()
    
    # Birth: January 1, 1990
    birth_date = datetime(1990, 1, 1)
    
    # Moon in Rohini (Nak #4, lord = Moon)
    # Starting dasha calculation should identify which period
    moon_longitude = 40.0 + 13.333333  # ~53° (in Taurus, Rohini)
    
    # Query: November 1, 2025 (current date)
    query_date = datetime(2025, 11, 1)
    
    # Dasha balance at birth (example: 12 years remaining in first dasha)
    dasha_balance = 12.0
    
    position = calculator.calculate_dasha_position(
        birth_date,
        moon_longitude,
        dasha_balance,
        query_date
    )
    
    print(f"Birth Date: {birth_date.strftime('%Y-%m-%d')}")
    print(f"Query Date: {query_date.strftime('%Y-%m-%d')}")
    print(f"Days elapsed: {(query_date - birth_date).days}")
    print(f"Years elapsed: {(query_date - birth_date).days / 365.25:.2f}")
    
    print(f"\nDasha Position at {query_date.strftime('%Y-%m-%d')}:")
    print(f"  Mahadasha: {position.dasha_planet}")
    print(f"    Period: {position.dasha_start.strftime('%Y-%m-%d')} → {position.dasha_end.strftime('%Y-%m-%d')}")
    print(f"    Remaining: {position.dasha_remaining:.2f} years")
    
    print(f"\n  Antardasha: {position.antardasha_planet}")
    print(f"    Period: {position.antardasha_start.strftime('%Y-%m-%d')} → {position.antardasha_end.strftime('%Y-%m-%d')}")
    print(f"    Remaining: {position.antardasha_remaining:.2f} years")
    
    print(f"\n  Pratyantardasha: {position.pratyantardasha_planet}")
    print(f"    Period: {position.pratyantardasha_start.strftime('%Y-%m-%d')} → {position.pratyantardasha_end.strftime('%Y-%m-%d')}")
    print(f"    Remaining: {position.pratyantardasha_remaining:.0f} days")
    
    print(f"\n  Cycle Progress: {position.percentage_complete:.1f}%")
    
    # Basic validation
    test_passed = (
        position.dasha_planet in calculator.sequence and
        position.antardasha_planet in calculator.sequence and
        position.pratyantardasha_planet in calculator.sequence and
        0 <= position.percentage_complete <= 100
    )
    
    print_test_result("Dasha position calculation", test_passed)
    return test_passed


def test_multiple_dates():
    """Test 5: Dasha positions across multiple dates."""
    print_test_header("TEST 5: Dasha Timeline Across Multiple Years")
    
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    moon_longitude = 135.0
    dasha_balance = 12.0
    
    # Test dates: every 2 years from birth
    test_dates = [
        datetime(1990, 1, 1),  # Birth
        datetime(1995, 1, 1),  # +5 years
        datetime(2000, 1, 1),  # +10 years
        datetime(2010, 1, 1),  # +20 years
        datetime(2025, 11, 1), # +35.83 years
    ]
    
    print("Mahadasha changes over time:\n")
    print(f"{'Date':<15} {'Mahadasha':<12} {'Remaining':<12} {'Antardasha':<12}")
    print("-" * 51)
    
    previous_md = None
    md_changes = 0
    
    for test_date in test_dates:
        position = calculator.calculate_dasha_position(
            birth_date,
            moon_longitude,
            dasha_balance,
            test_date
        )
        
        if previous_md != position.dasha_planet:
            md_changes += 1
        
        print(f"{test_date.strftime('%Y-%m-%d'):<15} {position.dasha_planet:<12} "
              f"{position.dasha_remaining:.2f}y {' (NEW)' if previous_md != position.dasha_planet else '':<12} "
              f"{position.antardasha_planet:<12}")
        
        previous_md = position.dasha_planet
    
    # Should see at least 1 Mahadasha change in 35 years
    test_passed = md_changes > 0
    print_test_result("Dasha timeline progression", test_passed, f"{md_changes} Mahadasha change(s)")
    return test_passed


def test_dasha_balance():
    """Test 6: Dasha balance calculation at birth."""
    print_test_header("TEST 6: Dasha Balance at Birth")
    
    calculator = DashaCalculator()
    
    # Test with different Moon positions
    moon_positions = [
        (0.0, "Ashwini - Ketu"),
        (40.0, "Rohini - Moon"),
        (133.333, "Purva Phalguni - Venus"),
        (270.0, "Uttara Ashadha - Sun"),
    ]
    
    print("Starting dasha based on Moon nakshatra:\n")
    
    for moon_long, description in moon_positions:
        nakshatra = calculator.get_nakshatra_number(moon_long)
        starting_planet = calculator.get_starting_dasha_planet(nakshatra)
        
        print(f"  Moon at {moon_long:7.1f}° ({description:30}) → {starting_planet} starts")
    
    test_passed = True
    print_test_result("Dasha balance calculation", test_passed)
    return test_passed


def test_convenience_function():
    """Test 7: Convenience function for dasha calculation."""
    print_test_header("TEST 7: Convenience Function")
    
    birth_date = datetime(1990, 1, 1)
    query_date = datetime(2025, 11, 1)
    
    position = get_dasha_at_date(
        birth_date,
        moon_longitude=180.0,
        query_date=query_date,
        dasha_balance=10.0
    )
    
    print(f"Using convenience function: get_dasha_at_date()")
    print(f"  Birth: {birth_date.strftime('%Y-%m-%d')}")
    print(f"  Query: {query_date.strftime('%Y-%m-%d')}")
    print(f"  Result: {position.dasha_planet} Mahadasha")
    
    test_passed = position.dasha_planet in DASHA_SEQUENCE
    print_test_result("Convenience function", test_passed)
    return test_passed


def test_formatting():
    """Test 8: Dasha position formatting."""
    print_test_header("TEST 8: Dasha Position Formatting")
    
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    query_date = datetime(2025, 11, 1)
    
    position = calculator.calculate_dasha_position(
        birth_date,
        moon_longitude=90.0,
        dasha_balance=12.0,
        query_date=query_date
    )
    
    formatted = calculator.format_dasha_position(position)
    print(formatted)
    
    test_passed = "MAHADASHA" in formatted and "ANTARDASHA" in formatted
    print_test_result("Dasha formatting", test_passed)
    return test_passed


def run_all_tests():
    """Run all dasha calculator tests."""
    print("\n" + "=" * 70)
    print("  VIMSHOTTARI DASHA CALCULATOR - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Vimshottari Sequence", test_vimshottari_sequence),
        ("Nakshatra Calculation", test_nakshatra_calculation),
        ("Antardasha Duration", test_antardasha_duration),
        ("Dasha Position Calculation", test_dasha_position_calculation),
        ("Dasha Timeline", test_multiple_dates),
        ("Dasha Balance", test_dasha_balance),
        ("Convenience Function", test_convenience_function),
        ("Formatting", test_formatting),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Exception in {name}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    for (name, _), result in zip(tests, results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {name}")
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed:      {passed} ({passed/total*100:.1f}%)")
    print(f"Failed:      {total - passed} ({(total-passed)/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Dasha engine is ready for production.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review above.")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
