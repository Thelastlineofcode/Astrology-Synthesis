# PDF to Markdown Conversion Guide

## Quick Start (Easiest Method)

### Option 1: Simple Bash Script (Fast)

```bash
# Install dependencies
brew install poppler

# Make script executable
chmod +x scripts/convert_pdfs_to_markdown.sh

# Run conversion
./scripts/convert_pdfs_to_markdown.sh
```

### Option 2: Advanced Python Script (Better Quality)

```bash
# Install dependencies
brew install poppler pandoc
pip install pdfminer.six

# Run conversion
python3 scripts/convert_pdfs_advanced.py
```

### Option 3: AI-Powered (Best Quality, Slow)

```bash
# Install marker-pdf (uses AI/ML for better accuracy)
pip install marker-pdf

# Run with marker option
python3 scripts/convert_pdfs_advanced.py
# Select option 3 when prompted
```

---

## Conversion Methods Comparison

| Method         | Speed       | Quality              | Best For                      |
| -------------- | ----------- | -------------------- | ----------------------------- |
| **pdftotext**  | ⚡ Fast     | ⭐ Basic             | Simple text PDFs              |
| **pandoc**     | ⚡⚡ Medium | ⭐⭐⭐ Good          | Formatted documents           |
| **marker-pdf** | 🐌 Slow     | ⭐⭐⭐⭐⭐ Excellent | Complex layouts, scanned PDFs |

---

## What Each Tool Does

### pdftotext (Poppler)

- **Pros**: Very fast, simple, works on most PDFs
- **Cons**: Basic formatting, no tables/images
- **Good for**: Plain text books like Vedic astrology texts
- **Install**: `brew install poppler`

### Pandoc

- **Pros**: Better formatting, preserves structure
- **Cons**: May struggle with complex layouts
- **Good for**: Academic papers, structured documents
- **Install**: `brew install pandoc`

### Marker (AI-powered)

- **Pros**: Best quality, handles tables/equations/images
- **Cons**: Very slow (5-10 min per PDF), requires GPU for speed
- **Good for**: Scanned PDFs, complex layouts, critical documents
- **Install**: `pip install marker-pdf`

---

## Usage Examples

### Convert All PDFs (Default Method)

```bash
python3 scripts/convert_pdfs_advanced.py
# Press Enter to use pdftotext (fastest)
```

### Convert Specific Directory

```bash
# Bash script
./scripts/convert_pdfs_to_markdown.sh /path/to/pdfs

# Python script (edit KNOWLEDGE_BASE path in script)
```

### Selective Conversion (Only Vedic Books)

```bash
# Convert only 03_vedic_advanced folder
find /Users/houseofobi/Documents/GitHub/Astrology-Synthesis/knowledge_base/texts/03_vedic_advanced -name "*.pdf" -exec pdftotext -layout {} {}.md \;
```

### Batch Convert with Quality Check

```python
# After running conversion, check quality of a sample:
less /path/to/converted.md
# If quality is poor, delete .md files and retry with pandoc or marker
```

---

## Expected Results

### Your Knowledge Base Structure

```
knowledge_base/texts/
├── 01_voodoo_spiritual_apex/
│   ├── Vodou_Visions.pdf
│   └── Vodou_Visions.md          ✓ Already converted!
├── 02_vedic_core/
│   ├── Secrets_Nakshatras.pdf
│   └── Secrets_Nakshatras.md     ← Will be created
├── 03_vedic_advanced/
│   ├── Hindu_Predictive_Astrology_BV_Raman.pdf
│   └── Hindu_Predictive_Astrology_BV_Raman.md  ← Will be created
└── ...
```

### Conversion Stats (Estimated)

- **~150 PDFs** in your knowledge base
- **pdftotext**: ~5-10 minutes total
- **pandoc**: ~15-20 minutes total
- **marker**: ~10-15 hours total (use selectively!)

---

## Quality Verification

After conversion, check a few samples:

```bash
# View first 100 lines of converted file
head -100 /path/to/converted.md

# Check file size (should be reasonable)
ls -lh /path/to/converted.md

# Search for specific content
grep -i "chart" /path/to/converted.md
```

