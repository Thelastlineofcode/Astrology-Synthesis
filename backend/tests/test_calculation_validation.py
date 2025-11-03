"""
Chart Calculation Validation Tests
Tests accuracy of calculations with famous people's birth data
"""

import pytest
from backend.services.calculation_service import CalculationService
from backend.schemas import BirthDataInput


@pytest.fixture
def calc_service():
    return CalculationService()


class TestPlanetaryCalculations:
    """Test planetary position calculations"""
    
    def test_sun_position_accuracy(self, calc_service):
        """Test Sun position calculation - December 19, 1984, 12:00 PM CST"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Find Sun
        sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
        
        # Sun should be in Sagittarius (240-270 degrees) on Dec 19
        assert sun["zodiac_sign"] == "Sagittarius"
        assert 240 <= sun["longitude"] < 270
        assert sun["house"] is not None
        assert "retrograde" in sun
        assert "nakshatra" in sun
        assert "pada" in sun
        assert "degree" in sun
        assert "minutes" in sun
        assert "seconds" in sun
    
    def test_all_planets_present(self, calc_service):
        """Test that all planets are calculated"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        planets = [p["planet"] for p in chart["planet_positions"]]
        
        expected = ["Sun", "Moon", "Mercury", "Venus", "Mars", 
                   "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
                   "Rahu", "Ketu"]
        
        for planet in expected:
            assert planet in planets, f"{planet} missing from calculations"
    
    def test_retrograde_detection(self, calc_service):
        """Test retrograde planet detection"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # All planets should have retrograde field
        for planet in chart["planet_positions"]:
            assert "retrograde" in planet
            assert isinstance(planet["retrograde"], bool)


class TestHouseCalculations:
    """Test house cusp calculations"""
    
    def test_house_cusps_count(self, calc_service):
        """Test that all 12 house cusps are calculated"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        assert len(chart["house_cusps"]) == 12
        houses = [h["house"] for h in chart["house_cusps"]]
        assert houses == list(range(1, 13))
    
    def test_house_cusp_structure(self, calc_service):
        """Test house cusp data structure"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        for cusp in chart["house_cusps"]:
            assert "house" in cusp
            assert "longitude" in cusp
            assert "zodiac_sign" in cusp
            assert "degree" in cusp
            assert "minutes" in cusp
            assert "seconds" in cusp
            
            # Validate ranges
            assert 1 <= cusp["house"] <= 12
            assert 0 <= cusp["longitude"] < 360
            assert 0 <= cusp["degree"] < 360
            assert 0 <= cusp["minutes"] < 60
            assert 0 <= cusp["seconds"] < 60
    
    def test_ascendant_calculation(self, calc_service):
        """Test ascendant (1st house cusp) calculation"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        assert "ascendant" in chart
        assert chart["ascendant"] is not None
        
        # Ascendant should match 1st house cusp
        first_house = next(h for h in chart["house_cusps"] if h["house"] == 1)
        assert chart["ascendant"] == first_house["longitude"]


class TestNakshatraCalculations:
    """Test nakshatra assignment calculations"""
    
    def test_nakshatra_assignment(self, calc_service):
        """Test that all planets have nakshatra assignments"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        for planet in chart["planet_positions"]:
            if planet["planet"] not in ["Rahu", "Ketu"]:
                assert "nakshatra" in planet
                assert planet["nakshatra"] is not None
                assert "pada" in planet
                assert 1 <= planet["pada"] <= 4
    
    def test_nakshatra_valid_names(self, calc_service):
        """Test that nakshatra names are valid"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        valid_nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", 
            "Uttara Bhadrapada", "Revati"
        ]
        
        for planet in chart["planet_positions"]:
            if "nakshatra" in planet and planet["nakshatra"]:
                assert planet["nakshatra"] in valid_nakshatras


class TestAspectCalculations:
    """Test aspect detection and calculation"""
    
    def test_aspects_structure(self, calc_service):
        """Test aspect data structure"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        assert "aspects" in chart
        assert isinstance(chart["aspects"], list)
        
        if len(chart["aspects"]) > 0:
            for aspect in chart["aspects"]:
                assert "planet1" in aspect
                assert "planet2" in aspect
                assert "aspect_type" in aspect
                assert "angle" in aspect
                assert "orb" in aspect
    
    def test_major_aspects_detected(self, calc_service):
        """Test that major aspects are detected"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Should have at least some aspects
        assert len(chart["aspects"]) > 0
        
        # Check aspect types are valid
        valid_aspects = ["Conjunction", "Opposition", "Trine", "Square", "Sextile"]
        for aspect in chart["aspects"]:
            assert aspect["aspect_type"] in valid_aspects


