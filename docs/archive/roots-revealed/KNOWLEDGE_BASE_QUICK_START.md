# Quick Start: Knowledge Base & Interpretive Engine Implementation

**Status:** Ready to Begin  
**Estimated Duration:** 4-6 weeks (phased)  
**Created:** November 2, 2025

---

## 📋 Executive Summary

This document provides a step-by-step quick start guide to implement the Knowledge Base and Interpretive Engine alongside the completion of Phase 3 Week 3.

### Current State

```
✅ Phase 3 Weeks 1-2: COMPLETE
   - Database: 15 tables, 64 indices
   - Authentication: 22/22 tests passing
   - API Framework: 17 endpoints
   - Calculation Service: Core working

⏳ Phase 3 Week 3: IN PROGRESS (parallel track)
   - Fix calculation tests (delegated)
   - Integration tests (delegated)
   - Docker & CI/CD (delegated)

🆕 NEW TRACK: Knowledge Base & Interpretive Engine
   - Can start immediately in parallel
   - 4-6 weeks to full implementation
   - Phases 1-3 well-defined
```

### What You'll Build

1. **Knowledge Base System** (Weeks 1-2)
   - Process 50+ astrological texts
   - Create semantic search capabilities
   - Build concept graph

2. **Interpretation Engine** (Weeks 3-5)
   - Generate natural language interpretations
   - Integrate with LLM (OpenAI/Anthropic)
   - Create hybrid interpretation strategies

3. **API Layer** (Week 6)
   - 10+ new endpoints
   - Full integration with existing system
   - Production-ready deployment

---

## 🚀 Getting Started (Today)

### Step 1: Review the Plan

**Time:** 20 minutes

```bash
# Read the comprehensive plan
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
cat KNOWLEDGE_BASE_INTERPRETIVE_ENGINE_PLAN.md | head -100
```

**Key sections to understand:**

- Section 1: Vision & current state
- Section 2: Knowledge base architecture
- Section 3: Interpretation engine design
- Section 4: API endpoints

### Step 2: Setup LLM Access

**Time:** 10 minutes

Choose one (or both):

**Option A: OpenAI (Recommended)**

```bash
# 1. Create account at https://openai.com/api/
# 2. Generate API key
# 3. Add to .env
export OPENAI_API_KEY="sk-..."
export LLM_MODEL="gpt-4-turbo-preview"
export LLM_PROVIDER="openai"

# 4. Test connection
python << 'EOF'
import openai
openai.api_key = "sk-..."
response = openai.ChatCompletion.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response)
EOF
```

**Option B: Local Llama 2 (Free)**

```bash
# Install ollama from https://ollama.ai
brew install ollama

# Pull Llama 2 model
ollama pull llama2

# Run server
ollama serve

# Update .env
export LLM_PROVIDER="local"
export LLM_BASE_URL="http://localhost:11434"
```

### Step 3: Create Development Branches

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis

# Create feature branch for knowledge base
git checkout -b feature/knowledge-base-implementation

# Create branches for each phase
git checkout -b feature/knowledge-base-phase1-extraction
git checkout -b feature/knowledge-base-phase2-interpretation
git checkout -b feature/knowledge-base-phase3-api
```

---

## 📊 Phase 1: Knowledge Base Setup (Weeks 1-2)

### Day 1: Project Structure & Dependencies

**Tasks:**

1. **Create new service structure**

```bash
mkdir -p backend/services/knowledge/
mkdir -p backend/utils/text_processing/
mkdir -p backend/data/knowledge_index/
mkdir -p tests/knowledge/
```

2. **Create requirements for knowledge services**

```bash
# Create backend/requirements-knowledge.txt
cat > backend/requirements-knowledge.txt << 'EOF'
# PDF Processing
PyPDF2==3.0.1
pdfplumber==0.9.0

# EPUB Processing
ebooklib==0.18.0
lxml==4.9.2

# Embeddings & Vector Search
sentence-transformers==2.2.2
numpy==1.24.0
faiss-cpu==1.7.4

# LLM Integration
openai==1.0.0
anthropic==0.9.0

# Language Processing
nltk==3.8.1
spacy==3.6.1

