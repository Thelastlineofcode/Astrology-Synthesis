#!/usr/bin/env python3
"""
Simple BMAD-only Flask Server
Standalone server that only runs BMAD endpoints without dependencies on chart calculation.
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def create_bmad_app():
    """Create Flask app with only BMAD endpoints."""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    @app.route('/')
    def index():
        return {
            'message': 'BMAD API Server',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'personality_analysis': '/api/bmad/personality/analyze',
                'behavior_profile': '/api/bmad/behavior/profile',
                'full_analysis': '/api/bmad/combined/full-analysis',
                'info': '/api/bmad/info/endpoints'
            }
        }
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'BMAD API',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/bmad/personality/analyze', methods=['POST'])
    def analyze_personality():
        """Analyze personality from chart data."""
        try:
            from bmad.services.personality_analyzer import PersonalityAnalyzer
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            chart_data = data.get('chart_data')
            birth_data = data.get('birth_data')
            profile_name = data.get('profile_name', 'Analysis Subject')
            
            if not chart_data:
                return jsonify({'error': 'chart_data is required'}), 400
            if not birth_data:
                return jsonify({'error': 'birth_data is required'}), 400
            
            analyzer = PersonalityAnalyzer()
            personality_profile = analyzer.analyze_personality(chart_data, birth_data, profile_name)
            
            return jsonify({
                'success': True,
                'personality_profile': personality_profile.to_dict()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/behavior/profile', methods=['POST'])
    def create_behavior_profile():
        """Create behavioral profile from chart data."""
        try:
            from bmad.services.behavior_predictor import BehaviorPredictor
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            chart_data = data.get('chart_data')
            birth_data = data.get('birth_data')
            person_name = data.get('person_name', 'Analysis Subject')
            
            if not chart_data:
                return jsonify({'error': 'chart_data is required'}), 400
            if not birth_data:
                return jsonify({'error': 'birth_data is required'}), 400
            
            predictor = BehaviorPredictor()
            behavior_profile = predictor.create_behavior_profile(chart_data, birth_data, person_name)
            
            return jsonify({
                'success': True,
                'behavior_profile': behavior_profile.to_dict()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/combined/full-analysis', methods=['POST'])
    def full_analysis():
        """Perform complete BMAD analysis."""
        try:
            from bmad.services.personality_analyzer import PersonalityAnalyzer
            from bmad.services.behavior_predictor import BehaviorPredictor
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            chart_data = data.get('chart_data')
            birth_data = data.get('birth_data')
            person_name = data.get('person_name', 'Analysis Subject')
            options = data.get('analysis_options', {})
            
            if not chart_data:
                return jsonify({'error': 'chart_data is required'}), 400
            if not birth_data:
                return jsonify({'error': 'birth_data is required'}), 400
            
            # Personality analysis
            personality_analyzer = PersonalityAnalyzer()
            personality_profile = personality_analyzer.analyze_personality(chart_data, birth_data, person_name)
            
            # Behavioral analysis
            behavior_predictor = BehaviorPredictor()
            behavior_profile = behavior_predictor.create_behavior_profile(chart_data, birth_data, person_name)
            
            result = {
                'success': True,
                'metadata': {
                    'person_name': person_name,
                    'analysis_date': datetime.now().isoformat(),
                    'analysis_timestamp': datetime.now().isoformat()
                },
                'personality_profile': personality_profile.to_dict(),
                'behavior_profile': behavior_profile.to_dict()
            }
            
            # Add predictions if requested
            if options.get('include_predictions', False):
                from datetime import timedelta
                prediction_months = options.get('prediction_months', 3)
                predictions = []
                
                current_date = datetime.now()
                
                for month in range(1, prediction_months + 1):
                    future_date = current_date + timedelta(days=30 * month)
                    month_predictions = behavior_predictor.predict_behavior_for_date(
                        behavior_profile, future_date.date().isoformat()
                    )
                    predictions.extend(month_predictions)
                
                result['future_predictions'] = [pred.to_dict() for pred in predictions]
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/symbolon/cards', methods=['GET'])
    def get_symbolon_cards():
        """Get all available Symbolon cards."""
        try:
            from bmad.services.symbolon_analyzer import SymbolonAnalyzer
            
            analyzer = SymbolonAnalyzer()
            cards_data = [card.to_dict() for card in analyzer.cards]
            
            return jsonify({
                'total_cards': len(cards_data),
                'cards': cards_data
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/symbolon/analyze', methods=['POST'])
    def analyze_symbolon():
        """Perform Symbolon card analysis on a chart."""
        try:
            from bmad.services.symbolon_analyzer import SymbolonAnalyzer
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            chart_data = data.get('chart_data')
            birth_data = data.get('birth_data')
            
            if not chart_data:
                return jsonify({'error': 'chart_data is required'}), 400
            if not birth_data:
                return jsonify({'error': 'birth_data is required'}), 400
            
            analyzer = SymbolonAnalyzer()
            symbolon_reading = analyzer.analyze_chart(chart_data, birth_data)
            
            return jsonify({
                'success': True,
                'symbolon_reading': symbolon_reading.to_dict(),
                'analysis_timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/symbolon/cards/<int:card_id>', methods=['GET'])
    def get_symbolon_card(card_id):
        """Get details for a specific Symbolon card."""
        try:
            from bmad.services.symbolon_analyzer import SymbolonAnalyzer
            
            analyzer = SymbolonAnalyzer()
            card = analyzer.card_lookup.get(card_id)
            
            if not card:
                return jsonify({'error': f'Card {card_id} not found'}), 404
            
            return jsonify({
                'card': card.to_dict()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/symbolon/cards/planet/<planet>', methods=['GET'])
    def get_cards_by_planet(planet):
        """Get all Symbolon cards associated with a planet."""
        try:
            from bmad.services.symbolon_analyzer import SymbolonAnalyzer
            
            analyzer = SymbolonAnalyzer()
            cards = analyzer.get_cards_by_planet(planet)
            
            return jsonify({
                'planet': planet,
                'total_cards': len(cards),
                'cards': [card.to_dict() for card in cards]
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/symbolon/cards/sign/<sign>', methods=['GET'])
    def get_cards_by_sign(sign):
        """Get all Symbolon cards associated with a sign."""
        try:
            from bmad.services.symbolon_analyzer import SymbolonAnalyzer
            
            analyzer = SymbolonAnalyzer()
            cards = analyzer.get_cards_by_sign(sign)
            
            return jsonify({
                'sign': sign,
                'total_cards': len(cards),
                'cards': [card.to_dict() for card in cards]
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bmad/info/endpoints', methods=['GET'])
    def get_endpoints():
        """Get available BMAD endpoints."""
        return jsonify({
            'bmad_endpoints': {
                'personality_analysis': {
                    'url': '/api/bmad/personality/analyze',
                    'method': 'POST',
                    'description': 'Analyze personality traits from chart data'
                },
                'behavior_profile': {
                    'url': '/api/bmad/behavior/profile', 
                    'method': 'POST',
                    'description': 'Create behavioral profile from chart data'
                },
                'full_analysis': {
                    'url': '/api/bmad/combined/full-analysis',
                    'method': 'POST', 
                    'description': 'Complete personality and behavioral analysis'
                },
                'symbolon_cards': {
                    'url': '/api/bmad/symbolon/cards',
                    'method': 'GET',
                    'description': 'Get all Symbolon cards'
                },
                'symbolon_analysis': {
                    'url': '/api/bmad/symbolon/analyze',
                    'method': 'POST',
                    'description': 'Perform Symbolon archetypal analysis'
                },
                'symbolon_card_detail': {
                    'url': '/api/bmad/symbolon/cards/{card_id}',
                    'method': 'GET',
                    'description': 'Get specific Symbolon card details'
                },
                'symbolon_by_planet': {
                    'url': '/api/bmad/symbolon/cards/planet/{planet}',
                    'method': 'GET',
                    'description': 'Get Symbolon cards for a planet'
                },
                'symbolon_by_sign': {
                    'url': '/api/bmad/symbolon/cards/sign/{sign}',
                    'method': 'GET',
                    'description': 'Get Symbolon cards for a sign'
                },
                'health_check': {
                    'url': '/api/health',
                    'method': 'GET',
                    'description': 'Server health status'
                }
            }
        })
    
    return app

if __name__ == '__main__':
    print("🚀 Starting BMAD API Server...")
    print("=" * 40)
    print("Server will be available at: http://localhost:5001")
    print("API endpoints:")
    print("  • Health: GET /api/health")
    print("  • Personality: POST /api/bmad/personality/analyze")
    print("  • Behavior: POST /api/bmad/behavior/profile")
    print("  • Full Analysis: POST /api/bmad/combined/full-analysis")
    print("=" * 40)
    
    app = create_bmad_app()
    app.run(host='0.0.0.0', port=5001, debug=True)