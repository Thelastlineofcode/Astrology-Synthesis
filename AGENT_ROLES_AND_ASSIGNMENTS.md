# Agent Roles & Development Assignments

## Syncretic AI Prediction Engine - Phase 2 Development Plan

**Project Status**: KP Engine Validated ✅ (100% test pass rate)  
**Current Phase**: Core Engine → Knowledge Processing → AI Integration  
**Target**: Production-ready prediction API with multi-tradition synthesis

---

## 🎯 Agent Specializations & Assignments

### **@architect** - System Design & Architecture Lead

**Primary Responsibilities:**

- Design the overall prediction API architecture
- Define data flow between KP engine → AI layer → response formatting
- Create database schema for prediction history and user queries
- Design caching strategy for ephemeris data and repeated calculations
- Document API endpoints, request/response formats, authentication

**Specific Tasks:**

1. **API Architecture Document**
   - RESTful endpoints: `/predict`, `/chart`, `/transits`, `/remedies`
   - WebSocket support for real-time transit notifications
   - Rate limiting and authentication strategy
   - Error handling and validation patterns

2. **Data Pipeline Design**
   - Swiss Ephemeris integration architecture
   - Real-time planetary position caching
   - Prediction confidence scoring pipeline
   - Multi-tradition synthesis workflow

3. **Scalability Planning**
   - Microservices vs monolith decision
   - Database selection (PostgreSQL for structured predictions?)
   - Redis caching for ephemeris and chart data
   - Load balancing for concurrent predictions

**Deliverables:**

- `API_ARCHITECTURE.md` - Complete system design
- `DATABASE_SCHEMA.md` - Prediction storage structure
- `INTEGRATION_PATTERNS.md` - How traditions synthesize
- Architecture diagrams (sequence, component, deployment)

---

### **@backend** - Core Engine Development

**Primary Responsibilities:**

- Extend KP engine with transit timing calculations
- Integrate Swiss Ephemeris for real planetary positions
- Build Vimshottari dasha calculator
- Implement planetary hours (Rosicrucian timing)
- Create Arabic parts/lots calculator

**Specific Tasks:**

1. **Transit Timing Engine** (`backend/calculations/transit_engine.py`)

   ```python
   def calculate_transit_timing(natal_chart, query_date, target_house):
       """
       Given natal significators, find when transiting planets
       enter favorable sub-lords in next 2 years.
       Returns: List of date ranges with confidence scores.
       """
   ```

2. **Dasha Calculator** (`backend/calculations/dasha_engine.py`)
   - Vimshottari Mahadasha (120-year cycle)
   - Antardasha (sub-periods within Mahadasha)
   - Pratyantardasha (micro-periods)
   - Current running period at query time

3. **Swiss Ephemeris Integration** (`backend/calculations/ephemeris.py`)
   - Wrapper for pyswisseph library
   - Real-time planetary positions
   - Ayanamsa handling (Lahiri for KP)
   - House calculation (Placidus, Equal, Whole Sign)

4. **Planetary Hours Calculator** (`backend/calculations/planetary_hours.py`)
   - Sunrise/sunset calculation for location
   - Day/night hour division (unequal hours)
   - Current ruling planet at query time
   - Rosicrucian ceremonial timing

5. **Arabic Parts** (`backend/calculations/arabic_parts.py`)
   - Part of Fortune: ASC + Moon - Sun
   - Part of Spirit: ASC + Sun - Moon
   - 20+ additional Arabic lots
   - Integration with house significators

**Deliverables:**

- 5 new calculation modules (fully tested)
- Integration tests with existing KP engine
- Performance benchmarks (<100ms per prediction)
- API wrappers for each calculation type

---

### **@data** - Knowledge Base Processing & NLP

**Primary Responsibilities:**

- Extract prediction methodologies from 72 knowledge base books
- Build structured prediction database from texts
- Create embeddings for semantic search of astrological knowledge
- Process PDF/EPUB files into usable formats

**Specific Tasks:**

1. **Book Processing Pipeline** (`scripts/process_knowledge_base.py`)
   - PDF/EPUB → Clean text extraction
   - Chapter segmentation by topic
   - Metadata tagging (tradition, topic, planet, house)
   - Quality validation (OCR errors, missing pages)

2. **Prediction Methodology Extraction**
   - Identify prediction rules (if-then patterns)
   - Extract timing windows for events
   - Catalog remedy recommendations by tradition
   - Map planetary transits → life events

