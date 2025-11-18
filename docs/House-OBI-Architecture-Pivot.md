# House of OBI – Pivoted Architecture & Work Plan

_Last updated: 2025-11-16_

## 1. Strategic Pivot

- Remove Vercel-centric deployment configs; rely on MCP connectors and cloud-agnostic deployment skills.
- Move all gamification and questing implementation items (issues, TODOs, stories) into the product backlog.
- Prioritize completion and stabilization of the astrological engine as the foundation for all gamification, quests, and adaptive content.

## 2. Updated High-Level Architecture

### 2.1 Core Layers

1. **Astrological Engine (Priority Now)**
   - Syncretic archetype & aspect data store (systems, elements, houses, planets, patterns).
   - Profile calculation pipelines (natal, synastry, timing/transits) with validation.
   - Public API for: profile snapshots, archetypal scores, timing signals, and "seed" objects for quests.

2. **Agent & Tooling Layer (MCP + RAG)**
   - MCP connections for filesystem, repo management, and external tools.
   - LangChain / RAG agents operating over `/langchain-dev-orchestrator/mula_knowledge_base`.
   - Skill library for: content retrieval, explanation, summarization, and quest seeding based on astrological outputs.

3. **Experience Layer (Deferred Until Astrology Stable)**
   - Quest engine (templates, branching logic, pacing) consuming astrological seeds.
   - Gamification engine (XP, streaks, achievements, levels) wired to quest and practice completion.
   - UX surfaces: onboarding, profile dashboard, insights feed, quest views, progress views.

### 2.2 Module Folders (Target Structure)

- `/astrology/`
  - `engine/` – core calculation logic, ephemeris integration, composite profiles.
  - `data/` – archetypes, mappings, rules, weightings.
  - `api/` – stable interface for other modules and agents.
  - `tests/` – regression suite to keep outputs stable.

- `/agents/`
  - `skills/` – MCP-based tools and LangChain tools.
  - `orchestrators/` – multi-step agents (e.g., "explain chart", "generate quest seeds").
  - `pipelines/` – RAG flows over `mula_knowledge_base`.

- `/experience/`
  - `quests/` – quest templates, flows, but marked experimental or feature-flagged.
  - `gamification/` – XP/streaks/badges/levels.
  - `ui/` – components and pages for the app front-end.

- `/analytics/`
  - Event schema, tracking, experiment flags, funnels.

## 3. Current Focus: Astrological Engine

### 3.1 Completion Checklist

- [ ] Define canonical syncretic data model (signs, houses, planets, aspects, patterns, archetypes).
- [ ] Implement core natal chart calculation and archetype scoring.
- [ ] Implement relationship/synastry scoring (where in scope for v1).
- [ ] Implement timing/transit scoring (MVP level for v1).
- [ ] Create a stable public API (`/astrology/api`) for:
  - [ ] `get_profile(archetype_view)`
  - [ ] `get_relationship_profile` (if in v1)
  - [ ] `get_timing_signals`
  - [ ] `get_quest_seeds_from_profile`
- [ ] Build and run regression tests for key example charts.

### 3.2 Interfaces for Agents & Tools

- Input: birth data, relationship data, current time window, plus user state.
- Output: structured JSON objects with archetype scores, narrative tags, and practice/quest seed hints.
- Contract: agents and quest systems treat astrology as read-only, stable API; they do not implement their own chart logic.

## 4. Gamification & Quests — Backlog For Now

- Move all quest/gamification tickets to Backlog with tags:
  - `feature:questing`, `feature:gamification`, `blocked:astrology-engine`.
- Defer implementation of:
  - New quest templates beyond what is needed for testing astrology outputs.
  - XP/streak progression logic.
  - Achievement/badge systems.
  - Long-term narrative arcs and multi-stage campaigns.

## 5. MCP-Driven Workflow From Here

1. Use MCP filesystem and repo tools to:
   - Keep this architecture document updated as decisions change.
   - Inspect and refactor the codebase into the target module structure.

2. Use MCP-connected agents to:
   - Identify and remove or neutralize Vercel-specific configs.
   - Locate and tag quest/gamification-related issues and TODOs for backlog movement.

3. Keep the astrological engine as the only active implementation priority until:
   - All items in Section 3.1 are complete.
   - API contracts in Section 3.2 are stable and documented.

---

This document is the single source of truth for the current pivot and priorities until superseded by a new version.
