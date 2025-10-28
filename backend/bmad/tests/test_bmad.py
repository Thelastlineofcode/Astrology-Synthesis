"""
BMAD Test Suite
Comprehensive unit tests for Behavioral Model and Data analysis.
"""

import unittest
import json
from datetime import datetime
from unittest.mock import Mock, patch

# Import BMAD components
from backend.bmad.models.personality import (
    PersonalityDimension, IntensityLevel, Trait, BehavioralPattern, 
    PersonalityProfile, CompatibilityAnalysis
)
from backend.bmad.models.behavior import (
    BehaviorCategory, PredictionConfidence, LifePhase, BehaviorIndicator,
    BehaviorPrediction, BehaviorEvolution, BehaviorTrigger, BehaviorProfile
)
from backend.bmad.services.personality_analyzer import PersonalityAnalyzer
from backend.bmad.services.behavior_predictor import BehaviorPredictor
from backend.bmad.config import BMADConfig, validate_full_config


class TestPersonalityModels(unittest.TestCase):
    """Test personality data models."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_trait = Trait(
            name="Test Trait",
            dimension=PersonalityDimension.EXTRAVERSION,
            intensity=IntensityLevel.HIGH,
            description="A test personality trait",
            astrological_source={"planet": "Sun", "sign": "Leo"},
            keywords=["confident", "outgoing"]
        )
    
    def test_trait_creation(self):
        """Test Trait model creation and methods."""
        self.assertEqual(self.sample_trait.name, "Test Trait")
        self.assertEqual(self.sample_trait.dimension, PersonalityDimension.EXTRAVERSION)
        self.assertEqual(self.sample_trait.intensity, IntensityLevel.HIGH)
        
        # Test to_dict method
        trait_dict = self.sample_trait.to_dict()
        self.assertIsInstance(trait_dict, dict)
        self.assertEqual(trait_dict['name'], "Test Trait")
        self.assertEqual(trait_dict['dimension'], "extraversion")
        self.assertEqual(trait_dict['intensity'], 4)
    
    def test_behavioral_pattern_creation(self):
        """Test BehavioralPattern model creation."""
        pattern = BehavioralPattern(
            pattern_id="test_pattern",
            name="Test Pattern",
            description="A test behavioral pattern",
            probability=0.7,
            triggers=[{"type": "aspect", "planets": ["Sun", "Mars"]}],
            manifestations=["increased energy", "assertive behavior"],
            related_traits=["leadership", "confidence"]
        )
        
        self.assertEqual(pattern.pattern_id, "test_pattern")
        self.assertEqual(pattern.probability, 0.7)
        self.assertIn("increased energy", pattern.manifestations)
        
        # Test to_dict method
        pattern_dict = pattern.to_dict()
        self.assertIsInstance(pattern_dict, dict)
        self.assertEqual(pattern_dict['probability'], 0.7)
    
    def test_personality_profile_creation(self):
        """Test PersonalityProfile model creation and methods."""
        profile = PersonalityProfile(
            profile_id="test_profile",
            name="Test Person",
            birth_data={"year": 1990, "month": 8, "day": 15},
            traits=[self.sample_trait],
            behavioral_patterns=[],
            dominant_dimensions=[PersonalityDimension.EXTRAVERSION],
            summary="Test personality profile",
            created_timestamp=datetime.now().isoformat()
        )
        
        self.assertEqual(profile.profile_id, "test_profile")
        self.assertEqual(len(profile.traits), 1)
        
        # Test trait retrieval by dimension
        extraversion_traits = profile.get_trait_by_dimension(PersonalityDimension.EXTRAVERSION)
        self.assertEqual(len(extraversion_traits), 1)
        self.assertEqual(extraversion_traits[0].name, "Test Trait")
        
        # Test dominant trait intensity calculation
        dominant_intensities = profile.get_dominant_trait_intensity()
        self.assertIn(PersonalityDimension.EXTRAVERSION, dominant_intensities)
        self.assertEqual(dominant_intensities[PersonalityDimension.EXTRAVERSION], IntensityLevel.HIGH)


class TestBehaviorModels(unittest.TestCase):
    """Test behavior data models."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_indicator = BehaviorIndicator(
            indicator_id="test_indicator",
            name="Test Behavior",
            category=BehaviorCategory.SOCIAL,
            description="A test behavioral indicator",
            intensity=0.8,
            astrological_basis={"planet": "Venus", "house": 7},
            life_phases=[LifePhase.ADULT]
        )
    
    def test_behavior_indicator_creation(self):
        """Test BehaviorIndicator model creation."""
        self.assertEqual(self.sample_indicator.indicator_id, "test_indicator")
        self.assertEqual(self.sample_indicator.category, BehaviorCategory.SOCIAL)
        self.assertEqual(self.sample_indicator.intensity, 0.8)
        
        # Test to_dict method
        indicator_dict = self.sample_indicator.to_dict()
        self.assertIsInstance(indicator_dict, dict)
        self.assertEqual(indicator_dict['category'], "social")
        self.assertEqual(indicator_dict['intensity'], 0.8)
    
    def test_behavior_prediction_creation(self):
        """Test BehaviorPrediction model creation."""
        prediction = BehaviorPrediction(
            prediction_id="test_prediction",
            target_date="2024-06-15",
            category=BehaviorCategory.PROFESSIONAL,
            predicted_behaviors=["increased leadership", "assertive communication"],
            confidence=PredictionConfidence.HIGH,
            astrological_transits=[{"transit": "Mars conjunct Midheaven"}],
            duration_days=7,
            intensity_curve=[("2024-06-15", 0.7)],
            recommendations=["Channel energy into leadership roles"]
        )
        
        self.assertEqual(prediction.target_date, "2024-06-15")
        self.assertEqual(prediction.confidence, PredictionConfidence.HIGH)
        self.assertEqual(prediction.duration_days, 7)
        
        # Test to_dict method
        prediction_dict = prediction.to_dict()
        self.assertIsInstance(prediction_dict, dict)
        self.assertEqual(prediction_dict['confidence'], 4)
    
    def test_behavior_profile_creation(self):
        """Test BehaviorProfile model creation and methods."""
        profile = BehaviorProfile(
            profile_id="test_behavior_profile",
            person_name="Test Person",
            birth_data={"year": 1990, "month": 8, "day": 15},
            current_indicators=[self.sample_indicator],
            behavior_triggers=[],
            future_predictions=[],
            evolution_history=[],
            dominant_categories=[BehaviorCategory.SOCIAL],
            behavioral_summary="Test behavioral profile",
            last_updated=datetime.now().isoformat()
        )
        
        self.assertEqual(profile.profile_id, "test_behavior_profile")
        self.assertEqual(len(profile.current_indicators), 1)
        
        # Test indicator retrieval by category
        social_indicators = profile.get_indicators_by_category(BehaviorCategory.SOCIAL)
        self.assertEqual(len(social_indicators), 1)
        self.assertEqual(social_indicators[0].name, "Test Behavior")


