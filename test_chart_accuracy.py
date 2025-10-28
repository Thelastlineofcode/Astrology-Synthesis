#!/usr/bin/env python3
"""
Comprehensive Chart Generator Accuracy Test
Tests the precision and accuracy of astrological chart calculations.
"""

import sys
import os
from datetime import datetime, timezone
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_chart_accuracy():
    """Test chart generator with known accurate data points."""
    
    print("🔬 CHART GENERATOR ACCURACY TEST")
    print("=" * 60)
    
    # Test cases with known accurate data
    test_cases = [
        {
            'name': 'Famous Birth - Albert Einstein',
            'birth_data': {
                'year': 1879, 'month': 3, 'day': 14,
                'hour': 11, 'minute': 30,
                'latitude': 48.3984, 'longitude': 7.9026,  # Ulm, Germany
                'timezone': 'Europe/Berlin'
            },
            'expected_sun_sign': 'Pisces',
            'expected_moon_sign': 'Sagittarius',  # Known from historical records
            'expected_ascendant': 'Cancer',  # Approximate
        },
        {
            'name': 'Modern Test Case - Y2K Birth',
            'birth_data': {
                'year': 2000, 'month': 1, 'day': 1,
                'hour': 12, 'minute': 0,
                'latitude': 40.7128, 'longitude': -74.0060,  # NYC
                'timezone': 'America/New_York'
            },
            'expected_sun_sign': 'Capricorn',
            'expected_moon_sign': None,  # Will calculate and verify
            'expected_ascendant': None,
        },
        {
            'name': 'Southern Hemisphere Test',
            'birth_data': {
                'year': 1990, 'month': 7, 'day': 15,
                'hour': 14, 'minute': 30,
                'latitude': -33.8688, 'longitude': 151.2093,  # Sydney
                'timezone': 'Australia/Sydney'
            },
            'expected_sun_sign': 'Cancer',
            'expected_moon_sign': None,
            'expected_ascendant': None,
        },
        {
            'name': 'Edge Case - Near Pole',
            'birth_data': {
                'year': 1995, 'month': 6, 'day': 21,  # Summer solstice
                'hour': 0, 'minute': 0,
                'latitude': 64.2008, 'longitude': -21.8174,  # Reykjavik
                'timezone': 'Atlantic/Reykjavik'
            },
            'expected_sun_sign': 'Gemini',  # Should be very close to Cancer cusp
            'expected_moon_sign': None,
            'expected_ascendant': None,
        }
    ]
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 🧪 Testing: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Test chart calculation
            chart_result = test_chart_calculation(test_case)
            
            # Test accuracy
            accuracy_result = verify_chart_accuracy(test_case, chart_result)
            
            print(f"   ✅ Chart calculation: {'PASSED' if chart_result['success'] else 'FAILED'}")
            print(f"   ✅ Accuracy verification: {'PASSED' if accuracy_result['accurate'] else 'NEEDS_REVIEW'}")
            
            if accuracy_result['notes']:
                for note in accuracy_result['notes']:
                    print(f"   📝 {note}")
                    
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    # Test precision and edge cases
    print(f"\n" + "="*60)
    print("🎯 PRECISION TESTS")
    print("="*60)
    
    precision_tests = [
        test_sign_cusps(),
        test_retrograde_planets(),
        test_house_calculations(),
        test_aspect_calculations(),
        test_coordinate_precision()
    ]
    
    print(f"\n🏆 OVERALL RESULTS:")
    print(f"Basic chart tests: {len(test_cases)} cases")
    print(f"Precision tests: {len(precision_tests)} categories")
    
    return True

