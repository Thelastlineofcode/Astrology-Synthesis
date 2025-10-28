#!/bin/bash
# Complete Testing Script for Astrology Synthesis
# Run all tests from syntax to integration

echo "========================================"
echo "  ASTROLOGY SYNTHESIS - FULL TEST SUITE"
echo "========================================"
echo ""

# Check we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

echo "Current directory: $(pwd)"
echo ""

# ============================================
# PHASE 1: VERIFY EPHEMERIS FILES
# ============================================
echo "========================================"
echo "PHASE 1: Ephemeris Files Verification"
echo "========================================"
echo ""

cd backend/ephe

EPHE_COUNT=$(ls -1 *.se1 2>/dev/null | wc -l | tr -d ' ')

if [ "$EPHE_COUNT" -lt 3 ]; then
    echo "❌ ERROR: Only $EPHE_COUNT ephemeris file(s) found"
    echo "   Required: sepl_18.se1, semo_18.se1, seas_18.se1"
    echo ""
    echo "Files currently in backend/ephe:"
    ls -lh
    exit 1
else
    echo "✅ Found $EPHE_COUNT ephemeris files:"
    ls -lh *.se1
    echo ""
fi

cd ../..

# ============================================
# PHASE 2: BACKEND SETUP & DEPENDENCIES
# ============================================
echo "========================================"
echo "PHASE 2: Backend Setup & Dependencies"
echo "========================================"
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Check Python version
echo "Python version:"
python --version
echo ""

# Install/verify dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Verify key imports
echo "Verifying key imports..."
python << 'EOF'
import sys
try:
    import flask
    print(f"✅ Flask {flask.__version__}")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

try:
    import flask_cors
    print("✅ Flask-CORS installed")
except ImportError as e:
    print(f"❌ Flask-CORS import failed: {e}")
    sys.exit(1)

try:
    import swisseph as swe
    print(f"✅ pyswisseph {swe.version}")
except ImportError as e:
    print(f"❌ pyswisseph import failed: {e}")
    sys.exit(1)

try:
    from api.routes import api_bp
    print("✅ api.routes module")
except ImportError as e:
    print(f"❌ api.routes import failed: {e}")
    sys.exit(1)

try:
    from calculations.chart_calculator import ChartCalculator
    print("✅ calculations.chart_calculator module")
except ImportError as e:
    print(f"❌ chart_calculator import failed: {e}")
    sys.exit(1)

try:
    from calculations.aspects import AspectCalculator
    print("✅ calculations.aspects module")
except ImportError as e:
    print(f"❌ aspects import failed: {e}")
    sys.exit(1)

print("")
print("✅ All imports successful")
EOF

if [ $? -ne 0 ]; then
    echo "❌ Import verification failed"
    exit 1
fi

echo ""

# ============================================
# PHASE 3: UNIT TESTS
# ============================================
echo "========================================"
echo "PHASE 3: Running Unit Tests"
echo "========================================"
echo ""

python test_astrology_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Unit tests FAILED"
    echo "Please review errors above"
    exit 1
fi

echo ""
echo "✅ All unit tests PASSED"
echo ""

# ============================================
# PHASE 4: QUICK CALCULATION TEST
# ============================================
echo "========================================"
echo "PHASE 4: Quick Calculation Test"
echo "========================================"
echo ""

echo "Testing chart calculation directly..."
python << 'EOF'
import sys
from calculations.chart_calculator import ChartCalculator
from calculations.aspects import AspectCalculator

try:
    # Create calculator
    calc = ChartCalculator(zodiac_type='sidereal', ayanamsa='LAHIRI')
    print("✅ ChartCalculator initialized")
    
    # Test birth data (Houston, TX - Aug 15, 1990, 2:30 PM)
    birth_data = {
        'year': 1990,
        'month': 8,
        'day': 15,
        'hour': 14,
        'minute': 30,
        'latitude': 29.7604,
        'longitude': -95.3698,
        'house_system': 'P'
    }
    
    # Calculate chart
    chart = calc.generate_chart(birth_data)
    print(f"✅ Chart calculated successfully")
    print(f"   Planets: {len(chart['planets'])} calculated")
    print(f"   Houses: {len(chart['houses'])} calculated")
    print(f"   Zodiac Type: {chart['chartInfo']['zodiacType']}")
    print(f"   Ayanamsa: {chart['chartInfo']['ayanamsa']}")
    
    # Test aspects
    aspect_calc = AspectCalculator()
    aspects = aspect_calc.calculate_aspects(chart['planets'], include_minor=False)
    print(f"✅ Aspects calculated: {len(aspects)} found")
    
    # Display sample planet
    if 'Sun' in chart['planets']:
        sun = chart['planets']['Sun']
        print(f"\n   Sample: Sun at {sun['zodiacSign']} {sun['degree']}° {sun['minute']}'")
        print(f"           House: {sun.get('house', 'N/A')}")
    
    print("\n✅ Chart calculation engine working correctly")
    
except Exception as e:
    print(f"❌ Chart calculation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ Calculation test failed"
    exit 1
fi

echo ""

# ============================================
# PHASE 5: FRONTEND CHECK
# ============================================
echo "========================================"
echo "PHASE 5: Frontend Dependencies Check"
echo "========================================"
echo ""

cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "⚠️  Frontend dependencies not installed"
    echo "   Run: cd frontend && npm install"
    echo ""
else
    echo "✅ Frontend node_modules exists"
    
    # Check package.json
    if [ -f "package.json" ]; then
        echo "✅ package.json found"
        echo "   Proxy configured: $(grep -o '"proxy".*' package.json)"
    fi
    echo ""
fi

cd ..

# ============================================
# TEST SUMMARY
# ============================================
echo "========================================"
echo "          TEST SUMMARY"
echo "========================================"
echo ""
echo "✅ Phase 1: Ephemeris files verified"
echo "✅ Phase 2: Backend dependencies installed"
echo "✅ Phase 3: Unit tests passed"
echo "✅ Phase 4: Chart calculation working"
echo "✅ Phase 5: Frontend dependencies checked"
echo ""
echo "========================================"
echo "    ALL TESTS PASSED! 🎉"
echo "========================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. Start Backend Server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. Start Frontend (in new terminal):"
echo "   cd frontend"
echo "   npm install  # if not done yet"
echo "   npm start"
echo ""
echo "3. Open browser:"
echo "   http://localhost:3000"
echo ""
echo "========================================"
