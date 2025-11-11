"""
Main Interpretation Engine

Orchestrates all interpretation subsystems:
- Core interpretations (planets, houses, lunar mansions, aspects)
- Synastry interpretations (compatibility analysis)

This is the primary interface for generating astrological interpretations.
"""

from .core import PlanetInterpreter, HouseInterpreter, AspectInterpreter
from .synastry import InterAspectInterpreter, HouseOverlayInterpreter, LunarMansionSynastryInterpreter


class InterpretationEngine:
    """Main interpretation orchestrator"""
    
    def __init__(self):
        """Initialize all interpretation subsystems"""
        # Core interpreters
        self.planets = PlanetInterpreter()
        self.houses = HouseInterpreter()
        self.aspects = AspectInterpreter()
        
        # Synastry interpreters
        self.inter_aspects = InterAspectInterpreter()
        self.house_overlays = HouseOverlayInterpreter()
        self.nakshatra_synastry = LunarMansionSynastryInterpreter()
    
    def interpret_birth_chart(self, chart_data: dict) -> dict:
        """
        Generate full interpretation for a birth chart
        
        Args:
            chart_data: Dictionary with chart calculations
        
        Returns:
            dict: Comprehensive chart interpretation
        """
        interpretation = {
            "planets": [],
            "houses": [],
            "aspects": [],
            "synthesis": ""
        }
        
        # Interpret each planet
        for planet_data in chart_data.get("planets", []):
            planet_interp = self.planets.interpret_planet_in_sign(
                planet_data["name"],
                planet_data["sign"]
            )
            house_interp = self.houses.interpret_planet_in_house(
                planet_data["name"],
                planet_data["house"]
            )
            
            interpretation["planets"].append({
                "planet": planet_data["name"],
                "sign_interpretation": planet_interp,
                "house_interpretation": house_interp
            })
        
        # Interpret aspects
        for aspect_data in chart_data.get("aspects", []):
            aspect_interp = self.aspects.interpret_aspect(
                aspect_data["planet1"],
                aspect_data["planet2"],
                aspect_data["type"]
            )
            interpretation["aspects"].append(aspect_interp)
        
        return interpretation
    
    def interpret_synastry(self, chart1: dict, chart2: dict) -> dict:
        """
        Generate synastry (compatibility) interpretation
        
        Args:
            chart1: Person A's chart data
            chart2: Person B's chart data
        
        Returns:
            dict: Comprehensive compatibility interpretation
        """
        synastry = {
            "inter_aspects": [],
            "house_overlays": [],
            "nakshatra_compatibility": {},
            "overall_score": 0.0
        }
        
        # Calculate and interpret inter-chart aspects
        # TODO: Implement aspect calculation between charts
        
        # Calculate and interpret house overlays
        # TODO: Implement house overlay calculations
        
        # Interpret Nakshatra compatibility
        person1_nakshatra = chart1.get("moon_nakshatra")
        person2_nakshatra = chart2.get("moon_nakshatra")
        
        if person1_nakshatra and person2_nakshatra:
            synastry["nakshatra_compatibility"] = self.nakshatra_synastry.interpret_nakshatra_compatibility(
                person1_nakshatra,
                person2_nakshatra
            )
        
        return synastry
