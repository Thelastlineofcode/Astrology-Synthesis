# Knowledge Base & Interpretive Engine Development Plan

**Status:** Planning Phase  
**Created:** November 2, 2025  
**Target Completion:** 4-6 weeks (phased approach)  
**Integration Point:** After Phase 3 Week 3 completion

---

## 1. Executive Overview

### Vision

Transform Astrology-Synthesis from a calculation engine into a **comprehensive interpretive AI system** that:

1. Combines astrological calculations with deep interpretive knowledge
2. Generates natural language interpretations grounded in 50+ astrological texts
3. Provides context-aware predictions and remedies
4. Scales from simple lookups to complex semantic reasoning

### Current State

```
✅ Calculation Layer (Complete)
   ├─ Birth chart generation
   ├─ Transit analysis
   ├─ Synastry compatibility
   └─ Dasha predictions

❌ Knowledge & Interpretation Layer (Missing)
   ├─ No semantic knowledge base
   ├─ No interpretation generation
   ├─ No LLM integration
   └─ No context awareness
```

### Target State

```
✅ Calculation Layer (Complete)
✅ Knowledge Base Layer (New)
   ├─ 50+ astrological texts processed
   ├─ Semantic search capabilities
   ├─ Knowledge graph with relationships
   └─ Context-aware retrieval

✅ Interpretation Layer (New)
   ├─ Multi-strategy interpretation generation
   ├─ Natural language output
   ├─ LLM-powered reasoning
   └─ Personalized recommendations
```

### Phased Approach

| Phase                       | Duration  | Deliverables                               | Status   |
| --------------------------- | --------- | ------------------------------------------ | -------- |
| **Knowledge Base Setup**    | 1-2 weeks | Text processing, indexing, semantic search | Planning |
| **Interpretation Engine**   | 2-3 weeks | Services, LLM integration, templates       | Planning |
| **API Integration**         | 1 week    | Endpoints, error handling, testing         | Planning |
| **Testing & Documentation** | 1 week    | Comprehensive tests, guides                | Planning |

---

## 2. Knowledge Base System Architecture

### 2.1 Data Pipeline

```
┌─────────────────────────────────────────────────────────┐
│         Knowledge Base Processing Pipeline              │
└─────────────────────────────────────────────────────────┘

Step 1: Text Extraction
├─ PDF parsing (40+ PDFs, 3,000+ pages)
├─ EPUB conversion (5+ EPUBs)
├─ Markdown processing (existing guides)
└─ Output: Raw text chunks (10,000-50,000 passages)

Step 2: Semantic Chunking
├─ Context-aware splitting (500-1500 chars per chunk)
├─ Preserve section hierarchies
├─ Extract headers and metadata
└─ Output: Structured chunks with context

Step 3: Embedding Generation
├─ Use sentence-transformers (all-MiniLM-L6-v2)
├─ Batch process for efficiency
├─ Store in FAISS/vector DB
└─ Output: Vector embeddings (384-768 dims)

Step 4: Knowledge Graph Construction
├─ Extract concepts: planets, houses, aspects, signs
├─ Build relationships: describes, relates_to, causes
├─ Create semantic graph
└─ Output: Concept network with relationships

Step 5: Indexing & Storage
├─ SQLite full-text search (FTS5)
├─ Vector database (FAISS or Milvus)
├─ Knowledge graph (Neo4j or PostgreSQL JSON)
└─ Output: Production-ready index
```

### 2.2 Database Schema Additions

**New Tables (Backend Database):**

