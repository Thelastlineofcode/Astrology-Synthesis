# How to Use These Research Prompts

## Quick Start: Conducting the Deep Research

You now have two comprehensive documents:

1. **`RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md`** (2,500+ words)
   - High-level system architecture
   - Part-by-part breakdown of Koch, Horoscope Generation, Multi-layered Prediction, Validation
   - Each section has research areas with specific questions to answer

2. **`RESEARCH_DEEP_DIVE_QUESTIONS.md`** (2,000+ words)
   - Detailed question sets (12 sections, 100+ specific questions)
   - Practical code templates and examples
   - Test case frameworks
   - Deliverables checklist

---

## OPTION A: Have Me Research These Topics

**How to request:**

```
@architect research the following using RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md

Topic: "PART 1: KOCH HOUSE SYSTEM IMPLEMENTATION"
Focus: "Question Set 1-2: Koch mathematical foundations and pyswisseph implementation"

I want:
1. Complete mathematical derivation of Koch formula
2. Practical pyswisseph code examples
3. Comparison table: Koch vs Placidus (differences table, 10 test cases)
4. Validation results against Astro.com (test data)
5. Edge case handling (polar regions, equators)
6. Database schema recommendations
```

**Expected output:**

- 1,500-3,000 word detailed research document
- Python code snippets (tested/pseudocode)
- Comparison tables and charts
- Concrete implementation examples
- Validation test results
- Ready-to-implement recommendations

---

## OPTION B: Research Specific Areas Sequentially

### Session 1: Koch House System Foundation

```
Research the Koch House System using sections:
- RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md: PART 1, Research Areas 1-3
- RESEARCH_DEEP_DIVE_QUESTIONS.md: Question Sets 1-3

Deliver:
1. Mathematical foundation (Koch formula derivation)
2. pyswisseph integration guide (code examples)
3. Comparison: Koch vs. 7 other house systems (accuracy table)
4. Validation framework (how to test against Astro.com)
5. Python implementation module (ready to use)
```

### Session 2: Horoscope Generation Engine

```
Research Horoscope Generation using sections:
- RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md: PART 2
- RESEARCH_DEEP_DIVE_QUESTIONS.md: Question Sets 5-10

Deliver:
1. Transit interpretation dictionary (all aspects + planets)
2. Horoscope structure specification (sections, flow, formatting)
3. Template system design (50+ templates with examples)
4. Event clustering algorithm (pseudocode + walkthrough)
5. Narrative generation module (Python code)
```

### Session 3: Multi-Layer Prediction Integration

```
Research System Integration using sections:
- RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md: PART 3
- RESEARCH_DEEP_DIVE_QUESTIONS.md: Question Sets 11-12

Deliver:
1. Integration architecture (Vedic + Western)
2. Confidence scoring system (algorithm with weights)
3. Conflict resolution strategy (when systems disagree)
4. Edge case handling (retrograde, eclipses, stationary points)
5. Integration test suite (20+ test cases)
```

### Session 4: Validation & Testing

```
Research Validation using sections:
- RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md: PART 4-5
- RESEARCH_DEEP_DIVE_QUESTIONS.md: Section D (Testing)

Deliver:
1. Benchmark strategy (comparison with professional software)
2. Test suite (100+ test cases with expected outputs)
3. Celebrity chart validation (10 famous people, known events)
4. Performance benchmarks (calculations/sec, memory)
5. Quality metrics (accuracy scoring framework)
```

---

## Using the Research Documents

### When Starting Koch Implementation:

1. Read: `RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md` → PART 1
2. Study: `RESEARCH_DEEP_DIVE_QUESTIONS.md` → Question Sets 1-4
3. Request: "Research Koch implementation details - focus on pyswisseph integration"
4. Expected: Detailed guide with code, test cases, validation
5. Apply: Implement using provided code templates

### When Building Horoscope Generator:

1. Read: `RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md` → PART 2
2. Study: `RESEARCH_DEEP_DIVE_QUESTIONS.md` → Question Sets 5-10
3. Request: "Create 100 narrative templates covering all transit scenarios"
4. Expected: Template collection with usage patterns, examples
5. Apply: Build generator using templates

### When Integrating Systems:

1. Read: `RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md` → PART 3
2. Study: `RESEARCH_DEEP_DIVE_QUESTIONS.md` → Question Sets 11-12
3. Request: "Design conflict resolution for Vedic+Western system disagreements"
4. Expected: Algorithm, weighting scheme, test cases
5. Apply: Implement multi-layer scoring

### When Testing/Validating:

1. Read: `RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md` → PART 4-5
2. Study: `RESEARCH_DEEP_DIVE_QUESTIONS.md` → Section D
3. Request: "Generate test suite comparing against Astro.com and JHora"
4. Expected: 100+ test cases with reference data
5. Apply: Run validation, compare results

---

## Making Effective Research Requests

### Bad Request:

```
"Research Koch houses"
```

