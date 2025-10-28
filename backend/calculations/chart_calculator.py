import swisseph as swe
from datetime import datetime
import os
from utils.constants import PLANETS, get_zodiac_sign, AYANAMSA_TYPES

class ChartCalculator:
    def __init__(self, zodiac_type='tropical', ayanamsa='LAHIRI'):
        self.zodiac_type = zodiac_type
        self.ayanamsa = ayanamsa
        
        # Set ephemeris files path
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ephe_path = os.path.join(current_dir, 'ephe')
        swe.set_ephe_path(ephe_path)
        
        if zodiac_type == 'sidereal':
            swe.set_sid_mode(AYANAMSA_TYPES.get(ayanamsa, swe.SIDM_LAHIRI))
    
    def calculate_julian_day(self, year, month, day, hour, minute, second=0):
        time_decimal = hour + minute/60 + second/3600
        jd = swe.julday(year, month, day, time_decimal)
        return jd
    
    def calculate_planetary_positions(self, jd):
        planetary_data = {}
        
        flag = swe.FLG_SWIEPH | swe.FLG_SPEED
        if self.zodiac_type == 'sidereal':
            flag |= swe.FLG_SIDEREAL
        
        for planet_name, planet_id in PLANETS.items():
            try:
                result, ret_flag = swe.calc_ut(jd, planet_id, flag)
                
                longitude = result[0]
                latitude = result[1]
                distance = result[2]
                speed = result[3]
                
                zodiac_info = get_zodiac_sign(longitude)
                
                planetary_data[planet_name] = {
                    'longitude': longitude,
                    'latitude': latitude,
                    'distance': distance,
                    'speed': speed,
                    'isRetrograde': speed < 0,
                    'zodiacSign': zodiac_info['sign'],
                    'degree': zodiac_info['degree'],
                    'minute': zodiac_info['minute'],
                    'second': zodiac_info['second']
                }
            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")
                planetary_data[planet_name] = None
        
        # Add South Node (Ketu) as 180° opposite North Node
        if 'NorthNode' in planetary_data and planetary_data['NorthNode'] is not None:
            nn = planetary_data['NorthNode']
            ketu_long = (nn['longitude'] + 180) % 360
            zodiac_info = get_zodiac_sign(ketu_long)
            planetary_data['SouthNode'] = {
                **nn,
                'longitude': ketu_long,
                'zodiacSign': zodiac_info['sign'],
                'degree': zodiac_info['degree'],
                'minute': zodiac_info['minute'],
                'second': zodiac_info['second']
            }

        return planetary_data
    
    def calculate_houses(self, jd, latitude, longitude, house_system='P'):
        flag = 0
        if self.zodiac_type == 'sidereal':
            flag = swe.FLG_SIDEREAL
        
        try:
            cusps, ascmc = swe.houses_ex(jd, latitude, longitude, 
                                         house_system.encode(), flag)
            
            houses_data = []
            for i, cusp in enumerate(cusps):
                zodiac_info = get_zodiac_sign(cusp)
                houses_data.append({
                    'house': i + 1,
                    'cusp': cusp,
                    'zodiacSign': zodiac_info['sign'],
                    'degree': zodiac_info['degree'],
                    'minute': zodiac_info['minute']
                })
            
            asc_info = get_zodiac_sign(ascmc[0])
            mc_info = get_zodiac_sign(ascmc[1])
            
            angles = {
                'ascendant': {
                    'longitude': ascmc[0],
                    'zodiacSign': asc_info['sign'],
                    'degree': asc_info['degree'],
                    'minute': asc_info['minute']
                },
                'midheaven': {
                    'longitude': ascmc[1],
                    'zodiacSign': mc_info['sign'],
                    'degree': mc_info['degree'],
                    'minute': mc_info['minute']
                }
            }
            
            return houses_data, angles
        
        except Exception as e:
            print(f"Error calculating houses: {e}")
            return [], {}
    
    def calculate_planet_houses(self, planet_positions, house_cusps, ascendant):
        planet_houses = {}
        
        for planet_name, planet_data in planet_positions.items():
            if planet_data is None:
                continue
            
            planet_long = planet_data['longitude']
            house_num = 1
            
            for i in range(12):
                next_cusp = house_cusps[(i + 1) % 12]['cusp']
                current_cusp = house_cusps[i]['cusp']
                
                if next_cusp < current_cusp:
                    if planet_long >= current_cusp or planet_long < next_cusp:
                        house_num = i + 1
                        break
                else:
                    if current_cusp <= planet_long < next_cusp:
                        house_num = i + 1
                        break
            
            planet_houses[planet_name] = house_num
        
        return planet_houses
    
    def generate_chart(self, birth_data):
        jd = self.calculate_julian_day(
            birth_data['year'],
            birth_data['month'],
            birth_data['day'],
            birth_data['hour'],
            birth_data['minute'],
            birth_data.get('second', 0)
        )
        
        planets = self.calculate_planetary_positions(jd)
        
        house_system = birth_data.get('house_system', 'P')
        houses, angles = self.calculate_houses(
            jd,
            birth_data['latitude'],
            birth_data['longitude'],
            house_system
        )
        
        planet_houses = self.calculate_planet_houses(planets, houses, angles['ascendant'])
        
        for planet_name in planets:
            if planets[planet_name]:
                planets[planet_name]['house'] = planet_houses.get(planet_name, 0)
        
        return {
            'planets': planets,
            'houses': houses,
            'angles': angles,
            'chartInfo': {
                'zodiacType': self.zodiac_type,
                'ayanamsa': self.ayanamsa if self.zodiac_type == 'sidereal' else None,
                'houseSystem': house_system,
                'julianDay': jd
            }
        }
