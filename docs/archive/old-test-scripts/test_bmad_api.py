#!/usr/bin/env python3
"""
BMAD API Usage Examples
Shows how to use BMAD through the REST API when Flask server is running.
"""

import requests
import json
from datetime import datetime

# API base URL (adjust if your server runs on different port)
API_BASE = "http://localhost:5000/api"

def test_bmad_api():
    """Test BMAD API endpoints."""
    
    print("🌐 BMAD API Usage Examples")
    print("=" * 50)
    
    # Sample data for API calls
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
            'house_5': {'sign': 'Leo', 'degree': 12.0}
        },
        'aspects': [
            {'planet1': 'Sun', 'planet2': 'Venus', 'aspect': 'conjunction', 'orb': 4.5}
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
    
    try:
        # Test 1: Personality Analysis
        print("🧠 Testing Personality Analysis API...")
        personality_url = f"{API_BASE}/bmad/personality/analyze"
        personality_payload = {
            "chart_data": sample_chart_data,
            "birth_data": sample_birth_data,
            "profile_name": "API Test Person"
        }
        
        response = requests.post(personality_url, json=personality_payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Personality analysis successful!")
            print(f"   Traits found: {len(result['personality_profile']['traits'])}")
        else:
            print(f"❌ Personality analysis failed: {response.status_code}")
        
        # Test 2: Behavior Profile
        print("\n🎯 Testing Behavior Profile API...")
        behavior_url = f"{API_BASE}/bmad/behavior/profile"
        behavior_payload = {
            "chart_data": sample_chart_data,
            "birth_data": sample_birth_data,
            "person_name": "API Test Person"
        }
        
        response = requests.post(behavior_url, json=behavior_payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Behavior profile successful!")
            print(f"   Indicators found: {len(result['behavior_profile']['current_indicators'])}")
        else:
            print(f"❌ Behavior profile failed: {response.status_code}")
        
        # Test 3: Full Analysis
        print("\n🌟 Testing Full BMAD Analysis API...")
        full_url = f"{API_BASE}/bmad/combined/full-analysis"
        full_payload = {
            "chart_data": sample_chart_data,
            "birth_data": sample_birth_data,
            "person_name": "API Test Person",
            "analysis_options": {
                "include_predictions": True,
                "prediction_months": 3
            }
        }
        
        response = requests.post(full_url, json=full_payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Full analysis successful!")
            print(f"   Personality traits: {len(result['personality_profile']['traits'])}")
            print(f"   Behavior indicators: {len(result['behavior_profile']['current_indicators'])}")
            if 'future_predictions' in result:
                print(f"   Future predictions: {len(result['future_predictions'])}")
        else:
            print(f"❌ Full analysis failed: {response.status_code}")
        
        # Test 4: Enhanced Chart (integrated with regular chart calculation)
        print("\n📊 Testing Enhanced Chart API...")
        enhanced_url = f"{API_BASE}/chart/enhanced"
        enhanced_payload = {
            "birthData": sample_birth_data,
            "options": {
                "zodiacType": "tropical",
                "houseSystem": "P"
            },
            "bmadOptions": {
                "includeBMAD": True,
                "includePersonality": True,
                "includeBehavior": True,
                "includePredictions": True,
                "predictionMonths": 6,
                "personName": "Enhanced Chart Test"
            }
        }
        
        response = requests.post(enhanced_url, json=enhanced_payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Enhanced chart successful!")
            print(f"   Chart data: {'chart' in result}")
            print(f"   BMAD personality: {'bmad_personality' in result}")
            print(f"   BMAD behavior: {'bmad_behavior' in result}")
            print(f"   BMAD predictions: {'bmad_predictions' in result}")
        else:
            print(f"❌ Enhanced chart failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure Flask server is running on http://localhost:5000")
        print("\nTo start the server:")
        print("1. cd backend")
        print("2. python app.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def show_curl_examples():
    """Show curl command examples for API usage."""
    
    print("\n🔧 CURL Command Examples")
    print("=" * 50)
    
    print("1. Personality Analysis:")
    print("""curl -X POST http://localhost:5000/api/bmad/personality/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "chart_data": {
      "planets": {
        "Sun": {"sign": "Leo", "degree": 15.5, "house": 5}
      }
    },
    "birth_data": {
      "year": 1990, "month": 8, "day": 15,
      "hour": 14, "minute": 30,
      "latitude": 40.7128, "longitude": -74.0060
    },
    "profile_name": "Test Person"
  }'""")
    
    print("\n2. Full BMAD Analysis:")
    print("""curl -X POST http://localhost:5000/api/bmad/combined/full-analysis \\
  -H "Content-Type: application/json" \\
  -d '{
    "chart_data": {...},
    "birth_data": {...},
    "person_name": "Test Person",
    "analysis_options": {
      "include_predictions": true,
      "prediction_months": 6
    }
  }'""")
    
    print("\n3. Enhanced Chart with BMAD:")
    print("""curl -X POST http://localhost:5000/api/chart/enhanced \\
  -H "Content-Type: application/json" \\
  -d '{
    "birthData": {...},
    "bmadOptions": {
      "includeBMAD": true,
      "includePersonality": true,
      "includeBehavior": true,
      "includePredictions": true
    }
  }'""")


if __name__ == '__main__':
    test_bmad_api()
    show_curl_examples()
    
    print(f"\n✨ BMAD Integration Summary:")
    print(f"1. 🐍 Direct Python: Use the analysis script we just created")
    print(f"2. 🌐 REST API: Use HTTP requests when Flask server is running")  
    print(f"3. 📊 Enhanced Charts: Get regular charts + BMAD analysis together")
    print(f"4. 🔧 Custom Integration: Import BMAD services directly in your code")