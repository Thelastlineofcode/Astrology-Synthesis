"""Tests for Interpretation Service."""

import pytest
from backend.services.interpretation_service import create_interpretation_service, InterpretationTemplate


class TestInterpretationService:
    """Test suite for InterpretationService."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return create_interpretation_service()
    
    def test_service_initialization(self, service):
        """Test service initialization."""
        assert service is not None
        assert len(service.templates) > 0
    
    def test_list_templates(self, service):
        """Test listing available templates."""
        templates = service.list_templates()
        assert isinstance(templates, list)
        assert len(templates) >= 3
        
        # Check for core templates
        template_ids = [t['id'] for t in templates]
        assert 'sun_sign' in template_ids
        assert 'moon_sign' in template_ids
        assert 'ascendant' in template_ids
    
    def test_sun_sign_interpretation(self, service):
        """Test Sun sign interpretation generation."""
        chart_data = {
            'sun_sign': 'Aries',
            'id': 'test_chart_1',
        }
        result = service.generate_sun_sign_interpretation('Aries', chart_data)
        
        assert result['type'] == 'sun_sign'
        assert 'Aries' in result['content']
        assert result['confidence_score'] == 0.95
    
    def test_moon_sign_interpretation(self, service):
        """Test Moon sign interpretation generation."""
        chart_data = {
            'moon_sign': 'Taurus',
            'id': 'test_chart_1',
        }
        result = service.generate_moon_sign_interpretation('Taurus', chart_data)
        
        assert result['type'] == 'moon_sign'
        assert 'Taurus' in result['content']
        assert result['confidence_score'] == 0.95
    
    def test_ascendant_interpretation(self, service):
        """Test Ascendant interpretation generation."""
        chart_data = {
            'ascendant': 'Gemini',
            'id': 'test_chart_1',
        }
        result = service.generate_ascendant_interpretation('Gemini', chart_data)
        
        assert result['type'] == 'ascendant'
        assert 'Gemini' in result['content']
        assert result['confidence_score'] == 0.95
    
    def test_vedic_interpretation(self, service):
        """Test Vedic astrology interpretation."""
        chart_data = {
            'id': 'test_chart_1',
            'nakshatra': 'Ashwini',
            'current_dasha': 'Venus',
        }
        result = service.generate_vedic_interpretation(chart_data)
        
        assert result['type'] == 'vedic'
        assert 'interpretations' in result
        assert len(result['interpretations']) > 0
        assert result['strategy'] == 'hybrid'
    
    def test_health_interpretation(self, service):
        """Test health interpretation."""
        chart_data = {
            'constitution': 'Vata',
            'id': 'test_chart_1',
        }
        result = service.generate_health_interpretation(chart_data)
        
        assert result['type'] == 'health'
        assert result['constitution'] == 'Vata'
        assert len(result['recommendations']) > 0
    
    def test_full_chart_interpretation(self, service):
        """Test full chart interpretation."""
        chart_data = {
            'id': 'test_chart_1',
            'sun_sign': 'Leo',
            'moon_sign': 'Cancer',
            'ascendant': 'Virgo',
            'nakshatra': 'Magha',
            'current_dasha': 'Sun',
            'constitution': 'Pitta',
        }
        result = service.generate_full_interpretation(chart_data)
        
        assert result['chart_id'] == 'test_chart_1'
        assert 'interpretations' in result
        assert 'sun' in result['interpretations']
        assert 'moon' in result['interpretations']
        assert 'ascendant' in result['interpretations']
        assert 'vedic' in result['interpretations']
        assert 'health' in result['interpretations']
        assert result['total_confidence'] > 0


class TestInterpretationTemplate:
    """Test suite for InterpretationTemplate."""
    
    def test_template_creation(self):
        """Test creating an interpretation template."""
        template = InterpretationTemplate(
            'test_id',
            'Test Template',
            'test_category',
            'Your {sign} is important.',
            'template'
        )
        assert template.template_id == 'test_id'
        assert template.name == 'Test Template'
        assert template.strategy == 'template'
    
    def test_template_formatting(self):
        """Test template formatting with context."""
        template = InterpretationTemplate(
            'test_id',
            'Test',
            'test',
            'Your {sign} influences {aspect}.',
            'template'
        )
        result = template.format({'sign': 'Aries', 'aspect': 'destiny'})
        assert result == 'Your Aries influences destiny.'
    
    def test_template_formatting_missing_key(self):
        """Test template formatting with missing key."""
        template = InterpretationTemplate(
            'test_id',
            'Test',
            'test',
            'Your {sign} and {missing}.',
            'template'
        )
        result = template.format({'sign': 'Aries'})
        # Should handle missing key gracefully
        assert 'Aries' in result or template.template_text in result