# Utilities
tqdm==4.65.0
pandas==2.0.0
EOF

# Install
pip install -r backend/requirements-knowledge.txt
```

3. **Download spacy model**

```bash
python -m spacy download en_core_web_sm
```

### Day 2: Text Extraction Pipeline

**Create `backend/utils/text_processing/extractor.py`:**

```python
"""
Text extraction from PDFs, EPUBs, and markdown files
"""

import os
from pathlib import Path
from typing import List, Dict
import PyPDF2
from ebooklib import epub
import spacy
from tqdm import tqdm

class TextExtractor:
    """Extract text from various document formats"""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.knowledge_base_path = Path("knowledge_base")

    def extract_all_texts(self) -> List[Dict]:
        """Extract texts from all sources"""
        all_texts = []

        # Process PDFs
        pdf_files = list(self.knowledge_base_path.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files")
        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            texts = self.extract_pdf(pdf_file)
            all_texts.extend(texts)

        # Process EPUBs
        epub_files = list(self.knowledge_base_path.glob("*.epub"))
        print(f"Found {len(epub_files)} EPUB files")
        for epub_file in tqdm(epub_files, desc="Processing EPUBs"):
            texts = self.extract_epub(epub_file)
            all_texts.extend(texts)

        # Process Markdown
        md_files = list(self.knowledge_base_path.glob("*.md"))
        print(f"Found {len(md_files)} Markdown files")
        for md_file in tqdm(md_files, desc="Processing Markdown"):
            texts = self.extract_markdown(md_file)
            all_texts.extend(texts)

        print(f"Total texts extracted: {len(all_texts)}")
        return all_texts

    def extract_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extract text from PDF"""
        texts = []
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        texts.append({
                            'source': pdf_path.name,
                            'page': page_num + 1,
                            'content': text,
                            'type': 'pdf'
                        })
        except Exception as e:
            print(f"Error extracting {pdf_path}: {e}")
        return texts

    def extract_epub(self, epub_path: Path) -> List[Dict]:
        """Extract text from EPUB"""
        texts = []
        try:
            book = epub.read_epub(epub_path)
            for item in book.get_items():
                if item.get_type() == 9:  # ITEM_DOCUMENT
                    text = item.get_content().decode('utf-8')
                    if text.strip():
                        texts.append({
                            'source': epub_path.name,
                            'chapter': item.get_name(),
                            'content': text,
                            'type': 'epub'
                        })
        except Exception as e:
            print(f"Error extracting {epub_path}: {e}")
        return texts

    def extract_markdown(self, md_path: Path) -> List[Dict]:
        """Extract text from Markdown"""
        texts = []
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    texts.append({
                        'source': md_path.name,
                        'content': content,
                        'type': 'markdown'
                    })
        except Exception as e:
            print(f"Error extracting {md_path}: {e}")
        return texts

# Usage
if __name__ == "__main__":
    extractor = TextExtractor()
    all_texts = extractor.extract_all_texts()

    # Save extracted texts
    import json
    with open("backend/data/knowledge_index/extracted_texts.json", "w") as f:
        json.dump(all_texts, f, indent=2)

    print(f"Extracted {len(all_texts)} text chunks")
```

**Run extraction:**

```bash
cd backend
python utils/text_processing/extractor.py
```

### Day 3: Semantic Chunking

**Create `backend/utils/text_processing/chunker.py`:**

```python
"""
Semantic chunking with context preservation
"""

import spacy
from typing import List, Dict
import json

class SemanticChunker:
    """Split texts into semantic chunks with context"""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.nlp = spacy.load("en_core_web_sm")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_texts(self, texts: List[Dict]) -> List[Dict]:
        """Convert extracted texts to semantic chunks"""
        chunks = []
        chunk_id = 0

        for text_item in texts:
            doc = self.nlp(text_item['content'])

            # Split by sentences
            sentences = list(doc.sents)
            current_chunk = []
            current_length = 0

            for sent in sentences:
                sent_length = len(sent.text)

                if current_length + sent_length > self.chunk_size:
                    if current_chunk:
                        chunk_text = " ".join([s.text for s in current_chunk])
                        chunks.append({
                            'id': f"chunk_{chunk_id}",
                            'content': chunk_text,
                            'source': text_item['source'],
                            'page': text_item.get('page', 0),
                            'tokens': len(chunk_text.split()),
                            'metadata': text_item
                        })
                        chunk_id += 1

                        # Keep overlap
                        overlap_size = 0
                        for overlap_sent in reversed(current_chunk):
                            if overlap_size + len(overlap_sent.text) > self.overlap:
                                break
                            overlap_size += len(overlap_sent.text)
                        current_chunk = current_chunk[-1:] if current_chunk else []
                        current_length = overlap_size

                current_chunk.append(sent)
                current_length += sent_length

            # Add remaining chunk
            if current_chunk:
                chunk_text = " ".join([s.text for s in current_chunk])
                chunks.append({
                    'id': f"chunk_{chunk_id}",
                    'content': chunk_text,
                    'source': text_item['source'],
                    'metadata': text_item
                })
                chunk_id += 1

        return chunks

# Usage
if __name__ == "__main__":
    # Load extracted texts
    with open("backend/data/knowledge_index/extracted_texts.json", "r") as f:
        texts = json.load(f)

    # Chunk them
    chunker = SemanticChunker(chunk_size=1000, overlap=200)
    chunks = chunker.chunk_texts(texts)

    # Save chunks
    with open("backend/data/knowledge_index/chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"Created {len(chunks)} chunks")
```

**Run chunking:**

```bash
cd backend
python utils/text_processing/chunker.py
```

### Days 4-5: Embedding Generation & Vector Index

**Create `backend/services/knowledge/embedding_service.py`:**

```python
"""
Generate embeddings and build vector index
"""

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
from tqdm import tqdm

class EmbeddingService:
    """Generate embeddings and manage vector index"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunks_metadata = []

    def generate_embeddings(self, chunks: list) -> tuple:
        """Generate embeddings for all chunks"""
        embeddings = []

        print(f"Generating embeddings for {len(chunks)} chunks...")
        for chunk in tqdm(chunks, desc="Embedding"):
            embedding = self.model.encode(
                chunk['content'],
                convert_to_numpy=True
            )
            embeddings.append(embedding)
            self.chunks_metadata.append({
                'id': chunk['id'],
                'source': chunk['source'],
                'preview': chunk['content'][:200]
            })

        return np.array(embeddings), self.chunks_metadata

    def build_index(self, embeddings: np.ndarray) -> faiss.IndexFlatL2:
        """Build FAISS index"""
        print(f"Building FAISS index with {len(embeddings)} embeddings...")
        index = faiss.IndexFlatL2(self.embedding_dim)
        index.add(embeddings)
        return index

    def search(self, query: str, top_k: int = 5) -> list:
        """Search for similar chunks"""
        if self.index is None:
            raise ValueError("Index not initialized")

        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True
        ).reshape(1, -1)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks_metadata):
                results.append({
                    'chunk_id': self.chunks_metadata[idx]['id'],
                    'source': self.chunks_metadata[idx]['source'],
                    'preview': self.chunks_metadata[idx]['preview'],
                    'distance': float(distance)
                })

        return results