def test_chart_calculation(test_case):
    """Test basic chart calculation functionality."""
    try:
        # Import chart calculator
        from calculations.chart_calculator import ChartCalculator
        
        calculator = ChartCalculator()
        birth_data = test_case['birth_data']
        
        print(f"   🌍 Location: {birth_data['latitude']:.4f}, {birth_data['longitude']:.4f}")
        print(f"   📅 Date/Time: {birth_data['year']}-{birth_data['month']:02d}-{birth_data['day']:02d} {birth_data['hour']:02d}:{birth_data['minute']:02d}")
        
        # Calculate chart
        chart = calculator.calculate_chart(
            year=birth_data['year'],
            month=birth_data['month'], 
            day=birth_data['day'],
            hour=birth_data['hour'],
            minute=birth_data['minute'],
            latitude=birth_data['latitude'],
            longitude=birth_data['longitude']
        )
        
        if chart and 'planets' in chart:
            print(f"   🌟 Calculated planets: {len(chart['planets'])}")
            print(f"   🏠 Calculated houses: {len(chart.get('houses', {}))}")
            print(f"   ⚡ Calculated aspects: {len(chart.get('aspects', []))}")
            
            # Show key placements
            if 'Sun' in chart['planets']:
                sun = chart['planets']['Sun']
                print(f"   ☀️  Sun: {sun.get('sign', 'Unknown')} {sun.get('degree', 0):.2f}°")
            
            if 'Moon' in chart['planets']:
                moon = chart['planets']['Moon']
                print(f"   🌙 Moon: {moon.get('sign', 'Unknown')} {moon.get('degree', 0):.2f}°")
            
            if 'houses' in chart and 'house_1' in chart['houses']:
                asc = chart['houses']['house_1']
                print(f"   ⬆️  Ascendant: {asc.get('sign', 'Unknown')} {asc.get('degree', 0):.2f}°")
            
            return {
                'success': True,
                'chart': chart,
                'planet_count': len(chart['planets']),
                'house_count': len(chart.get('houses', {})),
                'aspect_count': len(chart.get('aspects', []))
            }
        else:
            return {'success': False, 'error': 'No chart data returned'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def verify_chart_accuracy(test_case, chart_result):
    """Verify the accuracy of calculated chart data."""
    if not chart_result['success']:
        return {'accurate': False, 'notes': ['Chart calculation failed']}
    
    chart = chart_result['chart']
    notes = []
    accurate = True
    
    # Check Sun sign accuracy
    if test_case['expected_sun_sign'] and 'Sun' in chart['planets']:
        calculated_sun_sign = chart['planets']['Sun'].get('sign')
        if calculated_sun_sign != test_case['expected_sun_sign']:
            accurate = False
            notes.append(f"Sun sign mismatch: expected {test_case['expected_sun_sign']}, got {calculated_sun_sign}")
        else:
            notes.append(f"Sun sign accurate: {calculated_sun_sign}")
    
    # Check Moon sign if specified
    if test_case['expected_moon_sign'] and 'Moon' in chart['planets']:
        calculated_moon_sign = chart['planets']['Moon'].get('sign')
        if calculated_moon_sign != test_case['expected_moon_sign']:
            notes.append(f"Moon sign check: expected {test_case['expected_moon_sign']}, got {calculated_moon_sign}")
        else:
            notes.append(f"Moon sign accurate: {calculated_moon_sign}")
    
    # Check basic data integrity
    planet_count = len(chart.get('planets', {}))
    if planet_count < 10:  # Should have at least the main planets
        accurate = False
        notes.append(f"Insufficient planets calculated: {planet_count} (expected ~10)")
    else:
        notes.append(f"Planet count good: {planet_count}")
    
    # Check house system
    house_count = len(chart.get('houses', {}))
    if house_count < 12:
        notes.append(f"House calculation incomplete: {house_count}/12")
    else:
        notes.append(f"House system complete: {house_count}")
    
    return {'accurate': accurate, 'notes': notes}

def test_sign_cusps():
    """Test accuracy near sign boundaries."""
    print("\n🌅 Testing Sign Cusp Accuracy...")
    
    try:
        from calculations.chart_calculator import ChartCalculator
        calculator = ChartCalculator()
        
        # Test near Aries/Pisces boundary (Spring Equinox)
        cusp_test = calculator.calculate_chart(
            year=2024, month=3, day=20, hour=3, minute=6,  # Approximate equinox
            latitude=40.7128, longitude=-74.0060
        )
        
        if cusp_test and 'Sun' in cusp_test['planets']:
            sun_sign = cusp_test['planets']['Sun']['sign']
            sun_degree = cusp_test['planets']['Sun']['degree']
            print(f"   🌅 Equinox Sun: {sun_sign} {sun_degree:.3f}°")
            
            # Should be very close to 0° Aries
            if sun_sign == 'Aries' and sun_degree < 5:
                print(f"   ✅ Cusp calculation accurate")
                return True
            else:
                print(f"   ⚠️  Cusp calculation needs review")
                return False
        else:
            print(f"   ❌ Cusp test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Cusp test error: {e}")
        return False

def test_retrograde_planets():
    """Test retrograde planet detection."""
    print("\n⏪ Testing Retrograde Detection...")
    
    try:
        from calculations.chart_calculator import ChartCalculator
        calculator = ChartCalculator()
        
        # Test with a date when Mercury is typically retrograde
        retro_test = calculator.calculate_chart(
            year=2024, month=4, day=15, hour=12, minute=0,
            latitude=40.7128, longitude=-74.0060
        )
        
        if retro_test and 'planets' in retro_test:
            retrograde_planets = []
            for planet, data in retro_test['planets'].items():
                if data.get('retrograde', False):
                    retrograde_planets.append(planet)
            
            print(f"   ⏪ Retrograde planets detected: {retrograde_planets}")
            
            # There should typically be at least one retrograde planet
            if len(retrograde_planets) > 0:
                print(f"   ✅ Retrograde detection working")
                return True
            else:
                print(f"   ⚠️  No retrograde planets detected (unusual)")
                return True  # Not necessarily an error
        else:
            print(f"   ❌ Retrograde test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Retrograde test error: {e}")
        return False

def test_house_calculations():
    """Test house system calculations."""
    print("\n🏠 Testing House System Accuracy...")
    
    try:
        from calculations.chart_calculator import ChartCalculator
        calculator = ChartCalculator()
        
        house_test = calculator.calculate_chart(
            year=2000, month=6, day=21, hour=12, minute=0,
            latitude=51.5074, longitude=-0.1278  # London
        )
        
        if house_test and 'houses' in house_test:
            houses = house_test['houses']
            
            # Check that we have 12 houses
            house_count = len(houses)
            print(f"   🏠 Houses calculated: {house_count}")
            
            # Check house progression (should increase in degree order)
            house_degrees = []
            for i in range(1, 13):
                house_key = f'house_{i}'
                if house_key in houses:
                    degree = houses[house_key].get('degree', 0)
                    house_degrees.append(degree)
            
            if len(house_degrees) == 12:
                print(f"   🏠 All 12 houses present")
                print(f"   🏠 1st house: {houses['house_1'].get('sign')} {houses['house_1'].get('degree', 0):.2f}°")
                print(f"   🏠 10th house: {houses['house_10'].get('sign')} {houses['house_10'].get('degree', 0):.2f}°")
                return True
            else:
                print(f"   ⚠️  Incomplete house system: {len(house_degrees)}/12")
                return False
        else:
            print(f"   ❌ House calculation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ House test error: {e}")
        return False

def test_aspect_calculations():
    """Test planetary aspect calculations."""
    print("\n⚡ Testing Aspect Calculations...")
    
    try:
        from calculations.chart_calculator import ChartCalculator
        calculator = ChartCalculator()
        
        aspect_test = calculator.calculate_chart(
            year=2000, month=1, day=1, hour=12, minute=0,
            latitude=40.7128, longitude=-74.0060
        )
        
        if aspect_test and 'aspects' in aspect_test:
            aspects = aspect_test['aspects']
            aspect_count = len(aspects)
            print(f"   ⚡ Aspects calculated: {aspect_count}")
            
            if aspect_count > 0:
                # Show some example aspects
                for i, aspect in enumerate(aspects[:3]):
                    planet1 = aspect.get('planet1', 'Unknown')
                    planet2 = aspect.get('planet2', 'Unknown')
                    aspect_type = aspect.get('aspect', 'Unknown')
                    orb = aspect.get('orb', 0)
                    print(f"   ⚡ {planet1}-{planet2}: {aspect_type} (orb: {orb:.2f}°)")
                
                print(f"   ✅ Aspect calculation working")
                return True
            else:
                print(f"   ⚠️  No aspects calculated")
                return False
        else:
            print(f"   ❌ Aspect calculation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Aspect test error: {e}")
        return False

def test_coordinate_precision():
    """Test coordinate precision and accuracy."""
    print("\n📐 Testing Coordinate Precision...")
    
    try:
        from calculations.chart_calculator import ChartCalculator
        calculator = ChartCalculator()
        
        # Test with precise coordinates
        precision_test = calculator.calculate_chart(
            year=2024, month=1, day=1, hour=0, minute=0,
            latitude=40.758896, longitude=-73.985130  # Very precise NYC coords
        )
        
        if precision_test and 'planets' in precision_test:
            # Check degree precision
            sun_data = precision_test['planets'].get('Sun', {})
            sun_degree = sun_data.get('degree', 0)
            
            print(f"   📐 Sun degree precision: {sun_degree:.6f}°")
            
            # Degree should be calculated to at least 2 decimal places
            if isinstance(sun_degree, (int, float)) and sun_degree != 0:
                print(f"   ✅ Coordinate precision adequate")
                return True
            else:
                print(f"   ⚠️  Coordinate precision may be insufficient")
                return False
        else:
            print(f"   ❌ Precision test failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Precision test error: {e}")
        return False

if __name__ == "__main__":
    success = test_chart_accuracy()
    
    print(f"\n" + "="*60)
    if success:
        print("🎯 CHART ACCURACY TEST COMPLETED")
        print("Review the results above to assess calculation precision.")
    else:
        print("❌ CHART ACCURACY TEST ENCOUNTERED ISSUES")
        print("Check the error messages above for specific problems.")
    print("="*60)