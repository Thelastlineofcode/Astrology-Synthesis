#!/bin/bash

# PDF to Markdown Batch Converter
# Converts all PDFs in knowledge base to markdown files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Source and destination directories
KNOWLEDGE_BASE="/Users/houseofobi/Documents/GitHub/Astrology-Synthesis/knowledge_base/texts"
LOG_FILE="pdf_conversion.log"

echo -e "${GREEN}PDF to Markdown Conversion Script${NC}"
echo "======================================"

# Check if required tools are installed
check_dependencies() {
    echo "Checking dependencies..."
    
    if ! command -v pdftotext &> /dev/null; then
        echo -e "${RED}Error: pdftotext not found${NC}"
        echo "Install with: brew install poppler"
        exit 1
    fi
    
    if ! command -v pandoc &> /dev/null; then
        echo -e "${YELLOW}Warning: pandoc not found (optional but recommended)${NC}"
        echo "Install with: brew install pandoc"
    fi
    
    echo -e "${GREEN}✓ Dependencies OK${NC}"
}

# Convert single PDF to markdown
convert_pdf() {
    local pdf_file="$1"
    local base_name=$(basename "$pdf_file" .pdf)
    local dir_name=$(dirname "$pdf_file")
    local md_file="${dir_name}/${base_name}.md"
    
    echo -e "\n${YELLOW}Converting:${NC} $base_name.pdf"
    
    # Skip if markdown already exists
    if [ -f "$md_file" ]; then
        echo -e "${YELLOW}  ⊘ Skipping - markdown already exists${NC}"
        return
    fi
    
    # Method 1: pdftotext (simple, fast)
    if pdftotext -layout "$pdf_file" "$md_file" 2>/dev/null; then
        echo -e "${GREEN}  ✓ Converted successfully${NC}"
        
        # Get file sizes for comparison
        pdf_size=$(du -h "$pdf_file" | cut -f1)
        md_size=$(du -h "$md_file" | cut -f1)
        echo "    PDF: $pdf_size → Markdown: $md_size"
        
        # Log success
        echo "$(date '+%Y-%m-%d %H:%M:%S') SUCCESS $base_name.pdf" >> "$LOG_FILE"
        return 0
    else
        echo -e "${RED}  ✗ Conversion failed${NC}"
        echo "$(date '+%Y-%m-%d %H:%M:%S') FAILED $base_name.pdf" >> "$LOG_FILE"
        return 1
    fi
}

# Main conversion function
main() {
    check_dependencies
    
    # Clear log file
    > "$LOG_FILE"
    
    echo -e "\n${GREEN}Searching for PDFs...${NC}"
    
    # Find all PDFs in knowledge base
    local pdf_count=0
    local success_count=0
    local skip_count=0
    
    while IFS= read -r -d '' pdf_file; do
        ((pdf_count++))
        if convert_pdf "$pdf_file"; then
            ((success_count++))
        fi
    done < <(find "$KNOWLEDGE_BASE" -type f -name "*.pdf" -print0)
    
    # Summary
    echo -e "\n======================================"
    echo -e "${GREEN}Conversion Summary${NC}"
    echo "Total PDFs found: $pdf_count"
    echo "Successfully converted: $success_count"
    echo "Failed: $((pdf_count - success_count))"
    echo "Log file: $LOG_FILE"
    
    # Show which ones failed
    if [ $((pdf_count - success_count)) -gt 0 ]; then
        echo -e "\n${RED}Failed conversions:${NC}"
        grep "FAILED" "$LOG_FILE" | cut -d' ' -f4-
    fi
}

# Run with specific directory if provided
if [ $# -eq 1 ]; then
    KNOWLEDGE_BASE="$1"
fi

main