class TestPersonalityAnalyzer(unittest.TestCase):
    """Test PersonalityAnalyzer service."""
    
    def setUp(self):
        """Set up test data."""
        self.analyzer = PersonalityAnalyzer()
        self.sample_chart_data = {
            'planets': {
                'Sun': {'sign': 'Leo', 'degree': 15.5, 'house': 5},
                'Moon': {'sign': 'Cancer', 'degree': 22.3, 'house': 4},
                'Mercury': {'sign': 'Virgo', 'degree': 8.1, 'house': 6}
            },
            'houses': {
                'house_1': {'sign': 'Aries', 'degree': 12.0}
            },
            'aspects': [
                {
                    'planet1': 'Sun',
                    'planet2': 'Mars',
                    'aspect': 'conjunction',
                    'orb': 3.2
                }
            ]
        }
        self.sample_birth_data = {
            'year': 1990,
            'month': 8,
            'day': 15,
            'hour': 14,
            'minute': 30,
            'latitude': 40.7128,
            'longitude': -74.0060
        }
    
    def test_analyze_personality(self):
        """Test personality analysis from chart data."""
        profile = self.analyzer.analyze_personality(
            self.sample_chart_data, 
            self.sample_birth_data,
            "Test Analysis"
        )
        
        self.assertIsInstance(profile, PersonalityProfile)
        self.assertEqual(profile.name, "Test Analysis")
        self.assertIsInstance(profile.traits, list)
        self.assertIsInstance(profile.behavioral_patterns, list)
        self.assertIsInstance(profile.dominant_dimensions, list)
        self.assertIsInstance(profile.summary, str)
    
    def test_extract_sun_traits(self):
        """Test extraction of Sun sign traits."""
        sun_data = {'sign': 'Aries', 'degree': 10.0}
        traits = self.analyzer._analyze_sun_traits(sun_data)
        
        # Should return some traits for Aries if rules are defined
        self.assertIsInstance(traits, list)
        for trait in traits:
            self.assertIsInstance(trait, Trait)
            self.assertEqual(trait.astrological_source['sign'], 'Aries')
    
    def test_intensity_calculation(self):
        """Test trait intensity calculation."""
        # Test early degree (should get intensity bonus)
        intensity1 = self.analyzer._calculate_intensity(2.0, 3)
        self.assertIsInstance(intensity1, IntensityLevel)
        
        # Test mid-degree (normal intensity)
        intensity2 = self.analyzer._calculate_intensity(15.0, 3)
        self.assertIsInstance(intensity2, IntensityLevel)
        
        # Test late degree (should get intensity bonus)
        intensity3 = self.analyzer._calculate_intensity(28.0, 3)
        self.assertIsInstance(intensity3, IntensityLevel)
    
    def test_aspect_intensity_calculation(self):
        """Test aspect-based intensity calculation."""
        # Test exact aspect (should be very high intensity)
        intensity1 = self.analyzer._calculate_aspect_intensity(0.0, 8.0)
        self.assertEqual(intensity1, IntensityLevel.VERY_HIGH)
        
        # Test medium orb
        intensity2 = self.analyzer._calculate_aspect_intensity(4.0, 8.0)
        self.assertEqual(intensity2, IntensityLevel.MODERATE)
        
        # Test wide orb (should be low intensity)
        intensity3 = self.analyzer._calculate_aspect_intensity(7.5, 8.0)
        self.assertEqual(intensity3, IntensityLevel.LOW)


