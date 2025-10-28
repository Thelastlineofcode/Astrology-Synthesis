from utils.constants import ASPECTS, ASPECT_SYMBOLS

class AspectCalculator:
    def __init__(self, orbs=None):
        self.default_orbs = {
            'conjunction': 8, 'opposition': 8, 'trine': 8,
            'square': 7, 'sextile': 6, 'quincunx': 3,
            'semisextile': 2, 'semisquare': 2, 'sesquisquare': 2,
            'quintile': 2, 'biquintile': 2
        }
        self.orbs = orbs if orbs else self.default_orbs
    
    def calculate_angle_between(self, long1, long2):
        diff = abs(long1 - long2)
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def find_aspect(self, angle):
        for aspect_name, aspect_angle in ASPECTS.items():
            orb = self.orbs.get(aspect_name, 5)
            if abs(angle - aspect_angle) <= orb:
                return aspect_name, abs(angle - aspect_angle)
        return None, None
    
    def calculate_aspects(self, planet_positions, include_minor=True):
        aspects_list = []
        planet_names = list(planet_positions.keys())
        
        for i, planet1 in enumerate(planet_names):
            for planet2 in planet_names[i+1:]:
                if planet_positions[planet1] is None or planet_positions[planet2] is None:
                    continue
                
                long1 = planet_positions[planet1]['longitude']
                long2 = planet_positions[planet2]['longitude']
                
                angle = self.calculate_angle_between(long1, long2)
                
                if abs(angle - 180) <= self.orbs.get('opposition', 8):
                    aspect_name = 'opposition'
                    orb = abs(angle - 180)
                else:
                    aspect_name, orb = self.find_aspect(angle)
                
                if aspect_name:
                    minor_aspects = ['semisextile', 'semisquare', 'sesquisquare', 
                                   'quintile', 'biquintile', 'quincunx']
                    if not include_minor and aspect_name in minor_aspects:
                        continue
                    
                    speed1 = planet_positions[planet1].get('speed', 0)
                    speed2 = planet_positions[planet2].get('speed', 0)
                    is_applying = self._is_applying(long1, long2, speed1, speed2)
                    
                    aspects_list.append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'aspect': aspect_name,
                        'angle': ASPECTS[aspect_name],
                        'orb': round(orb, 2),
                        'isApplying': is_applying,
                        'symbol': ASPECT_SYMBOLS.get(aspect_name, '')
                    })
        
        return aspects_list
    
    def _is_applying(self, long1, long2, speed1, speed2):
        relative_speed = speed1 - speed2
        angle_diff = long2 - long1
        
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        return (relative_speed * angle_diff) < 0
