#!/usr/bin/env python3
"""
BMAD Analysis Script
Easy-to-use script for running BMAD personality and behavior analysis.
"""

import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def run_bmad_analysis(birth_data, chart_data=None, person_name="Analysis Subject"):
    """
    Run complete BMAD analysis on birth data.
    
    Args:
        birth_data: Dictionary with birth information
        chart_data: Optional pre-calculated chart data
        person_name: Name for the analysis subject
    
    Returns:
        Dictionary with complete analysis results
    """
    try:
        from bmad.services.personality_analyzer import PersonalityAnalyzer
        from bmad.services.behavior_predictor import BehaviorPredictor
        
        print(f"🧠 Running BMAD Analysis for {person_name}")
        print("=" * 60)
        
        # If no chart data provided, create sample data
        if chart_data is None:
            print("⚠️  No chart data provided, using sample data for demonstration")
            chart_data = create_sample_chart_data()
        
        # Initialize analyzers
        personality_analyzer = PersonalityAnalyzer()
        behavior_predictor = BehaviorPredictor()
        
        # Run personality analysis
        print("🔍 Analyzing personality traits...")
        personality_profile = personality_analyzer.analyze_personality(
            chart_data, birth_data, person_name
        )
        
        # Run behavioral analysis
        print("🎯 Analyzing behavioral patterns...")
        behavior_profile = behavior_predictor.create_behavior_profile(
            chart_data, birth_data, person_name
        )
        
        # Generate predictions
        print("📅 Generating future predictions...")
        future_date = "2024-06-15"  # You can customize this
        predictions = behavior_predictor.predict_behavior_for_date(
            behavior_profile, future_date
        )
        
        # Compile results
        results = {
            'timestamp': datetime.now().isoformat(),
            'person_name': person_name,
            'birth_data': birth_data,
            'personality_profile': personality_profile.to_dict(),
            'behavior_profile': behavior_profile.to_dict(),
            'future_predictions': [pred.to_dict() for pred in predictions],
            'analysis_summary': generate_summary(personality_profile, behavior_profile, predictions)
        }
        
        # Display results
        display_results(personality_profile, behavior_profile, predictions)
        
        return results
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_sample_chart_data():
    """Create sample chart data for demonstration."""
    return {
        'planets': {
            'Sun': {'sign': 'Leo', 'degree': 15.5, 'house': 5},
            'Moon': {'sign': 'Cancer', 'degree': 22.3, 'house': 4},
            'Mercury': {'sign': 'Virgo', 'degree': 8.1, 'house': 6},
            'Venus': {'sign': 'Leo', 'degree': 20.0, 'house': 5},
            'Mars': {'sign': 'Aries', 'degree': 12.0, 'house': 1},
            'Jupiter': {'sign': 'Sagittarius', 'degree': 8.0, 'house': 9},
            'Saturn': {'sign': 'Capricorn', 'degree': 18.0, 'house': 10}
        },
        'houses': {
            'house_1': {'sign': 'Aries', 'degree': 12.0},
            'house_4': {'sign': 'Cancer', 'degree': 12.0},
            'house_5': {'sign': 'Leo', 'degree': 12.0},
            'house_6': {'sign': 'Virgo', 'degree': 12.0},
            'house_9': {'sign': 'Sagittarius', 'degree': 12.0},
            'house_10': {'sign': 'Capricorn', 'degree': 12.0}
        },
        'aspects': [
            {'planet1': 'Sun', 'planet2': 'Venus', 'aspect': 'conjunction', 'orb': 4.5},
            {'planet1': 'Moon', 'planet2': 'Mars', 'aspect': 'trine', 'orb': 2.3},
            {'planet1': 'Mercury', 'planet2': 'Jupiter', 'aspect': 'sextile', 'orb': 3.1}
        ]
    }


