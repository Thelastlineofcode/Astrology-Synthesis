import os
from pathlib import Path

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', True)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3001,http://127.0.0.1:3001').split(',')
    EPHE_PATH = os.path.join(Path(__file__).parent, 'ephe')
    DEFAULT_HOUSE_SYSTEM = 'P'
    DEFAULT_AYANAMSA = 'LAHIRI'
    
    HOUSE_SYSTEMS = {
        'P': 'Placidus',
        'K': 'Koch',
        'W': 'Whole Sign',
        'E': 'Equal',
        'R': 'Regiomontanus',
        'C': 'Campanus',
        'T': 'Topocentric'
    }
    
    ASPECT_ORBS = {
        'conjunction': 8,
        'opposition': 8,
        'trine': 8,
        'square': 7,
        'sextile': 6,
        'quincunx': 3,
        'semisextile': 2,
        'semisquare': 2,
        'sesquisquare': 2,
        'quintile': 2,
        'biquintile': 2
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

