"""
Comprehensive Chart Generation Test Suite
Tests all calculations using famous people's verified birth data
"""

import pytest
from datetime import datetime
from backend.services.calculation_service import CalculationService
from backend.schemas import BirthDataInput


class TestFamousPeopleCharts:
    """Test chart generation against known birth data of famous people"""
    
    @pytest.fixture
    def calc_service(self):
        return CalculationService()
    
    # ==================================================================
    # Test Case 1: Steve Jobs
    # Born: February 24, 1955, 7:15 PM PST
    # Location: San Francisco, CA (37.7749° N, 122.4194° W)
    # ==================================================================
    
    def test_steve_jobs_chart(self, calc_service):
        """Test Steve Jobs birth chart - Known Pisces with innovative mind"""
        birth_data = BirthDataInput(
            date="1955-02-24",
            time="19:15:00",
            timezone="America/Los_Angeles",
            latitude=37.7749,
            longitude=-122.4194,
            location_name="San Francisco, CA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Validate basic structure
        assert "planet_positions" in chart
        assert "house_cusps" in chart
        assert "ascendant" in chart
        assert len(chart["planet_positions"]) == 12  # All planets including Rahu/Ketu
        assert len(chart["house_cusps"]) == 12
        
        # Find Sun position - should be in Pisces (330-360 degrees)
        sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
        assert sun is not None
        assert sun["zodiac_sign"] == "Pisces"
        assert 330 <= sun["longitude"] <= 360
        
        # Validate all required fields for planets
        for planet in chart["planet_positions"]:
            assert "planet" in planet
            assert "longitude" in planet
            assert "degree" in planet
            assert "minutes" in planet
            assert "seconds" in planet
            assert "house" in planet
            assert "retrograde" in planet
            assert "nakshatra" in planet
            assert "pada" in planet
            assert isinstance(planet["retrograde"], bool)
            assert 1 <= planet["pada"] <= 4
    
    # ==================================================================
    # Test Case 2: Princess Diana
    # Born: July 1, 1961, 7:45 PM BST
    # Location: Sandringham, England (52.8303° N, 0.5115° E)
    # ==================================================================
    
    def test_princess_diana_chart(self, calc_service):
        """Test Princess Diana birth chart - Known Cancer Sun"""
        birth_data = BirthDataInput(
            date="1961-07-01",
            time="19:45:00",
            timezone="Europe/London",
            latitude=52.8303,
            longitude=0.5115,
            location_name="Sandringham, England"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Find Sun position - should be in Cancer (90-120 degrees)
        sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
        assert sun["zodiac_sign"] == "Cancer"
        assert 90 <= sun["longitude"] <= 120
        
        # Validate house cusps
        for house in chart["house_cusps"]:
            assert "house" in house
            assert "degree" in house
            assert "minutes" in house
            assert "seconds" in house
            assert "zodiac_sign" in house
            assert 1 <= house["house"] <= 12
            assert 0 <= house["degree"] < 360
    
    # ==================================================================
    # Test Case 3: Albert Einstein
    # Born: March 14, 1879, 11:30 AM LMT
    # Location: Ulm, Germany (48.4011° N, 9.9876° E)
    # ==================================================================
    
    def test_albert_einstein_chart(self, calc_service):
        """Test Albert Einstein birth chart - Known Pisces Sun"""
        birth_data = BirthDataInput(
            date="1879-03-14",
            time="11:30:00",
            timezone="Europe/Berlin",
            latitude=48.4011,
            longitude=9.9876,
            location_name="Ulm, Germany"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Sun should be in Pisces
        sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
        assert sun["zodiac_sign"] == "Pisces"
        
        # Validate aspects are calculated
        assert "aspects" in chart
        assert len(chart["aspects"]) > 0
        
        # Each aspect should have required fields
        for aspect in chart["aspects"]:
            assert "planet1" in aspect
            assert "planet2" in aspect
            assert "aspect" in aspect
            assert "angle" in aspect
    
    # ==================================================================
    # Test Case 4: Oprah Winfrey
    # Born: January 29, 1954, 4:30 AM CST
    # Location: Kosciusko, MS (33.0576° N, 89.5876° W)
    # ==================================================================
    
    def test_oprah_winfrey_chart(self, calc_service):
        """Test Oprah Winfrey birth chart - Known Aquarius Sun"""
        birth_data = BirthDataInput(
            date="1954-01-29",
            time="04:30:00",
            timezone="America/Chicago",
            latitude=33.0576,
            longitude=-89.5876,
            location_name="Kosciusko, MS"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Sun should be in Aquarius (300-330 degrees)
        sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
        assert sun["zodiac_sign"] == "Aquarius"
        assert 300 <= sun["longitude"] <= 330
    
    # ==================================================================
    # Test Case 5: Mahatma Gandhi
    # Born: October 2, 1869, 7:12 AM LMT
    # Location: Porbandar, India (21.6417° N, 69.6293° E)
    # ==================================================================
    
    def test_mahatma_gandhi_chart(self, calc_service):
        """Test Mahatma Gandhi birth chart - Known Libra Sun"""
        birth_data = BirthDataInput(
            date="1869-10-02",
            time="07:12:00",
            timezone="Asia/Kolkata",
            latitude=21.6417,
            longitude=69.6293,
            location_name="Porbandar, India"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # Sun should be in Libra (180-210 degrees)
        sun = next(p for p in chart["planet_positions"] if p["planet"] == "Sun")
        assert sun["zodiac_sign"] == "Libra"
        assert 180 <= sun["longitude"] <= 210


class TestPlanetaryCalculations:
    """Test individual planetary calculation accuracy"""
    
    @pytest.fixture
    def calc_service(self):
        return CalculationService()
    
    def test_all_planets_present(self, calc_service):
        """Verify all 12 bodies are calculated"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="12:00:00",
            timezone="UTC",
            latitude=0.0,
            longitude=0.0,
            location_name="Equator"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        planet_names = [p["planet"] for p in chart["planet_positions"]]
        
        expected_planets = [
            "Sun", "Moon", "Mercury", "Venus", "Mars",
            "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
            "Rahu", "Ketu"
        ]
        
        for planet in expected_planets:
            assert planet in planet_names, f"{planet} not found in calculations"
    
    def test_planet_longitude_ranges(self, calc_service):
        """Verify all planetary longitudes are within valid range"""
        birth_data = BirthDataInput(
            date="2024-06-15",
            time="15:30:00",
            timezone="America/New_York",
            latitude=40.7128,
            longitude=-74.0060,
            location_name="New York, NY"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        for planet in chart["planet_positions"]:
            assert 0 <= planet["longitude"] < 360, \
                f"{planet['planet']} longitude {planet['longitude']} out of range"
    
    def test_retrograde_detection(self, calc_service):
        """Test retrograde motion detection"""
        # Mercury retrograde period example
        birth_data = BirthDataInput(
            date="2024-04-01",  # Mercury retrograde period
            time="12:00:00",
            timezone="UTC",
            latitude=0.0,
            longitude=0.0,
            location_name="Test Location"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        # At least one planet should have retrograde status defined
        retrograde_statuses = [p["retrograde"] for p in chart["planet_positions"]]
        assert any(isinstance(r, bool) for r in retrograde_statuses)
    
    def test_nakshatra_calculations(self, calc_service):
        """Verify nakshatra calculations for all planets"""
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
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
            "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
            "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
            "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
            "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        for planet in chart["planet_positions"]:
            assert planet["nakshatra"] in valid_nakshatras, \
                f"Invalid nakshatra {planet['nakshatra']} for {planet['planet']}"
            assert 1 <= planet["pada"] <= 4, \
                f"Invalid pada {planet['pada']} for {planet['planet']}"


class TestHouseCalculations:
    """Test house cusp calculations"""
    
    @pytest.fixture
    def calc_service(self):
        return CalculationService()
    
    def test_twelve_houses(self, calc_service):
        """Verify 12 houses are calculated"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="00:00:00",
            timezone="UTC",
            latitude=51.5074,
            longitude=-0.1278,
            location_name="London, UK"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert len(chart["house_cusps"]) == 12
        
        house_numbers = [h["house"] for h in chart["house_cusps"]]
        assert house_numbers == list(range(1, 13))
    
    def test_house_cusp_degrees(self, calc_service):
        """Verify house cusps have valid degree values"""
        birth_data = BirthDataInput(
            date="1990-05-15",
            time="10:30:00",
            timezone="America/Los_Angeles",
            latitude=34.0522,
            longitude=-118.2437,
            location_name="Los Angeles, CA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        for house in chart["house_cusps"]:
            assert 0 <= house["degree"] < 360
            assert 0 <= house["minutes"] < 60
            assert 0 <= house["seconds"] < 60
    
    def test_ascendant_calculation(self, calc_service):
        """Verify ascendant (1st house cusp) is calculated"""
        birth_data = BirthDataInput(
            date="1995-08-20",
            time="14:45:00",
            timezone="Europe/Paris",
            latitude=48.8566,
            longitude=2.3522,
            location_name="Paris, France"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        assert "ascendant" in chart
        assert "degree" in chart["ascendant"]
        assert "zodiac_sign" in chart["ascendant"]
        assert 0 <= chart["ascendant"]["degree"] < 360
    
    def test_midheaven_calculation(self, calc_service):
        """Verify midheaven (10th house cusp) is calculated"""
        birth_data = BirthDataInput(
            date="1988-03-10",
            time="08:00:00",
            timezone="Asia/Tokyo",
            latitude=35.6762,
            longitude=139.6503,
            location_name="Tokyo, Japan"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        assert "midheaven" in chart
        assert "degree" in chart["midheaven"]
        assert "zodiac_sign" in chart["midheaven"]
        assert 0 <= chart["midheaven"]["degree"] < 360


class TestAspectCalculations:
    """Test planetary aspect calculations"""
    
    @pytest.fixture
    def calc_service(self):
        return CalculationService()
    
    def test_aspects_calculated(self, calc_service):
        """Verify aspects between planets are calculated"""
        birth_data = BirthDataInput(
            date="2010-07-04",
            time="16:20:00",
            timezone="America/New_York",
            latitude=40.7128,
            longitude=-74.0060,
            location_name="New York, NY"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        assert "aspects" in chart
        assert len(chart["aspects"]) > 0
    
    def test_aspect_types(self, calc_service):
        """Verify major aspect types are identified"""
        birth_data = BirthDataInput(
            date="1975-11-25",
            time="09:15:00",
            timezone="America/Los_Angeles",
            latitude=34.0522,
            longitude=-118.2437,
            location_name="Los Angeles, CA"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        valid_aspects = ["conjunction", "opposition", "trine", "square", "sextile"]
        
        for aspect in chart["aspects"]:
            assert aspect["aspect"] in valid_aspects
            assert 0 <= aspect["angle"] <= 180


class TestEdgeCases:
    """Test edge cases and special scenarios"""
    
    @pytest.fixture
    def calc_service(self):
        return CalculationService()
    
    def test_northern_hemisphere(self, calc_service):
        """Test calculations for northern hemisphere"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="12:00:00",
            timezone="America/Chicago",
            latitude=41.8781,
            longitude=-87.6298,
            location_name="Chicago, IL"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None
        assert len(chart["planet_positions"]) == 12
    
    def test_southern_hemisphere(self, calc_service):
        """Test calculations for southern hemisphere"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="12:00:00",
            timezone="Australia/Sydney",
            latitude=-33.8688,
            longitude=151.2093,
            location_name="Sydney, Australia"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None
        assert len(chart["planet_positions"]) == 12
    
    def test_equator(self, calc_service):
        """Test calculations at the equator"""
        birth_data = BirthDataInput(
            date="2000-06-21",
            time="12:00:00",
            timezone="Africa/Nairobi",
            latitude=0.0,
            longitude=36.8219,
            location_name="Equator, Kenya"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None
    
    def test_north_pole_region(self, calc_service):
        """Test calculations near north pole"""
        birth_data = BirthDataInput(
            date="2000-06-21",
            time="12:00:00",
            timezone="Arctic/Longyearbyen",
            latitude=78.2232,
            longitude=15.6267,
            location_name="Svalbard, Norway"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None
    
    def test_midnight_birth(self, calc_service):
        """Test calculations for midnight births"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="00:00:00",
            timezone="UTC",
            latitude=51.5074,
            longitude=-0.1278,
            location_name="London, UK"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None
    
    def test_noon_birth(self, calc_service):
        """Test calculations for noon births"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="12:00:00",
            timezone="UTC",
            latitude=0.0,
            longitude=0.0,
            location_name="Prime Meridian"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None
    
    def test_leap_year_date(self, calc_service):
        """Test calculations for leap year date"""
        birth_data = BirthDataInput(
            date="2000-02-29",
            time="12:00:00",
            timezone="America/New_York",
            latitude=40.7128,
            longitude=-74.0060,
            location_name="New York, NY"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        assert chart is not None


class TestDataConsistency:
    """Test data consistency and validation"""
    
    @pytest.fixture
    def calc_service(self):
        return CalculationService()
    
    def test_zodiac_sign_consistency(self, calc_service):
        """Verify zodiac signs match longitude ranges"""
        birth_data = BirthDataInput(
            date="2000-01-01",
            time="12:00:00",
            timezone="UTC",
            latitude=0.0,
            longitude=0.0,
            location_name="Test"
        )
        
        chart = calc_service.generate_birth_chart(birth_data)
        
        zodiac_ranges = {
            "Aries": (0, 30),
            "Taurus": (30, 60),
            "Gemini": (60, 90),
            "Cancer": (90, 120),
            "Leo": (120, 150),
            "Virgo": (150, 180),
            "Libra": (180, 210),
            "Scorpio": (210, 240),
            "Sagittarius": (240, 270),
            "Capricorn": (270, 300),
            "Aquarius": (300, 330),
            "Pisces": (330, 360)
        }
        
        for planet in chart["planet_positions"]:
            sign = planet["zodiac_sign"]
            longitude = planet["longitude"]
            min_deg, max_deg = zodiac_ranges[sign]
            assert min_deg <= longitude < max_deg, \
                f"{planet['planet']} at {longitude}° not in {sign} range"
    
    def test_dms_conversion_accuracy(self, calc_service):
        """Test degrees-minutes-seconds conversion"""
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
            # Reconstruct decimal from DMS
            reconstructed = planet["degree"] + planet["minutes"]/60 + planet["seconds"]/3600
            # Should be close to longitude (accounting for sign offset)
            zodiac_offset = (planet["degree"] // 30) * 30
            assert abs(planet["longitude"] - reconstructed) < 0.01 or \
                   abs(planet["longitude"] - (reconstructed + zodiac_offset)) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
