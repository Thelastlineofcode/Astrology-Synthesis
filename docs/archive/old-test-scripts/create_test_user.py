"""
Create a test user with complete profile data for system testing.
This script registers a user via the API with all required fields.
"""

import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8001/api/v1"

# Test User Data
test_user = {
    "email": "test@rootsrevealed.com",
    "password": "TestUser123!",
    "first_name": "Test",
    "last_name": "User"
}

# Birth Chart Data for Testing
test_chart_data = {
    "birth_date": "1990-01-15",
    "birth_time": "14:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York",
    "location_name": "New York, NY, USA"
}

def create_test_user():
    """Register a new test user and generate a sample chart."""
    
    print("=" * 70)
    print("CREATING TEST USER FOR ROOTS REVEALED SYSTEM")
    print("=" * 70)
    print()
    
    # Step 1: Register User
    print("Step 1: Registering test user...")
    print(f"  Email: {test_user['email']}")
    print(f"  Name: {test_user['first_name']} {test_user['last_name']}")
    print(f"  Password: {test_user['password']}")
    print()
    
    try:
        register_response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if register_response.status_code == 201:
            user_data = register_response.json()
            print("✅ User registered successfully!")
            print(f"  User ID: {user_data['user_id']}")
            print(f"  Email: {user_data['email']}")
            print(f"  Name: {user_data['first_name']} {user_data['last_name']}")
            print(f"  Access Token: {user_data['access_token'][:50]}...")
            print(f"  API Key: {user_data['api_key'][:50]}...")
            print()
            
            access_token = user_data['access_token']
            api_key = user_data['api_key']
            
        elif register_response.status_code == 400:
            # User might already exist, try logging in
            print("⚠️  User already exists, attempting login...")
            login_response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": test_user['email'],
                    "password": test_user['password']
                },
                headers={"Content-Type": "application/json"}
            )
            
            if login_response.status_code == 200:
                user_data = login_response.json()
                print("✅ Logged in successfully!")
                print(f"  User ID: {user_data['user_id']}")
                print(f"  Email: {user_data['email']}")
                print(f"  Name: {user_data.get('first_name', 'N/A')} {user_data.get('last_name', 'N/A')}")
                print(f"  Access Token: {user_data['access_token'][:50]}...")
                print()
                
                access_token = user_data['access_token']
                api_key = None
            else:
                print(f"❌ Login failed: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                return None
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return None
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend server!")
        print("   Make sure the backend is running on http://localhost:8001")
        return None
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None
    
    # Step 2: Generate Sample Birth Chart
    print("Step 2: Generating sample birth chart...")
    print(f"  Birth Date: {test_chart_data['birth_date']}")
    print(f"  Birth Time: {test_chart_data['birth_time']}")
    print(f"  Location: {test_chart_data['location_name']}")
    print(f"  Coordinates: ({test_chart_data['latitude']}, {test_chart_data['longitude']})")
    print()
    
    try:
        chart_response = requests.post(
            f"{BASE_URL}/charts/generate",
            json=test_chart_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        
        if chart_response.status_code == 201:
            chart_data = chart_response.json()
            print("✅ Birth chart generated successfully!")
            print(f"  Chart ID: {chart_data['chart_id']}")
            print(f"  Ascendant: {chart_data['ascendant']['sign']} {chart_data['ascendant']['degree']:.2f}°")
            print(f"  Moon Sign: {chart_data['moon_sign']}")
            print(f"  Sun Sign: {chart_data['sun_sign']}")
            print(f"  Nakshatra: {chart_data['nakshatra']['name']} ({chart_data['nakshatra']['pada']}/4)")
            print()
            print("  Planetary Positions:")
            for planet in chart_data['planets'][:5]:  # Show first 5 planets
                print(f"    {planet['name']}: {planet['sign']} {planet['degree']:.2f}° " +
                      f"(House {planet['house']}) {'R' if planet.get('retrograde') else ''}")
            print()
            
            chart_id = chart_data['chart_id']
            
        else:
            print(f"❌ Chart generation failed: {chart_response.status_code}")
            print(f"   Response: {chart_response.text}")
            chart_id = None
    
    except Exception as e:
        print(f"❌ ERROR generating chart: {str(e)}")
        chart_id = None
    
    # Step 3: Summary
    print("=" * 70)
    print("TEST USER SETUP COMPLETE")
    print("=" * 70)
    print()
    print("📋 Test Credentials:")
    print(f"  Email: {test_user['email']}")
    print(f"  Password: {test_user['password']}")
    print()
    print("🔑 Authentication:")
    print(f"  Access Token: {access_token[:50]}...")
    if api_key:
        print(f"  API Key: {api_key[:50]}...")
    print()
    print("📊 Test Data:")
    if chart_id:
        print(f"  Chart ID: {chart_id}")
    print(f"  Birth Date: {test_chart_data['birth_date']}")
    print(f"  Location: {test_chart_data['location_name']}")
    print()
    print("✨ You can now use these credentials to:")
    print("  1. Login at http://localhost:3001/auth/login")
    print("  2. View your chart at the readings page")
    print("  3. Test all API endpoints with the access token")
    print("  4. Make programmatic API calls with the API key")
    print()
    
    return {
        "user": user_data,
        "chart_id": chart_id,
        "credentials": test_user
    }


if __name__ == "__main__":
    result = create_test_user()
    
    if result:
        # Save credentials to file for easy reference
        with open("test_user_credentials.json", "w") as f:
            json.dump({
                "email": test_user['email'],
                "password": test_user['password'],
                "created_at": datetime.now().isoformat(),
                "note": "Test user for system validation"
            }, f, indent=2)
        
        print("💾 Credentials saved to: test_user_credentials.json")
        print()