class TestBehaviorPredictor(unittest.TestCase):
    """Test BehaviorPredictor service."""
    
    def setUp(self):
        """Set up test data."""
        self.predictor = BehaviorPredictor()
        self.sample_chart_data = {
            'planets': {
                'Mars': {'sign': 'Aries', 'degree': 10.0, 'house': 1},
                'Venus': {'sign': 'Taurus', 'degree': 20.0, 'house': 2}
            },
            'houses': {
                'house_1': {'sign': 'Aries', 'degree': 5.0},
                'house_2': {'sign': 'Taurus', 'degree': 5.0}
            },
            'aspects': [
                {
                    'planet1': 'Mars',
                    'planet2': 'Venus',
                    'aspect': 'sextile',
                    'orb': 2.1
                }
            ]
        }
        self.sample_birth_data = {
            'year': 1990,
            'month': 8,
            'day': 15,
            'hour': 14,
            'minute': 30
        }
    
    def test_create_behavior_profile(self):
        """Test behavioral profile creation."""
        profile = self.predictor.create_behavior_profile(
            self.sample_chart_data,
            self.sample_birth_data,
            "Test Person"
        )
        
        self.assertIsInstance(profile, BehaviorProfile)
        self.assertEqual(profile.person_name, "Test Person")
        self.assertIsInstance(profile.current_indicators, list)
        self.assertIsInstance(profile.behavior_triggers, list)
        self.assertIsInstance(profile.future_predictions, list)
        self.assertIsInstance(profile.dominant_categories, list)
    
    def test_predict_behavior_for_date(self):
        """Test behavior prediction for specific date."""
        # Create a sample profile first
        profile = self.predictor.create_behavior_profile(
            self.sample_chart_data,
            self.sample_birth_data,
            "Test Person"
        )
        
        predictions = self.predictor.predict_behavior_for_date(
            profile,
            "2024-06-15",
            [BehaviorCategory.SOCIAL, BehaviorCategory.PROFESSIONAL]
        )
        
        self.assertIsInstance(predictions, list)
        for prediction in predictions:
            self.assertIsInstance(prediction, BehaviorPrediction)
            self.assertEqual(prediction.target_date, "2024-06-15")
            self.assertIn(prediction.category, [BehaviorCategory.SOCIAL, BehaviorCategory.PROFESSIONAL])
    
    def test_analyze_behavior_evolution(self):
        """Test behavioral evolution analysis."""
        # Create a sample profile first
        profile = self.predictor.create_behavior_profile(
            self.sample_chart_data,
            self.sample_birth_data,
            "Test Person"
        )
        
        evolutions = self.predictor.analyze_behavior_evolution(
            profile,
            "2024-01-01",
            "2024-12-31"
        )
        
        self.assertIsInstance(evolutions, list)
        for evolution in evolutions:
            self.assertIsInstance(evolution, BehaviorEvolution)
            self.assertEqual(evolution.start_date, "2024-01-01")
            self.assertEqual(evolution.end_date, "2024-12-31")


