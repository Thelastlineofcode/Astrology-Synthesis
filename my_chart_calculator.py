#!/usr/bin/env python3
"""
Personal Chart Calculator
Enter your birth data and get a complete astrological analysis!
"""

import requests
import json
from datetime import datetime

def get_birth_data():
    """Get birth data from user input."""
    print("🌟 Welcome to Your Personal Astrology Chart Calculator!")
    print("="*60)
    print("Please enter your birth information:")
    
    # Get birth date and time
    year = int(input("Birth Year (e.g., 1990): "))
    month = int(input("Birth Month (1-12): "))
    day = int(input("Birth Day (1-31): "))
    hour = int(input("Birth Hour (0-23, 24-hour format): "))
    minute = int(input("Birth Minute (0-59): "))
    
    # Get location
    print("\nFor accurate calculations, please provide your birth location:")
    latitude = float(input("Latitude (e.g., 40.7128 for NYC): "))
    longitude = float(input("Longitude (e.g., -74.0060 for NYC): "))
    
    name = input("Your name (optional): ") or "Personal Chart"
    
    return {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'latitude': latitude,
        'longitude': longitude,
        'name': name
    }

def calculate_chart(birth_data):
    """Calculate the astrological chart."""
    print(f"\n🔮 Calculating your chart for {birth_data['name']}...")
    
    # Format data for the API
    api_data = {
        'birthData': {
            'year': birth_data['year'],
            'month': birth_data['month'],
            'day': birth_data['day'],
            'hour': birth_data['hour'],
            'minute': birth_data['minute'],
            'latitude': birth_data['latitude'],
            'longitude': birth_data['longitude']
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/chart',
            json=api_data,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error calculating chart: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def get_personality_analysis(birth_data):
    """Get BMAD personality analysis."""
    print("🧠 Analyzing your personality...")
    
    try:
        response = requests.post(
            'http://localhost:5001/api/bmad/personality/analyze',
            json=birth_data,
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  Personality analysis unavailable: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️  BMAD server connection issue: {e}")
        return None

def get_symbolon_analysis(birth_data):
    """Get Symbolon archetypal analysis."""
    print("🃏 Drawing your Symbolon cards...")
    
    try:
        response = requests.post(
            'http://localhost:5001/symbolon-cards',
            json=birth_data,
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  Symbolon analysis unavailable: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"⚠️  Symbolon server connection issue: {e}")
        return None

def display_chart_results(chart_data):
    """Display the calculated chart in a beautiful format."""
    if not chart_data:
        return
        
    chart = chart_data.get('chart', {})
    planets = chart.get('planets', {})
    houses = chart.get('houses', {})
    
    print("\n" + "="*60)
    print("🌟 YOUR ASTROLOGICAL CHART")
    print("="*60)
    
    # Display key planetary positions
    print("\n🪐 PLANETARY POSITIONS:")
    print("-" * 40)
    
    key_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    for planet in key_planets:
        if planet in planets and planets[planet]:
            p = planets[planet]
            retrograde = " ℞" if p.get('retrograde', False) else ""
            print(f"   {planet:8}: {p['sign']:12} {p['degree']:6.2f}° (House {p['house']:2}){retrograde}")
    
    # Display rising sign
    if 'ascendant' in houses:
        asc = houses['ascendant']
        print(f"\n⬆️  ASCENDANT (Rising): {asc['sign']} {asc['degree']:.2f}°")
    
    # Display midheaven
    if 'midheaven' in houses:
        mc = houses['midheaven']
        print(f"🔝 MIDHEAVEN: {mc['sign']} {mc['degree']:.2f}°")
    
    # Count working planets
    working_planets = len([p for p in planets.values() if p])
    print(f"\n📊 Chart calculated with {working_planets}/13 planets")

def display_personality_results(personality_data):
    """Display personality analysis results."""
    if not personality_data:
        return
        
    traits = personality_data.get('traits', [])
    patterns = personality_data.get('behavioral_patterns', [])
    
    print("\n" + "="*60)
    print("🧠 PERSONALITY ANALYSIS (BMAD)")
    print("="*60)
    
    if traits:
        print(f"\n🌟 Key Personality Traits ({len(traits)} identified):")
        print("-" * 50)
        for trait in traits[:5]:  # Show top 5 traits
            name = trait.get('name', 'Unknown')
            intensity = trait.get('intensity', 'Unknown')
            description = trait.get('description', '')[:80]
            print(f"   • {name} ({intensity})")
            if description:
                print(f"     {description}...")
            print()
    
    if patterns:
        print(f"🔗 Behavioral Patterns: {len(patterns)} identified")

def display_symbolon_results(symbolon_data):
    """Display Symbolon card analysis."""
    if not symbolon_data:
        return
        
    cards = symbolon_data.get('cards', [])
    
    print("\n" + "="*60)
    print("🃏 SYMBOLON ARCHETYPAL ANALYSIS")
    print("="*60)
    
    if cards:
        print(f"\n🎴 Your Symbolon Cards ({len(cards)} drawn):")
        print("-" * 50)
        for card in cards[:3]:  # Show top 3 cards
            name = card.get('name', 'Unknown')
            archetype = card.get('archetype', 'Unknown')
            meaning = card.get('meaning', '')[:100]
            print(f"   🃏 {name}")
            print(f"      Archetype: {archetype}")
            if meaning:
                print(f"      Meaning: {meaning}...")
            print()

def main():
    """Main function to run the personal chart calculator."""
    try:
        # Check if servers are running
        health_check = requests.get('http://localhost:5000/api/health', timeout=3)
        if health_check.status_code != 200:
            print("❌ Chart calculation server is not running!")
            print("Please start it with: cd backend && python app.py")
            return
    except:
        print("❌ Chart calculation server is not running!")
        print("Please start it with: cd backend && python app.py")
        return
    
    print("✅ Servers are ready!")
    
    # Get birth data from user
    birth_data = get_birth_data()
    
    # Calculate chart
    chart_data = calculate_chart(birth_data)
    display_chart_results(chart_data)
    
    # Get personality analysis
    personality_data = get_personality_analysis(birth_data)
    display_personality_results(personality_data)
    
    # Get Symbolon analysis
    symbolon_data = get_symbolon_analysis(birth_data)
    display_symbolon_results(symbolon_data)
    
    print("\n" + "="*60)
    print("🎉 YOUR COMPLETE ASTROLOGICAL ANALYSIS IS COMPLETE!")
    print("="*60)
    print("Thank you for using the Astrology Synthesis system!")

if __name__ == "__main__":
    main()