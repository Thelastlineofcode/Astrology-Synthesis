"""
Symbolon Card Models for BMAD System
Represents the 79 Symbolon cards and their astrological correspondences.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class CardStatus(Enum):
    """Status of card template completion."""
    FULLY_DETAILED = "FULLY_DETAILED"
    TEMPLATE_READY = "TEMPLATE_READY" 
    STRUCTURE_READY = "STRUCTURE_READY"
    MASTER_CARD = "MASTER_CARD"


class Element(Enum):
    """Astrological elements."""
    FIRE = "Fire"
    EARTH = "Earth"
    AIR = "Air"
    WATER = "Water"
    ALL = "All"


class Modality(Enum):
    """Astrological modalities."""
    CARDINAL = "Cardinal"
    FIXED = "Fixed"
    MUTABLE = "Mutable"
    ALL = "All"


@dataclass
class SymbolonCard:
    """Represents a single Symbolon card with its astrological properties."""
    
    card_id: int
    card_name: str
    sign1: str
    sign2: str
    planet1: str
    planet2: str
    element: str
    modality: str
    status: CardStatus
    
    # Additional computed properties
    is_pure_sign: bool = False  # True if both signs are the same
    is_pure_planet: bool = False  # True if both planets are the same
    
    def __post_init__(self):
        """Compute additional properties after initialization."""
        self.is_pure_sign = self.sign1 == self.sign2
        self.is_pure_planet = self.planet1 == self.planet2
    
    def get_signs(self) -> List[str]:
        """Get list of unique signs involved in this card."""
        if self.sign1 == "All":
            return ["All"]
        signs = [self.sign1]
        if self.sign2 != self.sign1:
            signs.append(self.sign2)
        return signs
    
    def get_planets(self) -> List[str]:
        """Get list of unique planets involved in this card."""
        if self.planet1 == "All":
            return ["All"]
        
        # Handle compound planets like "Mars/Pluto"
        planets = []
        for planet_str in [self.planet1, self.planet2]:
            if "/" in planet_str:
                planets.extend(planet_str.split("/"))
            else:
                planets.append(planet_str)
        
        return list(set(planets))  # Remove duplicates
    
    def get_elements(self) -> List[Element]:
        """Get list of elements involved in this card."""
        if self.element == "All":
            return [Element.ALL]
        
        element_map = {
            "Fire": Element.FIRE,
            "Earth": Element.EARTH,
            "Air": Element.AIR,
            "Water": Element.WATER
        }
        
        elements = []
        for elem_str in self.element.split("/"):
            if elem_str in element_map:
                elements.append(element_map[elem_str])
        
        return elements
    
    def get_modalities(self) -> List[Modality]:
        """Get list of modalities involved in this card."""
        if self.modality == "All":
            return [Modality.ALL]
        
        modality_map = {
            "Cardinal": Modality.CARDINAL,
            "Fixed": Modality.FIXED,
            "Mutable": Modality.MUTABLE
        }
        
        modalities = []
        for mod_str in self.modality.split("/"):
            if mod_str in modality_map:
                modalities.append(modality_map[mod_str])
        
        return modalities
    
    def matches_chart_placement(self, sign: str, planet: str) -> float:
        """
        Calculate how well this card matches a chart placement.
        Returns a score from 0.0 to 1.0.
        """
        score = 0.0
        
        # Check sign match
        card_signs = self.get_signs()
        if "All" in card_signs or sign in card_signs:
            score += 0.5
        
        # Check planet match
        card_planets = self.get_planets()
        if "All" in card_planets or planet in card_planets:
            score += 0.5
        
        # Bonus for exact match
        if (sign == self.sign1 and planet == self.planet1) or \
           (sign == self.sign2 and planet == self.planet2):
            score += 0.2
        
        # Bonus for pure cards (more archetypal)
        if self.is_pure_sign and self.is_pure_planet:
            score += 0.1
        
        return min(score, 1.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary format."""
        return {
            'card_id': self.card_id,
            'card_name': self.card_name,
            'sign1': self.sign1,
            'sign2': self.sign2,
            'planet1': self.planet1,
            'planet2': self.planet2,
            'element': self.element,
            'modality': self.modality,
            'status': self.status.value,
            'is_pure_sign': self.is_pure_sign,
            'is_pure_planet': self.is_pure_planet,
            'signs': self.get_signs(),
            'planets': self.get_planets(),
            'elements': [e.value for e in self.get_elements()],
            'modalities': [m.value for m in self.get_modalities()]
        }


