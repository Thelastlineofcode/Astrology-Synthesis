#!/usr/bin/env python3
"""
Advanced PDF to Markdown Converter
Batch converts PDFs with multiple quality options and OCR support
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Configuration
KNOWLEDGE_BASE = Path("/Users/houseofobi/Documents/GitHub/Astrology-Synthesis/knowledge_base/texts")
LOG_FILE = Path("pdf_conversion_log.json")
CONVERSION_LOG = []

# Color codes
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(text, color):
    print(f"{color}{text}{Colors.NC}")

def check_tool(tool_name, install_cmd):
    """Check if a tool is installed"""
    try:
        subprocess.run([tool_name, "--version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_color(f"✗ {tool_name} not found. Install with: {install_cmd}", Colors.YELLOW)
        return False

def check_dependencies():
    """Check for required conversion tools"""
    print_color("\n=== Checking Dependencies ===", Colors.BLUE)
    
    tools = {
        "pdftotext": ("brew install poppler", True),
        "pandoc": ("brew install pandoc", False),
        "marker_single": ("pip install marker-pdf", False),  # Advanced option
        "pdfminer": ("pip install pdfminer.six", False),
    }
    
    available = {}
    for tool, (install_cmd, required) in tools.items():
        if check_tool(tool, install_cmd):
            print_color(f"  ✓ {tool} available", Colors.GREEN)
            available[tool] = True
        else:
            if required:
                print_color(f"  ✗ {tool} REQUIRED - {install_cmd}", Colors.RED)
                return None
            available[tool] = False
    
    return available

def convert_with_pdftotext(pdf_path: Path, md_path: Path) -> bool:
    """Method 1: Simple pdftotext (fast, basic)"""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), str(md_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        print_color(f"    Error: {e}", Colors.RED)
        return False

def convert_with_pandoc(pdf_path: Path, md_path: Path) -> bool:
    """Method 2: Pandoc (better formatting)"""
    try:
        result = subprocess.run(
            ["pandoc", str(pdf_path), "-o", str(md_path), "--wrap=none"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0
    except Exception as e:
        print_color(f"    Error: {e}", Colors.RED)
        return False

def convert_with_marker(pdf_path: Path, md_path: Path) -> bool:
    """Method 3: Marker (AI-powered, best quality but slow)"""
    try:
        # marker_single input.pdf output_dir --batch_multiplier 2
        result = subprocess.run(
            ["marker_single", str(pdf_path), str(md_path.parent)],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0
    except Exception as e:
        print_color(f"    Error: {e}", Colors.RED)
        return False

def get_file_size(path: Path) -> str:
    """Get human-readable file size"""
    size = path.stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"

def convert_pdf(pdf_path: Path, method: str, available_tools: dict) -> dict:
    """Convert a single PDF to markdown"""
    base_name = pdf_path.stem
    md_path = pdf_path.parent / f"{base_name}.md"
    
    print(f"\n{Colors.YELLOW}Converting:{Colors.NC} {pdf_path.name}")
    
    # Skip if already exists
    if md_path.exists():
        print_color("  ⊘ Skipping - markdown already exists", Colors.YELLOW)
        return {
            "file": str(pdf_path),
            "status": "skipped",
            "reason": "markdown exists",
            "timestamp": datetime.now().isoformat()
        }
    
    # Try conversion with selected method
    start_time = datetime.now()
    success = False
    
    if method == "pdftotext" and available_tools.get("pdftotext"):
        success = convert_with_pdftotext(pdf_path, md_path)
    elif method == "pandoc" and available_tools.get("pandoc"):
        success = convert_with_pandoc(pdf_path, md_path)
    elif method == "marker" and available_tools.get("marker_single"):
        success = convert_with_marker(pdf_path, md_path)
    else:
        # Fallback to pdftotext
        success = convert_with_pdftotext(pdf_path, md_path)
    
    duration = (datetime.now() - start_time).total_seconds()
    
    if success and md_path.exists():
        pdf_size = get_file_size(pdf_path)
        md_size = get_file_size(md_path)
        print_color(f"  ✓ Converted: {pdf_size} → {md_size} ({duration:.1f}s)", Colors.GREEN)
        
        return {
            "file": str(pdf_path),
            "status": "success",
            "method": method,
            "pdf_size": pdf_size,
            "md_size": md_size,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat()
        }
    else:
        print_color(f"  ✗ Conversion failed ({duration:.1f}s)", Colors.RED)
        return {
            "file": str(pdf_path),
            "status": "failed",
            "method": method,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat()
        }

def main():
    print_color("\n╔══════════════════════════════════════╗", Colors.BLUE)
    print_color("║  PDF to Markdown Batch Converter    ║", Colors.BLUE)
    print_color("╚══════════════════════════════════════╝", Colors.BLUE)
    
    # Check dependencies
    available_tools = check_dependencies()
    if available_tools is None:
        sys.exit(1)
    
    # Choose method
    print(f"\nAvailable conversion methods:")
    print("  1. pdftotext (fast, basic formatting)")
    print("  2. pandoc (better formatting)" + ("" if available_tools.get("pandoc") else " [NOT INSTALLED]"))
    print("  3. marker (AI-powered, best quality, slow)" + ("" if available_tools.get("marker_single") else " [NOT INSTALLED]"))
    
    method_choice = input("\nSelect method (1-3, default=1): ").strip() or "1"
    methods = {"1": "pdftotext", "2": "pandoc", "3": "marker"}
    method = methods.get(method_choice, "pdftotext")
    
    print_color(f"\n=== Starting Conversion (method: {method}) ===", Colors.BLUE)
    
    # Find all PDFs
    pdf_files = list(KNOWLEDGE_BASE.rglob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files\n")
    
    # Convert each PDF
    results = []
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}]", end=" ")
        result = convert_pdf(pdf_path, method, available_tools)
        results.append(result)
    
    # Save log
    with open(LOG_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    success_count = sum(1 for r in results if r["status"] == "success")
    skip_count = sum(1 for r in results if r["status"] == "skipped")
    fail_count = sum(1 for r in results if r["status"] == "failed")
    
    print_color("\n╔══════════════════════════════════════╗", Colors.BLUE)
    print_color("║         Conversion Summary           ║", Colors.BLUE)
    print_color("╚══════════════════════════════════════╝", Colors.BLUE)
    print(f"Total PDFs:          {len(pdf_files)}")
    print_color(f"✓ Successfully converted: {success_count}", Colors.GREEN)
    print_color(f"⊘ Skipped (existing):     {skip_count}", Colors.YELLOW)
    print_color(f"✗ Failed:                 {fail_count}", Colors.RED)
    print(f"\nDetailed log saved to: {LOG_FILE}")
    
    # Show failures
    if fail_count > 0:
        print_color("\nFailed conversions:", Colors.RED)
        for r in results:
            if r["status"] == "failed":
                print(f"  - {Path(r['file']).name}")

if __name__ == "__main__":
    main()
