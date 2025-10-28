from flask import Blueprint, request, jsonify
from calculations.chart_calculator import ChartCalculator
from calculations.aspects import AspectCalculator
from datetime import datetime, UTC
import traceback

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health-check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(UTC).isoformat()
    })


@api_bp.route('/chart', methods=['POST'])
def calculate_chart():
    """Calculate a natal chart and aspects from posted birth data."""
    try:
        data = request.get_json(silent=True) or {}

        # -------- payload validation --------
        if 'birthData' not in data:
            return jsonify({'error': 'Missing birth data'}), 400

        birth_data: dict = data['birthData']
        options: dict = data.get('options', {})

        required_fields = [
            'year', 'month', 'day',
            'hour', 'minute'
        ]
        optional_fields = ['latitude', 'longitude', 'address']
        
        for field in required_fields:
            if field not in birth_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # If address is provided but no lat/long, we'll use default coordinates
        if 'latitude' not in birth_data or 'longitude' not in birth_data:
            if 'address' in birth_data:
                # Default to coordinates if not geocoded
                birth_data['latitude'] = 0.0
                birth_data['longitude'] = 0.0
            else:
                return jsonify({'error': 'Either latitude/longitude or address must be provided'}), 400
        # ------------------------------------

        # create calculator (sidereal / tropical)
        zodiac_type = options.get('zodiacType', 'tropical')
        ayanamsa = options.get('ayanamsa', 'LAHIRI')
        calculator = ChartCalculator(zodiac_type=zodiac_type, ayanamsa=ayanamsa)

        # chart + houses
        birth_data['house_system'] = options.get('houseSystem', 'P')
        chart_data = calculator.generate_chart(birth_data)

        # aspects
        include_minor = options.get('includeMinorAspects', False)
        aspects = AspectCalculator().calculate_aspects(
            chart_data['planets'], include_minor=include_minor
        )
        chart_data['aspects'] = aspects

        return jsonify({'success': True, 'chart': chart_data, 'birthData': birth_data})

    except Exception as exc:  # pragma: no cover
        print('Error in /chart:', exc)
        print(traceback.format_exc())
        return jsonify({'error': str(exc), 'type': type(exc).__name__}), 500


@api_bp.route('/chart/enhanced', methods=['POST'])
def calculate_enhanced_chart():
    """Calculate chart with optional BMAD personality and behavioral analysis."""
    try:
        data = request.get_json(silent=True) or {}

        # -------- payload validation --------
        if 'birthData' not in data:
            return jsonify({'error': 'Missing birth data'}), 400

        birth_data: dict = data['birthData']
        options: dict = data.get('options', {})
        bmad_options: dict = data.get('bmadOptions', {})

        required_fields = [
            'year', 'month', 'day',
            'hour', 'minute'
        ]
        
        for field in required_fields:
            if field not in birth_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Handle location data
        if 'latitude' not in birth_data or 'longitude' not in birth_data:
            if 'address' in birth_data:
                birth_data['latitude'] = 0.0
                birth_data['longitude'] = 0.0
            else:
                return jsonify({'error': 'Either latitude/longitude or address must be provided'}), 400
        # ------------------------------------

        # Calculate basic chart
        zodiac_type = options.get('zodiacType', 'tropical')
        ayanamsa = options.get('ayanamsa', 'LAHIRI')
        calculator = ChartCalculator(zodiac_type=zodiac_type, ayanamsa=ayanamsa)

        birth_data['house_system'] = options.get('houseSystem', 'P')
        chart_data = calculator.generate_chart(birth_data)

        # Calculate aspects
        include_minor = options.get('includeMinorAspects', False)
        aspects = AspectCalculator().calculate_aspects(
            chart_data['planets'], include_minor=include_minor
        )
        chart_data['aspects'] = aspects

        # Prepare response with basic chart
        response = {
            'success': True,
            'chart': chart_data,
            'birthData': birth_data
        }

        # Add BMAD analysis if requested
        if bmad_options.get('includeBMAD', False):
            try:
                from bmad.services.personality_analyzer import PersonalityAnalyzer
                from bmad.services.behavior_predictor import BehaviorPredictor
                
                person_name = bmad_options.get('personName', 'Chart Analysis')
                
                # Personality analysis
                if bmad_options.get('includePersonality', True):
                    personality_analyzer = PersonalityAnalyzer()
                    personality_profile = personality_analyzer.analyze_personality(
                        chart_data, birth_data, person_name
                    )
                    response['bmad_personality'] = personality_profile.to_dict()
                
                # Behavioral analysis
                if bmad_options.get('includeBehavior', True):
                    behavior_predictor = BehaviorPredictor()
                    behavior_profile = behavior_predictor.create_behavior_profile(
                        chart_data, birth_data, person_name
                    )
                    response['bmad_behavior'] = behavior_profile.to_dict()
                
                # Future predictions
                if bmad_options.get('includePredictions', False):
                    prediction_months = bmad_options.get('predictionMonths', 3)
                    from datetime import datetime, timedelta
                    
                    predictions = []
                    current_date = datetime.now()
                    
                    if 'behavior_profile' in locals():
                        for month in range(1, prediction_months + 1):
                            future_date = current_date + timedelta(days=30 * month)
                            month_predictions = behavior_predictor.predict_behavior_for_date(
                                behavior_profile, future_date.date().isoformat()
                            )
                            predictions.extend(month_predictions)
                    
                    response['bmad_predictions'] = [pred.to_dict() for pred in predictions]
                
                response['bmad_analysis_timestamp'] = datetime.now().isoformat()
                
            except ImportError:
                response['bmad_error'] = 'BMAD module not available or not properly configured'
            except Exception as bmad_exc:
                response['bmad_error'] = f'BMAD analysis failed: {str(bmad_exc)}'

        return jsonify(response)

    except Exception as exc:
        print('Error in /chart/enhanced:', exc)
        print(traceback.format_exc())
        return jsonify({'error': str(exc), 'type': type(exc).__name__}), 500


@api_bp.route('/zodiac-info', methods=['GET'])
def get_zodiac_info():
    """Return static symbol and sign metadata for the frontend."""
    from utils.constants import ZODIAC_SIGNS, ZODIAC_SYMBOLS, PLANET_SYMBOLS
    return jsonify({
        'zodiacSigns': ZODIAC_SIGNS,
        'zodiacSymbols': ZODIAC_SYMBOLS,
        'planetSymbols': PLANET_SYMBOLS,
        'houseSystems': {
            'P': 'Placidus',
            'K': 'Koch',
            'W': 'Whole Sign',
            'E': 'Equal',
            'R': 'Regiomontanus'
        }
    })
