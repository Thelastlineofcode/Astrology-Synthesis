"""
BMAD Behavior Prediction Service
Predicts behavioral patterns and trends based on astrological transits and progressions.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from ..models.behavior import (
    BehaviorCategory, PredictionConfidence, LifePhase, BehaviorIndicator,
    BehaviorPrediction, BehaviorEvolution, BehaviorTrigger, BehaviorProfile
)


class BehaviorPredictor:
    """Service for predicting behavioral patterns and trends."""
    
    def __init__(self):
        self.behavior_rules = self._initialize_behavior_rules()
        self.trigger_rules = self._initialize_trigger_rules()
        self.evolution_patterns = self._initialize_evolution_patterns()
    
    def create_behavior_profile(self, chart_data: Dict, birth_data: Dict,
                               person_name: str = None) -> BehaviorProfile:
        """
        Create a comprehensive behavioral profile from chart data.
        
        Args:
            chart_data: Calculated astrological chart data
            birth_data: Birth information
            person_name: Optional person name
        
        Returns:
            BehaviorProfile: Complete behavioral analysis
        """
        profile_id = str(uuid.uuid4())
        name = person_name or f"Person_{profile_id[:8]}"
        
        # Analyze current behavioral indicators
        current_indicators = self._analyze_current_indicators(chart_data)
        
        # Identify behavioral triggers
        behavior_triggers = self._identify_triggers(chart_data)
        
        # Generate future predictions (next 12 months)
        future_predictions = self._generate_predictions(chart_data, birth_data)
        
        # Determine dominant behavioral categories
        dominant_categories = self._find_dominant_categories(current_indicators)
        
        # Generate behavioral summary
        behavioral_summary = self._generate_behavior_summary(current_indicators, dominant_categories)
        
        return BehaviorProfile(
            profile_id=profile_id,
            person_name=name,
            birth_data=birth_data,
            current_indicators=current_indicators,
            behavior_triggers=behavior_triggers,
            future_predictions=future_predictions,
            evolution_history=[],  # Would be populated over time
            dominant_categories=dominant_categories,
            behavioral_summary=behavioral_summary,
            last_updated=datetime.now().isoformat()
        )
    
    def predict_behavior_for_date(self, profile: BehaviorProfile, target_date: str,
                                 categories: List[BehaviorCategory] = None) -> List[BehaviorPrediction]:
        """
        Predict behavioral patterns for a specific date.
        
        Args:
            profile: Existing behavioral profile
            target_date: Target date for prediction (ISO format)
            categories: Specific categories to predict (optional)
        
        Returns:
            List[BehaviorPrediction]: Predictions for the target date
        """
        predictions = []
        target_categories = categories or list(BehaviorCategory)
        
        for category in target_categories:
            prediction = self._create_date_prediction(profile, target_date, category)
            if prediction:
                predictions.append(prediction)
        
        return predictions
    
    def analyze_behavior_evolution(self, profile: BehaviorProfile, 
                                 start_date: str, end_date: str) -> List[BehaviorEvolution]:
        """
        Analyze how behaviors might evolve over a time period.
        
        Args:
            profile: Behavioral profile to analyze
            start_date: Start date for evolution analysis
            end_date: End date for evolution analysis
        
        Returns:
            List[BehaviorEvolution]: Evolution patterns for each category
        """
        evolutions = []
        
        for category in profile.dominant_categories:
            evolution = self._analyze_category_evolution(
                profile, category, start_date, end_date
            )
            if evolution:
                evolutions.append(evolution)
        
        return evolutions
    
    def identify_active_triggers(self, profile: BehaviorProfile, 
                               current_date: str) -> List[BehaviorTrigger]:
        """
        Identify behavioral triggers that are currently active.
        
        Args:
            profile: Behavioral profile
            current_date: Current date to check triggers against
        
        Returns:
            List[BehaviorTrigger]: Currently active triggers
        """
        active_triggers = []
        
        for trigger in profile.behavior_triggers:
            if self._is_trigger_active(trigger, current_date, profile.birth_data):
                active_triggers.append(trigger)
        
        return active_triggers
    
    def _analyze_current_indicators(self, chart_data: Dict) -> List[BehaviorIndicator]:
        """Analyze current behavioral indicators from chart data."""
        indicators = []
        
        # Analyze planetary positions for behavioral indicators
        planets = chart_data.get('planets', {})
        
        for planet_name, planet_data in planets.items():
            planet_indicators = self._get_planet_indicators(planet_name, planet_data)
            indicators.extend(planet_indicators)
        
        # Analyze house emphasis
        house_indicators = self._analyze_house_emphasis(chart_data.get('houses', {}))
        indicators.extend(house_indicators)
        
        # Analyze aspect patterns
        aspect_indicators = self._analyze_aspect_patterns(chart_data.get('aspects', []))
        indicators.extend(aspect_indicators)
        
        return indicators
    
    def _get_planet_indicators(self, planet_name: str, planet_data: Dict) -> List[BehaviorIndicator]:
        """Get behavioral indicators from a planet's position."""
        indicators = []
        
        # Handle None planet data (e.g., missing ephemeris files)
        if planet_data is None:
            return indicators
        
        sign = planet_data.get('sign')
        house = planet_data.get('house')
        
        if not sign or not house:
            return indicators
        
        # Look up behavioral indicators for this planet/sign/house combination
        planet_key = f"{planet_name}_{sign}_{house}"
        planet_rules = self.behavior_rules.get('planetary_positions', {}).get(planet_key, [])
        
        for rule in planet_rules:
            indicator = BehaviorIndicator(
                indicator_id=str(uuid.uuid4()),
                name=rule['name'],
                category=BehaviorCategory(rule['category']),
                description=rule['description'],
                intensity=rule.get('intensity', 0.5),
                astrological_basis={
                    'planet': planet_name,
                    'sign': sign,
                    'house': house
                },
                life_phases=[LifePhase(phase) for phase in rule.get('life_phases', [])]
            )
            indicators.append(indicator)
        
        return indicators
    
    def _analyze_house_emphasis(self, houses_data: Dict) -> List[BehaviorIndicator]:
        """Analyze house emphasis for behavioral indicators."""
        indicators = []
        
        # Count planets in each house to find emphasis
        house_counts = {}
        for house_num in range(1, 13):
            house_counts[house_num] = 0
        
        # This would require counting planets in houses from the chart data
        # For now, we'll use a simplified approach
        
        return indicators
    
    def _analyze_aspect_patterns(self, aspects_data: List[Dict]) -> List[BehaviorIndicator]:
        """Analyze aspect patterns for behavioral indicators."""
        indicators = []
        
        # Look for significant aspect patterns
        for aspect in aspects_data:
            aspect_type = aspect.get('aspect')
            planets = [aspect.get('planet1'), aspect.get('planet2')]
            orb = aspect.get('orb', 0)
            
            # Find behavioral indicators for this aspect
            aspect_key = f"{planets[0]}_{aspect_type}_{planets[1]}"
            aspect_rules = self.behavior_rules.get('aspect_patterns', {}).get(aspect_key, [])
            
            for rule in aspect_rules:
                if orb <= rule.get('max_orb', 8):
                    indicator = BehaviorIndicator(
                        indicator_id=str(uuid.uuid4()),
                        name=rule['name'],
                        category=BehaviorCategory(rule['category']),
                        description=rule['description'],
                        intensity=rule.get('intensity', 0.5) * (1 - orb / rule.get('max_orb', 8)),
                        astrological_basis={
                            'aspect': aspect_type,
                            'planets': planets,
                            'orb': orb
                        }
                    )
                    indicators.append(indicator)
        
        return indicators
    
    def _identify_triggers(self, chart_data: Dict) -> List[BehaviorTrigger]:
        """Identify potential behavioral triggers from chart data."""
        triggers = []
        
        # Create triggers based on planetary positions and aspects
        planets = chart_data.get('planets', {})
        
        for planet_name, planet_data in planets.items():
            planet_triggers = self._get_planet_triggers(planet_name, planet_data)
            triggers.extend(planet_triggers)
        
        return triggers
    
    def _get_planet_triggers(self, planet_name: str, planet_data: Dict) -> List[BehaviorTrigger]:
        """Get behavioral triggers associated with a planet."""
        triggers = []
        
        # Handle None planet data
        if planet_data is None:
            return triggers
        
        sign = planet_data.get('sign')
        degree = planet_data.get('degree', 0)
        
        if not sign:
            return triggers
        
        # Look up triggers for this planet/sign combination
        trigger_key = f"{planet_name}_{sign}"
        trigger_rules = self.trigger_rules.get(trigger_key, [])
        
        for rule in trigger_rules:
            trigger = BehaviorTrigger(
                trigger_id=str(uuid.uuid4()),
                name=rule['name'],
                astrological_condition={
                    'planet': planet_name,
                    'sign': sign,
                    'degree_range': rule.get('degree_range', [0, 30])
                },
                triggered_behaviors=rule['behaviors'],
                activation_probability=rule.get('probability', 0.5),
                duration_hours=rule.get('duration_hours', 24),
                intensity_pattern=rule.get('pattern', 'gradual'),
                historical_activations=[]
            )
            triggers.append(trigger)
        
        return triggers
    
    def _generate_predictions(self, chart_data: Dict, birth_data: Dict) -> List[BehaviorPrediction]:
        """Generate behavioral predictions for the future."""
        predictions = []
        
        # Generate predictions for the next 12 months
        current_date = datetime.now()
        
        for month_offset in range(1, 13):
            target_date = current_date + timedelta(days=30 * month_offset)
            
            for category in BehaviorCategory:
                prediction = self._create_monthly_prediction(
                    chart_data, birth_data, target_date.isoformat()[:10], category
                )
                if prediction:
                    predictions.append(prediction)
        
        return predictions
    
    def _create_monthly_prediction(self, chart_data: Dict, birth_data: Dict,
                                 target_date: str, category: BehaviorCategory) -> Optional[BehaviorPrediction]:
        """Create a prediction for a specific month and category."""
        # This would involve complex transit calculations
        # For now, we'll create a simplified prediction
        
        prediction = BehaviorPrediction(
            prediction_id=str(uuid.uuid4()),
            target_date=target_date,
            category=category,
            predicted_behaviors=[f"Enhanced {category.value} behaviors"],
            confidence=PredictionConfidence.MODERATE,
            astrological_transits=[],  # Would be calculated from ephemeris
            duration_days=30,
            intensity_curve=[(target_date, 0.5)],
            recommendations=[f"Focus on positive {category.value} expressions"]
        )
        
        return prediction
    
    def _create_date_prediction(self, profile: BehaviorProfile, target_date: str,
                              category: BehaviorCategory) -> Optional[BehaviorPrediction]:
        """Create a prediction for a specific date and category."""
        # Find relevant indicators for this category
        relevant_indicators = profile.get_indicators_by_category(category)
        
        if not relevant_indicators:
            return None
        
        # Create prediction based on indicators and transits
        prediction = BehaviorPrediction(
            prediction_id=str(uuid.uuid4()),
            target_date=target_date,
            category=category,
            predicted_behaviors=[f"Activation of {category.value} patterns"],
            confidence=PredictionConfidence.MODERATE,
            astrological_transits=[],  # Would calculate actual transits
            duration_days=1,
            intensity_curve=[(target_date, 0.6)],
            recommendations=[f"Be mindful of {category.value} impulses"]
        )
        
        return prediction
    
    def _analyze_category_evolution(self, profile: BehaviorProfile, category: BehaviorCategory,
                                  start_date: str, end_date: str) -> Optional[BehaviorEvolution]:
        """Analyze evolution for a specific behavioral category."""
        baseline_indicators = profile.get_indicators_by_category(category)
        
        if not baseline_indicators:
            return None
        
        # Create evolved indicators (simplified for demo)
        evolved_indicators = baseline_indicators.copy()
        
        evolution = BehaviorEvolution(
            evolution_id=str(uuid.uuid4()),
            person_id=profile.profile_id,
            start_date=start_date,
            end_date=end_date,
            category=category,
            baseline_indicators=baseline_indicators,
            evolved_indicators=evolved_indicators,
            key_transits=[],  # Would calculate major transits
            milestones=[],  # Would identify significant changes
            evolution_summary=f"Evolution of {category.value} behaviors over the period"
        )
        
        return evolution
    
    def _is_trigger_active(self, trigger: BehaviorTrigger, current_date: str,
                          birth_data: Dict) -> bool:
        """Check if a behavioral trigger is currently active."""
        # This would involve calculating current transits and comparing
        # to the trigger's astrological conditions
        # For now, we'll use a simplified check
        
        return trigger.activation_probability > 0.5
    
    def _find_dominant_categories(self, indicators: List[BehaviorIndicator]) -> List[BehaviorCategory]:
        """Find the most prominent behavioral categories."""
        category_scores = {}
        
        for indicator in indicators:
            category = indicator.category
            score = indicator.intensity
            category_scores[category] = category_scores.get(category, 0) + score
        
        # Get top 3 categories
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        return [category for category, score in sorted_categories[:3]]
    
    def _generate_behavior_summary(self, indicators: List[BehaviorIndicator],
                                 dominant_categories: List[BehaviorCategory]) -> str:
        """Generate a narrative summary of behavioral patterns."""
        if not indicators:
            return "No significant behavioral patterns identified."
        
        summary_parts = []
        
        if dominant_categories:
            category_names = [cat.value.replace('_', ' ') for cat in dominant_categories]
            summary_parts.append(f"Primary behavioral focus areas: {', '.join(category_names)}.")
        
        high_intensity = [ind for ind in indicators if ind.intensity > 0.7]
        if high_intensity:
            summary_parts.append(f"Strong patterns identified in {len(high_intensity)} areas.")
        
        summary_parts.append(f"Analysis based on {len(indicators)} behavioral indicators.")
        
        return " ".join(summary_parts)
    
    def _initialize_behavior_rules(self) -> Dict:
        """Initialize behavioral analysis rules."""
        return {
            'planetary_positions': {
                'Mars_Aries_1': [{
                    'name': 'Assertive Leadership',
                    'category': 'professional',
                    'description': 'Strong drive for leadership in professional settings',
                    'intensity': 0.8,
                    'life_phases': ['young_adult', 'adult']
                }],
                'Venus_Taurus_2': [{
                    'name': 'Financial Stability Focus',
                    'category': 'financial',
                    'description': 'Strong emphasis on financial security and material stability',
                    'intensity': 0.7,
                    'life_phases': ['adult', 'middle_age']
                }],
                # Add more planetary position rules
            },
            'aspect_patterns': {
                'Sun_conjunction_Mars': [{
                    'name': 'High Energy Drive',
                    'category': 'professional',
                    'description': 'Intense drive and energy for achievement',
                    'intensity': 0.8,
                    'max_orb': 8
                }],
                # Add more aspect pattern rules
            }
        }
    
    def _initialize_trigger_rules(self) -> Dict:
        """Initialize behavioral trigger rules."""
        return {
            'Mars_Aries': [{
                'name': 'Competitive Trigger',
                'behaviors': ['increased assertiveness', 'competitive behavior', 'leadership actions'],
                'probability': 0.7,
                'duration_hours': 48,
                'pattern': 'immediate'
            }],
            'Moon_Cancer': [{
                'name': 'Emotional Sensitivity Trigger',
                'behaviors': ['emotional reactivity', 'protective behavior', 'nurturing actions'],
                'probability': 0.6,
                'duration_hours': 12,
                'pattern': 'wave'
            }],
            # Add more trigger rules
        }
    
    def _initialize_evolution_patterns(self) -> Dict:
        """Initialize behavioral evolution patterns."""
        return {
            # Evolution pattern rules would go here
        }