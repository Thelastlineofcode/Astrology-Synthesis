# Custom Agent Mapping for Redesign Issues

This document maps your custom GitHub Copilot agents (from `.github/agents/`) to the redesign issues #10-25.

## Available Custom Agents

1. **@code-development-agent** - Implementation, coding, technical development
2. **@bmad-agent** - Product management, strategic planning (includes sub-agents)
3. **@qa-testing-agent** - Testing, validation, quality assurance
4. **@analytics-agent** - Data analysis and metrics
5. **@content-creation-agent** - Documentation and content
6. **@product-management-agent** - Product planning
7. **@project-automation-agent** - Workflow automation
8. **@social-media-outreach-agent** - Marketing and outreach

## Agent Assignment by Issue

### Foundation Phase (Issues #10-13) - Sequential

**Issue #10: CSS Variables & Theme System**
- Agent: `@code-development-agent`
- Rationale: Core frontend implementation task
- Dependencies: None
- Status: Comment updated with agent assignment

**Issue #11: Typography System**
- Agent: `@code-development-agent`
- Rationale: Frontend styling and component implementation
- Dependencies: #10 (needs CSS variables)
- Status: Ready for assignment after #10

**Issue #12: Button Components**
- Agent: `@code-development-agent`
- Rationale: Reusable React component development
- Dependencies: #10, #11 (needs theme and typography)
- Status: Ready for assignment after #10-11

**Issue #13: Card Components**
- Agent: `@code-development-agent`
- Rationale: Reusable React component development
- Dependencies: #10, #11, #12 (needs design system foundation)
- Status: Ready for assignment after #10-12

### Core Features Phase (Issues #14-24) - Can Parallelize After Foundation

**Issue #14: Form Input Components**
- Agent: `@code-development-agent`
- Rationale: Frontend form component development
- Dependencies: #10-13 (design system)

**Issue #15: Loading States & Spinners**
- Agent: `@code-development-agent`
- Rationale: UI feedback components
- Dependencies: #10-13 (design system)

**Issue #16: Navigation Bar**
- Agent: `@code-development-agent`
- Rationale: Core navigation component
- Dependencies: #10-13 (design system)

**Issue #17: Dashboard Layout**
- Agent: `@code-development-agent`
- Rationale: Layout and structure implementation
- Dependencies: #10-13, #16 (design system + nav)

**Issue #18: Modal Dialog System**
- Agent: `@code-development-agent`
- Rationale: Interactive UI component
- Dependencies: #10-13 (design system)

**Issue #19: Toast Notification System**
- Agent: `@code-development-agent`
- Rationale: Notification component
- Dependencies: #10-13 (design system)

**Issue #20: Birth Data Input Form**
- Agent: `@code-development-agent`
- Rationale: Core form implementation
- Dependencies: #10-14 (design system + form inputs)

**Issue #21: Chart Canvas Component**
- Agent: `@code-development-agent`
- Rationale: Complex visualization component
- Dependencies: #10-13, #17 (design system + dashboard)
- Note: May need @qa-testing-agent for calculation accuracy

**Issue #22: BMAD Results Display**
- Agent: `@code-development-agent`
- Rationale: BMAD-specific visualization
- Dependencies: #10-13, #17, #21 (design system + dashboard + chart)
- Note: Core BMAD functionality

**Issue #23: Planet Position Table**
- Agent: `@code-development-agent`
- Rationale: Data display component
- Dependencies: #10-13, #21 (design system + chart data)

**Issue #24: House Table Component**
- Agent: `@code-development-agent`
- Rationale: Data display component
- Dependencies: #10-13, #21 (design system + chart data)

### Advanced Features Phase (Issue #25)

**Issue #25: Symbolon Card Gallery**
- Agent: `@code-development-agent`
- Rationale: Interactive gallery component
- Dependencies: #10-13, #18 (design system + modal for detail view)
- Note: Symbolon integration

## Testing Strategy

After each issue is implemented by `@code-development-agent`, assign `@qa-testing-agent` to:
- Verify implementation meets requirements
- Test cross-browser compatibility
- Validate responsive behavior
- Check accessibility compliance
- Test integration with existing functionality

## Deployment Sequence

### Phase 1: Foundation (Sequential)
```bash
# Issue #10 - ASSIGNED
# Wait for PR completion and merge

# Issue #11 - Next
gh issue comment 11 --body "@code-development-agent Please implement..."

# Issue #12 - After #11
gh issue comment 12 --body "@code-development-agent Please implement..."

# Issue #13 - After #12
gh issue comment 13 --body "@code-development-agent Please implement..."
```

### Phase 2: Core Features (Parallel after Foundation)
Once #10-13 are merged, can assign multiple agents in parallel:
```bash
# UI Components (can run in parallel)
gh issue comment 14 --body "@code-development-agent Please implement..."
gh issue comment 15 --body "@code-development-agent Please implement..."
gh issue comment 18 --body "@code-development-agent Please implement..."
gh issue comment 19 --body "@code-development-agent Please implement..."

# Navigation & Layout (sequential within this group)
gh issue comment 16 --body "@code-development-agent Please implement..."
# Wait for #16, then:
gh issue comment 17 --body "@code-development-agent Please implement..."

# Forms (sequential: #14 before #20)
# After #14 completes:
gh issue comment 20 --body "@code-development-agent Please implement..."

# Charts (sequential: #17 before #21, then #21 before #22-24)
# After #17 and #21 complete:
gh issue comment 21 --body "@code-development-agent Please implement..."
# After #21:
gh issue comment 22 --body "@code-development-agent Please implement..."
gh issue comment 23 --body "@code-development-agent Please implement..."
gh issue comment 24 --body "@code-development-agent Please implement..."
```

### Phase 3: Advanced Features
```bash
# After #18 (modal) completes:
gh issue comment 25 --body "@code-development-agent Please implement..."
```

## Notes

- **Primary Agent**: `@code-development-agent` handles all implementation work
- **QA Support**: `@qa-testing-agent` validates each completed feature
- **Product Oversight**: `@bmad-agent` (Product Management) for strategic decisions
- **Documentation**: `@content-creation-agent` for user-facing docs if needed

All agents are custom GitHub Copilot agents configured in `.github/agents/` directory.
