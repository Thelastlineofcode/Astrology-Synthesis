#!/usr/bin/env python3
"""
Register user and get auth token for chart generation
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8001/api/v1"

def register_user():
    """Register The Last of Laplace user"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "laplace@mula.app",
        "username": "TheLastOfLaplace",
        "password": "Mula2025!Astrology",
        "full_name": "The Last of Laplace"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("✅ User registered successfully!")
            return response.json()
        elif response.status_code == 400 and "already exists" in response.text.lower():
            print("ℹ️  User already exists, proceeding to login...")
            return None
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def login_user():
    """Login and get access token"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "laplace@mula.app",
        "password": "Mula2025!Astrology"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"\n🔑 Access Token:\n{result['access_token']}\n")
            return result['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_chart_generation(token):
    """Test generating a birth chart"""
    url = f"{BASE_URL}/chart"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "birth_data": {
            "date": "1984-12-19",
            "time": "12:00:00",
            "latitude": 29.9844,
            "longitude": -90.1547,
            "timezone": "America/Chicago",
            "location_name": "Metairie, LA"
        }
    }
    
    try:
        print("\n🌟 Generating test chart...")
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            chart = response.json()
            print("✅ Chart generated successfully!")
            print(f"\nChart ID: {chart['chart_id']}")
            print(f"Location: {chart['birth_location']}")
            
            # Show some chart data
            if 'chart_data' in chart and 'planets' in chart['chart_data']:
                print("\n📊 Planetary Positions:")
                for planet in list(chart['chart_data']['planets'].keys())[:5]:
                    pos = chart['chart_data']['planets'][planet]
                    print(f"  {planet}: {pos.get('longitude', 0):.2f}°")
            
            return chart
        else:
            print(f"❌ Chart generation failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🌟 Mula Chart Generation Setup\n" + "="*50)
    
    # Register
    register_user()
    
    # Login
    token = login_user()
    
    if token:
        # Test chart generation
        chart = test_chart_generation(token)
        
        if chart:
            print("\n" + "="*50)
            print("✅ SETUP COMPLETE!")
            print("\nYour auth token has been generated.")
            print("Copy it to use in the frontend chart tool.")
            print("\n🔑 Save this token:")
            print(f"\n{token}\n")
    else:
        print("\n❌ Setup failed. Please check if backend is running on port 8001")
        sys.exit(1)