```sql
-- Knowledge management
CREATE TABLE knowledge_sources (
    id PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    source_type ENUM('book', 'guide', 'webpage'),
    created_at TIMESTAMP,
    indexed_at TIMESTAMP
);

CREATE TABLE knowledge_chunks (
    id PRIMARY KEY,
    source_id FOREIGN KEY,
    content TEXT NOT NULL,
    embedding VECTOR(384),  -- or store separately
    section TEXT,
    metadata JSON,
    created_at TIMESTAMP
);

CREATE TABLE concepts (
    id PRIMARY KEY,
    name TEXT UNIQUE,
    type ENUM('planet', 'house', 'sign', 'aspect', 'dasha', 'remedy'),
    description TEXT,
    synonyms TEXT[],
    created_at TIMESTAMP
);

CREATE TABLE concept_relationships (
    id PRIMARY KEY,
    concept_id_1 FOREIGN KEY,
    concept_id_2 FOREIGN KEY,
    relationship_type TEXT,
    weight FLOAT,
    source_id FOREIGN KEY,  -- which knowledge source
    created_at TIMESTAMP
);

CREATE TABLE interpretations_cache (
    id PRIMARY KEY,
    chart_id FOREIGN KEY,
    element_type ENUM('planet', 'house', 'aspect', 'synastry'),
    element_id TEXT,
    interpretation TEXT,
    confidence FLOAT,
    generated_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

### 2.3 Vector Database Setup

**Technology Stack:**

```python
# Option 1: FAISS (lightweight, local)
- In-memory vector search
- No server needed
- Good for <10M vectors
- Python-only

# Option 2: Milvus (scalable)
- Distributed vector DB
- Production-ready
- Scales to billions
- Docker-based deployment

# Option 3: Weaviate (enterprise)
- GraphQL API
- Built-in semantic search
- Knowledge graph support
- Cloud-ready

Recommendation: Start with FAISS, scale to Milvus
```

**Integration with Backend:**

```python
# backend/services/knowledge_service.py
class KnowledgeService:
    def __init__(self):
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_db = FAISSVectorDB()  # or Milvus
        self.graph_db = Neo4jClient()  # optional
        self.fts_db = SQLiteFTS()

    def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        """Vector semantic search"""
        embedding = self.embeddings.encode(query)
        return self.vector_db.search(embedding, top_k)

    def search_concepts(self, concept_name: str) -> Dict:
        """Concept lookup with relationships"""
        concept = self.get_concept(concept_name)
        relationships = self.graph_db.get_relationships(concept)
        return {concept, relationships}

    def full_text_search(self, query: str) -> List[Dict]:
        """FTS for keyword search"""
        return self.fts_db.search(query)
```

---

## 3. Interpretive Engine Architecture

### 3.1 Interpretation System Design

```
┌──────────────────────────────────────────────────────────┐
│              Interpretation Generation Flow              │
└──────────────────────────────────────────────────────────┘

User Query: "Tell me about Sun in Scorpio"

     ↓

Context Retrieval:
├─ Sun concept + keywords
├─ Scorpio sign characteristics
├─ Traditional meanings from knowledge base
└─ Synastry if birth chart available

     ↓

Template Selection (Rule-based, strategy-dependent):
├─ Simple: Return cached interpretation
├─ Complex: Build context + invoke LLM
├─ Custom: User-specific parameters
└─ Hybrid: Combine multiple strategies

     ↓

Interpretation Generation:
├─ Strategy 1: Template-based (rules)
├─ Strategy 2: Knowledge retrieval (facts)
├─ Strategy 3: LLM-powered (semantic)
├─ Strategy 4: Hybrid (combined)
└─ Fallback: Generic interpretation

     ↓

Post-Processing:
├─ Fact-check against knowledge base
├─ Add confidence scores
├─ Personalize based on user profile
├─ Cache for future requests
└─ Return with sources

     ↓

Response: Structured interpretation with sources
```

### 3.2 Interpretation Strategies

**Strategy 1: Rule-Based Templates**

```python
class TemplateInterpretation:
    """Fast, consistent, rule-based interpretations"""

    TEMPLATES = {
        'planet_in_sign': """
            {planet} in {sign} suggests:
            - Core expression: {core_expression}
            - Challenges: {challenges}
            - Strengths: {strengths}
            - Recommendations: {recommendations}
        """,
        'aspect': """
            {planet1} {aspect_type} {planet2}:
            - Dynamic: {dynamic_description}
            - Integration challenge: {challenge}
            - Growth opportunity: {opportunity}
        """,
        'house_placement': """
            {planet} in {house} House ({domain}):
            - Life area: {life_area}
            - Expression: {expression}
            - Potential: {potential}
        """
    }

    def generate(self, element_type: str, element_data: Dict) -> str:
        template = self.TEMPLATES[element_type]
        context = self.retrieve_context(element_data)
        return template.format(**context)