3. **Semantic Database Build**
   - Vector embeddings using sentence-transformers
   - ChromaDB or Pinecone for vector storage
   - Metadata filtering (tradition, confidence, source)
   - RAG (Retrieval Augmented Generation) setup

4. **Key Books Priority List:**

   ```
   HIGH PRIORITY (Process First):
   1. "Astrological transits" - Timing methodology
   2. "27 Stars 27 Gods" - Nakshatra interpretations
   3. "Astrology, Karma & Transformation" - Psychological depth
   4. "Aniesha Voodoo Readings" - Vodou integration
   5. KSK's "Krishnamurti Paddhati" volumes - KP rules

   MEDIUM PRIORITY:
   - Medical Astrology texts
   - Planetary periods books
   - House significations

   LOW PRIORITY:
   - General astrology theory
   - Historical texts
   ```

**Deliverables:**

- Processed knowledge base (structured JSON/database)
- Embedding model for semantic search
- `KNOWLEDGE_BASE_SCHEMA.md` - Data structure docs
- Sample queries showing retrieval accuracy

---

### **@ai** - AI Interpretation & Synthesis Layer

**Primary Responsibilities:**

- Design prompt engineering for multi-tradition synthesis
- Build AI agent that combines KP + Vedic + Vodou + Arabic predictions
- Implement confidence scoring across traditions
- Create natural language prediction generation

**Specific Tasks:**

1. **Multi-Tradition Synthesis Agent** (`backend/ai/synthesis_agent.py`)

   ```python
   class SynthesisAgent:
       def synthesize_prediction(
           kp_analysis,      # KP sub-lords & significators
           vedic_dashas,     # Current planetary periods
           vodou_lwa,        # Relevant Lwa for situation
           arabic_parts,     # Arabic lots
           rosicrucian_hours # Timing recommendations
       ) -> Prediction:
           """
           Synthesizes insights from all traditions into
           coherent prediction with reasoning chain.
           """
   ```

2. **Prompt Engineering**
   - System prompts for each tradition's "voice"
   - Chain-of-thought reasoning for predictions
   - Confidence calibration across traditions
   - Contradiction resolution (when traditions disagree)

3. **RAG Integration**
   - Query knowledge base for relevant passages
   - Ground predictions in source texts
   - Citation generation (book, page, tradition)
   - Hallucination detection and filtering

4. **Natural Language Generation**
   - Convert technical analysis → human-readable insights
   - Adjust tone (formal/casual) based on user preference
   - Multi-language support planning
   - Sensitivity handling (death, illness, relationships)

**Deliverables:**

- AI synthesis engine with configurable models
- Prompt library for each tradition
- Evaluation metrics (accuracy, consistency, citations)
- `AI_REASONING_EXAMPLES.md` - Sample outputs

---

### **@qa** - Testing, Validation & Quality Assurance

**Primary Responsibilities:**

- Expand test suite beyond KP engine
- Historical prediction validation (100+ cases)
- Cross-tradition consistency testing
- Performance and load testing

**Specific Tasks:**

1. **Comprehensive Test Suite Expansion**
   - Transit timing tests (known event dates)
   - Dasha period accuracy validation
   - Planetary hours calculation verification
   - Arabic parts formula correctness

2. **Historical Prediction Validation**
   - Collect 100+ real-world cases with known outcomes
   - Test each case through full prediction pipeline
   - Calculate accuracy rate per tradition
   - Identify failure patterns and edge cases

3. **Integration Testing**

   ```python
   # Test: Full prediction workflow
   def test_complete_prediction_pipeline():
       # 1. Birth data → Chart calculation
       # 2. Query → Significator analysis
       # 3. Timing → Transit windows
       # 4. AI synthesis → Natural language output
       # 5. Remedies → Tradition-specific recommendations
   ```

4. **Performance Benchmarks**
   - Target: <500ms per full prediction
   - Concurrent requests: 100+ simultaneous users
   - Cache effectiveness monitoring
   - Memory usage profiling

5. **Accuracy Metrics**
   - Prediction confidence vs actual outcomes
   - Per-tradition accuracy rates
   - Timing window precision (±days, ±weeks)
   - User satisfaction simulation

**Deliverables:**

- Expanded test suite (500+ test cases)
- `VALIDATION_REPORT.md` - Historical accuracy data
- Performance benchmarking results
- CI/CD integration for automated testing

---

### **@security** - Security, Privacy & Ethics

**Primary Responsibilities:**

