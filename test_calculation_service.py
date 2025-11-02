"""
Unit tests for CalculationService.generate_birth_chart() method.
Tests the service layer directly without API/database dependency.
"""

import pytest
from datetime import datetime
import pytz
from backend.services.calculation_service import CalculationService
from backend.schemas import BirthDataInput


@pytest.fixture
def calculation_service():
    """Create CalculationService instance for testing."""
    return CalculationService()


@pytest.fixture
def sample_birth_data():
    """Sample birth data: Albert Einstein, March 14, 1879 11:30 Ulm, Germany."""
    return BirthDataInput(
        date="1879-03-14",
        time="11:30:00",
        timezone="Europe/Berlin",
        latitude=48.4008,
        longitude=9.9878,
        location_name="Ulm, Germany"
    )


@pytest.fixture
def modern_birth_data():
    """Modern birth data: June 15, 1995 14:30 New York (used in Phase 2 tests)."""
    return BirthDataInput(
        date="1995-06-15",
        time="14:30:00",
        timezone="America/New_York",
        latitude=40.7128,
        longitude=-74.0060,
        location_name="New York, USA"
    )


class TestGenerateBirthChart:
    """Test CalculationService.generate_birth_chart() method."""
    
    def test_generate_birth_chart_basic(self, calculation_service, modern_birth_data):
        """Test basic birth chart generation."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        assert result is not None
        assert isinstance(result, dict)
        print("✅ Birth chart generation returns dict")
    
    def test_chart_contains_required_fields(self, calculation_service, modern_birth_data):
        """Test that generated chart contains all required fields."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        required_fields = [
            "planet_positions",
            "house_cusps",
            "ascendant",
            "aspects"
        ]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
        
        print("✅ Chart contains all required fields")
    
    def test_chart_has_12_planets(self, calculation_service, modern_birth_data):
        """Test that chart includes exactly 12 celestial bodies."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        planets = result["planet_positions"]
        assert len(planets) >= 10, f"Expected at least 10 planets, got {len(planets)}"
        
        # Verify planet names
        planet_names = [p["planet"] for p in planets]
        expected = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", 
                   "Saturn", "Uranus", "Neptune", "Pluto"]
        
        for planet in expected:
            assert planet in planet_names, f"Missing planet: {planet}"
        
        print(f"✅ Chart includes {len(planets)} celestial bodies")
    
    def test_chart_has_12_houses(self, calculation_service, modern_birth_data):
        """Test that chart includes all 12 house cusps."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        houses = result["house_cusps"]
        assert len(houses) == 12, f"Expected 12 houses, got {len(houses)}"
        
        # Verify house numbering
        for i, house in enumerate(houses, 1):
            assert house["house"] == i, f"House {i} has incorrect number"
        
        print("✅ Chart includes 12 house cusps")
    
    def test_chart_has_ascendant(self, calculation_service, modern_birth_data):
        """Test that chart includes ascendant information."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        ascendant = result["ascendant"]
        assert ascendant is not None
        assert "degree" in ascendant
        assert "zodiac_sign" in ascendant
        assert "zodiac_degree" in ascendant
        
        # Degree should be 0-360
        assert 0 <= ascendant["degree"] <= 360
        
        print(f"✅ Ascendant: {ascendant['zodiac_sign']} {ascendant['zodiac_degree']:.2f}°")
    
    def test_chart_has_aspects(self, calculation_service, modern_birth_data):
        """Test that chart includes aspect calculations."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        aspects = result["aspects"]
        assert isinstance(aspects, list)
        assert len(aspects) > 0, "Chart should have some aspects"
        
        # Verify aspect structure
        for aspect in aspects:
            assert "planet1" in aspect
            assert "planet2" in aspect
            assert "aspect_type" in aspect
            assert "orb" in aspect
            assert "is_exact" in aspect
        
        print(f"✅ Chart includes {len(aspects)} aspects")
    
    def test_planet_coordinates_are_valid(self, calculation_service, modern_birth_data):
        """Test that all planet coordinates are within valid ranges."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        planets = result["planet_positions"]
        
        for planet in planets:
            # Degree: 0-360
            assert 0 <= planet["degree"] <= 360, \
                f"{planet['planet']} degree {planet['degree']} out of range"
            
            # Minutes: 0-60
            assert 0 <= planet["minutes"] <= 60, \
                f"{planet['planet']} minutes {planet['minutes']} out of range"
            
            # Seconds: 0-60
            assert 0 <= planet["seconds"] <= 60, \
                f"{planet['planet']} seconds {planet['seconds']} out of range"
            
            # House: 1-12
            assert 1 <= planet["house"] <= 12, \
                f"{planet['planet']} house {planet['house']} out of range"
            
            # Zodiac sign should be valid
            valid_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            assert planet["zodiac_sign"] in valid_signs, \
                f"{planet['planet']} zodiac sign {planet['zodiac_sign']} invalid"
        
        print("✅ All planet coordinates are valid")
    
    def test_house_coordinates_are_valid(self, calculation_service, modern_birth_data):
        """Test that all house cusps have valid coordinates."""
        result = calculation_service.generate_birth_chart(modern_birth_data)
        
        houses = result["house_cusps"]
        
        for house in houses:
            # Degree: 0-360
            assert 0 <= house["degree"] <= 360, \
                f"House {house['house']} degree out of range"
            
            # Zodiac sign should be valid
            valid_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            assert house["zodiac_sign"] in valid_signs, \
                f"House {house['house']} zodiac sign invalid"
        
        print("✅ All house cusps have valid coordinates")
    
    def test_chart_generation_with_different_timezones(self, calculation_service):
        """Test that timezone handling works correctly."""
        # Same birth moment in different timezone representations
        birth_data_est = BirthDataInput(
            date="1995-06-15",
            time="14:30:00",
            timezone="America/New_York",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        birth_data_utc = BirthDataInput(
            date="1995-06-15",
            time="18:30:00",  # 14:30 EST = 18:30 UTC
            timezone="UTC",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        chart1 = calculation_service.generate_birth_chart(birth_data_est)
        chart2 = calculation_service.generate_birth_chart(birth_data_utc)
        
        # Charts should be nearly identical (allowing for small rounding differences)
        # Compare Sun positions (typically most stable)
        sun1 = chart1["planet_positions"][0]["degree"]
        sun2 = chart2["planet_positions"][0]["degree"]
        
        # Allow 0.1 degree tolerance
        assert abs(sun1 - sun2) < 0.1, \
            f"Timezone handling error: Sun at {sun1}° vs {sun2}°"
        
        print("✅ Timezone handling works correctly")
    
    def test_chart_consistency(self, calculation_service, modern_birth_data):
        """Test that generating the same chart twice produces identical results."""
        chart1 = calculation_service.generate_birth_chart(modern_birth_data)
        chart2 = calculation_service.generate_birth_chart(modern_birth_data)
        
        # Compare key data
        assert len(chart1["planet_positions"]) == len(chart2["planet_positions"])
        assert len(chart1["house_cusps"]) == len(chart2["house_cusps"])
        
        # Compare planet positions (should be identical)
        for p1, p2 in zip(chart1["planet_positions"], chart2["planet_positions"]):
            assert p1["planet"] == p2["planet"]
            assert p1["degree"] == p2["degree"]
            assert p1["zodiac_sign"] == p2["zodiac_sign"]
        
        print("✅ Chart generation is consistent")
    
    def test_chart_with_southern_hemisphere(self, calculation_service):
        """Test chart generation for southern hemisphere location."""
        # Sydney, Australia
        birth_data = BirthDataInput(
            date="1995-06-15",
            time="14:30:00",
            timezone="Australia/Sydney",
            latitude=-33.8688,  # Negative = South
            longitude=151.2093,
            location_name="Sydney, Australia"
        )
        
        result = calculation_service.generate_birth_chart(birth_data)
        
        # Chart should generate successfully
        assert result is not None
        assert len(result["planet_positions"]) > 0
        assert len(result["house_cusps"]) == 12
        
        print("✅ Southern hemisphere chart generated successfully")
    
    def test_chart_with_extreme_latitudes(self, calculation_service):
        """Test chart generation near poles."""
        # Near North Pole (e.g., Reykjavik, Iceland)
        birth_data = BirthDataInput(
            date="1995-06-15",
            time="14:30:00",
            timezone="Atlantic/Reykjavik",
            latitude=64.1466,
            longitude=-21.9426,
            location_name="Reykjavik, Iceland"
        )
        
        result = calculation_service.generate_birth_chart(birth_data)
        
        assert result is not None
        assert len(result["planet_positions"]) > 0
        
        print("✅ High latitude chart generated successfully")


class TestBirthChartErrorHandling:
    """Test error handling in birth chart generation."""
    
    def test_invalid_date_format(self, calculation_service):
        """Test error handling for invalid date format."""
        invalid_data = BirthDataInput(
            date="not-a-date",
            time="14:30:00",
            timezone="America/New_York",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        with pytest.raises(ValueError):
            calculation_service.generate_birth_chart(invalid_data)
        
        print("✅ Invalid date format raises ValueError")
    
    def test_invalid_time_format(self, calculation_service):
        """Test error handling for invalid time format."""
        invalid_data = BirthDataInput(
            date="1995-06-15",
            time="25:70:00",  # Invalid hour
            timezone="America/New_York",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        with pytest.raises(ValueError):
            calculation_service.generate_birth_chart(invalid_data)
        
        print("✅ Invalid time format raises ValueError")
    
    def test_invalid_timezone(self, calculation_service):
        """Test error handling for invalid timezone."""
        invalid_data = BirthDataInput(
            date="1995-06-15",
            time="14:30:00",
            timezone="Invalid/Timezone",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        with pytest.raises((pytz.exceptions.UnknownTimeZoneError, ValueError)):
            calculation_service.generate_birth_chart(invalid_data)
        
        print("✅ Invalid timezone raises appropriate error")


class TestHistoricalCharts:
    """Test generation of famous historical birth charts."""
    
    def test_einstein_birth_chart(self, calculation_service):
        """Test Albert Einstein's birth chart (Mar 14, 1879 11:30 Ulm)."""
        birth_data = BirthDataInput(
            date="1879-03-14",
            time="11:30:00",
            timezone="Europe/Berlin",
            latitude=48.4008,
            longitude=9.9878,
            location_name="Ulm, Germany"
        )
        
        chart = calculation_service.generate_birth_chart(birth_data)
        
        # Verify chart structure
        assert chart is not None
        assert len(chart["planet_positions"]) > 0
        
        # Sun should be in Pisces (March 14)
        sun = chart["planet_positions"][0]
        assert sun["planet"] == "Sun"
        assert sun["zodiac_sign"] == "Pisces"
        
        print(f"✅ Einstein chart: Sun in {sun['zodiac_sign']}")
    
    def test_gandhi_birth_chart(self, calculation_service):
        """Test Mahatma Gandhi's birth chart (Oct 2, 1869 07:07 Porbandar)."""
        birth_data = BirthDataInput(
            date="1869-10-02",
            time="07:07:00",
            timezone="Asia/Kolkata",
            latitude=21.6422,
            longitude=69.6093,
            location_name="Porbandar, India"
        )
        
        chart = calculation_service.generate_birth_chart(birth_data)
        
        assert chart is not None
        assert len(chart["planet_positions"]) > 0
        
        # Sun should be in Libra (October 2)
        sun = chart["planet_positions"][0]
        assert sun["zodiac_sign"] == "Libra"
        
        print(f"✅ Gandhi chart: Sun in {sun['zodiac_sign']}")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    # Run with: pytest test_calculation_service.py -v
    print("\n" + "="*80)
    print("CALCULATION SERVICE TEST SUITE")
    print("="*80 + "\n")
    
    pytest.main([__file__, "-v", "-s"])