(Too vague, unclear what you need)

### Good Request:

```
"Using RESEARCH_DEEP_DIVE_QUESTIONS.md Question Set 2,
research pyswisseph implementation for Koch houses.

Provide:
1. Complete function signature and usage example
2. How to extract 12 cusps + ASC + MC + AVX + VX
3. How to verify output is correct (comparison with Astro.com)
4. Code template ready to integrate into calculation_service.py
5. Expected performance (ms per calculation)

Include concrete examples with latitude 40.7N, longitude -74.0W"
```

(Specific, focused, clear deliverables)

### Research Structure Template:

```
Reference Document: [RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md or RESEARCH_DEEP_DIVE_QUESTIONS.md]
Section/Questions: [Specific section or question set numbers]
Topic: [Clear title of research area]

Research Goals:
1. [Specific question 1]
2. [Specific question 2]
3. [Specific question 3]

Deliverables Needed:
1. [Specific output type 1 - e.g., "Python code module"]
2. [Specific output type 2 - e.g., "Comparison table"]
3. [Specific output type 3 - e.g., "Test cases"]

Context:
- [Current system status if relevant]
- [Constraints (performance, accuracy, etc.)]
- [Integration points with existing code]

Example Data to Use:
- Birth date: 1980-07-13 10:30:00
- Location: 40.7128°N, 74.0060°W (New York)
- System: Should match Astro.com within ±0.016°
```

---

## Iterative Research Process

### Cycle 1: Understand

```
Request: "Explain Koch house system basics - what is it, why use it, how differs from Placidus?"
Output: Educational summary, conceptual understanding
Next: Move to implementation questions
```

### Cycle 2: Deep Dive

```
Request: "Provide mathematical derivation of Koch formula with worked examples"
Output: Formulas, step-by-step calculations, code pseudocode
Next: Move to implementation details
```

### Cycle 3: Implement

```
Request: "Write complete Python module for Koch house calculation using pyswisseph"
Output: Production-ready code, docstrings, error handling, test coverage
Next: Move to validation
```

### Cycle 4: Validate

```
Request: "Compare 50 Koch calculations with Astro.com reference data - identify discrepancies"
Output: Validation report, accuracy metrics, edge cases identified
Next: Iterate or move to next component
```

### Cycle 5: Document

```
Request: "Create implementation guide for Koch houses - how to integrate into Mula system"
Output: Documentation, diagrams, troubleshooting guide, API specs
Next: Hand off to implementation team
```

---

## Expected Timelines

### Research Timeline (Using These Prompts)

| Phase     | Topic                   | Research Time   | Deliverable                         |
| --------- | ----------------------- | --------------- | ----------------------------------- |
| 1         | Koch Foundation         | 2-4 hours       | Math foundations + code templates   |
| 2         | pyswisseph Integration  | 2-3 hours       | Working code module + tests         |
| 3         | Horoscope Generation    | 4-6 hours       | 100+ templates + algorithm          |
| 4         | Multi-layer Integration | 3-4 hours       | Conflict resolution + scoring       |
| 5         | Validation & Testing    | 3-5 hours       | Test suite + benchmarks             |
| **Total** | **Full System**         | **14-22 hours** | **Production-ready specifications** |

### Implementation Timeline (After Research)

| Phase     | Task                  | Implementation Time | Team Size    |
| --------- | --------------------- | ------------------- | ------------ |
| 1         | Koch Module           | 8-12 hours          | 1 dev        |
| 2         | Transit Analysis      | 12-16 hours         | 1-2 devs     |
| 3         | Horoscope Generator   | 16-20 hours         | 1-2 devs     |
| 4         | Integration & Testing | 12-16 hours         | 2 devs       |
| 5         | API & Frontend        | 16-20 hours         | 2 devs       |
| **Total** | **Full System**       | **64-84 hours**     | **2-3 devs** |

---

## How Research Maps to Implementation

### Research → Code Mapping

```
RESEARCH PHASE                    CODE DELIVERABLE
────────────────────────────────────────────────────

1. Koch Math Research      →      backend/calculations/koch_houses.py
   (formulas, examples)           - koch_cusp_calculation()
                                  - validate_cusps()
                                  - compare_with_placidus()

2. pyswisseph Integration  →      backend/calculations/ephemeris.py (enhance)
   (function usage, examples)     - class KochHouseCalculator
                                  - method: calculate_koch_cusps()
                                  - method: get_house_placements()

3. Horoscope Templates     →      backend/services/horoscope_templates.py
   (100+ templates)               - NARRATIVE_TEMPLATES dict
                                  - TemplateRenderer class
                                  - personalization_rules()

4. Multi-layer Integration →      backend/services/prediction_engine.py
   (conflict resolution)          - class SyncreticPredictor
                                  - score_from_multiple_sources()
                                  - resolve_conflicts()

5. Testing & Validation    →      tests/test_koch_houses.py
   (test cases, benchmarks)       tests/test_horoscope_generation.py
                                  tests/test_multi_layer_prediction.py
                                  - 200+ test cases
                                  - performance benchmarks
```

