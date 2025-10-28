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
