#!/usr/bin/env python3
"""
Comprehensive Astrology Synthesis Application Test
Tests all major functionality across both servers.
"""

import requests
import json
import time
from datetime import datetime

# Server configurations
MAIN_API_BASE = "http://localhost:5000"
BMAD_API_BASE = "http://localhost:5001"

# Test birth data
TEST_BIRTH_DATA = {
    "birthData": {
        "year": 1990,
        "month": 7,
        "day": 4,
        "hour": 12,
        "minute": 0,
        "latitude": 40.7128,
        "longitude": -74.0060
    },
    "options": {
        "house_system": "P"
    }
}

# BMAD format test data
BMAD_BIRTH_DATA = {
    "year": 1990,
    "month": 7,
    "day": 4,
    "hour": 12,
    "minute": 0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "name": "Test Person"
}

def print_header(title):
    """Print a formatted test section header."""
    print(f"\n{'='*60}")
    print(f"🔬 {title}")
    print('='*60)

def print_result(endpoint, status_code, success=True, details=""):
    """Print a formatted test result."""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"   {status} {endpoint} - Status: {status_code}")
    if details:
        print(f"        {details}")

def test_server_health():
    """Test both servers are responding."""
    print_header("SERVER HEALTH CHECKS")
    
    # Test main Flask app
    try:
        response = requests.get(f"{MAIN_API_BASE}/api/health", timeout=5)
        print_result("/api/health (Main)", response.status_code, 
                    response.status_code == 200, 
                    f"Response time: {response.elapsed.total_seconds():.3f}s")
    except Exception as e:
        print_result("/api/health (Main)", "ERROR", False, str(e))
    
    # Test BMAD server
    try:
        response = requests.get(f"{BMAD_API_BASE}/api/health", timeout=5)
        print_result("/api/health (BMAD)", response.status_code,
                    response.status_code == 200,
                    f"Response time: {response.elapsed.total_seconds():.3f}s")
    except Exception as e:
        print_result("/api/health (BMAD)", "ERROR", False, str(e))

