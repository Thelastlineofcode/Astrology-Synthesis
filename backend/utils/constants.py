import swisseph as swe

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'NorthNode': swe.TRUE_NODE,
    'SouthNode': swe.TRUE_NODE,  # Calculated as opposite of North Node
    'Chiron': swe.CHIRON
}

ZODIAC_SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

ZODIAC_SYMBOLS = {
    'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊',
    'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
    'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐',
    'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'
}

PLANET_SYMBOLS = {
    'Sun': '☉', 'Moon': '☽', 'Mercury': '☿', 'Venus': '♀',
    'Mars': '♂', 'Jupiter': '♃', 'Saturn': '♄', 'Uranus': '♅',
    'Neptune': '♆', 'Pluto': '♇', 'NorthNode': '☊', 'SouthNode': '☋', 'Chiron': '⚷'
}

AYANAMSA_TYPES = {
    'LAHIRI': swe.SIDM_LAHIRI,
    'KRISHNAMURTI': swe.SIDM_KRISHNAMURTI,
    'RAMAN': swe.SIDM_RAMAN,
    'FAGAN_BRADLEY': swe.SIDM_FAGAN_BRADLEY
}

ASPECTS = {
    'conjunction': 0,
    'opposition': 180,
    'trine': 120,
    'square': 90,
    'sextile': 60,
    'quincunx': 150,
    'semisextile': 30,
    'semisquare': 45,
    'sesquisquare': 135,
    'quintile': 72,
    'biquintile': 144
}

ASPECT_SYMBOLS = {
    'conjunction': '☌',
    'opposition': '☍',
    'trine': '△',
    'square': '□',
    'sextile': '⚹',
    'quincunx': '⚻',
    'semisextile': '⚺',
    'semisquare': '∠',
    'sesquisquare': '⚼',
    'quintile': 'Q',
    'biquintile': 'bQ'
}

def get_zodiac_sign(longitude):
    sign_num = int(longitude / 30)
    degree_in_sign = longitude % 30
    return {
        'sign': ZODIAC_SIGNS[sign_num],
        'sign_num': sign_num,
        'degree': int(degree_in_sign),
        'minute': int((degree_in_sign % 1) * 60),
        'second': int(((degree_in_sign % 1) * 60 % 1) * 60)
    }

