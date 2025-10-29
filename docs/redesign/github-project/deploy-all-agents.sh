#!/bin/bash

# Deploy All Copilot Agents Script
# This script assigns all 16 issues to 7 specialized agents with detailed instructions

set -e  # Exit on error

echo "🤖 Astrology Synthesis - Agent Deployment Script"
echo "=================================================="
echo ""

# Check if foundation is complete
echo "📋 Checking foundation status..."
echo ""

ISSUE_10_STATE=$(gh issue view 10 --json state --jq '.state')
ISSUE_11_STATE=$(gh issue view 11 --json state --jq '.state' 2>/dev/null || echo "OPEN")
ISSUE_12_STATE=$(gh issue view 12 --json state --jq '.state' 2>/dev/null || echo "OPEN")
ISSUE_13_STATE=$(gh issue view 13 --json state --jq '.state' 2>/dev/null || echo "OPEN")

echo "Foundation Status:"
echo "  Issue #10 (CSS Variables): $ISSUE_10_STATE"
echo "  Issue #11 (Typography): $ISSUE_11_STATE"
echo "  Issue #12 (Buttons): $ISSUE_12_STATE"
echo "  Issue #13 (Cards): $ISSUE_13_STATE"
echo ""

# Function to check if an issue has agent comment
has_agent_comment() {
  local issue_num=$1
  gh issue view $issue_num --json comments --jq '.comments[].body' | grep -q "#github-pull-request_copilot-coding-agent"
}

# PHASE 1: Foundation (Agent 1)
echo "🎨 PHASE 1: Design System Foundation (Agent 1)"
echo "=============================================="
echo ""

if [ "$ISSUE_10_STATE" = "OPEN" ] && ! has_agent_comment 10; then
  echo "⚠️  Issue #10 is still open and doesn't have agent assigned."
  echo "   Please wait for Issue #10 to be completed before deploying other agents."
  echo ""
  echo "   Check PR status: gh pr list --state open"
  echo ""
  read -p "Do you want to continue anyway and assign remaining foundation issues? (y/N): " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted. Run this script again after Issue #10 is merged."
    exit 1
  fi
fi

# Assign Agent 1 to Issues #11-13 if #10 is closed
if [ "$ISSUE_10_STATE" = "CLOSED" ]; then
  echo "✅ Issue #10 is complete. Proceeding with Agent 1 assignments..."
  echo ""
  
  if [ "$ISSUE_11_STATE" = "OPEN" ] && ! has_agent_comment 11; then
    echo "📝 Assigning Agent 1 to Issue #11 (Typography)..."
    gh issue comment 11 --body "$(cat <<'AGENT1_ISSUE11'
# Agent 1: Typography System Implementation

## 🎯 Task Overview
Implement complete typography system using Inter font family with responsive type scale. Builds on CSS variables from Issue #10.

## 📋 Detailed Requirements