def test_chart_calculation():
    """Test core chart calculation functionality."""
    print_header("CHART CALCULATION TESTS")
    
    try:
        response = requests.post(
            f"{MAIN_API_BASE}/api/chart",
            json=TEST_BIRTH_DATA,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            chart = data.get('chart', {})
            planets = chart.get('planets', {})
            houses = chart.get('houses', {})
            
            working_planets = len([p for p in planets.values() if p])
            house_count = len(houses)
            
            print_result("/api/chart", response.status_code, True,
                        f"Planets: {working_planets}/13, Houses: {house_count}")
            
            # Show some key planetary positions
            if 'Sun' in planets and planets['Sun']:
                sun = planets['Sun']
                print(f"        ☀️  Sun: {sun.get('sign')} {sun.get('degree', 0):.1f}°")
            
            if 'Moon' in planets and planets['Moon']:
                moon = planets['Moon']
                print(f"        🌙 Moon: {moon.get('sign')} {moon.get('degree', 0):.1f}°")
                
            if 'ascendant' in houses:
                asc = houses['ascendant']
                print(f"        ⬆️  Ascendant: {asc.get('sign')} {asc.get('degree', 0):.1f}°")
        else:
            print_result("/api/chart", response.status_code, False, 
                        response.text[:100])
            
    except Exception as e:
        print_result("/api/chart", "ERROR", False, str(e))

def test_bmad_personality():
    """Test BMAD personality analysis."""
    print_header("BMAD PERSONALITY ANALYSIS")
    
    try:
        response = requests.post(
            f"{BMAD_API_BASE}/api/bmad/personality/analyze",
            json=BMAD_BIRTH_DATA,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            traits = data.get('traits', [])
            patterns = data.get('behavioral_patterns', [])
            
            print_result("/api/bmad/personality/analyze", response.status_code, True,
                        f"Traits: {len(traits)}, Patterns: {len(patterns)}")
            
            # Show sample trait
            if traits:
                trait = traits[0]
                print(f"        🌟 Sample: {trait.get('name', 'Unknown')} - {trait.get('intensity', 'Unknown')}")
                
        else:
            print_result("/api/bmad/personality/analyze", response.status_code, False,
                        response.text[:100])
            
    except Exception as e:
        print_result("/api/bmad/personality/analyze", "ERROR", False, str(e))

def test_bmad_behavior():
    """Test BMAD behavior prediction."""
    print_header("BMAD BEHAVIOR PREDICTION")
    
    try:
        response = requests.post(
            f"{BMAD_API_BASE}/api/bmad/behavior/profile",
            json=BMAD_BIRTH_DATA,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            indicators = data.get('current_indicators', [])
            predictions = data.get('future_predictions', [])
            triggers = data.get('behavior_triggers', [])
            
            print_result("/api/bmad/behavior/profile", response.status_code, True,
                        f"Indicators: {len(indicators)}, Predictions: {len(predictions)}, Triggers: {len(triggers)}")
            
        else:
            print_result("/api/bmad/behavior/profile", response.status_code, False,
                        response.text[:100])
            
    except Exception as e:
        print_result("/api/bmad/behavior/profile", "ERROR", False, str(e))

def test_symbolon_analysis():
    """Test Symbolon card analysis."""
    print_header("SYMBOLON ARCHETYPAL ANALYSIS")
    
    try:
        response = requests.post(
            f"{BMAD_API_BASE}/symbolon-cards",
            json=BMAD_BIRTH_DATA,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            cards = data.get('cards', [])
            analysis = data.get('analysis', {})
            
            print_result("/symbolon-cards", response.status_code, True,
                        f"Cards: {len(cards)}, Analysis sections: {len(analysis)}")
            
            # Show sample card
            if cards:
                card = cards[0]
                print(f"        🃏 Sample: {card.get('name', 'Unknown')} - {card.get('archetype', 'Unknown')}")
                
        else:
            print_result("/symbolon-cards", response.status_code, False,
                        response.text[:100])
            
    except Exception as e:
        print_result("/symbolon-cards", "ERROR", False, str(e))

def test_full_analysis():
    """Test complete BMAD analysis integration."""
    print_header("COMPLETE INTEGRATED ANALYSIS")
    
    try:
        response = requests.post(
            f"{BMAD_API_BASE}/api/bmad/combined/full-analysis",
            json=BMAD_BIRTH_DATA,
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result("/api/bmad/combined/full-analysis", response.status_code, True,
                        f"Complete analysis generated successfully")
            
            # Show analysis components
            components = [key for key in data.keys() if key != 'metadata']
            print(f"        📊 Components: {', '.join(components)}")
            
        else:
            print_result("/api/bmad/combined/full-analysis", response.status_code, False,
                        response.text[:100])
            
    except Exception as e:
        print_result("/api/bmad/combined/full-analysis", "ERROR", False, str(e))

def run_performance_test():
    """Test system performance."""
    print_header("PERFORMANCE TESTING")
    
    start_time = time.time()
    
    # Test chart calculation speed
    try:
        start = time.time()
        response = requests.post(f"{MAIN_API_BASE}/api/chart", json=TEST_BIRTH_DATA, timeout=10)
        chart_time = time.time() - start
        
        print_result("Chart Calculation Speed", "PERF", True,
                    f"Time: {chart_time:.3f}s")
    except Exception as e:
        print_result("Chart Calculation Speed", "ERROR", False, str(e))
    
    # Test BMAD analysis speed  
    try:
        start = time.time()
        response = requests.post(f"{BMAD_API_BASE}/api/bmad/personality/analyze", 
                               json=BMAD_BIRTH_DATA, timeout=15)
        bmad_time = time.time() - start
        
        print_result("BMAD Analysis Speed", "PERF", True,
                    f"Time: {bmad_time:.3f}s")
    except Exception as e:
        print_result("BMAD Analysis Speed", "ERROR", False, str(e))

def main():
    """Run comprehensive application tests."""
    print("🚀 ASTROLOGY SYNTHESIS APPLICATION TEST SUITE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing servers:")
    print(f"  • Main API: {MAIN_API_BASE}")
    print(f"  • BMAD API: {BMAD_API_BASE}")
    
    # Run all tests
    test_server_health()
    test_chart_calculation()
    test_bmad_personality()
    test_bmad_behavior()
    test_symbolon_analysis()
    test_full_analysis()
    run_performance_test()
    
    print_header("TEST SUITE COMPLETE")
    print("🎯 All functionality tests completed!")
    print("Check the results above to verify system status.")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()