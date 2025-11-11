"""
House Overlay Interpretations

Interprets where one person's planets fall in another's houses.
Example: Person A's Sun in Person B's 7th house
"""

class HouseOverlayInterpreter:
    """Interprets house overlays in synastry"""
    
    def __init__(self, data_path: str = None):
        """Initialize with house overlay data"""
        self.data_path = data_path or "backend/interpretations/data/synastry_interpretations.json"
        self.interpretations = self._load_interpretations()
    
    def _load_interpretations(self) -> dict:
        """Load house overlay interpretations"""
        # TODO: Load from JSON
        return {}
    
    def interpret_house_overlay(
        self,
        planet: str,
        house: int,
        person_label: str = "Person A"
    ) -> dict:
        """
        Get interpretation for planet in partner's house
        
        Args:
            planet: Planet name (e.g., "Sun", "Venus")
            house: House number in partner's chart (1-12)
            person_label: "Person A" or "Person B"
        
        Returns:
            dict: {
                "title": str,
                "description": str,
                "activation": str,  # What area gets activated
                "dynamic": str
            }
        """
        key = f"{planet.lower()}_house_{house}_overlay"
        
        return self.interpretations.get(key, {
            "title": f"{person_label}'s {planet} in Partner's {house}th House",
            "description": "Interpretation pending - data to be added",
            "activation": f"Partner's {house}th house themes activated",
            "dynamic": ""
        })