```

**Strategy 2: Knowledge Retrieval**

```python
class KnowledgeBasedInterpretation:
    """Retrieve relevant knowledge, synthesize into interpretation"""

    def generate(self, element: str, context: Dict) -> str:
        # Get all relevant passages from knowledge base
        passages = self.knowledge_service.search(element, top_k=10)

        # Synthesize into coherent interpretation
        interpretation = self.synthesize(element, passages)

        # Add sources and confidence
        return InterpretationResult(
            text=interpretation,
            sources=passages,
            confidence=self.calculate_confidence(passages)
        )
```

**Strategy 3: LLM-Powered Semantic**

```python
class LLMInterpretation:
    """Use LLM for complex reasoning and personalization"""

    def generate(self, element: str, user_context: Dict) -> str:
        # Build rich context
        element_info = self.knowledge_service.search(element)
        related_concepts = self.get_related_concepts(element)
        user_profile = self.get_user_profile(user_context)

        # Construct prompt
        prompt = self.build_prompt(element, element_info, related_concepts, user_profile)

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Post-process and cache
        return InterpretationResult(
            text=response,
            sources=element_info,
            method='llm',
            confidence=self.measure_confidence(response)
        )
```

**Strategy 4: Hybrid Multi-Source**

```python
class HybridInterpretation:
    """Combine multiple strategies for robust interpretation"""

    def generate(self, element: str, context: Dict) -> str:
        # Get interpretations from multiple sources
        template_result = self.template_strategy.generate(element, context)
        knowledge_result = self.knowledge_strategy.generate(element, context)
        llm_result = self.llm_strategy.generate(element, context)  # if complex

        # Synthesize results
        combined = self.synthesize([
            (template_result, weight=0.3),
            (knowledge_result, weight=0.4),
            (llm_result, weight=0.3)  # only if confidence high
        ])

        return combined
```

### 3.3 Interpretation Service Implementation

```python
# backend/services/interpretation_service.py

class InterpretationService:
    """Main orchestrator for all interpretive tasks"""

    def __init__(self):
        self.knowledge = KnowledgeService()
        self.template = TemplateInterpretation()
        self.kb_based = KnowledgeBasedInterpretation()
        self.llm = LLMInterpretation()
        self.hybrid = HybridInterpretation()
        self.cache = CacheService()

    def interpret_chart(self, chart: BirthChart, depth: str = 'standard') -> Dict:
        """Generate full chart interpretation"""
        interpretation = {
            'sun': self.interpret_sun(chart.sun, depth),
            'moon': self.interpret_moon(chart.moon, depth),
            'ascendant': self.interpret_ascendant(chart.ascendant, depth),
            'aspects': self.interpret_aspects(chart.aspects, depth),
            'houses': self.interpret_houses(chart.houses, depth),
            'summary': self.generate_summary(chart, depth)
        }
        return interpretation

    def interpret_planet_placement(self, planet: str, sign: str, house: int,
                                   context: Dict = None, strategy: str = 'hybrid') -> Dict:
        """Interpret specific planet placement"""
        # Check cache
        cache_key = f"{planet}_{sign}_{house}"
        if self.cache.exists(cache_key):
            return self.cache.get(cache_key)

        # Generate interpretation
        if strategy == 'template':
            result = self.template.generate('planet_in_sign', {planet, sign, house})
        elif strategy == 'knowledge':
            result = self.kb_based.generate(f'{planet} in {sign}', context)
        elif strategy == 'llm':
            result = self.llm.generate(f'{planet} in {sign}', context)
        elif strategy == 'hybrid':
            result = self.hybrid.generate(f'{planet} in {sign}', context)

        # Cache result
        self.cache.set(cache_key, result, ttl=86400)  # 24 hours

        return result

    def interpret_aspect(self, planet1: str, planet2: str, aspect: str,
                        context: Dict = None) -> Dict:
        """Interpret planetary aspect"""
        return self.hybrid.generate(f'{planet1} {aspect} {planet2}', context)

    def interpret_synastry(self, chart1: BirthChart, chart2: BirthChart) -> Dict:
        """Interpret synastry compatibility"""
        comparison = {
            'sun_compatibility': self.compare_suns(chart1.sun, chart2.sun),
            'moon_compatibility': self.compare_moons(chart1.moon, chart2.moon),
            'venus_compatibility': self.compare_venus(chart1.venus, chart2.venus),
            'mars_compatibility': self.compare_mars(chart1.mars, chart2.mars),
            'aspects': self.analyze_synastry_aspects(chart1, chart2),
            'overall': self.generate_synastry_summary(chart1, chart2)
        }
        return comparison

    def search_knowledge(self, query: str, search_type: str = 'hybrid') -> List[Dict]:
        """Search knowledge base"""
        if search_type == 'semantic':
            return self.knowledge.search_similar(query)
        elif search_type == 'keyword':
            return self.knowledge.full_text_search(query)
        elif search_type == 'concept':
            return self.knowledge.search_concepts(query)
        else:  # hybrid
            results = []
            results.extend(self.knowledge.search_similar(query, top_k=3))
            results.extend(self.knowledge.full_text_search(query, top_k=3))
            return self.deduplicate_results(results)