class TestZodiacCalculations:
    """Test zodiac sign assignments"""
    
    def test_zodiac_signs_valid(self, calc_service):
        """Test that all zodiac signs are valid"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        valid_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        for planet in chart["planet_positions"]:
            assert planet["zodiac_sign"] in valid_signs
        
        for cusp in chart["house_cusps"]:
            assert cusp["zodiac_sign"] in valid_signs
    
    def test_sign_longitude_correspondence(self, calc_service):
        """Test that zodiac signs match longitude ranges"""
        birth_data = BirthDataInput(
            date="1984-12-19",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=29.9844,
            longitude=-90.1547,
            location_name="Metairie, LA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        sign_ranges = {
            "Aries": (0, 30), "Taurus": (30, 60), "Gemini": (60, 90),
            "Cancer": (90, 120), "Leo": (120, 150), "Virgo": (150, 180),
            "Libra": (180, 210), "Scorpio": (210, 240), "Sagittarius": (240, 270),
            "Capricorn": (270, 300), "Aquarius": (300, 330), "Pisces": (330, 360)
        }
        
        for planet in chart["planet_positions"]:
            sign = planet["zodiac_sign"]
            longitude = planet["longitude"]
            start, end = sign_ranges[sign]
            assert start <= longitude < end, f"{planet['planet']} at {longitude}° not in {sign} range {start}-{end}"


class TestDateTimeValidation:
    """Test date/time handling"""
    
    def test_valid_date_formats(self, calc_service):
        """Test various valid date formats"""
        valid_dates = [
            ("1984-12-19", "12:00:00"),
            ("2000-01-01", "00:00:00"),
            ("1955-02-24", "19:15:00"),
        ]
        
        for date, time in valid_dates:
            birth_data = BirthDataInput(
                date=date,
                time=time,
                timezone="America/Chicago",
                latitude=29.9844,
                longitude=-90.1547,
                location_name="Test"
            )
            
            chart = calc_service.generate_birth_chart(birth_data)
            assert chart is not None
            assert "planet_positions" in chart
    
    def test_timezone_handling(self, calc_service):
        """Test different timezone inputs"""
        timezones = [
            "America/Chicago",
            "America/New_York",
            "America/Los_Angeles",
            "Europe/London",
            "Asia/Kolkata",
        ]
        
        for tz in timezones:
            birth_data = BirthDataInput(
                date="1984-12-19",
                time="12:00:00",
                timezone=tz,
                latitude=29.9844,
                longitude=-90.1547,
                location_name="Test"
            )
            
            chart = calc_service.generate_birth_chart(birth_data)
            assert chart is not None


class TestCoordinateValidation:
    """Test geographic coordinate handling"""
    
    def test_latitude_ranges(self, calc_service):
        """Test valid latitude values"""
        latitudes = [
            (0, 0),  # Equator
            (90, 0),  # North Pole
            (-90, 0),  # South Pole
            (40.7128, -74.0060),  # New York
        ]
        
        for lat, lon in latitudes:
            birth_data = BirthDataInput(
                date="1984-12-19",
                time="12:00:00",
                timezone="UTC",
                latitude=lat,
                longitude=lon,
                location_name="Test"
            )
            
            chart = calc_service.generate_birth_chart(birth_data)
            assert chart is not None
    
    def test_longitude_ranges(self, calc_service):
        """Test valid longitude values"""
        coordinates = [
            (0, 0),  # Prime Meridian
            (0, 180),  # International Date Line
            (0, -180),  # International Date Line (West)
            (51.5074, -0.1278),  # London
        ]
        
        for lat, lon in coordinates:
            birth_data = BirthDataInput(
                date="1984-12-19",
                time="12:00:00",
                timezone="UTC",
                latitude=lat,
                longitude=lon,
                location_name="Test"
            )
            
            chart = calc_service.generate_birth_chart(birth_data)
            assert chart is not None
