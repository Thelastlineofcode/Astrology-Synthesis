"""
Lunar Mansion (Nakshatra) Synastry Interpretations

Analyzes compatibility based on Moon's position in the 27 Nakshatras.
This is a CORE compatibility technique, not just a Vedic addition.
"""

class LunarMansionSynastryInterpreter:
    """Interprets Nakshatra compatibility between two charts"""
    
    # Nakshatra compatibility matrix (Kuta system)
    COMPATIBILITY_CATEGORIES = {
        "excellent": 1.0,
        "good": 0.75,
        "neutral": 0.5,
        "challenging": 0.25
    }
    
    def __init__(self, data_path: str = None):
        """Initialize with Nakshatra compatibility data"""
        self.data_path = data_path or "backend/interpretations/data/lunar_mansion_interpretations.json"
        self.interpretations = self._load_interpretations()
    
    def _load_interpretations(self) -> dict:
        """Load Nakshatra compatibility data"""
        # TODO: Load from JSON
        return {}
    
    def interpret_nakshatra_compatibility(
        self,
        person1_nakshatra: str,
        person2_nakshatra: str
    ) -> dict:
        """
        Get compatibility interpretation for two Nakshatras
        
        Args:
            person1_nakshatra: Person A's Moon Nakshatra
            person2_nakshatra: Person B's Moon Nakshatra
        
        Returns:
            dict: {
                "compatibility_score": float,  # 0.0 to 1.0
                "category": str,  # "excellent", "good", "neutral", "challenging"
                "description": str,
                "emotional_harmony": str,
                "challenges": list[str],
                "strengths": list[str]
            }
        """
        key = f"{person1_nakshatra}_{person2_nakshatra}"
        
        return self.interpretations.get(key, {
            "compatibility_score": 0.5,
            "category": "neutral",
            "description": "Interpretation pending - data to be added",
            "emotional_harmony": "",
            "challenges": [],
            "strengths": []
        })
