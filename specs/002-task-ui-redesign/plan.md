# Implementation Plan: Task Tracker Visual Redesign

**Branch**: `002-task-ui-redesign` | **Date**: 2026-08-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-task-ui-redesign/spec.md`

## Summary

Restyle the existing Task Tracker frontend (task list, task form, task item, active/archived tabs) with an Airbnb-inspired visual system: a warm coral/neutral color palette, the Inter typeface, larger and more rounded inputs/buttons, and an icon on every button via `lucide-react`. This is a presentation-only change — no backend, data model, or API changes. Styling is implemented as plain CSS (a global stylesheet + design tokens) to stay consistent with Principle V (Simplicity First); no CSS framework or CSS-in-JS library is introduced.

## Technical Context

**Language/Version**: TypeScript 5.x + React 18 (frontend only; no backend changes)

**Primary Dependencies**: `lucide-react` (icon set, new supporting dependency), Google Fonts "Inter" (loaded via `<link>` in `index.html`), plain CSS (no CSS framework/CSS-in-JS added)

**Storage**: N/A — no data model or persistence changes

**Testing**: Manual verification in the browser (dev server), consistent with this project's existing frontend approach (no dedicated frontend test framework — see `001-task-management` plan's Complexity Tracking); no backend tests needed since no backend behavior changes

**Target Platform**: Web — same React SPA (Vite), served statically, no change to deployment target

**Project Type**: Web application — frontend-only change (`src/frontend`)

**Performance Goals**: No functional performance target; keep the added payload minimal (one small icon library + one hosted font) so initial load stays comparable to today

**Constraints**: Visual/presentation-only (FR-009) — must not alter component behavior, data flow, or API contracts; must meet WCAG AA contrast (SC-004); must remain usable from 375px to 1920px viewport widths (SC-005)

**Scale/Scope**: Touches 4 existing frontend components (`TasksPage`, `TaskForm`, `TaskItem`, `TaskList`), `index.html` (font link), one new global stylesheet, and one new npm dependency (`lucide-react`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Fixed Technology Stack | Frontend remains React; `lucide-react` is a supporting icon library (not a replacement frontend framework), and Google Fonts is a font asset, not a stack component | PASS |
| II. REST API Contract | No API endpoints added, changed, or removed | PASS (not applicable) |
| III. Backend Test Coverage (NON-NEGOTIABLE) | No backend code changes, so no new backend tests are required | PASS (not applicable) |
| IV. Frontend/Backend Separation | No new data access introduced; frontend continues to call only the existing REST API via `taskApi.ts`, unchanged | PASS |
| V. Simplicity First (YAGNI) | Plain global CSS + design tokens (no CSS-in-JS, no Tailwind/CSS framework, no theming engine); one small, focused icon library instead of a full UI kit | PASS |

No violations — Complexity Tracking table is not needed.

*Re-checked after Phase 1 design: unchanged — the design system (research.md) and UI contract (contracts/design-system.md) stayed within the same plain-CSS, single-icon-library scope; no new dependency beyond `lucide-react` was introduced.*

## Project Structure

### Documentation (this feature)

```text
specs/002-task-ui-redesign/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md         # Phase 1 output (/speckit-plan command) — N/A, no data model changes
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   └── design-system.md  # Color/typography/spacing tokens + icon-per-button mapping
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/frontend/
├── index.html                    # + Google Fonts "Inter" <link>
├── package.json                  # + lucide-react dependency
└── src/
    ├── main.tsx                  # + import of global stylesheet
    ├── styles/
    │   └── global.css            # NEW: design tokens (CSS custom properties) + base/reset + shared styles
    ├── pages/
    │   └── TasksPage.tsx         # restyled: layout, tabs get icons
    └── components/
        ├── TaskForm.tsx          # restyled: larger/rounder inputs + button, icon on Add Task
        ├── TaskItem.tsx          # restyled: larger/rounder inputs + buttons, icons on Edit/Save/Cancel/Archive/Delete/Confirm
        └── TaskList.tsx          # restyled: list/empty-state spacing (no new icons)
```

**Structure Decision**: No structural changes to the existing `src/frontend` layout from `001-task-management`. Styling is added as a single new `src/frontend/src/styles/global.css` (design tokens + base styles) imported once from `main.tsx`, plus per-component className/markup updates in the four existing components. No new directories beyond `src/styles/`.

## Complexity Tracking

*No Constitution Check violations — table intentionally left empty.*
