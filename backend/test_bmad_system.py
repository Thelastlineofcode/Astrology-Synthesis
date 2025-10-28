#!/usr/bin/env python3
"""
BMAD Test Runner
Comprehensive test script for the Behavioral Model and Data analysis system.
"""

import sys
import os
import unittest
from io import StringIO

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

def run_bmad_tests():
    """Run all BMAD tests and return results."""
    
    print("🧠 BMAD Test Suite")
    print("=" * 50)
    print("Testing Behavioral Model and Data Analysis System")
    print()
    
    # Capture test output
    test_output = StringIO()
    
    try:
        # Import the test module
        from bmad.tests.test_bmad import (
            TestPersonalityModels,
            TestBehaviorModels, 
            TestPersonalityAnalyzer,
            TestBehaviorPredictor,
            TestBMADConfig,
            TestBMADIntegration
        )
        
        # Create test suite
        test_suite = unittest.TestSuite()
        
        # Add test classes
        test_classes = [
            TestPersonalityModels,
            TestBehaviorModels,
            TestPersonalityAnalyzer,
            TestBehaviorPredictor,
            TestBMADConfig,
            TestBMADIntegration
        ]
        
        for test_class in test_classes:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            test_suite.addTests(tests)
        
        # Run tests
        runner = unittest.TextTestRunner(
            stream=test_output,
            verbosity=2,
            buffer=True
        )
        
        result = runner.run(test_suite)
        
        # Print results
        output = test_output.getvalue()
        print(output)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print("\n❌ Failures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\n💥 Errors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
        
        if result.wasSuccessful():
            print("\n✅ All tests passed!")
            return True
        else:
            print("\n❌ Some tests failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all BMAD modules are properly installed and accessible.")
        return False
    
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        print("An unexpected error occurred while running tests.")
        return False


def run_basic_functionality_test():
    """Run a basic functionality test without dependencies."""
    
    print("\n🔧 Basic Functionality Test")
    print("=" * 50)
    
    try:
        # Test model imports
        print("Testing model imports...")
        from bmad.models.personality import PersonalityDimension, Trait, PersonalityProfile
        from bmad.models.behavior import BehaviorCategory, BehaviorIndicator, BehaviorProfile
        print("✅ Model imports successful")
        
        # Test service imports
        print("Testing service imports...")
        from bmad.services.personality_analyzer import PersonalityAnalyzer
        from bmad.services.behavior_predictor import BehaviorPredictor
        print("✅ Service imports successful")
        
        # Test configuration imports
        print("Testing configuration imports...")
        from bmad.config import BMADConfig, get_config
        print("✅ Configuration imports successful")
        
        # Test basic model creation
        print("Testing basic model creation...")
        
        trait = Trait(
            name="Test Trait",
            dimension=PersonalityDimension.EXTRAVERSION,
            intensity=trait.intensity if hasattr(trait, 'intensity') else "HIGH",
            description="Test description",
            astrological_source={"test": "data"}
        )
        print(f"✅ Created trait: {trait.name}")
        
        indicator = BehaviorIndicator(
            indicator_id="test_id",
            name="Test Indicator",
            category=BehaviorCategory.SOCIAL,
            description="Test description",
            intensity=0.5,
            astrological_basis={"test": "data"}
        )
        print(f"✅ Created behavior indicator: {indicator.name}")
        
        # Test configuration
        config = BMADConfig()
        print(f"✅ Created configuration with personality threshold: {config.personality.default_intensity_threshold}")
        
        print("\n✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        print(traceback.format_exc())
        return False


def run_sample_analysis():
    """Run a sample analysis to demonstrate BMAD functionality."""
    
    print("\n🌟 Sample BMAD Analysis")
    print("=" * 50)
    
    try:
        from bmad.services.personality_analyzer import PersonalityAnalyzer
        from bmad.services.behavior_predictor import BehaviorPredictor
        from datetime import datetime
        
        # Sample chart data
        sample_chart_data = {
            'planets': {
                'Sun': {'sign': 'Leo', 'degree': 15.5, 'house': 5},
                'Moon': {'sign': 'Cancer', 'degree': 22.3, 'house': 4},
                'Mercury': {'sign': 'Virgo', 'degree': 8.1, 'house': 6},
                'Venus': {'sign': 'Leo', 'degree': 20.0, 'house': 5},
                'Mars': {'sign': 'Aries', 'degree': 12.0, 'house': 1}
            },
            'houses': {
                'house_1': {'sign': 'Aries', 'degree': 12.0},
                'house_4': {'sign': 'Cancer', 'degree': 12.0},
                'house_5': {'sign': 'Leo', 'degree': 12.0},
                'house_6': {'sign': 'Virgo', 'degree': 12.0}
            },
            'aspects': [
                {
                    'planet1': 'Sun',
                    'planet2': 'Venus',
                    'aspect': 'conjunction',
                    'orb': 4.5
                }
            ]
        }
        
        sample_birth_data = {
            'year': 1990,
            'month': 8,
            'day': 15,
            'hour': 14,
            'minute': 30,
            'latitude': 40.7128,
            'longitude': -74.0060
        }
        
        print("Performing personality analysis...")
        personality_analyzer = PersonalityAnalyzer()
        personality_profile = personality_analyzer.analyze_personality(
            sample_chart_data,
            sample_birth_data,
            "Sample Person"
        )
        
        print(f"✅ Generated personality profile with {len(personality_profile.traits)} traits")
        print(f"   Dominant dimensions: {[dim.value for dim in personality_profile.dominant_dimensions]}")
        print(f"   Summary: {personality_profile.summary}")
        
        print("\nPerforming behavioral analysis...")
        behavior_predictor = BehaviorPredictor()
        behavior_profile = behavior_predictor.create_behavior_profile(
            sample_chart_data,
            sample_birth_data,
            "Sample Person"
        )
        
        print(f"✅ Generated behavior profile with {len(behavior_profile.current_indicators)} indicators")
        print(f"   Dominant categories: {[cat.value for cat in behavior_profile.dominant_categories]}")
        print(f"   Behavioral summary: {behavior_profile.behavioral_summary}")
        
        print("\nGenerating future predictions...")
        predictions = behavior_predictor.predict_behavior_for_date(
            behavior_profile,
            "2024-06-15"
        )
        
        print(f"✅ Generated {len(predictions)} behavioral predictions")
        
        print("\n✅ Sample analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Sample analysis failed: {e}")
        import traceback
        print(traceback.format_exc())
        return False


def main():
    """Main test runner function."""
    
    print("🚀 BMAD System Test Runner")
    print("=" * 70)
    print("Behavioral Model and Data Analysis System")
    print("Testing all components and functionality")
    print("=" * 70)
    
    # Track test results
    results = {
        'basic_functionality': False,
        'sample_analysis': False,
        'full_test_suite': False
    }
    
    # Run basic functionality test first
    results['basic_functionality'] = run_basic_functionality_test()
    
    # Run sample analysis if basic functionality works
    if results['basic_functionality']:
        results['sample_analysis'] = run_sample_analysis()
    
    # Run full test suite if basic functionality works
    if results['basic_functionality']:
        results['full_test_suite'] = run_bmad_tests()
    
    # Final summary
    print("\n" + "=" * 70)
    print("🏁 Final Test Results")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All BMAD system tests passed!")
        print("The Behavioral Model and Data analysis system is ready for use.")
        return 0
    else:
        print("\n⚠️  Some tests failed.")
        print("Please check the error messages above and fix any issues.")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)