---

## What NOT to Do

❌ Request entire system at once ("Build me a horoscope generator")
→ Do: Break into phases - Koch, then Transit, then Templates, then Integration

❌ Request without context ("Research horoscopes")
→ Do: "Using RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md PART 2, research horoscope generation..."

❌ Ignore the test framework
→ Do: Always include validation/testing in research requests

❌ Skip the "why" questions
→ Do: Ask "Why Koch over Placidus?" to understand design decisions

❌ Implement without research complete
→ Do: Complete research first, then use results for implementation

---

## Success Indicators

### Research Phase Complete When:

✅ Can answer all 100+ questions in RESEARCH_DEEP_DIVE_QUESTIONS.md
✅ Have tested code examples for each component
✅ Compared system output with 3+ professional software (Astro.com, JHora, etc.)
✅ Documented edge cases and how to handle them
✅ Created test suite with 200+ cases
✅ Established accuracy/performance benchmarks
✅ Identified integration points and dependencies
✅ Created implementation roadmap with timelines

### Implementation Phase Ready When:

✅ Have complete specifications from research phase
✅ Have test cases ready to validate against
✅ Have reference data for comparison
✅ Have performance targets defined
✅ Have database schema designed
✅ Have API specifications written
✅ Have implementation team trained on context

---

## AI/Researcher Interaction Pattern

**Best Approach for Iterative Research:**

```
You: "Research Koch house system basics"
→ AI: [Provides overview, 500 words]

You: "Deeper - show me the mathematical formula"
→ AI: [Provides derivations, 1000 words]

You: "Now show pyswisseph usage - how to call it"
→ AI: [Provides code examples, 800 words]

You: "Give me a working module I can import"
→ AI: [Provides complete Python module, 1200 words]

You: "How to test this? Compare with Astro.com"
→ AI: [Provides test framework, 1000 words]

You: "Generate 50 test cases with reference data"
→ AI: [Provides test suite, 2000+ words]
```

Each request builds on previous, getting more specific and implementation-ready.

---

## File Organization

```
/Mula/
├── RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md      ← Main system spec
├── RESEARCH_DEEP_DIVE_QUESTIONS.md          ← Detailed Q&A
├── RESEARCH_FINDINGS/                       ← Create this folder
│   ├── koch_research.md                     ← After Koch research
│   ├── horoscope_research.md                ← After Horoscope research
│   ├── integration_research.md              ← After Integration research
│   └── validation_results.md                ← After Testing research
├── backend/
│   ├── calculations/
│   │   ├── koch_houses.py                   ← New module (from research)
│   │   └── ephemeris.py                     ← Enhanced (from research)
│   └── services/
│       ├── horoscope_service.py             ← New module (from research)
│       └── prediction_engine.py             ← Enhanced (from research)
└── tests/
    ├── test_koch_houses.py                  ← New tests (from research)
    ├── test_horoscope_generation.py         ← New tests (from research)
    └── validation_data/                     ← Reference data (from research)
        ├── astro_com_reference.json
        ├── jhora_reference.json
        └── celebrity_charts.json
```

---

## Next Steps

1. **Choose Starting Point:**
   - Option A: Start with Koch research (foundation for everything)
   - Option B: Start with Horoscope templates (quick wins)
   - Option C: Start with Multi-layer integration (understand system vision)

2. **Make First Research Request:**

   ```
   "I want to start with Koch house system research.
   Using RESEARCH_PROMPT_HOROSCOPE_SYSTEM.md and RESEARCH_DEEP_DIVE_QUESTIONS.md,
   please provide:

   1. Mathematical foundation of Koch vs Placidus
   2. pyswisseph implementation examples
   3. How to validate against Astro.com
   4. Complete Python module ready to integrate
   5. Test cases for verification

   Focus on production-ready accuracy (±1 arcminute)"
   ```

3. **Iterate Through Phases:**
   - Complete Koch research + implementation
   - Then move to Horoscope research + implementation
   - Then Multi-layer integration
   - Then Validation & Testing

4. **Document Findings:**
   - Save each research result in RESEARCH_FINDINGS/
   - Keep references to professional software comparisons
   - Document any deviations from standard approaches
   - Create implementation notes for dev team

5. **Build Incrementally:**
   - Each research phase → Working code
   - Each code module → Test suite
   - Each test → Validation results
   - Each validation → Production deployment

---

**These prompts are designed to be used iteratively.**  
**Each research request builds system understanding and produces implementation-ready deliverables.**

**Start with Koch. Master it. Move to next component.**

**Timeline: 2-3 weeks of focused research → Production-ready multi-layered prediction system.**

---

**Document Created**: November 3, 2025  
**Status**: Ready to begin research  
**Estimated Completion**: November 24, 2025 (with dedicated research effort)
