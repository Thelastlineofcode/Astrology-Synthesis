"""
Inter-Chart Aspect Interpretations

Interprets aspects between two people's charts (synastry aspects).
Example: Person A's Venus trine Person B's Mars
"""

class InterAspectInterpreter:
    """Interprets aspects between two charts"""
    
    def __init__(self, data_path: str = None):
        """Initialize with synastry aspect data"""
        self.data_path = data_path or "backend/interpretations/data/synastry_interpretations.json"
        self.interpretations = self._load_interpretations()
    
    def _load_interpretations(self) -> dict:
        """Load synastry aspect interpretations"""
        # TODO: Load from JSON
        return {}
    
    def interpret_inter_aspect(
        self,
        person1_planet: str,
        person2_planet: str,
        aspect_type: str
    ) -> dict:
        """
        Get interpretation for aspect between two charts
        
        Args:
            person1_planet: Person A's planet (e.g., "Venus")
            person2_planet: Person B's planet (e.g., "Mars")
            aspect_type: Aspect type (e.g., "trine", "square")
        
        Returns:
            dict: {
                "title": str,
                "compatibility_score": float,  # 0.0 to 1.0
                "description": str,
                "relationship_impact": str,
                "advice": str
            }
        """
        key = f"{person1_planet.lower()}_{aspect_type}_{person2_planet.lower()}"
        
        return self.interpretations.get(key, {
            "title": f"Person A's {person1_planet} {aspect_type.title()} Person B's {person2_planet}",
            "compatibility_score": 0.5,
            "description": "Interpretation pending - data to be added",
            "relationship_impact": "",
            "advice": ""
        })
