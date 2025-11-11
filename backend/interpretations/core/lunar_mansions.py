"""
Lunar Mansions (Nakshatras) Interpretation System
27 Lunar Mansions with esoteric and predictive meanings
"""

from typing import Dict, List, Optional
from datetime import datetime


class LunarMansionInterpreter:
    """Interprets planetary positions through Lunar Mansions (Nakshatras)."""
    
    # 27 Lunar Mansions with esoteric meanings
    MANSIONS = {
        "Ashwini": {
            "degrees": (0, 13.33),
            "deity": "Ashwini Kumaras (Twin Physicians)",
            "symbol": "Horse's Head",
            "essence": "Swift healing, new beginnings, sudden changes",
            "prediction_themes": ["rapid healing", "quick decisions", "fresh starts", "magical interventions"],
            "mystical_power": "Power to reach things quickly",
            "voodoo_aspect": "Speed magic, healing rituals, horse spirit work",
            "favorable_for": ["medical matters", "travel", "initiations", "emergency actions"],
        },
        "Bharani": {
            "degrees": (13.33, 26.66),
            "deity": "Yama (God of Death & Dharma)",
            "symbol": "Yoni (Womb)",
            "essence": "Restraint, transformation, carrying burdens",
            "prediction_themes": ["major transformations", "endings and beginnings", "moral decisions", "death and rebirth"],
            "mystical_power": "Power to take things away",
            "voodoo_aspect": "Death magic, transformation rituals, ancestor work",
            "favorable_for": ["letting go", "major life changes", "confronting truth", "purification"],
        },
        "Krittika": {
            "degrees": (26.66, 40.00),
            "deity": "Agni (Fire God)",
            "symbol": "Razor/Flame",
            "essence": "Cutting through illusion, purification by fire",
            "prediction_themes": ["sharp insights", "burning away old patterns", "fierce protection", "clarity"],
            "mystical_power": "Power to burn",
            "voodoo_aspect": "Fire magic, candle work, protection spells",
            "favorable_for": ["cutting ties", "protection", "clarity", "purification rituals"],
        },
        "Rohini": {
            "degrees": (40.00, 53.33),
            "deity": "Brahma (Creator)",
            "symbol": "Chariot/Ox Cart",
            "essence": "Growth, fertility, abundance, beauty",
            "prediction_themes": ["manifestation", "material success", "fertility", "creative projects"],
            "mystical_power": "Power to grow",
            "voodoo_aspect": "Abundance magic, fertility spells, beauty work",
            "favorable_for": ["starting businesses", "relationships", "creative endeavors", "prosperity"],
        },
        "Mrigashira": {
            "degrees": (53.33, 66.66),
            "deity": "Soma (Moon God)",
            "symbol": "Deer's Head",
            "essence": "Searching, curiosity, gentle pursuit",
            "prediction_themes": ["seeking truth", "gentle approaches", "exploration", "romantic pursuit"],
            "mystical_power": "Power to give fulfillment",
            "voodoo_aspect": "Love magic, attraction spells, seeking rituals",
            "favorable_for": ["research", "romance", "spiritual seeking", "travel"],
        },
        "Ardra": {
            "degrees": (66.66, 80.00),
            "deity": "Rudra (Storm God)",
            "symbol": "Teardrop/Diamond",
            "essence": "Storms, upheaval, breakthrough",
            "prediction_themes": ["emotional releases", "major breakthroughs", "destruction before creation", "intensity"],
            "mystical_power": "Power of effort and destruction",
            "voodoo_aspect": "Storm magic, cleansing rituals, breaking curses",
            "favorable_for": ["major changes", "emotional healing", "breaking patterns", "transformation"],
        },
        "Punarvasu": {
            "degrees": (80.00, 93.33),
            "deity": "Aditi (Mother of Gods)",
            "symbol": "Bow and Quiver",
            "essence": "Return to light, renewal, restoration",
            "prediction_themes": ["recovery", "second chances", "return of what was lost", "restoration"],
            "mystical_power": "Power to gain wealth and substance",
            "voodoo_aspect": "Return magic, restoration spells, home protection",
            "favorable_for": ["recovery", "reunions", "rebuilding", "finding lost things"],
        },
        "Pushya": {
            "degrees": (93.33, 106.66),
            "deity": "Brihaspati (Jupiter)",
            "symbol": "Cow's Udder/Lotus",
            "essence": "Nourishment, spirituality, protection",
            "prediction_themes": ["spiritual growth", "protection", "nourishment", "blessings"],
            "mystical_power": "Power to create spiritual energy",
            "voodoo_aspect": "Blessing magic, protection work, spiritual elevation",
            "favorable_for": ["spiritual practices", "starting important ventures", "protection", "teaching"],
        },
        "Ashlesha": {
            "degrees": (106.66, 120.00),
            "deity": "Nagas (Serpent Deities)",
            "symbol": "Coiled Serpent",
            "essence": "Kundalini power, occult knowledge, poison/medicine",
            "prediction_themes": ["hidden knowledge", "occult power", "manipulation", "healing or harming"],
            "mystical_power": "Power over poisons",
            "voodoo_aspect": "Serpent magic, binding spells, occult work, hex/unhex",
            "favorable_for": ["occult studies", "confronting enemies", "deep healing", "tantric practices"],
        },
        "Magha": {
            "degrees": (120.00, 133.33),
            "deity": "Pitris (Ancestors)",
            "symbol": "Royal Throne",
            "essence": "Authority, tradition, ancestral power",
            "prediction_themes": ["ancestral blessings", "authority", "tradition", "royal power"],
            "mystical_power": "Power to leave the body",
            "voodoo_aspect": "Ancestor work, throne magic, authority spells",
            "favorable_for": ["honoring ancestors", "leadership", "traditional ceremonies", "inheritance"],
        },
        "Purva Phalguni": {
            "degrees": (133.33, 146.66),
            "deity": "Bhaga (God of Delight)",
            "symbol": "Front Legs of Bed/Hammock",
            "essence": "Pleasure, creativity, procreation",
            "prediction_themes": ["romance", "pleasure", "artistic success", "fertility"],
            "mystical_power": "Power of procreation",
            "voodoo_aspect": "Love magic, pleasure spells, fertility work",
            "favorable_for": ["romance", "arts", "entertainment", "marriage"],
        },
        "Uttara Phalguni": {
            "degrees": (146.66, 160.00),
            "deity": "Aryaman (God of Contracts)",
            "symbol": "Back Legs of Bed",
            "essence": "Partnerships, contracts, permanence",
            "prediction_themes": ["partnerships", "contracts", "lasting commitments", "stability"],
            "mystical_power": "Power of prosperity through marriage",
            "voodoo_aspect": "Binding magic, contract work, commitment spells",
            "favorable_for": ["partnerships", "contracts", "marriage", "long-term commitments"],
        },
        "Hasta": {
            "degrees": (160.00, 173.33),
            "deity": "Savitar (Sun God)",
            "symbol": "Hand/Fist",
            "essence": "Skill, craftsmanship, manifestation",
            "prediction_themes": ["skill mastery", "craftsmanship", "healing hands", "manifestation"],
            "mystical_power": "Power to manifest what you seek",
            "voodoo_aspect": "Hand magic, crafting spells, manifestation work",
            "favorable_for": ["skilled work", "healing", "crafting", "business transactions"],
        },
        "Chitra": {
            "degrees": (173.33, 186.66),
            "deity": "Tvashtar (Divine Architect)",
            "symbol": "Bright Jewel/Pearl",
            "essence": "Brilliance, beauty, architecture",
            "prediction_themes": ["creative brilliance", "beauty", "architecture", "shining forth"],
            "mystical_power": "Power to accumulate merit",
            "voodoo_aspect": "Beauty magic, glamour spells, creative inspiration",
            "favorable_for": ["design", "architecture", "beauty treatments", "creative projects"],
        },
        "Swati": {
            "degrees": (186.66, 200.00),
            "deity": "Vayu (Wind God)",
            "symbol": "Coral/Sword Blowing in Wind",
            "essence": "Independence, flexibility, dispersal",
            "prediction_themes": ["independence", "freedom", "flexibility", "scattered energies"],
            "mystical_power": "Power to scatter like the wind",
            "voodoo_aspect": "Wind magic, freedom spells, dispersal work",
            "favorable_for": ["independence", "business", "social connections", "adaptability"],
        },
        "Vishakha": {
            "degrees": (200.00, 213.33),
            "deity": "Indra-Agni (Gods of Power)",
            "symbol": "Triumphal Archway",
            "essence": "Goal achievement, determination, fork in road",
            "prediction_themes": ["achieving goals", "important decisions", "power struggles", "victory"],
            "mystical_power": "Power to achieve results",
            "voodoo_aspect": "Victory magic, power spells, achievement work",
            "favorable_for": ["achieving goals", "competitions", "important decisions", "victory"],
        },
        "Anuradha": {
            "degrees": (213.33, 226.66),
            "deity": "Mitra (God of Friendship)",
            "symbol": "Lotus Flower",
            "essence": "Friendship, devotion, success through cooperation",
            "prediction_themes": ["friendships", "devotion", "group work", "spiritual discipline"],
            "mystical_power": "Power of worship",
            "voodoo_aspect": "Friendship magic, devotional work, group bonding",
            "favorable_for": ["friendships", "devotion", "group activities", "spiritual practices"],
        },
        "Jyeshtha": {
            "degrees": (226.66, 240.00),
            "deity": "Indra (King of Gods)",
            "symbol": "Circular Amulet/Earring",
            "essence": "Seniority, protection, occult power",
            "prediction_themes": ["seniority", "authority", "protection", "occult mastery"],
            "mystical_power": "Power over courage in battle",
            "voodoo_aspect": "Protection magic, authority spells, occult power",
            "favorable_for": ["leadership", "protection", "occult work", "gaining authority"],
        },
        "Mula": {
            "degrees": (240.00, 253.33),
            "deity": "Nirriti (Goddess of Destruction)",
            "symbol": "Tied Roots/Lion's Tail",
            "essence": "Root causes, investigation, destruction of foundations",
            "prediction_themes": ["getting to root causes", "destroying foundations", "deep investigation", "transformation"],
            "mystical_power": "Power to destroy",
            "voodoo_aspect": "Root work, destruction magic, breaking curses, deep cleansing",
            "favorable_for": ["investigation", "destroying obstacles", "root cause analysis", "deep transformation"],
        },
        "Purva Ashadha": {
            "degrees": (253.33, 266.66),
            "deity": "Apas (Water Goddess)",
            "symbol": "Elephant's Tusk/Fan",
            "essence": "Invincibility, purification, victory",
            "prediction_themes": ["invincibility", "early success", "purification", "victory"],
            "mystical_power": "Power to invigorate",
            "voodoo_aspect": "Victory magic, purification rituals, invincibility spells",
            "favorable_for": ["competitions", "purification", "gaining momentum", "victory"],
        },
        "Uttara Ashadha": {
            "degrees": (266.66, 280.00),
            "deity": "Vishvadevas (Universal Gods)",
            "symbol": "Elephant's Tusk",
            "essence": "Final victory, enduring achievement, universal support",
            "prediction_themes": ["lasting victory", "final achievement", "universal support", "permanence"],
            "mystical_power": "Power to grant permanent victory",
            "voodoo_aspect": "Permanent success magic, universal blessing, enduring spells",
            "favorable_for": ["final victory", "lasting achievements", "permanent changes", "major milestones"],
        },
        "Shravana": {
            "degrees": (280.00, 293.33),
            "deity": "Vishnu (The Preserver)",
            "symbol": "Ear/Three Footprints",
            "essence": "Listening, learning, connection",
            "prediction_themes": ["learning", "listening", "making connections", "preserving knowledge"],
            "mystical_power": "Power to connect people",
            "voodoo_aspect": "Communication magic, connection spells, learning enhancement",
            "favorable_for": ["learning", "communication", "networking", "preserving traditions"],
        },
        "Dhanishtha": {
            "degrees": (293.33, 306.66),
            "deity": "Eight Vasus (Gods of Elements)",
            "symbol": "Drum/Flute",
            "essence": "Wealth, music, fame, adaptability",
            "prediction_themes": ["wealth", "fame", "music", "recognition"],
            "mystical_power": "Power to give abundance",
            "voodoo_aspect": "Wealth magic, fame spells, music rituals",
            "favorable_for": ["wealth", "music", "fame", "group activities"],
        },
        "Shatabhisha": {
            "degrees": (306.66, 320.00),
            "deity": "Varuna (God of Cosmic Waters)",
            "symbol": "Empty Circle/1000 Flowers",
            "essence": "Healing, mysticism, concealment, secrets",
            "prediction_themes": ["healing", "mysticism", "secrets", "hidden knowledge"],
            "mystical_power": "Power of healing",
            "voodoo_aspect": "Healing magic, secret work, mystical practices, water rituals",
            "favorable_for": ["healing", "mystical practices", "secrets", "alternative medicine"],
        },
        "Purva Bhadrapada": {
            "degrees": (320.00, 333.33),
            "deity": "Aja Ekapada (One-footed Goat)",
            "symbol": "Front Legs of Funeral Cot/Two-faced Man",
            "essence": "Transformation, mysticism, passion, duality",
            "prediction_themes": ["transformation", "intense experiences", "mysticism", "duality"],
            "mystical_power": "Power to raise spiritual fire",
            "voodoo_aspect": "Transformation magic, fire rituals, mystical elevation",
            "favorable_for": ["transformation", "mystical practices", "intense work", "spiritual elevation"],
        },
        "Uttara Bhadrapada": {
            "degrees": (333.33, 346.66),
            "deity": "Ahir Budhnya (Serpent of the Deep)",
            "symbol": "Back Legs of Funeral Cot/Twin",
            "essence": "Depth, patience, kundalini power, wisdom",
            "prediction_themes": ["deep wisdom", "patience", "kundalini awakening", "depth"],
            "mystical_power": "Power to bring rain",
            "voodoo_aspect": "Deep magic, serpent work, kundalini activation, rain rituals",
            "favorable_for": ["deep work", "patience required", "spiritual practices", "depth analysis"],
        },
        "Revati": {
            "degrees": (346.66, 360.00),
            "deity": "Pushan (Nourisher)",
            "symbol": "Fish/Drum",
            "essence": "Nourishment, completion, safe journey",
            "prediction_themes": ["completion", "safe travels", "nourishment", "endings that lead to beginnings"],
            "mystical_power": "Power to nourish and protect",
            "voodoo_aspect": "Journey magic, protection spells, completion rituals, nourishment work",
            "favorable_for": ["completion", "travel", "nourishment", "safe passage"],
        },
    }
    
    def get_mansion_from_longitude(self, longitude: float) -> str:
        """Get the lunar mansion (nakshatra) for a given longitude."""
        # Normalize longitude to 0-360
        normalized = longitude % 360
        
        for mansion_name, data in self.MANSIONS.items():
            min_deg, max_deg = data["degrees"]
            if min_deg <= normalized < max_deg:
                return mansion_name
        
        return "Revati"  # Last mansion as default
    
    def get_interpretation(self, planet: str, longitude: float, context: str = "general") -> Dict:
        """
        Get lunar mansion interpretation for a planet.
        
        Args:
            planet: Planet name
            longitude: Ecliptic longitude
            context: Context for interpretation (general, transit, natal, etc.)
        
        Returns:
            Dict with interpretation data
        """
        mansion_name = self.get_mansion_from_longitude(longitude)
        mansion_data = self.MANSIONS[mansion_name]
        
        return {
            "mansion": mansion_name,
            "deity": mansion_data["deity"],
            "symbol": mansion_data["symbol"],
            "essence": mansion_data["essence"],
            "planet": planet,
            "longitude": longitude,
            "prediction_themes": mansion_data["prediction_themes"],
            "mystical_power": mansion_data["mystical_power"],
            "voodoo_aspect": mansion_data["voodoo_aspect"],
            "favorable_for": mansion_data["favorable_for"],
            "synthesis": self._synthesize_planet_mansion(planet, mansion_name, mansion_data, context),
        }
    
    def _synthesize_planet_mansion(self, planet: str, mansion: str, data: Dict, context: str) -> str:
        """Create a synthesized interpretation combining planet and mansion."""
        planet_essences = {
            "Sun": "soul, authority, vitality",
            "Moon": "mind, emotions, intuition",
            "Mars": "action, courage, conflict",
            "Mercury": "intellect, communication, skill",
            "Jupiter": "wisdom, expansion, fortune",
            "Venus": "love, beauty, pleasure",
            "Saturn": "discipline, limitation, karma",
            "Rahu": "obsession, foreign influences, unconventional paths",
            "Ketu": "liberation, spirituality, past life influences",
        }
        
        planet_essence = planet_essences.get(planet, "energy")
        
        if context == "transit":
            return (f"{planet}'s {planet_essence} activates {mansion}'s power of "
                   f"{data['essence']}. {data['mystical_power']} becomes available. "
                   f"Voodoo aspect: {data['voodoo_aspect']}. "
                   f"This period favors: {', '.join(data['favorable_for'][:2])}.")
        elif context == "natal":
            return (f"Your {planet} in {mansion} mansion gives you innate ability to work with "
                   f"{data['essence']}. The {data['deity']} blesses you with {data['mystical_power']}. "
                   f"Your natural magical affinity is {data['voodoo_aspect']}.")
        else:
            return (f"{planet} in {mansion} mansion (governed by {data['deity']}) brings "
                   f"themes of {data['essence']}. {data['mystical_power']} is highlighted. "
                   f"Mystical work with {data['voodoo_aspect']} is especially potent.")
