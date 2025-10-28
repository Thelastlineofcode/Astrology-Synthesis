"""
BMAD API Routes
REST API endpoints for Behavioral Model and Data analysis.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback

from ..services.personality_analyzer import PersonalityAnalyzer
from ..services.behavior_predictor import BehaviorPredictor
from ..models.behavior import BehaviorCategory
from ..models.personality import PersonalityDimension

# Create Blueprint for BMAD API
bmad_bp = Blueprint('bmad', __name__)

# Initialize services
personality_analyzer = PersonalityAnalyzer()
behavior_predictor = BehaviorPredictor()


@bmad_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for BMAD services."""
    return jsonify({
        'status': 'healthy',
        'service': 'BMAD API',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@bmad_bp.route('/personality/analyze', methods=['POST'])
def analyze_personality():
    """
    Analyze personality from chart data.
    
    Expected payload:
    {
        "chart_data": {...},  # Calculated chart data
        "birth_data": {...},  # Birth information
        "profile_name": "Optional Name"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_data = data.get('chart_data')
        birth_data = data.get('birth_data')
        profile_name = data.get('profile_name')
        
        if not chart_data:
            return jsonify({'error': 'chart_data is required'}), 400
        
        if not birth_data:
            return jsonify({'error': 'birth_data is required'}), 400
        
        # Analyze personality
        personality_profile = personality_analyzer.analyze_personality(
            chart_data, birth_data, profile_name
        )
        
        return jsonify({
            'success': True,
            'personality_profile': personality_profile.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Personality analysis failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/personality/compatibility', methods=['POST'])
def analyze_compatibility():
    """
    Analyze compatibility between two personality profiles.
    
    Expected payload:
    {
        "profile1": {...},  # First personality profile data
        "profile2": {...}   # Second personality profile data
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        profile1_data = data.get('profile1')
        profile2_data = data.get('profile2')
        
        if not profile1_data or not profile2_data:
            return jsonify({'error': 'Both profile1 and profile2 are required'}), 400
        
        # Convert dict data back to PersonalityProfile objects
        # This is simplified - in a real application, you'd have proper serialization
        
        return jsonify({
            'error': 'Compatibility analysis requires pre-existing personality profiles',
            'note': 'Please analyze individual personalities first, then use their profile IDs'
        }), 400
        
    except Exception as e:
        return jsonify({
            'error': f'Compatibility analysis failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/behavior/profile', methods=['POST'])
def create_behavior_profile():
    """
    Create a behavioral profile from chart data.
    
    Expected payload:
    {
        "chart_data": {...},  # Calculated chart data
        "birth_data": {...},  # Birth information
        "person_name": "Optional Name"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_data = data.get('chart_data')
        birth_data = data.get('birth_data')
        person_name = data.get('person_name')
        
        if not chart_data:
            return jsonify({'error': 'chart_data is required'}), 400
        
        if not birth_data:
            return jsonify({'error': 'birth_data is required'}), 400
        
        # Create behavioral profile
        behavior_profile = behavior_predictor.create_behavior_profile(
            chart_data, birth_data, person_name
        )
        
        return jsonify({
            'success': True,
            'behavior_profile': behavior_profile.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Behavior profile creation failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/behavior/predict', methods=['POST'])
def predict_behavior():
    """
    Predict behavior for a specific date.
    
    Expected payload:
    {
        "chart_data": {...},      # Chart data for analysis
        "birth_data": {...},      # Birth information
        "target_date": "2024-01-15",  # Date to predict for
        "categories": ["social", "professional"]  # Optional: specific categories
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_data = data.get('chart_data')
        birth_data = data.get('birth_data')
        target_date = data.get('target_date')
        categories = data.get('categories', [])
        
        if not chart_data:
            return jsonify({'error': 'chart_data is required'}), 400
        
        if not birth_data:
            return jsonify({'error': 'birth_data is required'}), 400
        
        if not target_date:
            return jsonify({'error': 'target_date is required'}), 400
        
        # Validate target date format
        try:
            datetime.fromisoformat(target_date)
        except ValueError:
            return jsonify({'error': 'target_date must be in ISO format (YYYY-MM-DD)'}), 400
        
        # Convert category strings to enums
        behavior_categories = []
        if categories:
            try:
                behavior_categories = [BehaviorCategory(cat) for cat in categories]
            except ValueError as e:
                return jsonify({'error': f'Invalid category: {str(e)}'}), 400
        
        # Create a temporary behavior profile for prediction
        temp_profile = behavior_predictor.create_behavior_profile(
            chart_data, birth_data, "Temp Profile"
        )
        
        # Generate predictions
        predictions = behavior_predictor.predict_behavior_for_date(
            temp_profile, target_date, behavior_categories or None
        )
        
        return jsonify({
            'success': True,
            'target_date': target_date,
            'predictions': [pred.to_dict() for pred in predictions]
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Behavior prediction failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/behavior/evolution', methods=['POST'])
def analyze_evolution():
    """
    Analyze behavioral evolution over a time period.
    
    Expected payload:
    {
        "chart_data": {...},       # Chart data for analysis
        "birth_data": {...},       # Birth information
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_data = data.get('chart_data')
        birth_data = data.get('birth_data')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not all([chart_data, birth_data, start_date, end_date]):
            return jsonify({'error': 'chart_data, birth_data, start_date, and end_date are required'}), 400
        
        # Validate date formats
        try:
            datetime.fromisoformat(start_date)
            datetime.fromisoformat(end_date)
        except ValueError:
            return jsonify({'error': 'Dates must be in ISO format (YYYY-MM-DD)'}), 400
        
        # Create a temporary behavior profile
        temp_profile = behavior_predictor.create_behavior_profile(
            chart_data, birth_data, "Evolution Analysis"
        )
        
        # Analyze evolution
        evolutions = behavior_predictor.analyze_behavior_evolution(
            temp_profile, start_date, end_date
        )
        
        return jsonify({
            'success': True,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'evolutions': [evo.to_dict() for evo in evolutions]
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Evolution analysis failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/behavior/triggers/active', methods=['POST'])
def get_active_triggers():
    """
    Get currently active behavioral triggers.
    
    Expected payload:
    {
        "chart_data": {...},     # Chart data for analysis
        "birth_data": {...},     # Birth information
        "current_date": "2024-01-15"  # Optional: defaults to today
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_data = data.get('chart_data')
        birth_data = data.get('birth_data')
        current_date = data.get('current_date', datetime.now().date().isoformat())
        
        if not chart_data:
            return jsonify({'error': 'chart_data is required'}), 400
        
        if not birth_data:
            return jsonify({'error': 'birth_data is required'}), 400
        
        # Create a temporary behavior profile
        temp_profile = behavior_predictor.create_behavior_profile(
            chart_data, birth_data, "Trigger Analysis"
        )
        
        # Get active triggers
        active_triggers = behavior_predictor.identify_active_triggers(
            temp_profile, current_date
        )
        
        return jsonify({
            'success': True,
            'current_date': current_date,
            'active_triggers': [trigger.to_dict() for trigger in active_triggers]
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Active triggers analysis failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/combined/full-analysis', methods=['POST'])
def full_bmad_analysis():
    """
    Perform complete BMAD analysis including personality and behavior.
    
    Expected payload:
    {
        "chart_data": {...},  # Calculated chart data
        "birth_data": {...},  # Birth information
        "person_name": "Optional Name",
        "analysis_options": {
            "include_predictions": true,
            "prediction_months": 6,
            "include_evolution": false
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_data = data.get('chart_data')
        birth_data = data.get('birth_data')
        person_name = data.get('person_name')
        options = data.get('analysis_options', {})
        
        if not chart_data:
            return jsonify({'error': 'chart_data is required'}), 400
        
        if not birth_data:
            return jsonify({'error': 'birth_data is required'}), 400
        
        # Perform personality analysis
        personality_profile = personality_analyzer.analyze_personality(
            chart_data, birth_data, person_name
        )
        
        # Perform behavioral analysis
        behavior_profile = behavior_predictor.create_behavior_profile(
            chart_data, birth_data, person_name
        )
        
        result = {
            'success': True,
            'analysis_timestamp': datetime.now().isoformat(),
            'personality_profile': personality_profile.to_dict(),
            'behavior_profile': behavior_profile.to_dict()
        }
        
        # Add predictions if requested
        if options.get('include_predictions', False):
            prediction_months = options.get('prediction_months', 6)
            
            # Generate predictions for the next N months
            current_date = datetime.now()
            predictions = []
            
            for month in range(1, prediction_months + 1):
                future_date = current_date.replace(month=current_date.month + month)
                month_predictions = behavior_predictor.predict_behavior_for_date(
                    behavior_profile, future_date.date().isoformat()
                )
                predictions.extend(month_predictions)
            
            result['future_predictions'] = [pred.to_dict() for pred in predictions]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Full BMAD analysis failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@bmad_bp.route('/info/dimensions', methods=['GET'])
def get_personality_dimensions():
    """Get available personality dimensions."""
    return jsonify({
        'personality_dimensions': [
            {
                'value': dim.value,
                'name': dim.value.replace('_', ' ').title()
            }
            for dim in PersonalityDimension
        ]
    })


@bmad_bp.route('/info/behavior-categories', methods=['GET'])
def get_behavior_categories():
    """Get available behavior categories."""
    return jsonify({
        'behavior_categories': [
            {
                'value': cat.value,
                'name': cat.value.replace('_', ' ').title()
            }
            for cat in BehaviorCategory
        ]
    })


@bmad_bp.route('/info/endpoints', methods=['GET'])
def get_api_info():
    """Get information about available BMAD API endpoints."""
    return jsonify({
        'bmad_api': {
            'version': '1.0.0',
            'description': 'Behavioral Model and Data API for astrological analysis',
            'endpoints': {
                'personality': {
                    'analyze': '/bmad/personality/analyze',
                    'compatibility': '/bmad/personality/compatibility'
                },
                'behavior': {
                    'profile': '/bmad/behavior/profile',
                    'predict': '/bmad/behavior/predict',
                    'evolution': '/bmad/behavior/evolution',
                    'active_triggers': '/bmad/behavior/triggers/active'
                },
                'combined': {
                    'full_analysis': '/bmad/combined/full-analysis'
                },
                'info': {
                    'dimensions': '/bmad/info/dimensions',
                    'categories': '/bmad/info/behavior-categories',
                    'endpoints': '/bmad/info/endpoints'
                }
            }
        }
    })