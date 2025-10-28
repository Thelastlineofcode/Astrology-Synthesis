"""
Symbolon Card Analyzer Service
Analyzes astrological charts using the 79 Symbolon cards to provide archetypal insights.
"""

import csv
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from ..models.symbolon_card import (
    SymbolonCard, SymbolonReading, CardStatus, Element, Modality,
    SYMBOLON_PERSONALITY_MAPPINGS
)


class SymbolonAnalyzer:
    """Analyzes charts using Symbolon card archetypes."""
    
    def __init__(self):
        """Initialize the analyzer with card data."""
        self.cards: List[SymbolonCard] = []
        self.card_lookup: Dict[int, SymbolonCard] = {}
        self._load_cards()
    
    def _load_cards(self):
        """Load Symbolon cards from CSV file."""
        # Find the CSV file relative to this module
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, '..', '..', 'content', 'symbolon_79_cards_complete.csv')
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    card = SymbolonCard(
                        card_id=int(row['Card_ID']),
                        card_name=row['Card_Name'],
                        sign1=row['Sign1'],
                        sign2=row['Sign2'],
                        planet1=row['Planet1'],
                        planet2=row['Planet2'],
                        element=row['Element'],
                        modality=row['Modality'],
                        status=CardStatus(row['Status'])
                    )
                    self.cards.append(card)
                    self.card_lookup[card.card_id] = card
                    
            print(f"Loaded {len(self.cards)} Symbolon cards")
            
        except FileNotFoundError:
            print(f"Warning: Symbolon cards file not found at {csv_path}")
        except Exception as e:
            print(f"Error loading Symbolon cards: {e}")
    
    def analyze_chart(self, chart_data: Dict[str, Any], birth_data: Dict[str, Any]) -> SymbolonReading:
        """
        Analyze a natal chart using Symbolon cards.
        
        Args:
            chart_data: Chart information with planets, houses, aspects
            birth_data: Birth information (date, time, location)
            
        Returns:
            SymbolonReading with matched cards and interpretation
        """
        if not self.cards:
            raise ValueError("No Symbolon cards loaded")
        
        # Extract chart placements
        chart_placements = self._extract_chart_placements(chart_data)
        
        # Calculate card matches
        card_matches = self._calculate_card_matches(chart_placements)
        
        # Identify primary archetypes
        primary_archetypes = self._identify_primary_archetypes(card_matches)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(primary_archetypes, chart_placements)
        
        return SymbolonReading(
            cards=self.cards,
            chart_placements=chart_placements,
            card_matches=card_matches,
            primary_archetypes=primary_archetypes,
            interpretation=interpretation,
            timestamp=datetime.now().isoformat()
        )
    
    def _extract_chart_placements(self, chart_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract planet-sign-house placements from chart data."""
        placements = {}
        
        planets = chart_data.get('planets', {})
        for planet, data in planets.items():
            placements[planet] = {
                'sign': data.get('sign'),
                'house': data.get('house'),
                'degree': data.get('degree', 0)
            }
        
        return placements
    
    def _calculate_card_matches(self, chart_placements: Dict[str, Dict[str, Any]]) -> Dict[int, float]:
        """Calculate how well each card matches the chart."""
        card_matches = {}
        
        for card in self.cards:
            total_score = 0.0
            placement_count = 0
            
            # Check each planet placement against the card
            for planet, placement in chart_placements.items():
                sign = placement.get('sign')
                if sign:
                    match_score = card.matches_chart_placement(sign, planet)
                    total_score += match_score
                    placement_count += 1
            
            # Average score across all placements
            if placement_count > 0:
                card_matches[card.card_id] = total_score / placement_count
            else:
                card_matches[card.card_id] = 0.0
        
        return card_matches
    
    def _identify_primary_archetypes(self, card_matches: Dict[int, float], top_n: int = 7) -> List[SymbolonCard]:
        """Identify the most relevant Symbolon archetypes."""
        # Sort cards by match score
        sorted_matches = sorted(card_matches.items(), key=lambda x: x[1], reverse=True)
        
        primary_cards = []
        for card_id, score in sorted_matches[:top_n]:
            if score > 0.1:  # Only include cards with meaningful matches
                primary_cards.append(self.card_lookup[card_id])
        
        return primary_cards
    
    def _generate_interpretation(self, primary_archetypes: List[SymbolonCard], 
                               chart_placements: Dict[str, Dict[str, Any]]) -> str:
        """Generate a narrative interpretation of the Symbolon reading."""
        if not primary_archetypes:
            return "No strong archetypal patterns identified in this chart."
        
        interpretation_parts = []
        
        # Introduction
        interpretation_parts.append(
            f"This chart reveals {len(primary_archetypes)} primary Symbolon archetypes "
            f"that shape the individual's core personality and life path."
        )
        
        # Describe top 3 archetypes
        for i, card in enumerate(primary_archetypes[:3]):
            part_intro = f"\n{i+1}. **{card.card_name}**"
            
            if card.is_pure_sign and card.is_pure_planet:
                part_intro += f" ({card.sign1}) - Pure archetypal energy"
            else:
                part_intro += f" ({card.sign1}-{card.sign2}) - Blended archetypal energy"
            
            interpretation_parts.append(part_intro)
            
            # Add archetypal meaning based on card type
            archetype_meaning = self._get_archetype_meaning(card)
            interpretation_parts.append(archetype_meaning)
        
        # Overall pattern analysis
        if len(primary_archetypes) > 3:
            interpretation_parts.append(
                f"\nAdditional archetypal influences include: "
                f"{', '.join([card.card_name for card in primary_archetypes[3:]])}"
            )
        
        # Element and modality themes
        element_themes = self._analyze_element_themes(primary_archetypes)
        modality_themes = self._analyze_modality_themes(primary_archetypes)
        
        if element_themes:
            interpretation_parts.append(f"\n**Elemental Themes:** {element_themes}")
        
        if modality_themes:
            interpretation_parts.append(f"\n**Modal Themes:** {modality_themes}")
        
        return ' '.join(interpretation_parts)
    
    def _get_archetype_meaning(self, card: SymbolonCard) -> str:
        """Get the archetypal meaning for a specific card."""
        # Basic meanings for the 12 pure sign cards
        pure_meanings = {
            1: "Embodies the pioneering spirit, courage to initiate, and natural leadership qualities. This archetype brings dynamic energy and the drive to break new ground.",
            2: "Represents stability, perseverance, and the ability to build lasting foundations. This archetype brings practical wisdom and sensual appreciation of life.",
            3: "Symbolizes communication, adaptability, and intellectual curiosity. This archetype brings versatility and the ability to connect diverse ideas.",
            4: "Embodies nurturing care, emotional sensitivity, and protective instincts. This archetype brings intuitive wisdom and deep emotional understanding.",
            5: "Represents creative self-expression, confidence, and generous leadership. This archetype brings radiant energy and the desire to shine authentically.",
            6: "Symbolizes service, perfectionism, and analytical precision. This archetype brings practical healing abilities and attention to detail.",
            7: "Embodies harmony, beauty, and diplomatic balance. This archetype brings the ability to create peace and aesthetic appreciation.",
            8: "Represents transformation, intensity, and profound depth. This archetype brings the power to transform and regenerate through life's mysteries.",
            9: "Symbolizes adventure, philosophy, and the quest for truth. This archetype brings optimism and the drive to expand horizons.",
            10: "Embodies ambition, responsibility, and authoritative mastery. This archetype brings the ability to achieve lasting success through discipline.",
            11: "Represents innovation, humanitarianism, and unique vision. This archetype brings revolutionary thinking and concern for collective progress.",
            12: "Symbolizes compassion, imagination, and spiritual connection. This archetype brings transcendent wisdom and empathetic understanding."
        }
        
        if card.card_id in pure_meanings:
            return pure_meanings[card.card_id]
        
        # For combination cards, create meaning from component parts
        if not card.is_pure_sign:
            return f"This archetype blends the qualities of {card.sign1} and {card.sign2}, creating a unique synthesis of energies that manifests as {card.card_name.lower()}."
        
        return f"This archetype represents the essence of {card.card_name.lower()}."
    
    def _analyze_element_themes(self, cards: List[SymbolonCard]) -> str:
        """Analyze dominant elemental themes in the cards."""
        element_count = {}
        
        for card in cards:
            for element in card.get_elements():
                if element != Element.ALL:
                    element_count[element.value] = element_count.get(element.value, 0) + 1
        
        if not element_count:
            return ""
        
        dominant_element = max(element_count, key=element_count.get)
        
        element_themes = {
            'Fire': "Dynamic energy, initiative, and passionate expression dominate",
            'Earth': "Practical manifestation, stability, and grounded wisdom prevail",
            'Air': "Mental agility, communication, and intellectual pursuits are emphasized",
            'Water': "Emotional depth, intuition, and empathetic connection flow strongly"
        }
        
        return element_themes.get(dominant_element, "Balanced elemental expression")
    
    def _analyze_modality_themes(self, cards: List[SymbolonCard]) -> str:
        """Analyze dominant modal themes in the cards."""
        modality_count = {}
        
        for card in cards:
            for modality in card.get_modalities():
                if modality != Modality.ALL:
                    modality_count[modality.value] = modality_count.get(modality.value, 0) + 1
        
        if not modality_count:
            return ""
        
        dominant_modality = max(modality_count, key=modality_count.get)
        
        modality_themes = {
            'Cardinal': "Initiative, leadership, and pioneering action are key themes",
            'Fixed': "Stability, persistence, and unwavering focus characterize the approach",
            'Mutable': "Adaptability, flexibility, and transformative change guide the path"
        }
        
        return modality_themes.get(dominant_modality, "Balanced modal expression")
    
    def get_cards_by_planet(self, planet: str) -> List[SymbolonCard]:
        """Get all cards associated with a specific planet."""
        matching_cards = []
        
        for card in self.cards:
            if planet in card.get_planets():
                matching_cards.append(card)
        
        return matching_cards
    
    def get_cards_by_sign(self, sign: str) -> List[SymbolonCard]:
        """Get all cards associated with a specific sign."""
        matching_cards = []
        
        for card in self.cards:
            if sign in card.get_signs():
                matching_cards.append(card)
        
        return matching_cards
    
    def get_personality_insights(self, primary_archetypes: List[SymbolonCard]) -> Dict[str, Any]:
        """Extract personality insights from primary archetypes."""
        insights = {
            'dimensions': {},
            'traits': [],
            'behaviors': [],
            'archetypal_strengths': [],
            'archetypal_challenges': []
        }
        
        # Aggregate insights from each archetype
        for card in primary_archetypes:
            if card.card_id in SYMBOLON_PERSONALITY_MAPPINGS:
                mapping = SYMBOLON_PERSONALITY_MAPPINGS[card.card_id]
                
                # Add dimensional influences
                for dimension in mapping.get('dimensions', []):
                    insights['dimensions'][dimension] = insights['dimensions'].get(dimension, 0) + 1
                
                # Add traits and behaviors
                insights['traits'].extend(mapping.get('traits', []))
                insights['behaviors'].extend(mapping.get('behaviors', []))
        
        # Add archetypal perspectives
        insights['archetypal_strengths'] = [
            f"{card.card_name}: {self._get_archetype_strengths(card)}"
            for card in primary_archetypes[:3]
        ]
        
        insights['archetypal_challenges'] = [
            f"{card.card_name}: {self._get_archetype_challenges(card)}"
            for card in primary_archetypes[:3]
        ]
        
        return insights
    
    def _get_archetype_strengths(self, card: SymbolonCard) -> str:
        """Get the key strengths of an archetype."""
        strengths_map = {
            1: "Natural leadership, courage, pioneering spirit",
            2: "Reliability, practical wisdom, persistence",
            3: "Versatility, communication skills, intellectual curiosity",
            4: "Empathy, nurturing care, emotional intelligence",
            5: "Creativity, confidence, generous leadership",
            6: "Attention to detail, analytical skills, service orientation",
            7: "Diplomatic skills, aesthetic sense, harmony creation",
            8: "Transformative power, depth perception, regenerative ability",
            9: "Optimism, philosophical insight, adventurous spirit",
            10: "Ambition, discipline, authoritative competence",
            11: "Innovation, humanitarian vision, unique perspective",
            12: "Compassion, intuition, spiritual connection"
        }
        
        return strengths_map.get(card.card_id, "Unique archetypal gifts")
    
    def _get_archetype_challenges(self, card: SymbolonCard) -> str:
        """Get the potential challenges of an archetype."""
        challenges_map = {
            1: "Impulsiveness, impatience, tendency to dominate",
            2: "Stubbornness, resistance to change, materialism",
            3: "Restlessness, superficiality, inconsistency",
            4: "Moodiness, over-sensitivity, tendency to cling",
            5: "Pride, attention-seeking, dramatic tendencies",
            6: "Perfectionism, criticism, worry",
            7: "Indecision, people-pleasing, conflict avoidance",
            8: "Intensity, secretiveness, destructive tendencies",
            9: "Restlessness, irresponsibility, dogmatism",
            10: "Pessimism, rigidity, authoritarian tendencies",
            11: "Detachment, rebelliousness, unpredictability",
            12: "Escapism, confusion, boundary issues"
        }
        
        return challenges_map.get(card.card_id, "Shadow aspects to integrate")


# Helper function for external use
def create_symbolon_analyzer() -> SymbolonAnalyzer:
    """Create and return a new SymbolonAnalyzer instance."""
    return SymbolonAnalyzer()