"""
BMAD Personality Analysis Service
Analyzes astrological chart data to generate personality profiles and traits.
Enhanced with Symbolon card archetypal analysis.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from ..models.personality import (
    PersonalityDimension, IntensityLevel, Trait, BehavioralPattern, 
    PersonalityProfile, CompatibilityAnalysis
)


class PersonalityAnalyzer:
    """Service for analyzing personality traits from astrological data."""
    
    def __init__(self):
        self.trait_rules = self._initialize_trait_rules()
        self.pattern_rules = self._initialize_pattern_rules()
        
        # Initialize Symbolon analyzer if available
        self.symbolon_analyzer = None
        try:
            from .symbolon_analyzer import SymbolonAnalyzer
            self.symbolon_analyzer = SymbolonAnalyzer()
        except ImportError:
            print("Symbolon analyzer not available - continuing with basic analysis")
    
    def analyze_personality(self, chart_data: Dict, birth_data: Dict, 
                          profile_name: str = None) -> PersonalityProfile:
        """
        Generate a comprehensive personality profile from chart data.
        Enhanced with Symbolon archetypal analysis.
        
        Args:
            chart_data: Calculated astrological chart data
            birth_data: Birth information (date, time, location)
            profile_name: Optional name for the profile
        
        Returns:
            PersonalityProfile: Complete personality analysis
        """
        profile_id = str(uuid.uuid4())
        name = profile_name or f"Profile_{profile_id[:8]}"
        
        # Extract traits from chart data
        traits = self._extract_traits(chart_data)
        
        # Add Symbolon archetypal insights if available
        if self.symbolon_analyzer:
            symbolon_traits = self._extract_symbolon_traits(chart_data, birth_data)
            traits.extend(symbolon_traits)
        
        # Identify behavioral patterns
        behavioral_patterns = self._identify_patterns(chart_data, traits)
        
        # Determine dominant personality dimensions
        dominant_dimensions = self._find_dominant_dimensions(traits)
        
        # Generate summary (enhanced with Symbolon if available)
        summary = self._generate_personality_summary(chart_data, traits, behavioral_patterns)
        
        return PersonalityProfile(
            profile_id=profile_id,
            name=name,
            birth_data=birth_data,
            traits=traits,
            behavioral_patterns=behavioral_patterns,
            dominant_dimensions=dominant_dimensions,
            summary=summary,
            created_timestamp=datetime.now().isoformat(),
            chart_data_reference=chart_data
        )
    
    def analyze_compatibility(self, profile1: PersonalityProfile, 
                            profile2: PersonalityProfile) -> CompatibilityAnalysis:
        """
        Analyze compatibility between two personality profiles.
        
        Args:
            profile1: First personality profile
            profile2: Second personality profile
        
        Returns:
            CompatibilityAnalysis: Detailed compatibility analysis
        """
        # Calculate overall compatibility
        overall_compatibility = self._calculate_overall_compatibility(profile1, profile2)
        
        # Analyze compatibility by dimension
        dimension_compatibility = self._analyze_dimension_compatibility(profile1, profile2)
        
        # Identify strengths and challenges
        strengths, challenges = self._identify_compatibility_factors(profile1, profile2)
        
        # Generate recommendations
        recommendations = self._generate_compatibility_recommendations(
            profile1, profile2, strengths, challenges
        )
        
        # Analyze synastry influences
        synastry_influences = self._analyze_synastry_influences(
            profile1.chart_data_reference, profile2.chart_data_reference
        )
        
        return CompatibilityAnalysis(
            profile1_id=profile1.profile_id,
            profile2_id=profile2.profile_id,
            overall_compatibility=overall_compatibility,
            dimension_compatibility=dimension_compatibility,
            strengths=strengths,
            challenges=challenges,
            recommendations=recommendations,
            synastry_influences=synastry_influences
        )
    
    def _extract_traits(self, chart_data: Dict) -> List[Trait]:
        """Extract personality traits from chart data."""
        traits = []
        
        # Analyze Sun sign traits
        sun_traits = self._analyze_sun_traits(chart_data.get('planets', {}).get('Sun', {}))
        traits.extend(sun_traits)
        
        # Analyze Moon traits (emotional nature)
        moon_traits = self._analyze_moon_traits(chart_data.get('planets', {}).get('Moon', {}))
        traits.extend(moon_traits)
        
        # Analyze Ascendant traits (outward personality)
        asc_traits = self._analyze_ascendant_traits(chart_data.get('houses', {}))
        traits.extend(asc_traits)
        
        # Analyze planetary aspects for trait modifications
        aspect_traits = self._analyze_aspect_traits(chart_data.get('aspects', []))
        traits.extend(aspect_traits)
        
        # Analyze house placements
        house_traits = self._analyze_house_placements(chart_data.get('planets', {}))
        traits.extend(house_traits)
        
        return traits
    
    def _analyze_sun_traits(self, sun_data: Dict) -> List[Trait]:
        """Analyze Sun sign for core personality traits."""
        traits = []
        
        # Handle None or empty sun data
        if not sun_data or sun_data is None or 'sign' not in sun_data:
            return traits
        
        sign = sun_data['sign']
        degree = sun_data.get('degree', 0)
        
        # Get base traits for the sign
        sign_traits = self.trait_rules.get('sun_signs', {}).get(sign, [])
        
        for trait_data in sign_traits:
            trait = Trait(
                name=trait_data['name'],
                dimension=PersonalityDimension(trait_data['dimension']),
                intensity=self._calculate_intensity(degree, trait_data.get('intensity_base', 3)),
                description=trait_data['description'],
                astrological_source={
                    'type': 'sun_sign',
                    'sign': sign,
                    'degree': degree
                },
                keywords=trait_data.get('keywords', [])
            )
            traits.append(trait)
        
        return traits
    
    def _analyze_moon_traits(self, moon_data: Dict) -> List[Trait]:
        """Analyze Moon sign for emotional and instinctive traits."""
        traits = []
        
        # Handle None or empty moon data
        if not moon_data or moon_data is None or 'sign' not in moon_data:
            return traits
        
        sign = moon_data['sign']
        degree = moon_data.get('degree', 0)
        
        moon_traits = self.trait_rules.get('moon_signs', {}).get(sign, [])
        
        for trait_data in moon_traits:
            trait = Trait(
                name=trait_data['name'],
                dimension=PersonalityDimension(trait_data['dimension']),
                intensity=self._calculate_intensity(degree, trait_data.get('intensity_base', 3)),
                description=trait_data['description'],
                astrological_source={
                    'type': 'moon_sign',
                    'sign': sign,
                    'degree': degree
                },
                keywords=trait_data.get('keywords', [])
            )
            traits.append(trait)
        
        return traits
    
    def _analyze_ascendant_traits(self, houses_data: Dict) -> List[Trait]:
        """Analyze Ascendant for outward personality traits."""
        traits = []
        
        if not houses_data or 'house_1' not in houses_data:
            return traits
        
        asc_sign = houses_data['house_1'].get('sign')
        if not asc_sign:
            return traits
        
        asc_traits = self.trait_rules.get('ascendant_signs', {}).get(asc_sign, [])
        
        for trait_data in asc_traits:
            trait = Trait(
                name=trait_data['name'],
                dimension=PersonalityDimension(trait_data['dimension']),
                intensity=IntensityLevel(trait_data.get('intensity', 3)),
                description=trait_data['description'],
                astrological_source={
                    'type': 'ascendant',
                    'sign': asc_sign
                },
                keywords=trait_data.get('keywords', [])
            )
            traits.append(trait)
        
        return traits
    
    def _analyze_aspect_traits(self, aspects_data: List[Dict]) -> List[Trait]:
        """Analyze planetary aspects for trait modifications."""
        traits = []
        
        for aspect in aspects_data:
            aspect_type = aspect.get('aspect')
            planets = [aspect.get('planet1'), aspect.get('planet2')]
            orb = aspect.get('orb', 0)
            
            # Look for aspect-based traits
            aspect_key = f"{planets[0]}_{aspect_type}_{planets[1]}"
            aspect_traits = self.trait_rules.get('aspects', {}).get(aspect_key, [])
            
            for trait_data in aspect_traits:
                intensity = self._calculate_aspect_intensity(orb, trait_data.get('max_orb', 8))
                
                trait = Trait(
                    name=trait_data['name'],
                    dimension=PersonalityDimension(trait_data['dimension']),
                    intensity=intensity,
                    description=trait_data['description'],
                    astrological_source={
                        'type': 'aspect',
                        'aspect': aspect_type,
                        'planets': planets,
                        'orb': orb
                    },
                    keywords=trait_data.get('keywords', [])
                )
                traits.append(trait)
        
        return traits
    
    def _analyze_house_placements(self, planets_data: Dict) -> List[Trait]:
        """Analyze house placements for contextual traits."""
        traits = []
        
        for planet_name, planet_data in planets_data.items():
            # Handle None planet data
            if planet_data is None:
                continue
                
            house = planet_data.get('house')
            if house:
                house_key = f"{planet_name}_house_{house}"
                house_traits = self.trait_rules.get('house_placements', {}).get(house_key, [])
                
                for trait_data in house_traits:
                    trait = Trait(
                        name=trait_data['name'],
                        dimension=PersonalityDimension(trait_data['dimension']),
                        intensity=IntensityLevel(trait_data.get('intensity', 3)),
                        description=trait_data['description'],
                        astrological_source={
                            'type': 'house_placement',
                            'planet': planet_name,
                            'house': house
                        },
                        keywords=trait_data.get('keywords', [])
                    )
                    traits.append(trait)
        
        return traits
    
    def _calculate_intensity(self, degree: float, base_intensity: int) -> IntensityLevel:
        """Calculate trait intensity based on degree and other factors."""
        # Simple intensity calculation - can be made more sophisticated
        if degree < 5 or degree > 25:  # Early or late degrees
            intensity_mod = 1
        else:
            intensity_mod = 0
        
        final_intensity = min(5, max(1, base_intensity + intensity_mod))
        return IntensityLevel(final_intensity)
    
    def _calculate_aspect_intensity(self, orb: float, max_orb: float) -> IntensityLevel:
        """Calculate aspect-based trait intensity from orb."""
        if orb > max_orb:
            return IntensityLevel.VERY_LOW
        
        # Closer orb = higher intensity
        intensity_ratio = 1 - (orb / max_orb)
        
        if intensity_ratio > 0.8:
            return IntensityLevel.VERY_HIGH
        elif intensity_ratio > 0.6:
            return IntensityLevel.HIGH
        elif intensity_ratio > 0.4:
            return IntensityLevel.MODERATE
        elif intensity_ratio > 0.2:
            return IntensityLevel.LOW
        else:
            return IntensityLevel.VERY_LOW
    
    def _identify_patterns(self, chart_data: Dict, traits: List[Trait]) -> List[BehavioralPattern]:
        """Identify behavioral patterns from chart data and traits."""
        patterns = []
        
        # Pattern identification logic would go here
        # This is a simplified example
        
        return patterns
    
    def _find_dominant_dimensions(self, traits: List[Trait]) -> List[PersonalityDimension]:
        """Find the most prominent personality dimensions."""
        dimension_scores = {}
        
        for trait in traits:
            dim = trait.dimension
            score = trait.intensity.value
            dimension_scores[dim] = dimension_scores.get(dim, 0) + score
        
        # Get top 3 dimensions
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)
        return [dim for dim, score in sorted_dims[:3]]
    
    def _generate_personality_summary(self, traits: List[Trait], 
                                    patterns: List[BehavioralPattern]) -> str:
        """Generate a narrative summary of the personality profile."""
        if not traits:
            return "No significant personality traits identified."
        
        dominant_traits = [trait for trait in traits if trait.intensity.value >= 4]
        
        summary_parts = []
        
        if dominant_traits:
            summary_parts.append(f"Key personality strengths include {', '.join([trait.name for trait in dominant_traits[:3]])}.")
        
        if patterns:
            summary_parts.append(f"Notable behavioral patterns include {len(patterns)} distinct patterns.")
        
        summary_parts.append(f"Profile based on analysis of {len(traits)} personality traits.")
        
        return " ".join(summary_parts)
    
    def _calculate_overall_compatibility(self, profile1: PersonalityProfile, 
                                       profile2: PersonalityProfile) -> float:
        """Calculate overall compatibility score between two profiles."""
        # Simplified compatibility calculation
        # In a real implementation, this would be much more sophisticated
        
        dimension_scores = []
        
        for dim in PersonalityDimension:
            traits1 = profile1.get_trait_by_dimension(dim)
            traits2 = profile2.get_trait_by_dimension(dim)
            
            if traits1 and traits2:
                avg_intensity1 = sum(trait.intensity.value for trait in traits1) / len(traits1)
                avg_intensity2 = sum(trait.intensity.value for trait in traits2) / len(traits2)
                
                # Simple compatibility: closer intensities = better compatibility
                diff = abs(avg_intensity1 - avg_intensity2)
                score = max(0, 1 - (diff / 4))  # Scale to 0-1
                dimension_scores.append(score)
        
        return sum(dimension_scores) / len(dimension_scores) if dimension_scores else 0.5
    
    def _analyze_dimension_compatibility(self, profile1: PersonalityProfile, 
                                       profile2: PersonalityProfile) -> Dict[PersonalityDimension, float]:
        """Analyze compatibility for each personality dimension."""
        compatibility = {}
        
        for dim in PersonalityDimension:
            traits1 = profile1.get_trait_by_dimension(dim)
            traits2 = profile2.get_trait_by_dimension(dim)
            
            if traits1 and traits2:
                # Calculate dimension-specific compatibility
                avg_intensity1 = sum(trait.intensity.value for trait in traits1) / len(traits1)
                avg_intensity2 = sum(trait.intensity.value for trait in traits2) / len(traits2)
                
                diff = abs(avg_intensity1 - avg_intensity2)
                score = max(0, 1 - (diff / 4))
                compatibility[dim] = score
            else:
                compatibility[dim] = 0.5  # Neutral when data is missing
        
        return compatibility
    
    def _identify_compatibility_factors(self, profile1: PersonalityProfile, 
                                      profile2: PersonalityProfile) -> Tuple[List[str], List[str]]:
        """Identify compatibility strengths and challenges."""
        strengths = []
        challenges = []
        
        # Analyze shared dominant dimensions
        shared_dims = set(profile1.dominant_dimensions) & set(profile2.dominant_dimensions)
        if shared_dims:
            strengths.append(f"Shared focus on {', '.join([dim.value for dim in shared_dims])}")
        
        # Analyze complementary traits
        # This would be more sophisticated in a real implementation
        
        return strengths, challenges
    
    def _generate_compatibility_recommendations(self, profile1: PersonalityProfile, 
                                              profile2: PersonalityProfile,
                                              strengths: List[str], 
                                              challenges: List[str]) -> List[str]:
        """Generate recommendations for improving compatibility."""
        recommendations = []
        
        if strengths:
            recommendations.append("Focus on leveraging your shared strengths in communication.")
        
        if challenges:
            recommendations.append("Work on understanding and respecting your differences.")
        
        recommendations.append("Regular open communication will help bridge any personality gaps.")
        
        return recommendations
    
    def _analyze_synastry_influences(self, chart1: Optional[Dict], 
                                   chart2: Optional[Dict]) -> List[Dict[str, any]]:
        """Analyze synastry influences between two charts."""
        if not chart1 or not chart2:
            return []
        
        influences = []
        
        # This would involve detailed synastry analysis
        # For now, return a placeholder
        
        return influences
    
    def _initialize_trait_rules(self) -> Dict:
        """Initialize the trait analysis rules database."""
        # This would typically be loaded from a configuration file or database
        # For now, we'll include a sample set of rules
        
        return {
            'sun_signs': {
                'Aries': [
                    {
                        'name': 'Leadership Drive',
                        'dimension': 'leadership',
                        'description': 'Natural tendency to take charge and lead others',
                        'intensity_base': 4,
                        'keywords': ['leadership', 'initiative', 'courage', 'pioneering']
                    },
                    {
                        'name': 'High Assertiveness',
                        'dimension': 'assertiveness',
                        'description': 'Direct and assertive communication style',
                        'intensity_base': 4,
                        'keywords': ['assertive', 'direct', 'confident', 'bold']
                    }
                ],
                'Taurus': [
                    {
                        'name': 'Emotional Stability',
                        'dimension': 'emotional_stability',
                        'description': 'Steady and reliable emotional nature',
                        'intensity_base': 4,
                        'keywords': ['stable', 'reliable', 'practical', 'persistent']
                    }
                ],
                # Add more signs as needed
            },
            'moon_signs': {
                'Cancer': [
                    {
                        'name': 'Emotional Sensitivity',
                        'dimension': 'emotional_stability',
                        'description': 'Deep emotional sensitivity and intuition',
                        'intensity_base': 4,
                        'keywords': ['sensitive', 'intuitive', 'caring', 'protective']
                    }
                ],
                # Add more moon signs
            },
            'ascendant_signs': {
                'Leo': [
                    {
                        'name': 'Charismatic Presence',
                        'dimension': 'extraversion',
                        'description': 'Naturally charismatic and attention-drawing presence',
                        'intensity': 4,
                        'keywords': ['charismatic', 'confident', 'dramatic', 'generous']
                    }
                ],
                # Add more ascendant signs
            },
            'aspects': {
                # Add aspect-based traits
            },
            'house_placements': {
                # Add house placement traits
            }
        }
    
    def _initialize_pattern_rules(self) -> Dict:
        """Initialize the behavioral pattern rules."""
        return {
            # Pattern identification rules would go here
        }
    
    def _extract_symbolon_traits(self, chart_data: Dict, birth_data: Dict) -> List[Trait]:
        """Extract personality traits using Symbolon archetypal analysis."""
        traits = []
        
        if not self.symbolon_analyzer:
            return traits
        
        try:
            # Get Symbolon reading
            symbolon_reading = self.symbolon_analyzer.analyze_chart(chart_data, birth_data)
            
            # Extract personality insights from primary archetypes
            insights = self.symbolon_analyzer.get_personality_insights(symbolon_reading.primary_archetypes)
            
            # Convert archetypal insights to traits
            for archetype in symbolon_reading.primary_archetypes[:5]:  # Top 5 archetypes
                trait = self._create_archetypal_trait(archetype, symbolon_reading.card_matches)
                if trait:
                    traits.append(trait)
            
            return traits
            
        except Exception as e:
            print(f"Error extracting Symbolon traits: {e}")
            return traits
    
    def _create_archetypal_trait(self, archetype, card_matches: Dict[int, float]) -> Optional[Trait]:
        """Create a personality trait from a Symbolon archetype."""
        match_score = card_matches.get(archetype.card_id, 0.0)
        
        if match_score < 0.1:  # Too weak to be meaningful
            return None
        
        # Determine intensity based on match score
        if match_score >= 0.7:
            intensity = 5
        elif match_score >= 0.5:
            intensity = 4
        elif match_score >= 0.3:
            intensity = 3
        elif match_score >= 0.2:
            intensity = 2
        else:
            intensity = 1
        
        # Map archetype to personality dimension
        dimension = self._map_archetype_to_dimension(archetype)
        
        # Create archetypal description
        description = f"Embodies the {archetype.card_name} archetype, bringing {self._get_archetypal_qualities(archetype)}"
        
        return Trait(
            name=f"Archetypal {archetype.card_name}",
            dimension=dimension,
            intensity=intensity,
            description=description,
            astrological_basis=[f"Symbolon Card: {archetype.card_name}"],
            created_timestamp=datetime.now().isoformat()
        )
    
    def _map_archetype_to_dimension(self, archetype) -> str:
        """Map a Symbolon archetype to a personality dimension."""
        # Mapping based on archetypal qualities
        archetype_mappings = {
            1: 'extraversion',     # The Warrior
            2: 'conscientiousness', # The Builder
            3: 'openness',         # The Messenger
            4: 'empathy',          # The Nurturer
            5: 'extraversion',     # The Sovereign
            6: 'conscientiousness', # The Healer
            7: 'agreeableness',    # The Diplomat
            8: 'analytical_thinking', # The Alchemist
            9: 'openness',         # The Seeker
            10: 'independence',    # The Architect
            11: 'independence',    # The Visionary
            12: 'spiritual_orientation' # The Mystic
        }
        
        # Default mapping for combination cards
        if archetype.card_id not in archetype_mappings:
            if archetype.is_pure_sign:
                # Map based on primary sign characteristics
                sign_mappings = {
                    'Aries': 'extraversion',
                    'Taurus': 'conscientiousness',
                    'Gemini': 'openness',
                    'Cancer': 'empathy',
                    'Leo': 'extraversion',
                    'Virgo': 'conscientiousness',
                    'Libra': 'agreeableness',
                    'Scorpio': 'analytical_thinking',
                    'Sagittarius': 'openness',
                    'Capricorn': 'independence',
                    'Aquarius': 'independence',
                    'Pisces': 'spiritual_orientation'
                }
                return sign_mappings.get(archetype.sign1, 'openness')
            else:
                return 'openness'  # Default for combination cards
        
        return archetype_mappings[archetype.card_id]
    
    def _get_archetypal_qualities(self, archetype) -> str:
        """Get the key qualities associated with an archetype."""
        quality_mappings = {
            1: "courage, initiative, and pioneering spirit",
            2: "stability, persistence, and practical wisdom",
            3: "adaptability, communication skills, and intellectual curiosity",
            4: "nurturing care, emotional sensitivity, and protective instincts",
            5: "creative expression, confidence, and natural leadership",
            6: "analytical precision, service orientation, and healing abilities",
            7: "diplomatic balance, aesthetic appreciation, and harmony-seeking",
            8: "transformative depth, investigative insight, and regenerative power",
            9: "philosophical wisdom, adventurous spirit, and truth-seeking",
            10: "ambitious drive, disciplined focus, and authoritative competence",
            11: "innovative vision, humanitarian ideals, and unique perspective",
            12: "compassionate understanding, intuitive wisdom, and spiritual connection"
        }
        
        return quality_mappings.get(archetype.card_id, f"the essence of {archetype.card_name.lower()}")
    
    def _generate_personality_summary(self, chart_data: Dict, traits: List[Trait], 
                                    behavioral_patterns: List[BehavioralPattern]) -> str:
        """Generate enhanced personality summary including Symbolon insights."""
        # Get basic summary
        summary_parts = []
        
        # Trait summary
        if traits:
            trait_count = len(traits)
            summary_parts.append(f"This personality profile reveals {trait_count} significant traits")
            
            # Highlight archetypal traits if present
            archetypal_traits = [t for t in traits if "Archetypal" in t.name]
            if archetypal_traits:
                archetype_names = [t.name.replace("Archetypal ", "") for t in archetypal_traits]
                summary_parts.append(f"The core archetypal patterns include: {', '.join(archetype_names)}")
        
        # Symbolon archetypal summary if available
        if self.symbolon_analyzer:
            try:
                symbolon_reading = self.symbolon_analyzer.analyze_chart(chart_data, {})
                if symbolon_reading.primary_archetypes:
                    primary_archetype = symbolon_reading.primary_archetypes[0]
                    summary_parts.append(f"The dominant life archetype is {primary_archetype.card_name}")
            except:
                pass  # Continue without Symbolon summary if there's an error
        
        # Behavioral patterns summary
        if behavioral_patterns:
            summary_parts.append(f"Key behavioral patterns include {len(behavioral_patterns)} distinct tendencies")
        
        if not summary_parts:
            summary_parts.append("A unique personality profile with individual characteristics")
        
        return ". ".join(summary_parts) + "."