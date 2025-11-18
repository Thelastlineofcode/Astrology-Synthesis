#!/bin/bash

# Chronological Agent Deployment - Clean Start
# This ensures agents work in proper dependency order

set -e

echo "🎯 CHRONOLOGICAL AGENT DEPLOYMENT"
echo "=================================="
echo ""
echo "Goal: Deploy 7 agents to work on issues in proper order"
echo "Strategy: Sequential foundation, then parallel workstreams"
echo ""

# Step 1: Clean up out-of-order PRs
echo "📋 Step 1: Cleaning Out-of-Order PRs"
echo "======================================"
echo ""

declare -a OOO_PRS=(28 29 30 31 32)
CLOSE_MESSAGE="Closing this PR as it was created out of sequence. The foundation (Issues #10-13) must be completed sequentially before parallel work begins. This ensures proper dependencies and prevents merge conflicts. Will recreate this work in the correct order after foundation is complete."

for pr in "${OOO_PRS[@]}"; do
  PR_STATE=$(gh pr view $pr --json state --jq '.state' 2>/dev/null || echo "NOT_FOUND")
  if [ "$PR_STATE" = "OPEN" ]; then
    echo "❌ Closing PR #$pr (out of order)"
    gh pr close $pr --comment "$CLOSE_MESSAGE"
    sleep 1
  else
    echo "ℹ️  PR #$pr already closed or not found"
  fi
done

echo ""
echo "✅ Step 1 Complete: Out-of-order PRs closed"
echo ""

# Step 2: Verify Issue #10 PR status
echo "📋 Step 2: Foundation Phase - Issue #10"
echo "========================================"
echo ""

PR27_STATE=$(gh pr view 27 --json state --jq '.state')
ISSUE10_STATE=$(gh issue view 10 --json state --jq '.state')

echo "PR #27 (Issue #10): $PR27_STATE"
echo "Issue #10: $ISSUE10_STATE"
echo ""

if [ "$PR27_STATE" = "OPEN" ]; then
  echo "✅ PR #27 is ready for review"
  echo ""
  echo "🔍 NEXT ACTION: Review PR #27"
  echo "   1. View: gh pr view 27"
  echo "   2. Checkout: gh pr checkout 27"
  echo "   3. Test locally: cd frontend && npm start"
  echo "   4. Approve: gh pr review 27 --approve"
  echo "   5. Merge: gh pr merge 27 --squash"
  echo ""
  read -p "Have you reviewed and tested PR #27? Ready to merge? (y/N): " -n 1 -r
  echo ""
  
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Merging PR #27..."
    gh pr review 27 --approve --body "✅ CSS Variables and theme system look great! Foundation is solid."
    gh pr merge 27 --squash --delete-branch
    echo "✅ PR #27 merged!"
    ISSUE10_STATE="CLOSED"
  else
    echo "⏸️  Pausing deployment. Please review PR #27 first."
    echo ""
    echo "When ready, run this script again or merge manually:"
    echo "  gh pr merge 27 --squash"
    exit 0
  fi
fi

echo ""
echo "📋 Step 3: Sequential Foundation Deployment"
echo "============================================"
echo ""

# Step 3: Deploy Agent 1 to Issue #11 (only if #10 is closed)
if [ "$ISSUE10_STATE" = "CLOSED" ]; then
  echo "✅ Issue #10 complete. Deploying Agent 1 to Issue #11..."
  echo ""
  
  gh issue comment 11 --body "# Agent 1: Typography System

## 🎯 Your Task
Implement typography system with Inter font family and responsive type scale. This builds directly on the CSS variables you just created in Issue #10.

## 📦 Files to Create

### 1. /frontend/src/styles/fonts.css
\`\`\`css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  --font-mono: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}
\`\`\`

### 2. /frontend/src/styles/typography.css
\`\`\`css
:root {
  /* Base */
  --text-base: 16px;
  
  /* Type scale (Major Third 1.25) */
  --text-xs: 0.64rem;
  --text-sm: 0.8rem;
  --text-md: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.563rem;
  --text-2xl: 1.953rem;
  --text-3xl: 2.441rem;
  --text-4xl: 3.052rem;
  
  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Weights */
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
}

h1 { font-size: var(--text-4xl); font-weight: var(--font-bold); line-height: var(--leading-tight); }
h2 { font-size: var(--text-3xl); font-weight: var(--font-semibold); line-height: var(--leading-tight); }
h3 { font-size: var(--text-2xl); font-weight: var(--font-semibold); }
h4 { font-size: var(--text-xl); font-weight: var(--font-medium); }

@media (max-width: 768px) {
  :root { --text-base: 14px; }
}
\`\`\`

### 3. Modify /frontend/src/index.js
Add imports in this EXACT order:
\`\`\`javascript
import './styles/variables.css';  // From Issue #10
import './styles/fonts.css';      // NEW
import './styles/typography.css'; // NEW
\`\`\`

## ✅ Acceptance Criteria
- [ ] Inter font loads from Google Fonts
- [ ] All heading sizes render correctly  
- [ ] Typography responds to theme changes
- [ ] Mobile responsive (scales down)
- [ ] WCAG AA contrast maintained

## 🔗 Dependencies
**REQUIRED:** Issue #10 merged ✅

#github-pull-request_copilot-coding-agent Please implement this exactly as specified above. Create the 2 new CSS files and modify index.js. Use the CSS variables from Issue #10 (--text-primary, --font-primary, etc). Ensure typography works in both light and dark themes."

  echo "✅ Agent 1 assigned to Issue #11"
  echo ""
  echo "⏱️  Wait 30-60 minutes for PR to be created"
  echo "📊 Monitor: gh pr list --state open"
  echo ""
  
else
  echo "⚠️  Issue #10 not yet closed. Cannot proceed to Issue #11."
  echo "   Please merge PR #27 first."
  echo ""
fi

echo ""
echo "📋 Step 4: Waiting Strategy"
echo "==========================="
echo ""
echo "⏸️  Script paused. Next actions:"
echo ""
echo "1. Wait for Issue #11 PR to be created (~30-60 min)"
echo "2. When PR appears, review it:"
echo "   $ gh pr list --state open"
echo "   $ gh pr view <PR_NUMBER>"
echo "3. Test and merge the PR"
echo "4. Run this script again to deploy Agent 1 to Issue #12"
echo ""
echo "📖 Foundation Roadmap:"
echo "   Issue #10 (CSS Variables) → Issue #11 (Typography) → Issue #12 (Buttons) → Issue #13 (Cards)"
echo "   SEQUENTIAL - Each must be merged before the next begins"
echo ""
echo "🚀 After foundation complete, we'll deploy all 6 agents in parallel!"
echo ""
