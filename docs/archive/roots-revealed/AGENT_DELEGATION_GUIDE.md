# Agent Delegation Guide

## Purpose
This guide explains how to delegate work to specialized AI agents for the Astrology Synthesis project. Each agent from the BMAD (Behavioral, Modern, Archetypal, and Digital) Business & Development Suite has unique expertise and handles specific types of tasks.

## Quick Reference

### When to Delegate to Each Agent

#### 🎨 Content Creation Agent
**Delegate when you need:**
- UI/UX design and mockups
- Visual styling and branding
- Design system components
- Layout and responsive design
- Typography and color schemes
- Marketing content and copy

**Example Issues:** #17 (Dashboard Layout)

#### 💻 Code Development Agent
**Delegate when you need:**
- Frontend component development
- Interactive features and functionality
- Data visualization
- Form handling and validation
- State management
- API integration
- Performance optimization

**Example Issues:** #18 (Modal Component), #21 (Chart Canvas), #23, #24, #25

#### 📊 BMAD Business & Development Suite
**Delegate when you need:**
- BMAD pattern recognition logic
- Astrological calculation engines
- Business rule implementation
- Pattern scoring algorithms
- Domain-specific interpretations

**Example Issues:** #22 (BMAD Pattern Analysis)

#### ✅ QA/Testing Agent
**Delegate when you need:**
- Test suite development
- Quality assurance reviews
- Bug detection and reporting
- Cross-browser testing
- Performance testing
- Accessibility audits

#### 🚀 Project Automation Agent
**Delegate when you need:**
- CI/CD pipeline setup
- Workflow automation
- Deployment scripts
- Build optimization
- Development environment setup

#### 📈 Analytics Agent
**Delegate when you need:**
- User behavior analysis
- Performance metrics
- A/B testing setup
- Dashboard creation
- Data reporting

## How to Delegate Work

### Step 1: Identify the Task Type
Review the issue or task and determine which agent's expertise best matches the work required.

### Step 2: Review Current Assignments
Check `ISSUE_AGENT_ASSIGNMENTS.md` to see current workload distribution and ensure balanced delegation.

### Step 3: Provide Clear Context
When delegating to an agent, include:
- **Issue number and title**
- **Relevant background information**
- **Specific requirements or constraints**
- **Dependencies on other work**
- **Acceptance criteria**
- **Priority level**

### Step 4: Reference Documentation
Point the agent to relevant documentation:
- Design artifacts (for Content Creation Agent)
- API documentation (for Code Development Agent)
- Business logic specs (for BMAD Agent)
- Test requirements (for QA Agent)

## Delegation Examples

### Example 1: Dashboard Layout (Issue #17)

```
@Content-Creation-Agent

Please redesign the dashboard layout for Issue #17.

**Requirements:**
- Responsive grid: 1 col (mobile), 2 col (tablet), 3 col (desktop)
- Four main cards: Quick Chart Access, Recent Charts, BMAD Summary, Symbolon Readings
- Consistent with design system in COLOR_PALETTE_AND_DESIGN_SYSTEM.md

**References:**
- See COMPONENT_STRUCTURE.md for component hierarchy
- See UX_COPY_GUIDE.md for copy guidelines

**Deliverables:**
- Dashboard.jsx component
- Dashboard.css with responsive styles
- Documentation of design decisions
```

### Example 2: Modal Component (Issue #18)

```
@Code-Development-Agent

Please implement the Modal/Dialog component for Issue #18.

**Requirements:**
- Accessible modal with focus trapping
- Support for multiple sizes (small, medium, large)
- Escape key and overlay click to close
- Header, content, and footer sections
- Portal-based rendering

**References:**
- See COMPONENT_STRUCTURE.md for modal patterns
- See AI_COPILOT_GUIDE.md for accessibility requirements

**Priority:** P0-Critical (blocks other features)

**Deliverables:**
- Modal.jsx component
- Modal.css with animations
- Unit tests
- Usage documentation
```

### Example 3: BMAD Pattern Display (Issue #22)

```
@BMAD-Business-Development-Suite

Please implement the BMAD Pattern Analysis Results display for Issue #22.

**Requirements:**
- Display pattern scores with visual indicators
- Pattern cards sorted by significance
- Integration with backend BMAD logic in /backend/bmad/

**References:**
- See BMAD_USAGE_GUIDE.md for pattern structure
- See backend/bmad/ for calculation logic

**Deliverables:**
- BMADResults.jsx component
- Pattern scoring visualization
- Integration tests
- Documentation
```

## Agent Coordination

### When Multiple Agents Are Needed

Some features require coordination between agents:

1. **Design → Development Flow**
   - Content Creation Agent designs the UI
   - Code Development Agent implements the design
   - QA Agent validates the implementation

2. **Feature → Testing Flow**
   - Code Development Agent builds the feature
   - QA Agent creates comprehensive tests
   - Project Automation Agent sets up CI/CD

3. **BMAD Feature Flow**
   - BMAD Agent implements business logic
   - Code Development Agent creates UI components
   - Analytics Agent tracks usage patterns

### Handoff Protocol

When handing off work between agents:

1. **Complete Current Work**
   - Ensure deliverables are complete
   - Document any decisions made
   - Commit all code changes

2. **Create Handoff Document**
   - Summarize what was completed
   - Note any blockers or issues
   - List next steps for receiving agent

3. **Notify Next Agent**
   - Tag the next agent
   - Reference the handoff document
   - Provide timeline expectations

## Best Practices

### ✅ Do's

- **Be Specific**: Provide clear, detailed requirements
- **Include Context**: Reference relevant documentation and prior work
- **Set Priorities**: Indicate P0/P1/P2 priority levels
- **Check Dependencies**: Ensure prerequisite work is complete
- **Provide Examples**: Show similar implementations when possible
- **Review Work**: Validate agent output matches requirements

### ❌ Don'ts

- **Don't Overload**: Balance workload across agents
- **Don't Skip Context**: Always provide background information
- **Don't Ignore Blockers**: Address dependencies before delegation
- **Don't Forget Testing**: Include testing requirements in delegation
- **Don't Rush**: Allow adequate time for quality work

## Current Assignments (November 2025)

| Agent | Open Issues | Status |
|-------|-------------|---------|
| Content Creation Agent | 1 (#17) | Available for new work |
| Code Development Agent | 5 (#18, #21, #23, #24, #25) | Moderate workload |
| BMAD Business & Development Suite | 1 (#22) | Available for new work |
| QA/Testing Agent | 0 | Available |
| Project Automation Agent | 0 | Available |
| Analytics Agent | 0 | Available |

## Recommended Execution Order

Based on dependencies and priorities:

1. **#18** - Modal Component (P0-Critical, foundation component)
2. **#17** - Dashboard Layout (establishes visual framework)
3. **#22** - BMAD Pattern Display (specialized domain work)
4. **#21** - Interactive Chart Canvas (complex visualization)
5. **#23, #24** - Data tables (similar patterns, can parallelize)
6. **#25** - Symbolon Cards (after foundation components)

## Getting Help

If you're unsure which agent to delegate to:

1. Review the agent descriptions in the BMAD agent instructions
2. Check `ISSUE_AGENT_ASSIGNMENTS.md` for similar issues
3. Consult with the Product Management Agent for guidance
4. Start with the most specialized agent (e.g., BMAD Agent for BMAD features)

## Updates and Maintenance

This guide should be updated when:
- New agent types are added
- Assignment patterns change
- New delegation best practices emerge
- Team structure evolves

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-02  
**Maintained By:** Product Management Agent  
**Next Review:** 2025-12-02