```

---

## 4. API Endpoints

### 4.1 New Knowledge Base Endpoints

```python
# backend/api/v1/knowledge.py

@router.get("/knowledge/search")
async def search_knowledge(
    query: str,
    search_type: Literal['semantic', 'keyword', 'concept', 'hybrid'] = 'hybrid',
    top_k: int = 5,
    auth: User = Depends(verify_token)
) -> List[KnowledgeResult]:
    """Search knowledge base"""
    results = interpretation_service.search_knowledge(query, search_type)
    return results[:top_k]

@router.get("/knowledge/concepts")
async def list_concepts(
    concept_type: Optional[str] = None,
    auth: User = Depends(verify_token)
) -> List[Concept]:
    """List available concepts in knowledge base"""
    pass

@router.get("/knowledge/concepts/{concept_name}")
async def get_concept(
    concept_name: str,
    auth: User = Depends(verify_token)
) -> ConceptDetail:
    """Get concept details with relationships"""
    pass

@router.get("/knowledge/sources")
async def list_sources(
    auth: User = Depends(verify_token)
) -> List[KnowledgeSource]:
    """List all knowledge sources"""
    pass
```

### 4.2 Interpretation Endpoints

```python
# backend/api/v1/interpretations.py

@router.post("/interpretations/chart")
async def interpret_chart(
    chart_id: UUID,
    depth: Literal['summary', 'standard', 'detailed'] = 'standard',
    auth: User = Depends(verify_token)
) -> ChartInterpretation:
    """Generate full chart interpretation"""
    chart = db.get_chart(chart_id, user_id=auth.id)
    interpretation = interpretation_service.interpret_chart(chart, depth)
    return interpretation

@router.post("/interpretations/planet")
async def interpret_planet(
    planet: str,
    sign: str,
    house: int,
    context: Optional[Dict] = None,
    strategy: Literal['template', 'knowledge', 'llm', 'hybrid'] = 'hybrid',
    auth: User = Depends(verify_token)
) -> PlanetInterpretation:
    """Interpret specific planet placement"""
    interpretation = interpretation_service.interpret_planet_placement(
        planet, sign, house, context, strategy
    )
    return interpretation

@router.post("/interpretations/aspect")
async def interpret_aspect(
    planet1: str,
    planet2: str,
    aspect: str,
    context: Optional[Dict] = None,
    auth: User = Depends(verify_token)
) -> AspectInterpretation:
    """Interpret planetary aspect"""
    interpretation = interpretation_service.interpret_aspect(
        planet1, planet2, aspect, context
    )
    return interpretation

