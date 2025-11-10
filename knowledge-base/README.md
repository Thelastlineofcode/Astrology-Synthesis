# Mula Knowledge Base

Welcome to the Mula knowledge base repository. This contains documentation for all three product offerings.

## Products

### 1. Personal Development Tool
**Path:** `personal-development/`
**Description:** HR-compliant B2B coaching and wellness platform using numerology and astrology

**Key Documentation:**
- [API Quick Start](personal-development/technical/api-quick-start.md)
- [Compliance Guide](personal-development/compliance/legal-positioning.md)
- [Sales One-Pager](personal-development/sales/one-pager.md)
- [Numerology Interpretations](personal-development/interpretations/life-path-numbers.md)

### 2. Synastry Tool
**Path:** `synastry/`
**Description:** Relationship compatibility analysis for coaches, therapists, and dating platforms

**Key Documentation:**
- [API Reference](synastry/technical/api-reference.md)
- [Compatibility Methodology](synastry/product/compatibility-explained.md)
- [Aspect Interpretations](synastry/interpretations/aspects.md)
- [Use Cases](synastry/sales/use-cases.md)

### 3. Core Mula Platform
**Path:** `core-platform/`
**Description:** Birth chart calculation engine with Vedic, KP, and Western astrology

**Key Documentation:**
- [Calculation API](core-platform/technical/calculation-api.md)
- [Vedic Astrology Primer](core-platform/astrological-systems/vedic-primer.md)
- [KP System Reference](core-platform/astrological-systems/kp-system.md)
- [Integration Guide](core-platform/integration/getting-started.md)

## Directory Structure

```
knowledge-base/
├── personal-development/
│   ├── technical/          # API docs, integration guides
│   ├── product/            # Feature docs, user guides
│   ├── compliance/         # Legal, privacy, disclaimers
│   ├── sales/              # Pitch decks, one-pagers
│   ├── training/           # Facilitator guides, workshops
│   └── interpretations/    # Numerology content
│
├── synastry/
│   ├── technical/          # API docs
│   ├── product/            # Feature docs
│   ├── sales/              # Marketing materials
│   └── interpretations/    # Astrological content
│
└── core-platform/
    ├── technical/          # API docs
    ├── astrological-systems/ # Vedic, KP, Western
    ├── integration/        # Integration guides
    └── research/           # Accuracy reports, validation
```

## Contributing

When adding new documentation:

1. **Choose the right location** based on audience and purpose
2. **Use clear, descriptive filenames** (kebab-case.md)
3. **Start with a summary** at the top of each doc
4. **Include examples** wherever possible
5. **Link to related docs** for easy navigation
6. **Update this README** when adding major new sections

## Access Control

- **Public:** API documentation, user guides (in /technical and /product)
- **Customer-Only:** Advanced integration guides, training materials
- **Internal-Only:** Sales materials, business strategy, compliance templates
- **Founder-Only:** Contracts, sensitive legal matters

## Building the Docs Site

This knowledge base can be published as a static site:

### Option 1: MkDocs
```bash
pip install mkdocs mkdocs-material
mkdocs serve  # Local preview
mkdocs build  # Build static site
```

### Option 2: Docusaurus
```bash
npx create-docusaurus@latest docs-site classic
# Copy knowledge-base/ content to docs/
npm start  # Local preview
npm run build  # Build static site
```

### Option 3: GitHub Pages
Simply push to GitHub and enable Pages in settings.

## Maintenance

- **Review quarterly:** Ensure accuracy and relevance
- **Update with releases:** Keep API docs in sync with code
- **Track versions:** Note which product version docs apply to
- **Archive old versions:** Keep historical docs in /archive

## Questions?

Contact the documentation team or open an issue in the main repository.
