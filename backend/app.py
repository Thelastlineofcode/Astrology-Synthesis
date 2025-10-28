from flask import Flask
from flask_cors import CORS
from config import config
import swisseph as swe
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    ephe_path = app.config['EPHE_PATH']
    if not os.path.exists(ephe_path):
        os.makedirs(ephe_path)
        print(f"Created ephemeris directory at {ephe_path}")
        print("Please download Swiss Ephemeris data files from:")
        print("https://www.astro.com/ftp/swisseph/ephe/")
    swe.set_ephe_path(ephe_path)
    
    # Register main API routes
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register BMAD API routes
    from bmad.api.routes import bmad_bp
    app.register_blueprint(bmad_bp, url_prefix='/api/bmad')
    
    @app.route('/')
    def index():
        return {
            'message': 'Astrology Chart API with BMAD',
            'version': '1.0.0',
            'endpoints': {
                'calculate_chart': '/api/chart',
                'health': '/api/health',
                'bmad_personality': '/api/bmad/personality/analyze',
                'bmad_behavior': '/api/bmad/behavior/profile',
                'bmad_full_analysis': '/api/bmad/combined/full-analysis',
                'bmad_info': '/api/bmad/info/endpoints'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000)