- Secure API authentication and authorization
- User data privacy (birth data is sensitive!)
- Rate limiting and abuse prevention
- Ethical prediction guidelines

**Specific Tasks:**

1. **Authentication & Authorization**
   - JWT token-based auth
   - API key management for paid tiers
   - Role-based access (free vs premium users)
   - OAuth integration (Google, Apple sign-in)

2. **Data Privacy Compliance**
   - GDPR compliance for EU users
   - Birth data encryption at rest
   - Anonymous analytics (no PII in logs)
   - Right to deletion implementation

3. **Rate Limiting & Abuse Prevention**
   - Per-user request limits (10/day free, unlimited paid)
   - IP-based rate limiting for API abuse
   - Cost controls (prevent expensive LLM calls)
   - Bot detection and blocking

4. **Ethical Guidelines Document**
   - No predictions about: death timing, harm to others
   - Sensitive topics: health, legal matters (disclaimers)
   - Psychological safety in wording
   - Cultural sensitivity across traditions

**Deliverables:**

- `SECURITY_ARCHITECTURE.md`
- `PRIVACY_POLICY.md` (legal compliant)
- `ETHICAL_GUIDELINES.md` for AI prompts
- Security audit checklist

---

### **@research** - Astrological Research & Validation

**Primary Responsibilities:**

- Validate syncretic correspondence mappings
- Research cross-tradition equivalencies
- Document astrological sources and citations
- Consult with practitioners for accuracy

**Specific Tasks:**

1. **Syncretic Correspondence System** (`SYNCRETIC_CORRESPONDENCES.md`)

   ```
   Example Mapping:
   KP House 7 (Marriage) ↔
     Vedic: Kalatra Bhava
     Vodou: Erzulie Freda (love, relationships)
     Rosicrucian: Venus hour, Friday
     Arabic: Part of Marriage

   Integration Logic:
   - KP gives timing (sub-lord)
   - Vedic gives psychological depth
   - Vodou gives ritual remedy (offerings to Erzulie)
   - Rosicrucian gives ceremonial timing
   - Arabic gives additional chart points
   ```

2. **Cross-Tradition Research**
   - Planetary ruler equivalencies (KP vs Vedic)
   - Lwa-to-Planet mappings (Ogoun = Mars?)
   - Arabic lot formulas verification
   - Rosicrucian planetary hour tables

3. **Practitioner Consultation**
   - KP astrologer review (sub-lord accuracy)
   - Vodou priest consultation (Lwa appropriateness)
   - Vedic astrologer validation (dasha calculations)
   - Academic review of synthesis methodology

4. **Source Citation Management**
   - Bibliography for all knowledge base books
   - Page-level citations for specific predictions
   - Copyright compliance for excerpts
   - Academic credibility establishment

**Deliverables:**

- `SYNCRETIC_CORRESPONDENCES.md` - Complete mapping
- `ASTROLOGICAL_SOURCES.md` - Annotated bibliography
- Practitioner endorsement letters (if obtained)
- Research methodology paper (academic credibility)

---

### **@devops** - Infrastructure & Deployment

**Primary Responsibilities:**

- Docker containerization
- Cloud deployment (AWS/GCP/Azure)
- CI/CD pipeline setup
- Monitoring and alerting

**Specific Tasks:**

1. **Containerization**
   - `Dockerfile` for backend API
   - `docker-compose.yml` for local development
   - Environment variable management
   - Multi-stage builds (dev vs production)

2. **Cloud Deployment**
   - Cloud provider selection (AWS Lambda? EC2? GCP Cloud Run?)
   - Database hosting (managed PostgreSQL)
   - Redis caching setup
   - CDN for ephemeris data

3. **CI/CD Pipeline**
   - GitHub Actions for automated testing
   - Deploy on merge to `main`
   - Staging environment for testing
   - Rollback strategy

4. **Monitoring & Alerting**
   - Prometheus metrics collection
   - Grafana dashboards (request rate, latency, errors)
   - Error tracking (Sentry)
   - Uptime monitoring (99.9% SLA)

**Deliverables:**

- Complete deployment infrastructure
- `DEPLOYMENT_GUIDE.md`
- Monitoring dashboard access
- Incident response playbook

---

### **@frontend** (Future - Low Priority for Now)

**Primary Responsibilities:**

- Eventually build user interface (but backend-first approach)
- API documentation and playground
- Admin dashboard for monitoring

**Deferred Until:**