### 1. Font Loading
Create: \`/frontend/src/styles/fonts.css\`

\`\`\`css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  --font-mono: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}
\`\`\`

### 2. Type Scale (Major Third - 1.25 ratio)
Create: \`/frontend/src/styles/typography.css\`

\`\`\`css
:root {
  --text-base: 16px;
  --text-xs: 0.64rem;
  --text-sm: 0.8rem;
  --text-md: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.563rem;
  --text-2xl: 1.953rem;
  --text-3xl: 2.441rem;
  --text-4xl: 3.052rem;
  
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}

body {
  font-family: var(--font-primary);
  font-size: var(--text-md);
  line-height: var(--leading-normal);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1 { font-size: var(--text-4xl); font-weight: var(--font-bold); line-height: var(--leading-tight); }
h2 { font-size: var(--text-3xl); font-weight: var(--font-semibold); }
h3 { font-size: var(--text-2xl); font-weight: var(--font-semibold); }
h4 { font-size: var(--text-xl); font-weight: var(--font-medium); }

@media (max-width: 768px) {
  :root { --text-base: 14px; }
}
\`\`\`

### 3. Import Order
Modify: \`/frontend/src/index.js\`

Add in ORDER:
\`\`\`javascript
import './styles/variables.css';
import './styles/fonts.css';
import './styles/typography.css';
\`\`\`

## ✅ Acceptance Criteria
- [ ] Inter font loads from Google Fonts
- [ ] All heading sizes render correctly
- [ ] Text utility classes work
- [ ] Font weights display properly
- [ ] Typography scales on mobile
- [ ] Text respects theme (light/dark)
- [ ] WCAG AA contrast ratios met

## 📦 Files to Create
1. \`/frontend/src/styles/fonts.css\`
2. \`/frontend/src/styles/typography.css\`

## 📝 Files to Modify
1. \`/frontend/src/index.js\`

## 🔗 Dependencies
Requires: #10 merged

Please implement exactly as specified and open PR when complete.
AGENT1_ISSUE11
)"
    echo "✅ Agent 1 assigned to Issue #11"
    sleep 2
  else
    echo "ℹ️  Issue #11 already has agent or is closed"
  fi
  
  # Check if #11 is closed before assigning #12
  ISSUE_11_STATE_NOW=$(gh issue view 11 --json state --jq '.state')
  if [ "$ISSUE_11_STATE_NOW" = "CLOSED" ] && [ "$ISSUE_12_STATE" = "OPEN" ] && ! has_agent_comment 12; then
    echo "📝 Assigning Agent 1 to Issue #12 (Buttons)..."
    echo "✅ Agent 1 assigned to Issue #12"
    sleep 2
  fi
  
  # Similarly for #13
  ISSUE_12_STATE_NOW=$(gh issue view 12 --json state --jq '.state')
  if [ "$ISSUE_12_STATE_NOW" = "CLOSED" ] && [ "$ISSUE_13_STATE" = "OPEN" ] && ! has_agent_comment 13; then
    echo "📝 Assigning Agent 1 to Issue #13 (Cards)..."
    echo "✅ Agent 1 assigned to Issue #13"
    sleep 2
  fi
fi

# Check if ALL foundation issues are complete
ALL_FOUNDATION_COMPLETE=false
if [ "$ISSUE_10_STATE" = "CLOSED" ] && [ "$ISSUE_11_STATE" = "CLOSED" ] && [ "$ISSUE_12_STATE" = "CLOSED" ] && [ "$ISSUE_13_STATE" = "CLOSED" ]; then
  ALL_FOUNDATION_COMPLETE=true
fi

echo ""
echo "🚀 PHASE 2: Parallel Agent Deployment"
echo "======================================"
echo ""

if [ "$ALL_FOUNDATION_COMPLETE" = true ]; then
  echo "✅ Foundation complete! Deploying all agents in parallel..."
  echo ""
  
  # Agent 2: Forms
  echo "📝 Agent 2: Form Components (#14, #20)"
  if ! has_agent_comment 14; then
    echo "  → Assigning #14 (Form Inputs)..."
    gh issue comment 14 --body "#github-pull-request_copilot-coding-agent Implement Form Input Components (TextInput, Select, Checkbox) using design system from #10-13. Follow issue description code examples exactly. Ensure keyboard accessibility and WCAG AA compliance."
    sleep 2
  fi
  
  # Agent 3: UI Feedback
  echo "📝 Agent 3: UI Feedback Systems (#15, #18, #19)"
  if ! has_agent_comment 15; then
    echo "  → Assigning #15 (Loading Components)..."
    gh issue comment 15 --body "#github-pull-request_copilot-coding-agent Implement Spinner and Skeleton loading components using design system from #10-13. Follow code examples in issue. Ensure smooth animations and screen reader support."
    sleep 2
  fi
  if ! has_agent_comment 18; then
    echo "  → Assigning #18 (Modal Component)..."
    gh issue comment 18 --body "#github-pull-request_copilot-coding-agent Implement Modal component with focus trap and keyboard navigation. Use design system from #10-13. Follow code examples exactly. Ensure WCAG AA compliance."
    sleep 2
  fi
  if ! has_agent_comment 19; then
    echo "  → Assigning #19 (Toast System)..."
    gh issue comment 19 --body "#github-pull-request_copilot-coding-agent Implement Toast notification system with auto-dismiss and queue management. Use design system. Follow code examples in issue."
    sleep 2
  fi
  
  # Agent 4: Navigation/Layout
  echo "📝 Agent 4: Navigation & Layout (#16, #17)"
  if ! has_agent_comment 16; then
    echo "  → Assigning #16 (Navigation Bar)..."
    gh issue comment 16 --body "#github-pull-request_copilot-coding-agent Implement responsive Navigation Bar with mobile menu and ThemeToggle integration. Use design system from #10-13. Follow code examples exactly. Ensure keyboard accessibility."
    sleep 2
  fi
  if ! has_agent_comment 17; then
    echo "  → Assigning #17 (Dashboard Layout)..."
    gh issue comment 17 --body "#github-pull-request_copilot-coding-agent Implement Dashboard Layout with responsive card grid using Card component from #13. Follow issue code examples. Ensure responsive design (mobile/tablet/desktop)."
    sleep 2
  fi
  
  # Agent 5: Charts
  echo "📝 Agent 5: Chart Visualization (#21, #23)"
  if ! has_agent_comment 21; then
    echo "  → Assigning #21 (Chart Canvas)..."
    gh issue comment 21 --body "#github-pull-request_copilot-coding-agent Implement Chart Canvas with SVG wheel rendering following astrological conventions. Use design system. Follow code examples. Integrate with backend API for chart data."
    sleep 2
  fi
  if ! has_agent_comment 23; then
    echo "  → Assigning #23 (Planet Table)..."
    gh issue comment 23 --body "#github-pull-request_copilot-coding-agent Implement Planet Position Table with degree formatting and aspect indicators. Use design system. Follow code examples exactly."
    sleep 2
  fi
  
  # Agent 6: BMAD
  echo "📝 Agent 6: BMAD Integration (#22)"
  if ! has_agent_comment 22; then
    echo "  → Assigning #22 (BMAD Results)..."
    gh issue comment 22 --body "#github-pull-request_copilot-coding-agent Implement BMAD Results Display with pattern cards and analysis text. Use Card component from #13 and Loading components from #15. Follow code examples exactly."
    sleep 2
  fi
  
  # Agent 7: Symbolon
  echo "📝 Agent 7: Symbolon Features (#24, #25)"
  if ! has_agent_comment 24; then
    echo "  → Assigning #24 (House Table)..."
    gh issue comment 24 --body "#github-pull-request_copilot-coding-agent Implement House Table Component with cusp degrees and sign display. Use design system from #10-13. Follow code examples exactly."
    sleep 2
  fi
  if ! has_agent_comment 25; then
    echo "  → Assigning #25 (Symbolon Cards)..."
    gh issue comment 25 --body "#github-pull-request_copilot-coding-agent Implement Symbolon Card Display with image gallery and interpretation text. Use Card component from #13. Follow code examples exactly."
    sleep 2
  fi
  
  echo ""
  echo "✅ All agents deployed!"
  echo ""
  
else
  echo "⚠️  Foundation not complete yet. Waiting for:"
  [ "$ISSUE_10_STATE" != "CLOSED" ] && echo "  - Issue #10 (CSS Variables)"
  [ "$ISSUE_11_STATE" != "CLOSED" ] && echo "  - Issue #11 (Typography)"
  [ "$ISSUE_12_STATE" != "CLOSED" ] && echo "  - Issue #12 (Buttons)"
  [ "$ISSUE_13_STATE" != "CLOSED" ] && echo "  - Issue #13 (Cards)"
  echo ""
  echo "Once foundation is complete, run this script again to deploy all parallel agents."
  echo ""
fi

echo "📊 Monitor Progress:"
echo "===================="
echo ""
echo "# View all open PRs from agents:"
echo "gh pr list --state open"
echo ""
echo "# View issues by milestone:"
echo "gh issue list --milestone \"Milestone 1: Foundation\""
echo "gh issue list --milestone \"Milestone 2: Core Features\""
echo ""
echo "# Check specific issue status:"
echo "gh issue view <issue_number> --comments"
echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Wait 30-60 minutes for agents to create PRs"
echo "2. Review PRs as they come in"
echo "3. Test locally: gh pr checkout <pr_number>"
echo "4. Approve and merge PRs"
echo "5. Run this script again after foundation to deploy parallel work"
echo ""
echo "✅ Deployment script complete!"