def display_results(personality_profile, behavior_profile, predictions):
    """Display analysis results in a user-friendly format."""
    
    print("\n" + "=" * 60)
    print("📊 BMAD ANALYSIS RESULTS")
    print("=" * 60)
    
    # Personality Results
    print(f"\n🧠 PERSONALITY ANALYSIS")
    print("-" * 30)
    print(f"📈 {len(personality_profile.traits)} personality traits identified")
    print(f"🎯 Dominant dimensions: {', '.join([dim.value.replace('_', ' ').title() for dim in personality_profile.dominant_dimensions])}")
    print(f"📝 {personality_profile.summary}")
    
    if personality_profile.traits:
        print(f"\n🌟 Top Personality Traits:")
        for i, trait in enumerate(personality_profile.traits[:5], 1):
            print(f"   {i}. {trait.name}")
            print(f"      Dimension: {trait.dimension.value.replace('_', ' ').title()}")
            print(f"      Intensity: {trait.intensity.value}/5 ⭐")
            print(f"      Description: {trait.description}")
            print()
    
    # Behavioral Results
    print(f"🎯 BEHAVIORAL ANALYSIS")
    print("-" * 30)
    print(f"📈 {len(behavior_profile.current_indicators)} behavioral indicators")
    print(f"🎯 Dominant categories: {', '.join([cat.value.replace('_', ' ').title() for cat in behavior_profile.dominant_categories])}")
    print(f"📝 {behavior_profile.behavioral_summary}")
    
    if behavior_profile.current_indicators:
        print(f"\n🔍 Key Behavioral Indicators:")
        for i, indicator in enumerate(behavior_profile.current_indicators[:5], 1):
            print(f"   {i}. {indicator.name}")
            print(f"      Category: {indicator.category.value.replace('_', ' ').title()}")
            print(f"      Intensity: {indicator.intensity:.1f}/1.0 ⭐")
            print(f"      Description: {indicator.description}")
            print()
    
    # Predictions
    if predictions:
        print(f"🔮 FUTURE PREDICTIONS")
        print("-" * 30)
        print(f"📅 {len(predictions)} predictions generated")
        
        for i, pred in enumerate(predictions[:3], 1):
            print(f"\n   {i}. {pred.category.value.replace('_', ' ').title()} Prediction")
            print(f"      Behaviors: {', '.join(pred.predicted_behaviors)}")
            print(f"      Confidence: {pred.confidence.value}/5 ⭐")
            print(f"      Duration: {pred.duration_days} days")
            if pred.recommendations:
                print(f"      Recommendation: {pred.recommendations[0]}")
    
    print(f"\n✅ Analysis Complete!")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def generate_summary(personality_profile, behavior_profile, predictions):
    """Generate a text summary of the analysis."""
    summary_parts = [
        f"Personality analysis revealed {len(personality_profile.traits)} traits",
        f"with dominant focus on {', '.join([dim.value for dim in personality_profile.dominant_dimensions[:2]])}.",
        f"Behavioral analysis identified {len(behavior_profile.current_indicators)} key indicators",
        f"primarily in {', '.join([cat.value for cat in behavior_profile.dominant_categories[:2]])} areas.",
        f"Generated {len(predictions)} future predictions with varying confidence levels."
    ]
    return " ".join(summary_parts)


def save_results(results, filename=None):
    """Save analysis results to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"bmad_analysis_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Results saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
        return None


# Example usage
if __name__ == '__main__':
    print("🚀 BMAD Analysis Script")
    print("=" * 40)
    
    # Example birth data
    sample_birth_data = {
        'year': 1990,
        'month': 8,
        'day': 15,
        'hour': 14,
        'minute': 30,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    
    # Run analysis
    results = run_bmad_analysis(
        birth_data=sample_birth_data,
        person_name="Sample Analysis"
    )
    
    # Save results
    if results:
        save_results(results)
        
        print(f"\n🎯 How to use this script:")
        print(f"1. Modify the birth_data dictionary with real birth information")
        print(f"2. If you have chart data, pass it as chart_data parameter")
        print(f"3. Results are automatically saved to a JSON file")
        print(f"4. Integrate this script into your astrology application")