- Backend API is stable and tested
- At least 100 successful predictions validated
- Core team has bandwidth for UI work

**When Ready, Build:**

- Simple web form: birth data + question → prediction
- Beautiful prediction display (confidence, timing, remedies)
- User account management
- Prediction history

---

## 📋 Development Phases & Milestones

### **Phase 1: Core Calculations** ✅ COMPLETE

- [x] KP engine (100% tests passing)
- [x] Test suite validation
- [x] Documentation

### **Phase 2: Extended Calculations** 🔄 IN PROGRESS

**Assigned to: @backend**

- [ ] Transit timing engine
- [ ] Vimshottari dasha calculator
- [ ] Swiss Ephemeris integration
- [ ] Planetary hours calculator
- [ ] Arabic parts calculator

**Timeline:** 2-3 weeks  
**Success Metric:** All calculators tested and integrated

### **Phase 3: Knowledge Processing** ⏳ NEXT

**Assigned to: @data**

- [ ] Process top 10 priority books
- [ ] Build semantic search database
- [ ] Extract prediction rules
- [ ] Create embeddings for RAG

**Timeline:** 3-4 weeks  
**Success Metric:** Query knowledge base returns relevant passages

### **Phase 4: AI Synthesis** ⏳ UPCOMING

**Assigned to: @ai**

- [ ] Build synthesis agent
- [ ] Prompt engineering for each tradition
- [ ] RAG integration
- [ ] Natural language generation

**Timeline:** 2-3 weeks  
**Success Metric:** AI generates coherent multi-tradition predictions

### **Phase 5: API Development** ⏳ UPCOMING

**Assigned to: @architect + @backend**

- [ ] Design API endpoints
- [ ] Implement authentication
- [ ] Build request validation
- [ ] Create response formatting

**Timeline:** 2 weeks  
**Success Metric:** API handles 100 concurrent requests

### **Phase 6: Validation & Testing** ⏳ UPCOMING

**Assigned to: @qa + @research**

- [ ] Historical prediction testing (100+ cases)
- [ ] Cross-tradition consistency validation
- [ ] Performance benchmarking
- [ ] Practitioner review

**Timeline:** 3-4 weeks  
**Success Metric:** 70%+ accuracy on historical predictions

### **Phase 7: Security & Ethics** ⏳ UPCOMING

**Assigned to: @security**

- [ ] Implement authentication
- [ ] Privacy compliance
- [ ] Rate limiting
- [ ] Ethical guidelines enforcement

**Timeline:** 1-2 weeks  
**Success Metric:** Security audit passes

### **Phase 8: Deployment** ⏳ FINAL

**Assigned to: @devops**

- [ ] Cloud infrastructure setup
- [ ] CI/CD pipeline
- [ ] Monitoring and alerting
- [ ] Production launch

**Timeline:** 1-2 weeks  
**Success Metric:** 99.9% uptime, <500ms latency

---

## 🎯 Current Priority Queue

### Immediate (This Week)

1. **@backend**: Start transit timing engine
2. **@architect**: Design API architecture document
3. **@data**: Begin processing top 5 books

### Short-term (Next 2 Weeks)

1. **@backend**: Complete all calculation modules
2. **@data**: Build semantic search database
3. **@ai**: Design synthesis agent architecture

### Medium-term (Next Month)

1. **@ai**: Implement multi-tradition synthesis
2. **@qa**: Build expanded test suite
3. **@architect**: Finalize API design

### Long-term (2-3 Months)

1. **@security**: Implement full security layer
2. **@devops**: Production deployment
3. **@research**: Practitioner validation

---

## 📊 Success Metrics

### Technical Metrics

- **Prediction Latency:** <500ms per request
- **Test Coverage:** >90% for all modules
- **Uptime:** 99.9% availability
- **Accuracy:** 70%+ on historical validations

### Quality Metrics

- **Confidence Calibration:** Predictions match stated confidence
- **Citation Quality:** 90%+ of claims have source references
- **Cross-Tradition Coherence:** No contradictions in synthesis
- **User Satisfaction:** (when we have users) >4/5 rating

### Development Metrics

- **Code Reviews:** All PRs reviewed by 2+ agents
- **Documentation:** Every module has README + examples
- **Testing:** Every function has unit + integration tests
- **Performance:** Continuous monitoring and optimization

---

## 🤝 Agent Collaboration Patterns

### @backend ↔ @architect

- Backend implements calculations per architecture design
- Architect reviews performance characteristics
- Joint decisions on data structures and APIs