class TestBMADConfig(unittest.TestCase):
    """Test BMAD configuration system."""
    
    def test_config_creation(self):
        """Test configuration creation with defaults."""
        config = BMADConfig()
        
        # Test that all sections exist
        self.assertIsNotNone(config.personality)
        self.assertIsNotNone(config.behavior)
        self.assertIsNotNone(config.analysis)
        self.assertIsNotNone(config.api)
        
        # Test default values
        self.assertEqual(config.personality.default_intensity_threshold, 0.5)
        self.assertEqual(config.behavior.default_prediction_days, 30)
        self.assertEqual(config.analysis.orb_precision, 0.1)
        self.assertFalse(config.api.enable_debug_mode)
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = BMADConfig()
        
        # Test valid configuration
        validation_results = validate_full_config(config)
        self.assertEqual(len(validation_results), 0)  # No errors expected
        
        # Test invalid configuration
        config.personality.default_intensity_threshold = -1.0  # Invalid
        config.behavior.default_prediction_days = 0  # Invalid
        
        validation_results = validate_full_config(config)
        self.assertGreater(len(validation_results), 0)  # Should have errors
        self.assertIn('personality', validation_results)
        self.assertIn('behavior', validation_results)
    
    def test_config_to_dict(self):
        """Test configuration serialization to dictionary."""
        config = BMADConfig()
        config_dict = config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertIn('personality', config_dict)
        self.assertIn('behavior', config_dict)
        self.assertIn('analysis', config_dict)
        self.assertIn('api', config_dict)
        
        # Test that nested values are properly serialized
        self.assertEqual(
            config_dict['personality']['default_intensity_threshold'],
            config.personality.default_intensity_threshold
        )


class TestBMADIntegration(unittest.TestCase):
    """Integration tests for BMAD components."""
    
    def setUp(self):
        """Set up test data for integration tests."""
        self.sample_chart_data = {
            'planets': {
                'Sun': {'sign': 'Leo', 'degree': 15.5, 'house': 5},
                'Moon': {'sign': 'Cancer', 'degree': 22.3, 'house': 4},
                'Mercury': {'sign': 'Virgo', 'degree': 8.1, 'house': 6},
                'Venus': {'sign': 'Leo', 'degree': 20.0, 'house': 5},
                'Mars': {'sign': 'Gemini', 'degree': 12.0, 'house': 3}
            },
            'houses': {
                'house_1': {'sign': 'Aries', 'degree': 12.0},
                'house_2': {'sign': 'Taurus', 'degree': 12.0},
                'house_3': {'sign': 'Gemini', 'degree': 12.0},
                'house_4': {'sign': 'Cancer', 'degree': 12.0},
                'house_5': {'sign': 'Leo', 'degree': 12.0}
            },
            'aspects': [
                {
                    'planet1': 'Sun',
                    'planet2': 'Venus',
                    'aspect': 'conjunction',
                    'orb': 4.5
                },
                {
                    'planet1': 'Moon',
                    'planet2': 'Mars',
                    'aspect': 'trine',
                    'orb': 2.3
                }
            ]
        }
        self.sample_birth_data = {
            'year': 1990,
            'month': 8,
            'day': 15,
            'hour': 14,
            'minute': 30,
            'latitude': 40.7128,
            'longitude': -74.0060
        }
    
    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow from chart data to profiles."""
        # Initialize analyzers
        personality_analyzer = PersonalityAnalyzer()
        behavior_predictor = BehaviorPredictor()
        
        # Perform personality analysis
        personality_profile = personality_analyzer.analyze_personality(
            self.sample_chart_data,
            self.sample_birth_data,
            "Integration Test Person"
        )
        
        # Perform behavioral analysis
        behavior_profile = behavior_predictor.create_behavior_profile(
            self.sample_chart_data,
            self.sample_birth_data,
            "Integration Test Person"
        )
        
        # Verify both profiles were created successfully
        self.assertIsInstance(personality_profile, PersonalityProfile)
        self.assertIsInstance(behavior_profile, BehaviorProfile)
        
        # Verify they contain meaningful data
        self.assertGreater(len(personality_profile.traits), 0)
        self.assertGreater(len(behavior_profile.current_indicators), 0)
        
        # Test predictions
        predictions = behavior_predictor.predict_behavior_for_date(
            behavior_profile,
            "2024-06-15"
        )
        
        self.assertIsInstance(predictions, list)
        
        # Test serialization
        personality_dict = personality_profile.to_dict()
        behavior_dict = behavior_profile.to_dict()
        
        self.assertIsInstance(personality_dict, dict)
        self.assertIsInstance(behavior_dict, dict)
        
        # Verify key fields are present
        self.assertIn('profile_id', personality_dict)
        self.assertIn('traits', personality_dict)
        self.assertIn('profile_id', behavior_dict)
        self.assertIn('current_indicators', behavior_dict)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)