# Usage
if __name__ == "__main__":
    # Load chunks
    with open("backend/data/knowledge_index/chunks.json", "r") as f:
        chunks = json.load(f)

    # Generate embeddings
    embedding_service = EmbeddingService()
    embeddings, metadata = embedding_service.generate_embeddings(chunks)

    # Build index
    index = embedding_service.build_index(embeddings)

    # Save index
    faiss.write_index(index, "backend/data/knowledge_index/index.faiss")

    with open("backend/data/knowledge_index/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved index with {len(embeddings)} vectors")

    # Test search
    test_queries = [
        "Sun in Scorpio",
        "Moon aspects",
        "Dasha predictions"
    ]

    embedding_service.index = index
    for query in test_queries:
        results = embedding_service.search(query, top_k=3)
        print(f"\nQuery: {query}")
        for r in results:
            print(f"  - {r['source']}: {r['preview'][:50]}...")
```

**Run embedding generation:**

```bash
cd backend
python services/knowledge/embedding_service.py
```

### Days 5-6: Full-Text Search & Knowledge Service

**Create `backend/services/knowledge/knowledge_service.py`:**

```python
"""
Main knowledge service with semantic and keyword search
"""

import json
import sqlite3
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class KnowledgeService:
    """Main service for knowledge base operations"""

    def __init__(self, data_path: str = "backend/data/knowledge_index"):
        self.data_path = Path(data_path)
        self.embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load vector index
        self.vector_index = faiss.read_index(str(self.data_path / "index.faiss"))

        # Load metadata
        with open(self.data_path / "metadata.json", "r") as f:
            self.metadata = json.load(f)

        # Setup FTS database
        self.fts_db_path = self.data_path / "knowledge_fts.db"
        self._setup_fts()

    def _setup_fts(self):
        """Setup SQLite FTS for full-text search"""
        conn = sqlite3.connect(self.fts_db_path)
        cursor = conn.cursor()

        # Create FTS table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                chunk_id, source, content
            )
        """)

        # Load chunks and index
        with open(self.data_path / "chunks.json", "r") as f:
            chunks = json.load(f)

        for chunk in chunks:
            cursor.execute(
                "INSERT INTO chunks_fts VALUES (?, ?, ?)",
                (chunk['id'], chunk['source'], chunk['content'])
            )

        conn.commit()
        conn.close()

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search using semantic similarity"""
        query_embedding = self.embeddings_model.encode(query)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')

        distances, indices = self.vector_index.search(query_embedding, top_k)

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                results.append({
                    'type': 'semantic',
                    'chunk_id': self.metadata[idx]['id'],
                    'source': self.metadata[idx]['source'],
                    'preview': self.metadata[idx]['preview'],
                    'score': float(distance)
                })

        return results

    def keyword_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search using full-text search"""
        conn = sqlite3.connect(self.fts_db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT chunk_id, source, content FROM chunks_fts
            WHERE chunks_fts MATCH ?
            LIMIT ?
        """, (query, top_k))

        results = []
        for row in cursor.fetchall():
            results.append({
                'type': 'keyword',
                'chunk_id': row[0],
                'source': row[1],
                'preview': row[2][:200] + "..."
            })

        conn.close()
        return results

    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Combine semantic and keyword search"""
        semantic_results = self.semantic_search(query, top_k=3)
        keyword_results = self.keyword_search(query, top_k=3)

        # Deduplicate
        seen_ids = set()
        combined = []

        for result in semantic_results + keyword_results:
            if result['chunk_id'] not in seen_ids:
                combined.append(result)
                seen_ids.add(result['chunk_id'])

        return combined[:top_k]

# Usage
if __name__ == "__main__":
    service = KnowledgeService()

    # Test searches
    test_queries = [
        "Sun in Scorpio personality",
        "Moon compatibility",
        "Dasha cycles predictions"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)

        results = service.hybrid_search(query, top_k=3)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. [{result['type'].upper()}] {result['source']}")
            print(f"   {result['preview'][:100]}...")
```

**Run knowledge service setup:**

```bash
cd backend
python services/knowledge/knowledge_service.py
```

### Days 6-7: Testing & Documentation

**Create `tests/knowledge/test_knowledge_service.py`:**

```python
"""Tests for knowledge service"""

import pytest
from backend.services.knowledge.knowledge_service import KnowledgeService

@pytest.fixture
def knowledge_service():
    return KnowledgeService()

def test_semantic_search(knowledge_service):
    results = knowledge_service.semantic_search("Sun in Scorpio", top_k=5)
    assert len(results) > 0
    assert results[0]['type'] == 'semantic'

def test_keyword_search(knowledge_service):
    results = knowledge_service.keyword_search("astrology", top_k=5)
    assert len(results) > 0
    assert results[0]['type'] == 'keyword'

def test_hybrid_search(knowledge_service):
    results = knowledge_service.hybrid_search("Moon compatibility", top_k=5)
    assert len(results) > 0
    assert len(results) <= 5
```

**Run tests:**

```bash
cd backend
pytest tests/knowledge/ -v
```

---

## 📖 Phase 2: Interpretation Engine (Weeks 3-5)

### Overview

Once Phase 1 is complete, you'll have:

- ✅ 50+ texts processed
- ✅ 10,000+ chunks created
- ✅ Semantic + keyword search working
- ✅ Vector index ready

Now build the interpretation engine that **uses** this knowledge base.

### Implementation Steps (High-Level)

1. **Create InterpretationService** (Week 3)
   - Template-based strategies
   - Knowledge retrieval strategies
   - Caching layer

2. **Integrate LLM** (Week 4)
   - OpenAI/Anthropic integration
   - Prompt templates
   - Confidence scoring

3. **Build Hybrid System** (Week 5)
   - Multi-strategy synthesis
   - Context builders
   - Testing & optimization

---

## 🔌 Phase 3: API Integration (Week 6)

### New Endpoints

```python
# Knowledge endpoints
GET  /api/v1/knowledge/search?query=...
GET  /api/v1/knowledge/concepts
GET  /api/v1/knowledge/concepts/{concept_name}
GET  /api/v1/knowledge/sources

# Interpretation endpoints
POST /api/v1/interpretations/chart
POST /api/v1/interpretations/planet
POST /api/v1/interpretations/aspect
POST /api/v1/interpretations/synastry
GET  /api/v1/charts/{id}/interpret
```

---

## ✅ Verification Checklist

### Phase 1 Complete Checklist

- [ ] All 50+ texts extracted (check `extracted_texts.json`)
- [ ] Chunks created (check `chunks.json`, 10,000+ expected)
- [ ] Embeddings generated (check `index.faiss` file exists)
- [ ] Vector search working (<100ms response time)
- [ ] Full-text search working (keyword queries return results)
- [ ] Hybrid search working (combines results appropriately)
- [ ] Tests passing (`pytest tests/knowledge/ -v`)

### Phase 2 Complete Checklist

- [ ] InterpretationService created
- [ ] 3+ strategies implemented
- [ ] LLM integration working
- [ ] Caching reducing response times
- [ ] 50+ passing interpretation tests

### Phase 3 Complete Checklist

- [ ] 10+ new endpoints created
- [ ] All endpoints returning correct responses
- [ ] Integration tests passing
- [ ] Error handling comprehensive
- [ ] Performance <500ms P95

---

## 🔧 Debugging & Common Issues

### Issue: Embedding generation too slow

**Solution:**

```bash
# Use GPU if available
export CUDA_VISIBLE_DEVICES=0
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Or use smaller model
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
```

### Issue: LLM API costs too high

**Solution:**

```bash
# Use local model instead
export LLM_PROVIDER=local
# Run: ollama pull llama2-7b
# Run: ollama serve
```

### Issue: Vector search not finding relevant results

**Solution:**

```python
# Try different embedding models
models = [
    "all-MiniLM-L6-v2",  # Fast, general purpose
    "all-mpnet-base-v2",  # More accurate but slower
    "allenai-specter",    # Science-optimized
]

# Experiment and compare results
```

---

## 📞 Support & Resources

### Documentation

- Full plan: `KNOWLEDGE_BASE_INTERPRETIVE_ENGINE_PLAN.md`
- This guide: `KNOWLEDGE_BASE_QUICK_START.md`
- API docs: Will be generated during Phase 3

### Tools & Libraries

- **Embeddings:** sentence-transformers
- **Vector DB:** FAISS (local), Milvus (production)
- **LLM:** OpenAI, Anthropic, local Llama
- **Search:** SQLite FTS5
- **Testing:** pytest

### Getting Help

1. Check the comprehensive plan first
2. Review implementation examples in this guide
3. Test each phase incrementally
4. Use `pytest` for validation

---

## 🎯 Success Criteria

**By Week 2:** Knowledge base fully indexed and searchable
**By Week 5:** Interpretations generating with LLM
**By Week 6:** All APIs live and tested
**By Week 7:** Production-ready deployment

---

**Status:** Ready to Implement  
**Created:** November 2, 2025  
**Estimated Timeline:** 4-6 weeks  
**Next Action:** Day 1 - Create project structure & install dependencies