@router.post("/interpretations/synastry")
async def interpret_synastry(
    chart1_id: UUID,
    chart2_id: UUID,
    depth: Literal['summary', 'detailed'] = 'standard',
    auth: User = Depends(verify_token)
) -> SynastryInterpretation:
    """Interpret synastry between two charts"""
    chart1 = db.get_chart(chart1_id, user_id=auth.id)
    chart2 = db.get_chart(chart2_id, user_id=auth.id)
    interpretation = interpretation_service.interpret_synastry(chart1, chart2, depth)
    return interpretation

@router.get("/charts/{chart_id}/interpret")
async def get_chart_interpretation(
    chart_id: UUID,
    depth: Literal['summary', 'standard', 'detailed'] = 'standard',
    auth: User = Depends(verify_token)
) -> ChartInterpretation:
    """Get stored interpretation for chart"""
    chart = db.get_chart(chart_id, user_id=auth.id)
    if not chart.interpretation:
        interpretation = interpretation_service.interpret_chart(chart, depth)
        db.save_interpretation(chart_id, interpretation)
    return chart.interpretation
```

---

## 5. Implementation Phases

### Phase 1: Knowledge Base Setup (1-2 weeks)

**Tasks:**

1. **Text Extraction & Processing**
   - [ ] Create PDF parser (PyPDF2/pdfplumber)
   - [ ] Create EPUB extractor (ebooklib)
   - [ ] Process all 50+ texts
   - [ ] Clean and normalize text
   - [ ] Output: 10,000-50,000 text chunks

2. **Semantic Chunking**
   - [ ] Implement context-aware splitter
   - [ ] Preserve section structure
   - [ ] Extract metadata (author, book, chapter)
   - [ ] Output: Structured chunks with context

3. **Embedding Generation**
   - [ ] Setup sentence-transformers model
   - [ ] Batch process all chunks
   - [ ] Handle compute requirements (GPU optional)
   - [ ] Output: Embeddings for all chunks

4. **Vector Database Setup**
   - [ ] Choose implementation (FAISS for MVP)
   - [ ] Create vector index
   - [ ] Implement search interface
   - [ ] Output: Production-ready vector DB

5. **Full-Text Search**
   - [ ] Implement SQLite FTS5
   - [ ] Index all chunks
   - [ ] Create keyword search interface
   - [ ] Output: Production-ready FTS

6. **Knowledge Graph (Optional Phase 1)**
   - [ ] Extract concepts from texts
   - [ ] Build relationship graph
   - [ ] Implement concept lookup
   - [ ] Output: Queryable concept network

**Deliverables:**

- `backend/services/knowledge_service.py` (400+ lines)
- `backend/utils/text_processor.py` (300+ lines)
- Vector index files (FAISS)
- Database migrations for knowledge tables
- Initial documentation

---

### Phase 2: Interpretation Engine (2-3 weeks)

**Tasks:**

1. **Template System**
   - [ ] Design interpretation templates
   - [ ] Implement template engine
   - [ ] Create templates for all placements
   - [ ] Output: 50+ templates covering all combinations

2. **Interpretation Service**
   - [ ] Implement InterpretationService core
   - [ ] Implement strategy pattern
   - [ ] Create caching layer
   - [ ] Output: Production-ready service

3. **LLM Integration**
   - [ ] Setup OpenAI API (or local alternative)
   - [ ] Create prompt templates
   - [ ] Implement semantic generation
   - [ ] Add confidence scoring
   - [ ] Output: LLM-powered interpretation

4. **Context Builders**
   - [ ] User profile context
   - [ ] Chart context
   - [ ] Relationship context
   - [ ] Output: Rich context for all queries

5. **Synthesis & Hybridization**
   - [ ] Implement multi-source synthesis
   - [ ] Create weighting system
   - [ ] Add fact-checking
   - [ ] Output: Hybrid interpretation pipeline

**Deliverables:**

- `backend/services/interpretation_service.py` (500+ lines)
- Template library (300+ lines)
- LLM integration module (200+ lines)
- Cache service extensions
- Comprehensive tests

---

### Phase 3: API Integration & Testing (1-2 weeks)

**Tasks:**

1. **API Endpoints**
   - [ ] Create `/knowledge` endpoints (search, concepts, sources)
   - [ ] Create `/interpretations` endpoints (chart, planet, aspect, synastry)
   - [ ] Add to charts routes
   - [ ] Output: 10+ new endpoints

2. **Error Handling**
   - [ ] Handle edge cases
   - [ ] Implement fallbacks
   - [ ] Create error responses
   - [ ] Output: Robust error handling

3. **Testing**
   - [ ] Unit tests for services (50+ tests)
   - [ ] Integration tests for endpoints (20+ tests)
   - [ ] Performance benchmarks
   - [ ] Output: 70+ passing tests

4. **Documentation**
   - [ ] API documentation
   - [ ] Knowledge base guide
   - [ ] Interpretation examples
   - [ ] LLM configuration guide
   - [ ] Output: Comprehensive documentation

5. **Performance Optimization**
   - [ ] Profile code
   - [ ] Optimize vector search
   - [ ] Implement caching strategy
   - [ ] Output: Sub-500ms response times

**Deliverables:**

- `backend/api/v1/knowledge.py` (200+ lines)
- `backend/api/v1/interpretations.py` (300+ lines)
- 70+ passing tests
- API documentation
- Performance report

---

## 6. Technology Choices

### Vector Database Options

| Choice       | Pros                                       | Cons                           | Recommendation |
| ------------ | ------------------------------------------ | ------------------------------ | -------------- |
| **FAISS**    | Fast, lightweight, Python-native           | In-memory only, no persistence | ✅ MVP/Phase 1 |
| **Milvus**   | Distributed, scales well, production-ready | Requires Docker                | Phase 2+       |
| **Weaviate** | GraphQL, semantic search, enterprise       | Higher resource use            | Phase 3+       |
| **Pinecone** | Managed, easy scaling, cloud               | Monthly cost                   | Long-term      |

**Recommendation:** Start with FAISS (local, no dependencies), migrate to Milvus if needed.

### LLM Integration Options

| Choice                 | Pros                        | Cons                               | Recommendation     |
| ---------------------- | --------------------------- | ---------------------------------- | ------------------ |
| **OpenAI (GPT-4)**     | Best quality, reliable      | Requires API key, cost per request | ✅ Production      |
| **Anthropic (Claude)** | High quality, ethical       | Similar cost model                 | Good alternative   |
| **Local (Llama 2)**    | Free, private, no API calls | Requires GPU/large compute         | Development        |
| **Hugging Face**       | Open source, customizable   | Requires fine-tuning               | Future enhancement |

**Recommendation:** Start with OpenAI for quality/reliability, add local option for cost optimization.

### Search Strategy

```python
# Hybrid approach: semantic + keyword + concept
class HybridSearch:
    def search(self, query: str, top_k: int = 5):
        # 1. Semantic search (vector similarity)
        semantic_results = self.vector_db.search(self.embed(query), top_k=3)

        # 2. Keyword search (FTS)
        keyword_results = self.fts_db.search(query, top_k=3)

        # 3. Concept lookup (exact + relationships)
        concept_results = self.concept_db.search(query, top_k=2)

        # 4. Deduplicate and rank
        combined = self.deduplicate_and_rank(
            semantic_results + keyword_results + concept_results
        )

        return combined[:top_k]
