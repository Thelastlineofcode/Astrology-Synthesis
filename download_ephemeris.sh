#!/bin/bash
# Download Swiss Ephemeris files for macOS
# Astrology Synthesis Project

echo "======================================"
echo "Swiss Ephemeris File Download (macOS)"
echo "======================================"
echo ""

# Navigate to backend/ephe directory
cd "$(dirname "$0")/backend/ephe" || {
    echo "❌ Error: Could not find backend/ephe directory"
    echo "Please run this script from the project root directory"
    exit 1
}

echo "Current directory: $(pwd)"
echo ""

# Files to download
FILES=(
    "sepl_18.se1"
    "semo_18.se1"
    "seas_18.se1"
)

BASE_URL="https://www.astro.com/ftp/swisseph/ephe/"

# Download each file
for file in "${FILES[@]}"; do
    echo "Downloading $file..."
    if curl -# -f -O "${BASE_URL}${file}"; then
        echo "✅ $file downloaded successfully"
    else
        echo "❌ Failed to download $file"
        echo "   You can try downloading manually from:"
        echo "   ${BASE_URL}${file}"
        exit 1
    fi
    echo ""
done

echo "======================================"
echo "Download Complete!"
echo "======================================"
echo ""
echo "Files downloaded:"
ls -lh *.se1

echo ""
echo "Total size:"
du -sh .

echo ""
echo "======================================"
echo "Next Steps:"
echo "======================================"
echo "1. Run tests: cd backend && source venv/bin/activate && python test_astrology_app.py"
echo "2. Start server: python app.py"
echo "======================================"
