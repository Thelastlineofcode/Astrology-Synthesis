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
    
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {
            'message': 'Astrology Chart API',
            'version': '1.0.0',
            'endpoints': {
                'calculate_chart': '/api/chart',
                'health': '/api/health'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000)