### @data ↔ @ai

- Data team provides structured knowledge base
- AI team uses RAG to query knowledge
- Joint work on embeddings and retrieval accuracy

### @qa ↔ All Agents

- QA reviews all code for testability
- Agents write tests for their own modules
- QA maintains integration test suite

### @research ↔ @ai

- Research validates syncretic mappings
- AI implements reasoning based on research
- Joint work on cross-tradition synthesis logic

### @security ↔ @devops

- Security defines requirements
- DevOps implements infrastructure security
- Joint work on monitoring and incident response

---

## 📞 Communication Protocols

### When to Invoke Each Agent:

- **"@architect"** - System design questions, API structure decisions
- **"@backend"** - Calculation logic, algorithm implementation
- **"@data"** - Knowledge base processing, embeddings, RAG
- **"@ai"** - Prompt engineering, synthesis logic, LLM integration
- **"@qa"** - Testing strategies, validation, quality checks
- **"@security"** - Auth, privacy, ethical guidelines
- **"@research"** - Astrological accuracy, tradition validation
- **"@devops"** - Deployment, infrastructure, monitoring
- **"@frontend"** - (Future) UI/UX, client-side logic

### Decision-Making Hierarchy:

1. **Technical Architecture:** @architect has final say
2. **Astrological Accuracy:** @research has final say
3. **Code Quality:** @qa has veto power
4. **Security:** @security can block any feature
5. **AI Reasoning:** @ai owns synthesis logic

### Weekly Sync Points:

- Monday: @architect shares priority queue
- Wednesday: @backend, @data, @ai report progress
- Friday: @qa reports test coverage, @devops reports system health

---

## 🚀 Getting Started

### For Each Agent:

1. **Read this document completely**
2. **Review your assigned Phase tasks**
3. **Check current priority queue**
4. **Read relevant technical docs:**
   - KP_SYSTEM_ARCHITECTURE.md
   - SYNCRETIC_AI_PREDICTION_SYSTEM.md
   - Test files for examples
5. **Start with highest priority task**
6. **Coordinate with related agents**

### Development Workflow:

1. Pick a task from priority queue
2. Create implementation plan
3. Write tests first (TDD)
4. Implement functionality
5. Run tests (must pass 100%)
6. Update documentation
7. Request review from @qa
8. Integrate with main system

---

## 🎓 Resources & References

### Technical Documentation:

- `/docs/KP_SYSTEM_ARCHITECTURE.md` - KP calculation details
- `/docs/SYNCRETIC_AI_PREDICTION_SYSTEM.md` - Overall vision
- `/docs/KP_TEST_SUITE_DOCUMENTATION.md` - Testing standards
- `/backend/calculations/kp_engine.py` - Working example

### External Resources:

- Swiss Ephemeris: https://www.astro.com/swisseph/
- KSK Institute: http://www.kpastro.co.in/
- PySwissEph Docs: https://astrorigin.com/pyswisseph/
- Sentence Transformers: https://www.sbert.net/

### Knowledge Base:

- `/knowledge_base/` - 72 books on astrology
- Priority: "Astrological transits", "27 Stars 27 Gods", "KP Paddhati"

---

## ✅ Current Status Summary

**Completed:**

- ✅ KP calculation engine (100% validated)
- ✅ Sub-lord calculations (249 subdivisions)
- ✅ Cuspal sub-lords
- ✅ Significator analysis
- ✅ Ruling planets
- ✅ Confidence scoring
- ✅ Comprehensive test suite

**In Progress:**

- 🔄 Project architecture planning (this document)

**Next Up:**

- ⏳ Transit timing calculator (@backend)
- ⏳ API architecture design (@architect)
- ⏳ Knowledge base processing (@data)

**Blocked/Waiting:**

- 🚫 AI synthesis (waiting for knowledge base)
- 🚫 Frontend UI (intentionally deferred)

---

## 💬 Questions or Clarifications?

If any agent needs clarification on:

- **Scope of responsibility** → Ask @architect
- **Technical approach** → Ask relevant specialist agent
- **Priority conflicts** → Refer to this document's priority queue
- **Cross-agent dependencies** → Check collaboration patterns section

**This is a living document.** As development progresses, agents should update their sections with learnings, decisions, and progress.

---

**Last Updated:** November 1, 2025  
**Document Owner:** @architect  
**Status:** Active Development - Phase 2 Starting  
**Next Review:** Weekly (every Monday)
