"""Tests for Knowledge Service."""

import pytest
from pathlib import Path
from backend.services.knowledge_service import create_knowledge_service, TextChunk


class TestKnowledgeService:
    """Test suite for KnowledgeService."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return create_knowledge_service()
    
    def test_service_initialization(self, service):
        """Test service initialization."""
        assert service is not None
        assert service.kb_path.name == "knowledge_base"
    
    def test_list_categories(self, service):
        """Test listing categories."""
        categories = service.list_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0
        
        # Check apex section
        apex = [c for c in categories if "voodoo" in c['name'].lower()]
        assert len(apex) > 0
    
    def test_apex_category_present(self, service):
        """Test that apex category exists and has correct weight."""
        categories = service.list_categories()
        apex = next((c for c in categories if c['name'] == "01_voodoo_spiritual_apex"), None)
        assert apex is not None
        assert apex['weight'] == 1.5
    
    def test_vedic_category_weight(self, service):
        """Test Vedic category weights."""
        weight_core = service.get_category_weight("02_vedic_core")
        weight_adv = service.get_category_weight("03_vedic_advanced")
        assert weight_core == 1.3
        assert weight_adv == 1.3
    
    def test_dasha_category_weight(self, service):
        """Test Dasha category weight."""
        weight = service.get_category_weight("04_dasha_timing")
        assert weight == 1.2
    
    def test_default_category_weight(self, service):
        """Test default weight for unmapped categories."""
        weight = service.get_category_weight("19_other_materials")
        assert weight == 1.0
    
    def test_get_category_info(self, service):
        """Test getting category information."""
        info = service.get_category_info("01_voodoo_spiritual_apex")
        assert info['name'] == "01_voodoo_spiritual_apex"
        assert info['weight'] == 1.5
        assert info['is_primary'] is True
    
    def test_get_non_primary_category_info(self, service):
        """Test getting info for non-primary category."""
        info = service.get_category_info("12_complementary_systems")
        assert info['name'] == "12_complementary_systems"
        assert info['weight'] == 1.0
        assert info['is_primary'] is False
    
    def test_search_local(self, service):
        """Test local search functionality."""
        results = service.search_local("vedic", limit=3)
        assert isinstance(results, list)
        # Should find something or return empty list
        assert len(results) <= 3
    
    def test_search_with_category_filter(self, service):
        """Test search with category filter."""
        results = service.search_local("astrology", category="02_vedic_core", limit=5)
        assert isinstance(results, list)


class TestTextChunk:
    """Test suite for TextChunk."""
    
    def test_text_chunk_creation(self):
        """Test creating a text chunk."""
        chunk = TextChunk(
            content="Test content",
            source_file="test.pdf",
            category="01_voodoo_spiritual_apex",
            chunk_index=0,
        )
        assert chunk.content == "Test content"
        assert chunk.source_file == "test.pdf"
        assert chunk.chunk_index == 0
    
    def test_content_hash(self):
        """Test content hash generation."""
        chunk1 = TextChunk("Same content", "file1.pdf", "01", 0)
        chunk2 = TextChunk("Same content", "file2.pdf", "01", 0)
        assert chunk1.content_hash == chunk2.content_hash
    
    def test_different_content_different_hash(self):
        """Test different content produces different hash."""
        chunk1 = TextChunk("Content A", "file.pdf", "01", 0)
        chunk2 = TextChunk("Content B", "file.pdf", "01", 0)
        assert chunk1.content_hash != chunk2.content_hash