### Red Flags (Poor Conversion):

- Garbled text: `H e l l o W o r l d`
- Missing line breaks
- Random symbols: `□ ■ ◆`
- Very small file size (< 10KB for 200+ page book)

If you see these issues, try:

1. Use pandoc instead of pdftotext
2. Try marker for that specific PDF
3. PDF might be scanned (need OCR)

---

## Handling Scanned PDFs (OCR Required)

Some PDFs are scanned images, not text. For these:

```bash
# Install OCR tools
brew install tesseract
pip install ocrmypdf

# Convert scanned PDF
ocrmypdf input.pdf output.pdf  # Makes PDF searchable
pdftotext output.pdf output.md # Then convert to markdown
```

---

## Automation Tips

### Convert Only New PDFs

The scripts automatically skip existing `.md` files. To reconvert:

```bash
# Delete old markdown files first
find knowledge_base/texts -name "*.md" -delete

# Then run conversion again
python3 scripts/convert_pdfs_advanced.py
```

### Schedule Nightly Conversion

Add to crontab:

```bash
# Run conversion every night at 2 AM
0 2 * * * cd /path/to/Mula && python3 scripts/convert_pdfs_advanced.py >> conversion.log 2>&1
```

---

## Troubleshooting

### "pdftotext: command not found"

```bash
brew install poppler
```

### "Permission denied"

```bash
chmod +x scripts/convert_pdfs_to_markdown.sh
```

### "No such file or directory"

Check the `KNOWLEDGE_BASE` path in the script matches your setup.

### "Conversion failed" for specific PDF

Try these in order:

1. Open PDF in Preview - is it readable?
2. Try pandoc instead of pdftotext
3. Try marker for AI-powered conversion
4. PDF might be encrypted or corrupted

### Empty or Garbled Output

- PDF is scanned images → Use OCR first
- PDF has DRM protection → Remove protection first
- PDF has custom encoding → Try marker

---

## Performance Optimization

### Parallel Processing (Much Faster!)

```bash
# Convert multiple PDFs in parallel
find knowledge_base/texts -name "*.pdf" | \
  parallel -j 4 'pdftotext -layout {} {.}.md'
```

Requires: `brew install parallel`

### GPU Acceleration (For Marker)

If using marker with many PDFs:

```bash
# Install CUDA support for faster processing
pip install marker-pdf[cuda]
```

---

## After Conversion

### Verify Quality

```bash
# Count converted files
find knowledge_base/texts -name "*.md" | wc -l

# Check total size
du -sh knowledge_base/texts/*.md

# Sample random file
find knowledge_base/texts -name "*.md" | shuf -n 1 | xargs less
```

### Update Your Code

Now you can search markdown files instead of PDFs:

```python
# Search all knowledge base
grep -r "chart wheel" knowledge_base/texts/**/*.md

# Load in Python
with open("path/to/book.md") as f:
    content = f.read()
    # Parse and extract...
```

---

## Recommended Approach

For your ~150 PDFs, I recommend:

**Phase 1: Bulk Conversion (Fast)**

```bash
brew install poppler
python3 scripts/convert_pdfs_advanced.py
# Choose option 1 (pdftotext)
# ~10 minutes total
```

**Phase 2: Quality Check (Manual)**

- Spot check 5-10 random converted files
- Identify any problematic PDFs

**Phase 3: Selective Re-conversion (For Problem Files)**

```bash
# For 3-5 files that didn't convert well:
pip install marker-pdf
# Convert those specific ones with marker
```

This gives you 95% good quality in 10 minutes, then spend extra time on the 5% that need it.

---

## Next Steps

After conversion completes:

1. ✅ All PDFs → Markdown ✓
2. 🔍 Search is now instant (grep, ag, ripgrep)
3. 🤖 AI can read markdown easily
4. 📊 Build vector embeddings for semantic search
5. 🧠 Extract correspondences for your unified interpreter
6. 💾 Much smaller file sizes (text vs PDF)

Ready to convert! 🚀
