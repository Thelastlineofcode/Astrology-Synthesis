"""
Aspect Interpretation Engine

Interprets planetary aspects (angular relationships):
- Conjunction (0°): Blending
- Sextile (60°): Harmonious opportunity
- Square (90°): Dynamic tension
- Trine (120°): Natural flow
- Opposition (180°): Polarity/awareness
"""

class AspectInterpreter:
    """Interprets planetary aspects"""
    
    MAJOR_ASPECTS = {
        "conjunction": {"angle": 0, "orb": 8, "nature": "neutral"},
        "sextile": {"angle": 60, "orb": 6, "nature": "harmonious"},
        "square": {"angle": 90, "orb": 8, "nature": "challenging"},
        "trine": {"angle": 120, "orb": 8, "nature": "harmonious"},
        "opposition": {"angle": 180, "orb": 8, "nature": "challenging"}
    }
    
    def __init__(self, data_path: str = None):
        """Initialize with interpretation data"""
        self.data_path = data_path or "backend/interpretations/data/aspect_interpretations.json"
        self.interpretations = self._load_interpretations()
    
    def _load_interpretations(self) -> dict:
        """Load aspect interpretation data from JSON"""
        # TODO: Load from JSON file
        return {}
    
    def interpret_aspect(self, planet1: str, planet2: str, aspect_type: str) -> dict:
        """
        Get interpretation for aspect between two planets
        
        Args:
            planet1: First planet (e.g., "Sun")
            planet2: Second planet (e.g., "Moon")
            aspect_type: Type of aspect (e.g., "trine", "square")
        
        Returns:
            dict: {
                "title": str,
                "nature": str,  # "harmonious" or "challenging"
                "description": str,
                "manifestation": str
            }
        """
        key = f"{planet1.lower()}_{aspect_type}_{planet2.lower()}"
        aspect_info = self.MAJOR_ASPECTS.get(aspect_type, {})
        
        return self.interpretations.get(key, {
            "title": f"{planet1} {aspect_type.title()} {planet2}",
            "nature": aspect_info.get("nature", "neutral"),
            "description": "Interpretation pending - data to be added",
            "manifestation": ""
        })
