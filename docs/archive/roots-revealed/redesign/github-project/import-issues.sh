#!/bin/bash

# Script to import all GitHub issues from markdown files
# Usage: ./import-issues.sh

ISSUES_DIR="./issues"
REPO="Thelastlineofcode/Astrology-Synthesis"

echo "🚀 Starting GitHub Issues import for BMAD Astrology App Redesign"
echo "Repository: $REPO"
echo ""

# Issue 002: Typography System
echo "📝 Creating Issue #002: Typography System..."
gh issue create \
  --title "Establish Typography System" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-002-typography-system.md"

# Issue 003: Button Component
echo "📝 Creating Issue #003: Button Component..."
gh issue create \
  --title "Create Reusable Button Component" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-003-button-component.md"

# Issue 004: Card Component
echo "📝 Creating Issue #004: Card Component..."
gh issue create \
  --title "Build Card Component System" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-004-card-component.md"

# Issue 005: Form Inputs
echo "📝 Creating Issue #005: Form Input Components..."
gh issue create \
  --title "Design Form Input Components (Text, Select, Checkbox)" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-005-form-inputs.md"

# Issue 006: Loading Components
echo "📝 Creating Issue #006: Loading Components..."
gh issue create \
  --title "Create Loading & Skeleton Components" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P1-High" \
  --body-file "$ISSUES_DIR/issue-006-loading-components.md"

# Issue 007: Navigation Bar
echo "📝 Creating Issue #007: Navigation Bar..."
gh issue create \
  --title "Build Navigation Bar & Mobile Menu" \
  --milestone "Milestone 1: Foundation" \
  --label "component:navigation,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-007-navigation-bar.md"

# Issue 008: Dashboard Layout
echo "📝 Creating Issue #008: Dashboard Layout..."
gh issue create \
  --title "Redesign Dashboard Layout & Grid" \
  --milestone "Milestone 2: Core Features" \
  --label "component:dashboard,P1-High,feature" \
  --body-file "$ISSUES_DIR/issue-008-dashboard-layout.md"

# Issue 009: Modal Component
echo "📝 Creating Issue #009: Modal Component..."
gh issue create \
  --title "Create Modal/Dialog Component" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-009-modal-component.md"

# Issue 010: Toast System
echo "📝 Creating Issue #010: Toast System..."
gh issue create \
  --title "Build Toast/Notification System" \
  --milestone "Milestone 1: Foundation" \
  --label "component:design-system,P1-High" \
  --body-file "$ISSUES_DIR/issue-010-toast-system.md"

# Issue 014: Birth Data Form
echo "📝 Creating Issue #014: Birth Data Form..."
gh issue create \
  --title "Redesign Birth Data Input Form" \
  --milestone "Milestone 2: Core Features" \
  --label "component:chart,P0-Critical" \
  --body-file "$ISSUES_DIR/issue-014-birth-data-form.md"

# Issue 015: Chart Canvas
echo "📝 Creating Issue #015: Chart Canvas..."
gh issue create \
  --title "Build Interactive Chart Canvas (SVG)" \
  --milestone "Milestone 2: Core Features" \
  --label "component:chart,P1-High,feature" \
  --body-file "$ISSUES_DIR/issue-015-chart-canvas.md"

# Issue 020: BMAD Results
echo "📝 Creating Issue #020: BMAD Results..."
gh issue create \
  --title "Display BMAD Pattern Analysis Results" \
  --milestone "Milestone 2: Core Features" \
  --label "component:bmad,P1-High,feature" \
  --body-file "$ISSUES_DIR/issue-020-bmad-results.md"

# Issue 021: Planet Table
echo "📝 Creating Issue #021: Planet Table..."
gh issue create \
  --title "Display Planet List Table" \
  --milestone "Milestone 2: Core Features" \
  --label "component:chart,P1-High" \
  --body-file "$ISSUES_DIR/issue-021-planet-table.md"

# Issue 022: House Table
echo "📝 Creating Issue #022: House Table..."
gh issue create \
  --title "Show House System Table" \
  --milestone "Milestone 2: Core Features" \
  --label "component:chart,P1-High" \
  --body-file "$ISSUES_DIR/issue-022-house-table.md"

# Issue 024: Symbolon Cards
echo "📝 Creating Issue #024: Symbolon Cards..."
gh issue create \
  --title "Build Symbolon Card Display Component" \
  --milestone "Milestone 3: Advanced Features" \
  --label "component:symbolon,P1-High,feature" \
  --body-file "$ISSUES_DIR/issue-024-symbolon-cards.md"

echo ""
echo "✅ All issues created successfully!"
echo "🔗 View them at: https://github.com/$REPO/issues"
echo ""
echo "📊 Summary:"
echo "  - Total issues created: 15"
echo "  - Milestone 1: 8 issues"
echo "  - Milestone 2: 6 issues"
echo "  - Milestone 3: 1 issue"
echo ""
echo "🎯 Next steps:"
echo "  1. Visit the GitHub repo to verify issues"
echo "  2. Create a GitHub Project board (Projects tab)"
echo "  3. Add all issues to the project"
echo "  4. Start implementation with Issue #001 (CSS Variables)"