```

---

## 7. Integration with Existing Systems

### 7.1 Database Integration

**New tables in backend/models/database.py:**

```python
class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"
    id = Column(UUID, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    source_type = Column(Enum(SourceType), nullable=False)
    indexed_at = Column(DateTime, nullable=True)

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id = Column(UUID, primary_key=True)
    source_id = Column(UUID, ForeignKey("knowledge_sources.id"))
    content = Column(Text, nullable=False)
    section = Column(String(255))
    metadata = Column(JSON)
    # Embedding stored separately in vector DB

class Concept(Base):
    __tablename__ = "concepts"
    id = Column(UUID, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    concept_type = Column(Enum(ConceptType), nullable=False)
    description = Column(Text)
    # Relationships through separate table

class InterpretationCache(Base):
    __tablename__ = "interpretations_cache"
    id = Column(UUID, primary_key=True)
    chart_id = Column(UUID, ForeignKey("birth_charts.id"))
    element_type = Column(String(50), nullable=False)
    element_id = Column(String(255), nullable=False)
    interpretation = Column(Text, nullable=False)
    confidence = Column(Float)
    expires_at = Column(DateTime, nullable=False)
```

### 7.2 Service Integration

**How it works together:**

```
User Request
    ↓
Calculation Service (existing)
    ├─ Generate birth chart
    └─ Return chart data
    ↓
Interpretation Service (new)
    ├─ Retrieve knowledge base facts
    ├─ Generate interpretation strategies
    ├─ Apply LLM if needed
    └─ Return interpretation
    ↓
Response to User
```

### 7.3 API Layer Integration

**New endpoints added to existing API:**

```
/api/v1/
├─ /auth/* (existing)
├─ /charts/* (existing)
├─ /predictions/* (existing)
├─ /transits/* (existing)
├─ /knowledge/* (NEW - knowledge base search)
├─ /interpretations/* (NEW - interpretation generation)
└─ /charts/{id}/interpret (NEW - full chart interpretation)
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# tests/test_knowledge_service.py
class TestKnowledgeService:
    def test_semantic_search(self): pass
    def test_keyword_search(self): pass
    def test_concept_lookup(self): pass
    def test_embedding_generation(self): pass

# tests/test_interpretation_service.py
class TestInterpretationService:
    def test_template_generation(self): pass
    def test_knowledge_retrieval(self): pass
    def test_llm_generation(self): pass
    def test_hybrid_generation(self): pass
    def test_caching(self): pass
```

### 8.2 Integration Tests

```python
# tests/test_interpretation_endpoints.py
class TestInterpretationEndpoints:
    def test_chart_interpretation_endpoint(self): pass
    def test_planet_interpretation_endpoint(self): pass
    def test_aspect_interpretation_endpoint(self): pass
    def test_synastry_interpretation_endpoint(self): pass
    def test_knowledge_search_endpoint(self): pass
```

### 8.3 Performance Tests

```python
# tests/test_performance.py
class TestPerformance:
    def test_semantic_search_performance(self): pass  # target: <100ms
    def test_interpretation_generation(self): pass     # target: <500ms
    def test_llm_response_time(self): pass            # target: <2s
    def test_concurrent_requests(self): pass           # target: 10+ concurrent
```

---

## 9. Configuration & Deployment

### 9.1 Environment Variables

```bash
# .env additions for knowledge base & interpretation

# LLM Configuration
LLM_PROVIDER=openai                          # or anthropic, local
LLM_MODEL=gpt-4-turbo-preview               # or gpt-3.5-turbo
OPENAI_API_KEY=sk-...
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Vector Database
VECTOR_DB_TYPE=faiss                        # or milvus
VECTOR_DB_PATH=/data/vector_index
VECTOR_EMBEDDING_MODEL=all-MiniLM-L6-v2

# Knowledge Base
KNOWLEDGE_BASE_PATH=/data/knowledge_base
KNOWLEDGE_FTS_DB=/data/knowledge_fts.db
CONCEPT_GRAPH_DB=neo4j://localhost:7687    # optional

# Cache Configuration
INTERPRETATION_CACHE_TTL=86400              # 24 hours
CACHE_MAX_SIZE=10000

# Performance
VECTOR_SEARCH_TOP_K=10
HYBRID_SEARCH_TOP_K=5
```

### 9.2 Docker Setup

```dockerfile
# Additions to Dockerfile for knowledge services
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install \
    torch==2.0.0 \
    sentence-transformers==2.2.2 \
    faiss-cpu==1.7.4 \
    openai==1.0.0 \
    pydantic==2.0.0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 10. Success Metrics

### Phase 1 Success Criteria

- [ ] 50+ astrological texts processed
- [ ] 10,000+ knowledge chunks created
- [ ] Semantic search working (<100ms)
- [ ] Keyword search functional
- [ ] Concept lookup operational
- [ ] Documentation complete

### Phase 2 Success Criteria

- [ ] 50+ interpretation templates created
- [ ] InterpretationService fully implemented
- [ ] LLM integration working
- [ ] Hybrid generation producing quality output
- [ ] Caching reducing response times by 80%
- [ ] 50+ passing tests

### Phase 3 Success Criteria

- [ ] 10+ new API endpoints live
- [ ] All interpretations endpoints tested
- [ ] Error handling comprehensive
- [ ] Performance targets met (<500ms)
- [ ] Documentation complete
- [ ] 70+ passing tests total

### Overall Success Criteria

- [ ] End-to-end interpretation working
- [ ] 100+ passing tests
- [ ] <500ms P95 response time
- [ ] Cost-efficient LLM usage
- [ ] Knowledge base searchable
- [ ] Production-ready deployment

---

## 11. Cost Estimation

### Infrastructure Costs (Monthly)

```
Vector Database (FAISS): $0 (local)
LLM API (GPT-4 Turbo): $100-500/month (usage-dependent)
Database (PostgreSQL): $50-100/month (if cloud)
Hosting (API): $50-200/month
Total: $200-800/month
```

### One-Time Costs

```
Knowledge base setup: 40 hours @ $100/hr = $4,000
Interpretation engine: 60 hours @ $100/hr = $6,000
API integration: 30 hours @ $100/hr = $3,000
Testing & deployment: 20 hours @ $100/hr = $2,000
Total: ~$15,000
```

---

## 12. Risk Mitigation

| Risk                        | Impact | Mitigation                                       |
| --------------------------- | ------ | ------------------------------------------------ |
| LLM API costs exceed budget | High   | Implement local model alternative, rate limiting |
| Vector search performance   | Medium | Start with FAISS, optimize embeddings            |
| Knowledge base quality      | High   | Curate sources, validation layer                 |
| Integration complexity      | Medium | Phased approach, thorough testing                |
| Data privacy (user charts)  | High   | Encryption, audit logging, compliance checks     |

---

## 13. Timeline & Roadmap

```
Week 1-2: Knowledge Base Setup Phase
├─ Text extraction & processing (3 days)
├─ Semantic chunking (2 days)
├─ Embedding generation (2 days)
├─ Vector DB setup (2 days)
├─ FTS indexing (1 day)
└─ Testing & documentation (1 day)

Week 3-5: Interpretation Engine Phase
├─ Template system (3 days)
├─ Interpretation service (4 days)
├─ LLM integration (3 days)
├─ Context builders (2 days)
├─ Synthesis layer (2 days)
└─ Testing (2 days)

Week 6: API Integration Phase
├─ Endpoint creation (2 days)
├─ Error handling (1 day)
├─ Performance optimization (1 day)
├─ Testing (1 day)
└─ Documentation (1 day)

Post-Integration: Optimization & Production
├─ Performance tuning
├─ Cost optimization
├─ Monitoring setup
└─ Production deployment
```

---

## 14. Next Steps

### Immediate Actions

1. [ ] Review and approve this plan
2. [ ] Set up LLM API account (OpenAI/Anthropic)
3. [ ] Prepare knowledge base directory structure
4. [ ] Create project board for tracking

### Begin Phase 1

1. [ ] Create text extraction pipeline
2. [ ] Start processing PDFs/EPUBs
3. [ ] Setup vector database infrastructure
4. [ ] Implement knowledge service

### Communication

- Weekly progress updates
- Blockers escalation
- Cost tracking
- Performance monitoring

---

**Document Status:** Ready for Implementation  
**Last Updated:** November 2, 2025  
**Next Review:** Upon completion of Phase 1
