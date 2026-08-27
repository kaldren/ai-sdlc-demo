# Implementation Plan: Dark Mode Toggle

**Branch**: `004-dark-mode` | **Date**: 2026-08-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-dark-mode/spec.md`

## Summary

Add a single-action, discoverable toggle that switches the entire Task Tracker frontend between the existing light theme (from `002-task-ui-redesign`) and a new dark counterpart, instantly and without a page reload or lost in-progress input. The theme is applied by setting a `data-theme="light" | "dark"` attribute on `<html>`, which selects a dark override block for the same CSS custom properties `002-task-ui-redesign` already defined in `src/frontend/src/styles/global.css` — no new styling paradigm, framework, or theming library. On first visit (no stored choice) the initial theme is read once from `prefers-color-scheme`, falling back to light; a tiny inline `<script>` in `index.html` sets the attribute before first paint to avoid a flash of the wrong theme. Once the user explicitly toggles, the choice is written to `localStorage` (`theme-preference: "light" | "dark"`) and takes priority on every future load. This is a frontend-only, presentation-layer change — no backend, API, or data model changes.

## Technical Context

**Language/Version**: TypeScript 5.x + React 18 (frontend only; no backend changes)

**Primary Dependencies**: React (existing), `lucide-react` (existing dependency from `002-task-ui-redesign`; reuses its `Sun`/`Moon` icons for the toggle — no new icon library); no new npm dependency added

**Storage**: N/A for backend/database. Client-side only: browser `localStorage` holds one key (`theme-preference`) for the persisted explicit choice; no new dependency, no cookies, no IndexedDB

**Testing**: Manual verification in the browser (dev server), consistent with `002-task-ui-redesign`'s approach — no dedicated frontend test framework exists in this project (see `001-task-management` plan's Complexity Tracking); no backend tests needed since no backend behavior changes

**Target Platform**: Web — same React SPA (Vite), served statically, no change to deployment target

**Project Type**: Web application — frontend-only change (`src/frontend`)

**Performance Goals**: Theme switch must be visually complete in well under one second (SC-004) — trivially met since switching is a single DOM attribute write plus a CSS custom-property re-resolution (no component remount, no network call, no re-fetch of tasks)

**Constraints**: Client-side/display-only (no backend calls, per spec Assumptions); switching MUST NOT remount the task list/form or discard in-progress input (FR-004); initial theme MUST be determined before/at first paint to avoid a visible flash of the wrong theme; all text/icons/buttons/inputs MUST meet WCAG AA contrast in both themes (FR-006, SC-005); color-coded semantic elements (active tab, destructive/danger actions, error alerts) MUST keep their meaning in dark mode even though exact hex values differ (FR-007)

**Scale/Scope**: Touches `index.html` (1 inline script), `src/frontend/src/styles/global.css` (1 new `[data-theme="dark"]` override block, reusing existing token names), and adds 2 small new frontend files (`src/hooks/useTheme.ts`, `src/components/ThemeToggle.tsx`); `TasksPage.tsx` gets one new rendered component. No changes to `TaskForm.tsx`, `TaskItem.tsx`, `TaskList.tsx`, or any backend/service code.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Fixed Technology Stack | Frontend remains React; no new framework, no CSS-in-JS/theming library, no new runtime dependency — reuses the existing `lucide-react` icon library | PASS |
| II. REST API Contract | No API endpoints added, changed, or removed | PASS (not applicable) |
| III. Backend Test Coverage (NON-NEGOTIABLE) | No backend code changes, so no new backend tests are required | PASS (not applicable) |
| IV. Frontend/Backend Separation | No new data access introduced; theme preference lives entirely in browser `localStorage`, never sent to or read from the backend; frontend continues to call only the existing REST API via `taskApi.ts`, unchanged | PASS |
| V. Simplicity First (YAGNI) | Reuses `002-task-ui-redesign`'s existing CSS-custom-property token mechanism (just adds a dark override block keyed off a `data-theme` attribute) instead of introducing a theming library, CSS-in-JS, or a Context provider; a plain custom hook is used instead of React Context because there is exactly one consumer (the toggle button) — Context can be introduced later only if a second consumer emerges | PASS |

No violations — Complexity Tracking table is not needed.

*Re-checked after Phase 1 design: unchanged. `data-model.md` confirms the only "entity" is a client-side `localStorage` preference (no backend/data-model impact); `contracts/theming-contract.md` documents the `data-theme` attribute, the dark token overrides, and the `useTheme` hook's small surface area, all of which stayed within the plain-CSS + custom-property approach — no new dependency or abstraction was introduced during design.*

## Project Structure

### Documentation (this feature)

```text
specs/004-dark-mode/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md         # Phase 1 output (/speckit-plan command) — client-side Theme Preference only, no backend entities
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/            # Phase 1 output (/speckit-plan command)
│   └── theming-contract.md  # data-theme attribute, dark token table, useTheme hook surface, localStorage key
└── tasks.md              # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/frontend/
├── index.html                    # + inline theme-init <script> (sets data-theme on <html> before first paint)
└── src/
    ├── hooks/
    │   └── useTheme.ts           # NEW: reads/writes localStorage + data-theme attribute; exposes {theme, toggleTheme}
    ├── styles/
    │   └── global.css            # + `[data-theme="dark"]` block overriding existing design tokens (no new token names)
    ├── pages/
    │   └── TasksPage.tsx         # + renders <ThemeToggle /> in the page header
    └── components/
        └── ThemeToggle.tsx       # NEW: single button, Sun/Moon icon (lucide-react), toggles theme via useTheme
```

**Structure Decision**: No structural changes to the existing `src/frontend` layout from `001-task-management`/`002-task-ui-redesign`. This feature adds one new directory, `src/hooks/`, holding a single hook (`useTheme.ts`), plus one new component (`ThemeToggle.tsx`) alongside the existing `TaskForm`/`TaskItem`/`TaskList` components. `global.css` gains a dark override block but keeps every existing token name and selector from `002-task-ui-redesign` unchanged, so `TaskForm.tsx`, `TaskItem.tsx`, and `TaskList.tsx` require no code changes — they already render exclusively via those tokens.

## Complexity Tracking

*No Constitution Check violations — table intentionally left empty.*