@dataclass
class SymbolonReading:
    """Represents a Symbolon card reading for a chart."""
    
    cards: List[SymbolonCard]
    chart_placements: Dict[str, Dict[str, Any]]  # planet -> {sign, house, etc.}
    card_matches: Dict[int, float]  # card_id -> match score
    primary_archetypes: List[SymbolonCard]  # Most relevant cards
    interpretation: str
    timestamp: str
    
    def get_top_cards(self, limit: int = 5) -> List[SymbolonCard]:
        """Get the top matching cards by score."""
        sorted_cards = sorted(
            self.cards,
            key=lambda card: self.card_matches.get(card.card_id, 0.0),
            reverse=True
        )
        return sorted_cards[:limit]
    
    def get_cards_by_element(self, element: Element) -> List[SymbolonCard]:
        """Get cards that involve a specific element."""
        return [
            card for card in self.cards
            if element in card.get_elements()
        ]
    
    def get_cards_by_modality(self, modality: Modality) -> List[SymbolonCard]:
        """Get cards that involve a specific modality."""
        return [
            card for card in self.cards
            if modality in card.get_modalities()
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reading to dictionary format."""
        return {
            'total_cards': len(self.cards),
            'chart_placements': self.chart_placements,
            'card_matches': self.card_matches,
            'primary_archetypes': [card.to_dict() for card in self.primary_archetypes],
            'top_cards': [card.to_dict() for card in self.get_top_cards()],
            'interpretation': self.interpretation,
            'timestamp': self.timestamp,
            'element_distribution': {
                element.value: len(self.get_cards_by_element(element))
                for element in [Element.FIRE, Element.EARTH, Element.AIR, Element.WATER]
            },
            'modality_distribution': {
                modality.value: len(self.get_cards_by_modality(modality))
                for modality in [Modality.CARDINAL, Modality.FIXED, Modality.MUTABLE]
            }
        }


# Symbolon card personality and behavioral associations
SYMBOLON_PERSONALITY_MAPPINGS = {
    # Pure sign cards (1-12) - Core archetypes
    1: {  # The Warrior (Aries)
        'dimensions': ['extraversion', 'independence'],
        'traits': ['leadership', 'initiative', 'courage', 'impulsiveness'],
        'behaviors': ['decision_making', 'social_interaction', 'goal_orientation']
    },
    2: {  # The Builder (Taurus)
        'dimensions': ['conscientiousness', 'emotional_stability'],
        'traits': ['persistence', 'reliability', 'sensuality', 'stubbornness'],
        'behaviors': ['goal_orientation', 'stress_response', 'relationship_patterns']
    },
    3: {  # The Messenger (Gemini)
        'dimensions': ['openness', 'extraversion'],
        'traits': ['curiosity', 'adaptability', 'communication', 'restlessness'],
        'behaviors': ['communication_style', 'learning_preferences', 'social_interaction']
    },
    4: {  # The Nurturer (Cancer)
        'dimensions': ['agreeableness', 'empathy'],
        'traits': ['caring', 'intuition', 'protection', 'moodiness'],
        'behaviors': ['emotional_expression', 'relationship_patterns', 'stress_response']
    },
    5: {  # The Sovereign (Leo)
        'dimensions': ['extraversion', 'openness'],
        'traits': ['creativity', 'confidence', 'generosity', 'pride'],
        'behaviors': ['leadership_style', 'creative_expression', 'social_interaction']
    },
    6: {  # The Healer (Virgo)
        'dimensions': ['conscientiousness', 'analytical_thinking'],
        'traits': ['perfectionism', 'service', 'analysis', 'criticism'],
        'behaviors': ['decision_making', 'learning_preferences', 'goal_orientation']
    },
    7: {  # The Diplomat (Libra)
        'dimensions': ['agreeableness', 'empathy'],
        'traits': ['harmony', 'beauty', 'balance', 'indecision'],
        'behaviors': ['social_interaction', 'relationship_patterns', 'decision_making']
    },
    8: {  # The Alchemist (Scorpio)
        'dimensions': ['intuition', 'analytical_thinking'],
        'traits': ['intensity', 'transformation', 'depth', 'secretiveness'],
        'behaviors': ['emotional_expression', 'decision_making', 'relationship_patterns']
    },
    9: {  # The Seeker (Sagittarius)
        'dimensions': ['openness', 'independence'],
        'traits': ['adventure', 'philosophy', 'freedom', 'restlessness'],
        'behaviors': ['learning_preferences', 'goal_orientation', 'social_interaction']
    },
    10: {  # The Architect (Capricorn)
        'dimensions': ['conscientiousness', 'independence'],
        'traits': ['ambition', 'discipline', 'authority', 'pessimism'],
        'behaviors': ['leadership_style', 'goal_orientation', 'decision_making']
    },
    11: {  # The Visionary (Aquarius)
        'dimensions': ['openness', 'independence'],
        'traits': ['innovation', 'humanitarianism', 'detachment', 'rebellion'],
        'behaviors': ['social_interaction', 'creative_expression', 'learning_preferences']
    },
    12: {  # The Mystic (Pisces)
        'dimensions': ['spiritual_orientation', 'empathy'],
        'traits': ['compassion', 'intuition', 'imagination', 'escapism'],
        'behaviors': ['emotional_expression', 'creative_expression', 'stress_response']
    }
}

# Extended mappings for combination cards would go here
# For now, combination cards will use weighted combinations of their component signs