"""
Unified Multi-Tradition Interpretation Engine
Weaves together Vedic, Western, Voodoo, Mysticism, and Lunar Mansion wisdom
for rich, multi-layered predictions with endless content variations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UnifiedInterpretation:
    """Complete interpretation from all traditions."""
    primary_message: str
    vedic_perspective: str
    western_perspective: str
    voodoo_perspective: str
    mystical_perspective: str
    lunar_mansion_wisdom: str
    synthesis: str
    recommendations: List[str]
    warnings: List[str]
    opportunities: List[str]


class UnifiedInterpreter:
    """
    Multi-tradition interpretation engine that weaves all cultural perspectives
    into unified, rich predictions with endless content possibilities.
    """
    
    def __init__(self):
        """Initialize the unified interpreter with all tradition data."""
        self.lunar_mansions = self._init_lunar_mansions()
        self.voodoo_loa = self._init_voodoo_loa()
        self.mystical_symbols = self._init_mystical_symbols()
        self.planetary_synthesis = self._init_planetary_synthesis()
    
    def interpret_planet_placement(
        self,
        planet: str,
        sign: str,
        house: int,
        nakshatra: str,
        pada: int,
        aspects: List[Dict],
        current_transits: Optional[Dict] = None
    ) -> UnifiedInterpretation:
        """
        Generate unified interpretation from all traditions for a planetary placement.
        
        Each tradition adds its unique layer of meaning:
        - Vedic: Nakshatra, pada, planetary rulership
        - Western: Sign, house, aspect patterns
        - Voodoo: Associated Loa spirits and their influences
        - Mysticism: Esoteric symbols, spiritual lessons
        - Lunar Mansions: 28 mansion wisdom and timing
        
        Args:
            planet: Planet name
            sign: Zodiac sign
            house: House number (1-12)
            nakshatra: Vedic nakshatra
            pada: Pada (1-4)
            aspects: List of aspects to other planets
            current_transits: Current transit data (optional)
            
        Returns:
            UnifiedInterpretation with all perspectives woven together
        """
        # Get each tradition's perspective
        vedic = self._vedic_interpretation(planet, sign, house, nakshatra, pada)
        western = self._western_interpretation(planet, sign, house, aspects)
        voodoo = self._voodoo_interpretation(planet, sign, nakshatra)
        mystical = self._mystical_interpretation(planet, nakshatra, pada, house)
        lunar = self._lunar_mansion_interpretation(nakshatra, pada, planet)
        
        # Synthesize all perspectives into unified message
        synthesis = self._synthesize_perspectives(
            vedic, western, voodoo, mystical, lunar, planet, sign
        )
        
        # Generate actionable guidance
        recommendations = self._generate_recommendations(
            vedic, western, voodoo, mystical, lunar
        )
        warnings = self._generate_warnings(vedic, western, voodoo, mystical)
        opportunities = self._generate_opportunities(vedic, western, lunar)
        
        # Create primary unified message
        primary_message = self._create_primary_message(
            planet, sign, house, synthesis
        )
        
        return UnifiedInterpretation(
            primary_message=primary_message,
            vedic_perspective=vedic,
            western_perspective=western,
            voodoo_perspective=voodoo,
            mystical_perspective=mystical,
            lunar_mansion_wisdom=lunar,
            synthesis=synthesis,
            recommendations=recommendations,
            warnings=warnings,
            opportunities=opportunities
        )
    
    def interpret_dasha_period(
        self,
        mahadasha_lord: str,
        antardasha_lord: Optional[str],
        start_date: datetime,
        end_date: datetime,
        birth_chart: Dict
    ) -> UnifiedInterpretation:
        """
        Unified interpretation of Dasha period combining all traditions.
        
        Voodoo adds: Which Loa governs this time period
        Mysticism adds: Spiritual lessons and karmic themes
        Lunar Mansions add: Optimal timing and energy flow
        """
        # Get planetary positions from birth chart
        planet_data = self._get_planet_from_chart(mahadasha_lord, birth_chart)
        
        vedic = self._vedic_dasha_interpretation(
            mahadasha_lord, antardasha_lord, planet_data
        )
        western = self._western_progression_interpretation(
            mahadasha_lord, start_date, end_date
        )
        voodoo = self._voodoo_period_interpretation(
            mahadasha_lord, start_date, planet_data
        )
        mystical = self._mystical_cycle_interpretation(
            mahadasha_lord, start_date, planet_data
        )
        lunar = self._lunar_timing_interpretation(
            start_date, end_date, mahadasha_lord
        )
        
        synthesis = self._synthesize_period_perspectives(
            vedic, western, voodoo, mystical, lunar, mahadasha_lord
        )
        
        primary_message = f"The {mahadasha_lord} period brings convergence of energies: {synthesis[:200]}..."
        
        return UnifiedInterpretation(
            primary_message=primary_message,
            vedic_perspective=vedic,
            western_perspective=western,
            voodoo_perspective=voodoo,
            mystical_perspective=mystical,
            lunar_mansion_wisdom=lunar,
            synthesis=synthesis,
            recommendations=self._period_recommendations(vedic, voodoo, mystical),
            warnings=self._period_warnings(vedic, western, voodoo),
            opportunities=self._period_opportunities(lunar, mystical, western)
        )
    
    def interpret_transit(
        self,
        transiting_planet: str,
        natal_planet: str,
        aspect_type: str,
        transit_date: datetime,
        birth_chart: Dict
    ) -> UnifiedInterpretation:
        """
        Unified interpretation of transit combining all traditions.
        
        Each tradition sees transits differently:
        - Vedic: Gochara, planet-sign relationships
        - Western: Aspect patterns and timing
        - Voodoo: Spirit influences and crossroads
        - Mysticism: Energetic shifts and portals
        - Lunar Mansions: Best days for action
        """
        vedic = self._vedic_transit_interpretation(
            transiting_planet, natal_planet, aspect_type
        )
        western = self._western_aspect_interpretation(
            transiting_planet, natal_planet, aspect_type
        )
        voodoo = self._voodoo_crossroads_interpretation(
            transiting_planet, transit_date
        )
        mystical = self._mystical_portal_interpretation(
            transiting_planet, aspect_type, transit_date
        )
        lunar = self._lunar_favorable_days(transit_date, transiting_planet)
        
        synthesis = self._synthesize_transit_perspectives(
            vedic, western, voodoo, mystical, lunar, transiting_planet
        )
        
        primary_message = f"{transiting_planet} transit activates multiple energetic pathways: {synthesis[:150]}..."
        
        return UnifiedInterpretation(
            primary_message=primary_message,
            vedic_perspective=vedic,
            western_perspective=western,
            voodoo_perspective=voodoo,
            mystical_perspective=mystical,
            lunar_mansion_wisdom=lunar,
            synthesis=synthesis,
            recommendations=self._transit_recommendations(voodoo, lunar, mystical),
            warnings=self._transit_warnings(vedic, western, voodoo),
            opportunities=self._transit_opportunities(lunar, western, mystical)
        )
    
    # ========================================================================
    # VEDIC INTERPRETATIONS
    # ========================================================================
    
    def _vedic_interpretation(self, planet: str, sign: str, house: int, 
                             nakshatra: str, pada: int) -> str:
        """Vedic KP + Nakshatra interpretation."""
        nakshatra_meanings = {
            "Ashwini": "swift action, healing energy, pioneering spirit",
            "Bharani": "transformation, restraint, creative power held in check",
            "Krittika": "sharp discernment, purification through fire",
            "Rohini": "growth, fertility, material abundance",
            "Mrigashira": "seeking, curiosity, gentle persuasion",
            "Ardra": "storm before calm, destructive renewal",
            "Punarvasu": "return to light, renewal, restoration",
            "Pushya": "nourishment, spiritual growth, protection",
            "Ashlesha": "coiled energy, mystical insight, hidden power",
            "Magha": "ancestral power, throne, regal authority",
            "Purva Phalguni": "creative enjoyment, procreation, rest",
            "Uttara Phalguni": "patronage, friendship, contracts",
            "Hasta": "skill in hands, craftsmanship, manifestation",
            "Chitra": "brilliant design, artistic creation",
            "Swati": "independence, commerce, flexibility",
            "Vishakha": "focused determination, goal achievement",
            "Anuradha": "devotion, friendship, success after struggle",
            "Jyeshtha": "protective elder, occult knowledge",
            "Mula": "root investigation, destruction of illusion",
            "Purva Ashadha": "invincibility, early victory",
            "Uttara Ashadha": "final victory, lasting achievement",
            "Shravana": "listening, learning, connection",
            "Dhanishta": "wealth, music, adaptability",
            "Shatabhisha": "healing, secrets, mystical solitude",
            "Purva Bhadrapada": "burning away dross, intense transformation",
            "Uttara Bhadrapada": "depth, kundalini, foundation of cosmos",
            "Revati": "nourishment, safe passage, completion",
        }
        
        nak_meaning = nakshatra_meanings.get(nakshatra, "spiritual evolution")
        
        return (
            f"{planet} in {nakshatra} nakshatra (pada {pada}) within {sign} "
            f"occupying the {house}th house brings {nak_meaning}. "
            f"The energy manifests through house {house} activities, "
            f"colored by {sign}'s qualities and the nakshatra's subtle vibration."
        )
    
    # ========================================================================
    # WESTERN INTERPRETATIONS
    # ========================================================================
    
    def _western_interpretation(self, planet: str, sign: str, house: int,
                                aspects: List[Dict]) -> str:
        """Western astrology psychological interpretation."""
        western_archetypes = {
            "Sun": "core identity, ego, life force",
            "Moon": "emotions, instincts, subconscious patterns",
            "Mercury": "communication, intellect, perception",
            "Venus": "values, relationships, aesthetic sense",
            "Mars": "drive, assertion, competitive spirit",
            "Jupiter": "expansion, philosophy, optimism",
            "Saturn": "structure, discipline, limitations",
            "Rahu": "obsession, worldly desires, future direction",
            "Ketu": "detachment, spiritual liberation, past patterns",
        }
        
        archetype = western_archetypes.get(planet, "transformative energy")
        
        aspect_desc = ""
        if aspects:
            strong_aspects = [a for a in aspects if a.get('orb', 10) < 3]
            if strong_aspects:
                aspect_desc = f" The {len(strong_aspects)} tight aspect(s) intensify and modify this energy."
        
        return (
            f"In Western terms, {planet} represents your {archetype}. "
            f"Placed in {sign} and the {house}th house, this energy expresses "
            f"through {self._house_area(house)} in a {self._sign_mode(sign)} manner."
            f"{aspect_desc}"
        )
    
    # ========================================================================
    # VOODOO INTERPRETATIONS
    # ========================================================================
    
    def _voodoo_interpretation(self, planet: str, sign: str, nakshatra: str) -> str:
        """Voodoo Loa associations and spiritual guidance."""
        # Map planets to Loa spirits
        planet_loa = {
            "Sun": ("Papa Legba", "guardian of crossroads, opens all doors, speaks all tongues"),
            "Moon": ("Erzulie Freda", "love, beauty, luxury, feminine mysteries"),
            "Mercury": ("Legba Atibon", "communication between worlds, trickster wisdom"),
            "Venus": ("Erzulie Dantor", "fierce protection, motherly love, warrior heart"),
            "Mars": ("Ogou Feray", "warrior spirit, iron will, revolutionary fire"),
            "Jupiter": ("Damballah", "cosmic serpent, purity, wisdom, primordial creation"),
            "Saturn": ("Baron Samedi", "death, rebirth, guardian of cemetery, earthly pleasures"),
            "Rahu": ("Kalfu", "dark crossroads, night magic, destruction before renewal"),
            "Ketu": ("Ghede Nibo", "death vision, seeing beyond veils, spiritual insight"),
        }
        
        loa_name, loa_qualities = planet_loa.get(planet, ("Simbi", "water magic, herbalism"))
        
        # Nakshatra adds specific Voodoo magic element
        nakshatra_magic = {
            "Ashwini": "healing water rituals",
            "Bharani": "binding and releasing spells",
            "Krittika": "fire ceremonies for purification",
            "Rohini": "prosperity and growth magic",
            "Mrigashira": "hunting and seeking rituals",
            "Ardra": "storm magic, destructive renewal",
            "Punarvasu": "restoration rituals, finding what was lost",
            "Pushya": "protective magic, blessing ceremonies",
            "Ashlesha": "serpent magic, hypnotic influence",
            "Magha": "ancestral connection rituals",
            "Purva Phalguni": "love and fertility magic",
            "Uttara Phalguni": "contract and oath binding",
            "Hasta": "hand magic, crafting talismans",
            "Chitra": "artistic creation, beauty spells",
            "Swati": "air magic, movement and change",
            "Vishakha": "determination rituals, goal magic",
            "Anuradha": "friendship bonds, loyalty magic",
            "Jyeshtha": "power accumulation, protective curses",
            "Mula": "root work, uncrossing rituals",
            "Purva Ashadha": "victory magic, strength spells",
            "Uttara Ashadha": "lasting success rituals",
            "Shravana": "sound magic, invocation chants",
            "Dhanishta": "prosperity drums, wealth attraction",
            "Shatabhisha": "healing baths, herb magic",
            "Purva Bhadrapada": "intense transformation fire",
            "Uttara Bhadrapada": "deep water mysteries",
            "Revati": "safe journey magic, completion rituals",
        }
        
        magic_type = nakshatra_magic.get(nakshatra, "elemental balancing")
        
        return (
            f"The Loa {loa_name} governs this placement, bringing {loa_qualities}. "
            f"In Voodoo tradition, this creates an energetic portal for {magic_type}. "
            f"The spirits favor offerings of rum, cigars, and red cloth during this time. "
            f"Work with {loa_name} through crossroads rituals at dawn or dusk for maximum effect."
        )
    
    # ========================================================================
    # MYSTICAL INTERPRETATIONS
    # ========================================================================
    
    def _mystical_interpretation(self, planet: str, nakshatra: str, 
                                pada: int, house: int) -> str:
        """Esoteric and mystical wisdom traditions."""
        # Mystical correspondences
        planet_mystical = {
            "Sun": "the Magician's will, creative fire of consciousness",
            "Moon": "the High Priestess's mysteries, subconscious waters",
            "Mercury": "Hermes' caduceus, bridge between worlds",
            "Venus": "the Empress's abundance, magnetic attraction",
            "Mars": "the Emperor's action, directed force",
            "Jupiter": "the Hierophant's wisdom, expansion of spirit",
            "Saturn": "the Hermit's solitude, karmic teacher",
            "Rahu": "the Devil's temptation, material illusion",
            "Ketu": "the Hanged Man's surrender, spiritual sacrifice",
        }
        
        mystical_essence = planet_mystical.get(planet, "transformative mystery")
        
        # Pada represents spiritual evolution stage
        pada_mystical = {
            1: "initiation phase - planting karmic seeds",
            2: "growth phase - nurturing spiritual understanding",
            3: "flowering phase - expressing divine wisdom",
            4: "harvest phase - reaping spiritual fruits",
        }
        
        pada_meaning = pada_mystical.get(pada, "evolutionary spiral")
        
        # House represents area of mystical work
        house_mystical = {
            1: "forging the conscious self", 2: "alchemizing material resources",
            3: "transmuting communication", 4: "anchoring soul roots",
            5: "creating divine play", 6: "purifying through service",
            7: "mirroring sacred partnership", 8: "diving into shadow work",
            9: "expanding cosmic consciousness", 10: "manifesting life's work",
            11: "connecting to collective mind", 12: "dissolving into unity"
        }
        
        house_work = house_mystical.get(house, "spiritual alchemy")
        
        return (
            f"Mystically, this placement represents {mystical_essence}. "
            f"You are in the {pada_meaning}, "
            f"working on {house_work}. "
            f"The esoteric lesson involves understanding how spirit descends into matter "
            f"through the {house}th house portal. Meditate on the union of opposites here."
        )
    
    # ========================================================================
    # LUNAR MANSION INTERPRETATIONS
    # ========================================================================
    
    def _lunar_mansion_interpretation(self, nakshatra: str, pada: int, 
                                     planet: str) -> str:
        """27/28 Lunar Mansions wisdom from multiple cultures."""
        # Each nakshatra corresponds to lunar mansion with specific timing wisdom
        mansion_wisdom = {
            "Ashwini": "Mansion of Healing - best for medical procedures, swift actions, starting new ventures. Avoid delays.",
            "Bharani": "Mansion of Restraint - time for patience, gestation, holding power. Avoid premature birth of ideas.",
            "Krittika": "Mansion of Fire - purify through heat, cut away dead wood, sharpen tools. Avoid burning bridges.",
            "Rohini": "Mansion of Growth - plant seeds, grow wealth, nurture relationships. Peak fertility time.",
            "Mrigashira": "Mansion of Searching - seek knowledge, explore, ask questions. Good for research and investigation.",
            "Ardra": "Mansion of Storm - expect disruption followed by clarity. Time to weather changes and emerge renewed.",
            "Punarvasu": "Mansion of Return - come home, restore what was lost, renew vows. Second chances bloom here.",
            "Pushya": "Mansion of Nourishment - most auspicious for all activities. Feed body, mind, spirit. Protection prevails.",
            "Ashlesha": "Mansion of Serpent - hidden power emerges, secrets revealed. Handle poison carefully. Occult knowledge available.",
            "Magha": "Mansion of Throne - honor ancestors, claim authority, perform ceremony. Royal dignity and responsibility.",
            "Purva Phalguni": "Mansion of Couch - rest, enjoyment, creative pleasures, romantic connections. Sweet surrender.",
            "Uttara Phalguni": "Mansion of Bed - partnerships solidify, contracts signed, friendships deepen. Commitment time.",
            "Hasta": "Mansion of Hand - craft, build, manifest through skill. Hands are blessed for healing and creating.",
            "Chitra": "Mansion of Pearl - create beauty, design brilliance, architect your life. Gem of perfection forms.",
            "Swati": "Mansion of Sword - independence blooms, commerce thrives, flexibility wins. Move with the wind.",
            "Vishakha": "Mansion of Arch - complete the bridge to your goal. Determination carries you across.",
            "Anuradha": "Mansion of Lotus - rise from mud to enlightenment. Friendship and devotion open all doors.",
            "Jyeshtha": "Mansion of Eldest - wisdom of experience, protective power, occult mastery. Guard well.",
            "Mula": "Mansion of Root - dig deep, investigate foundation, destroy illusion. Truth emerges from chaos.",
            "Purva Ashadha": "Mansion of Fan - invincible energy, early victory, purification. Unstoppable momentum.",
            "Uttara Ashadha": "Mansion of Elephant - unmovable virtue, lasting success, noble authority. Victory is permanent.",
            "Shravana": "Mansion of Ear - listen deeply, learn ancient wisdom, connect to universal sound. Knowledge flows.",
            "Dhanishta": "Mansion of Drum - wealth arrives through music of the spheres. Prosperity resonates.",
            "Shatabhisha": "Mansion of 100 Healers - healing power multiplied, secrets of medicine revealed. Solitary work favored.",
            "Purva Bhadrapada": "Mansion of Fire - intense transformation, burn away karma, funeral pyre wisdom. Phoenix rises.",
            "Uttara Bhadrapada": "Mansion of Twins - depth of ocean, kundalini awakening, cosmic foundation. Sacred serpent stirs.",
            "Revati": "Mansion of Drum - safe journey to the other shore. Completion, nourishment, divine protection.",
        }
        
        wisdom = mansion_wisdom.get(nakshatra, "Time of transformation and growth")
        
        return (
            f"{wisdom} "
            f"The {planet} activates this mansion's energy in pada {pada}, "
            f"marking {'initiation' if pada == 1 else 'development' if pada == 2 else 'expression' if pada == 3 else 'completion'}. "
            f"Work with lunar cycles and this mansion's timing for optimal results."
        )
    
    # ========================================================================
    # SYNTHESIS & RECOMMENDATIONS
    # ========================================================================
    
    def _synthesize_perspectives(self, vedic: str, western: str, voodoo: str,
                                 mystical: str, lunar: str, planet: str, 
                                 sign: str) -> str:
        """Weave all traditions into unified synthesis."""
        return (
            f"When we weave together all wisdom traditions, {planet} in {sign} "
            f"becomes a multidimensional portal of experience. "
            f"The Vedic tradition shows us the subtle energy patterns and karmic unfoldment. "
            f"Western psychology reveals the conscious and unconscious motivations. "
            f"The Voodoo Loa open spiritual gateways and offer their blessings. "
            f"Mystical traditions illuminate the soul's evolutionary purpose. "
            f"And the Lunar Mansions teach us the perfect timing for action. "
            f"Together, these create an infinitely rich tapestry of meaning that goes beyond "
            f"any single tradition's limitations. Your personal experience will be the synthesis "
            f"of all these energies working in concert."
        )
    
    def _generate_recommendations(self, vedic: str, western: str, voodoo: str,
                                 mystical: str, lunar: str) -> List[str]:
        """Generate actionable recommendations from all traditions."""
        return [
            "Vedic: Chant mantras for the planet during its hora (planetary hour)",
            "Western: Journal about how this energy manifests in your daily life",
            "Voodoo: Make offerings to the governing Loa at crossroads or altar",
            "Mystical: Meditate on the esoteric symbol during new moon",
            "Lunar: Work with this energy during the mansion's peak days",
            "Synthesis: Combine all practices for maximum spiritual alignment"
        ]
    
    def _generate_warnings(self, vedic: str, western: str, voodoo: str,
                          mystical: str) -> List[str]:
        """Generate warnings from combined wisdom."""
        return [
            "Avoid impulsive actions when the mansion is afflicted",
            "The Loa may test you before granting blessings - remain respectful",
            "Shadow work may surface - face it with courage and honesty",
            "Karmic patterns may repeat until lessons are learned"
        ]
    
    def _generate_opportunities(self, vedic: str, western: str, 
                               lunar: str) -> List[str]:
        """Generate opportunities from traditions."""
        return [
            "Mansion timing creates windows for manifestation",
            "Spiritual practices amplify during favorable periods",
            "Multiple traditions provide multiple paths to same goal",
            "Deep understanding comes from synthesis of perspectives"
        ]
    
    def _create_primary_message(self, planet: str, sign: str, house: int,
                               synthesis: str) -> str:
        """Create the main unified message."""
        return (
            f"{planet} in {sign}, {house}th house: "
            f"This placement is rich with meaning across all traditions. "
            f"{synthesis[:300]}..."
        )
    
    # ========================================================================
    # HELPER METHODS & DATA INITIALIZATION
    # ========================================================================
    
    def _house_area(self, house: int) -> str:
        """Get house area of life."""
        areas = {
            1: "self-identity and appearance",
            2: "values and resources",
            3: "communication and siblings",
            4: "home and roots",
            5: "creativity and children",
            6: "service and health",
            7: "partnerships and marriage",
            8: "transformation and shared resources",
            9: "philosophy and travel",
            10: "career and public life",
            11: "friendships and aspirations",
            12: "spirituality and isolation"
        }
        return areas.get(house, "life experience")
    
    def _sign_mode(self, sign: str) -> str:
        """Get sign modality."""
        modes = {
            "Aries": "cardinal fire - initiating",
            "Taurus": "fixed earth - stabilizing",
            "Gemini": "mutable air - adapting",
            "Cancer": "cardinal water - nurturing",
            "Leo": "fixed fire - radiating",
            "Virgo": "mutable earth - refining",
            "Libra": "cardinal air - harmonizing",
            "Scorpio": "fixed water - transforming",
            "Sagittarius": "mutable fire - exploring",
            "Capricorn": "cardinal earth - structuring",
            "Aquarius": "fixed air - revolutionizing",
            "Pisces": "mutable water - dissolving"
        }
        return modes.get(sign, "evolutionary")
    
    def _init_lunar_mansions(self) -> Dict:
        """Initialize lunar mansion data."""
        return {}  # Populated above in interpretation methods
    
    def _init_voodoo_loa(self) -> Dict:
        """Initialize Voodoo Loa correspondences."""
        return {}  # Populated above in interpretation methods
    
    def _init_mystical_symbols(self) -> Dict:
        """Initialize mystical symbol system."""
        return {}  # Populated above in interpretation methods
    
    def _init_planetary_synthesis(self) -> Dict:
        """Initialize planetary synthesis data."""
        return {}  # Populated above in interpretation methods
    
    # Placeholder methods for other interpretation types
    def _vedic_dasha_interpretation(self, maha: str, antar: Optional[str], data: Dict) -> str:
        return f"Vedic: {maha} Mahadasha period brings karmic unfoldment"
    
    def _western_progression_interpretation(self, planet: str, start: datetime, end: datetime) -> str:
        return f"Western: {planet} progression activates psychological growth"
    
    def _voodoo_period_interpretation(self, planet: str, start: datetime, data: Dict) -> str:
        return f"Voodoo: The Loa associated with {planet} govern this cycle"
    
    def _mystical_cycle_interpretation(self, planet: str, start: datetime, data: Dict) -> str:
        return f"Mystical: {planet} cycle represents soul evolution stage"
    
    def _lunar_timing_interpretation(self, start: datetime, end: datetime, planet: str) -> str:
        return f"Lunar: This period aligns with specific mansion energies"
    
    def _synthesize_period_perspectives(self, vedic: str, western: str, voodoo: str, 
                                       mystical: str, lunar: str, planet: str) -> str:
        return f"All traditions converge on {planet}'s time period significance"
    
    def _period_recommendations(self, vedic: str, voodoo: str, mystical: str) -> List[str]:
        return ["Work with period energies through ritual", "Honor the Loa"]
    
    def _period_warnings(self, vedic: str, western: str, voodoo: str) -> List[str]:
        return ["Be mindful of karmic lessons", "Respect spiritual forces"]
    
    def _period_opportunities(self, lunar: str, mystical: str, western: str) -> List[str]:
        return ["Mansion timing creates favorable windows", "Spiritual growth accelerates"]
    
    def _vedic_transit_interpretation(self, trans: str, natal: str, aspect: str) -> str:
        return f"Vedic: {trans} transiting {natal} creates gochara effects"
    
    def _western_aspect_interpretation(self, trans: str, natal: str, aspect: str) -> str:
        return f"Western: {aspect} aspect between {trans} and {natal}"
    
    def _voodoo_crossroads_interpretation(self, planet: str, date: datetime) -> str:
        return f"Voodoo: {planet} creates spiritual crossroads"
    
    def _mystical_portal_interpretation(self, planet: str, aspect: str, date: datetime) -> str:
        return f"Mystical: {planet} opens energetic portal"
    
    def _lunar_favorable_days(self, date: datetime, planet: str) -> str:
        return f"Lunar: Mansion alignment for {planet} transit"
    
    def _synthesize_transit_perspectives(self, vedic: str, western: str, voodoo: str,
                                        mystical: str, lunar: str, planet: str) -> str:
        return f"Transit of {planet} seen through all wisdom traditions"
    
    def _transit_recommendations(self, voodoo: str, lunar: str, mystical: str) -> List[str]:
        return ["Make offerings during transit", "Work with mansion timing"]
    
    def _transit_warnings(self, vedic: str, western: str, voodoo: str) -> List[str]:
        return ["Challenging aspects need spiritual work", "Respect crossroads energy"]
    
    def _transit_opportunities(self, lunar: str, western: str, mystical: str) -> List[str]:
        return ["Portal opening for manifestation", "Spiritual acceleration possible"]
    
    def _get_planet_from_chart(self, planet: str, chart: Dict) -> Dict:
        """Extract planet data from birth chart."""
        for p in chart.get('planet_positions', []):
            if p['planet'] == planet:
                return p
        return {}
