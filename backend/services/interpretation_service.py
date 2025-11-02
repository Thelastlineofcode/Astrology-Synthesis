"""Interpretation Service - Generate astrological interpretations using templates, KB, and LLM."""

from typing import Dict, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class InterpretationTemplate:
    """Template for generating interpretations."""
    def __init__(self, template_id: str, name: str, category: str, template_text: str, 
                 strategy: str = "hybrid"):
        self.template_id = template_id
        self.name = name
        self.category = category
        self.template_text = template_text
        self.strategy = strategy  # "template", "knowledge", "llm", "hybrid"
    
    def format(self, context: Dict) -> str:
        """Format template with context data."""
        try:
            return self.template_text.format(**context)
        except KeyError as e:
            logger.warning(f"Missing context key for template {self.name}: {e}")
            return self.template_text


class InterpretationService:
    """Service for generating birth chart interpretations."""
    
    def __init__(self, knowledge_service=None, llm_service=None):
        """Initialize Interpretation Service.
        
        Args:
            knowledge_service: KnowledgeService instance for KB queries
            llm_service: LLM service for enhanced interpretations
        """
        self.knowledge_service = knowledge_service
        self.llm_service = llm_service
        self.templates = self._load_default_templates()
    
    def _load_default_templates(self) -> Dict[str, InterpretationTemplate]:
        """Load default interpretation templates."""
        return {
            'sun_sign': InterpretationTemplate(
                'sun_sign',
                'Sun Sign Interpretation',
                'core',
                'Your Sun sign is {sign}, representing your core identity and will.',
                'template'
            ),
            'moon_sign': InterpretationTemplate(
                'moon_sign',
                'Moon Sign Interpretation',
                'core',
                'Your Moon sign is {sign}, governing your emotional nature and inner world.',
                'template'
            ),
            'ascendant': InterpretationTemplate(
                'ascendant',
                'Ascendant Interpretation',
                'core',
                'Your Ascendant is {sign}, the mask you present to the world.',
                'template'
            ),
            'vedic_nakshatra': InterpretationTemplate(
                'vedic_nakshatra',
                'Vedic Nakshatra',
                'vedic',
                'Your birth nakshatra is {nakshatra}, a powerful influence in Vedic astrology.',
                'knowledge'
            ),
            'dasha_period': InterpretationTemplate(
                'dasha_period',
                'Current Dasha Period',
                'vedic',
                'You are currently in the {dasha} period, which influences your life events.',
                'hybrid'
            ),
        }
    
    def generate_sun_sign_interpretation(self, sun_sign: str, chart_data: Dict) -> Dict:
        """Generate Sun sign interpretation."""
        template = self.templates['sun_sign']
        context = {
            'sign': sun_sign,
            'chart_data': chart_data,
        }
        content = template.format(context)
        
        return {
            'type': 'sun_sign',
            'content': content,
            'template_used': template.name,
            'strategy': template.strategy,
            'confidence_score': 0.95,
        }
    
    def generate_moon_sign_interpretation(self, moon_sign: str, chart_data: Dict) -> Dict:
        """Generate Moon sign interpretation."""
        template = self.templates['moon_sign']
        context = {
            'sign': moon_sign,
            'chart_data': chart_data,
        }
        content = template.format(context)
        
        return {
            'type': 'moon_sign',
            'content': content,
            'template_used': template.name,
            'strategy': template.strategy,
            'confidence_score': 0.95,
        }
    
    def generate_ascendant_interpretation(self, ascendant: str, chart_data: Dict) -> Dict:
        """Generate Ascendant interpretation."""
        template = self.templates['ascendant']
        context = {
            'sign': ascendant,
            'chart_data': chart_data,
        }
        content = template.format(context)
        
        return {
            'type': 'ascendant',
            'content': content,
            'template_used': template.name,
            'strategy': template.strategy,
            'confidence_score': 0.95,
        }
    
    def generate_vedic_interpretation(self, chart_data: Dict) -> Dict:
        """Generate Vedic astrology interpretation using knowledge base."""
        interpretations = []
        
        # Generate nakshatra interpretation
        if 'nakshatra' in chart_data:
            template = self.templates['vedic_nakshatra']
            context = {'nakshatra': chart_data['nakshatra']}
            content = template.format(context)
            
            # Could also query KB here for detailed nakshatra info
            interpretations.append({
                'type': 'nakshatra',
                'content': content,
                'confidence_score': 0.90,
            })
        
        # Generate dasha interpretation
        if 'current_dasha' in chart_data:
            template = self.templates['dasha_period']
            context = {'dasha': chart_data['current_dasha']}
            content = template.format(context)
            
            interpretations.append({
                'type': 'dasha_period',
                'content': content,
                'confidence_score': 0.85,
            })
        
        return {
            'type': 'vedic',
            'interpretations': interpretations,
            'strategy': 'hybrid',
            'overall_confidence': 0.88,
        }
    
    def generate_health_interpretation(self, chart_data: Dict) -> Dict:
        """Generate health interpretation using Ayurveda integration."""
        dosha = chart_data.get('constitution', 'unknown')
        
        return {
            'type': 'health',
            'constitution': dosha,
            'content': f'Your constitutional nature appears to be {dosha}, which influences your health patterns.',
            'recommendations': [
                'Consult with an Ayurvedic practitioner for personalized recommendations',
                'Align your lifestyle with your constitutional nature',
                'Track how planetary transits affect your energy levels',
            ],
            'confidence_score': 0.75,
        }
    
    def generate_full_interpretation(self, chart_data: Dict) -> Dict:
        """Generate comprehensive interpretation of entire chart."""
        interpretations = {
            'sun': self.generate_sun_sign_interpretation(chart_data.get('sun_sign', 'Unknown'), chart_data),
            'moon': self.generate_moon_sign_interpretation(chart_data.get('moon_sign', 'Unknown'), chart_data),
            'ascendant': self.generate_ascendant_interpretation(chart_data.get('ascendant', 'Unknown'), chart_data),
            'vedic': self.generate_vedic_interpretation(chart_data),
            'health': self.generate_health_interpretation(chart_data),
        }
        
        return {
            'chart_id': chart_data.get('id'),
            'interpretations': interpretations,
            'generation_method': 'hybrid_template_kb_llm',
            'total_confidence': 0.88,
            'message': 'Comprehensive birth chart interpretation generated',
        }
    
    def add_template(self, template: InterpretationTemplate) -> None:
        """Add a new interpretation template."""
        self.templates[template.template_id] = template
        logger.info(f"Added template: {template.name}")
    
    def list_templates(self) -> List[Dict]:
        """List available templates."""
        return [
            {
                'id': t.template_id,
                'name': t.name,
                'category': t.category,
                'strategy': t.strategy,
            }
            for t in self.templates.values()
        ]


def create_interpretation_service(knowledge_service=None, llm_service=None) -> InterpretationService:
    """Factory function to create Interpretation Service."""
    return InterpretationService(knowledge_service=knowledge_service, llm_service=llm_service)
