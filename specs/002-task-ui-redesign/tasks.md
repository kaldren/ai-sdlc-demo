---

description: "Task list for feature implementation"
---

# Tasks: Task Tracker Visual Redesign

**Input**: Design documents from `/specs/002-task-ui-redesign/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md (N/A), contracts/design-system.md, quickstart.md

**Tests**: Not requested for this feature (presentation-only change; verified manually per quickstart.md, consistent with this project's existing frontend testing approach). No test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

## Path Conventions

All paths are under `src/frontend/` (existing web app frontend from `001-task-management`; no backend changes).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Bring in the new dependency and font asset needed by every user story

- [X] T001 [P] Add `lucide-react` as a dependency (`npm install lucide-react` in `src/frontend`), updating `src/frontend/package.json` and `src/frontend/package-lock.json`
- [X] T002 [P] Add Google Fonts preconnect + stylesheet `<link>` tags for "Inter" to `src/frontend/index.html`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the shared design-token stylesheet every screen depends on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Create `src/frontend/src/styles/global.css` with `:root` design tokens (`--color-primary`, `--color-primary-hover`, `--color-danger`, `--color-bg`, `--color-bg-subtle`, `--color-text`, `--color-text-muted`, `--color-border`, `--color-error-bg`, `--color-error-text`, `--font-family`, `--radius-md`, `--radius-lg`, `--space-sm/md/lg`, `--input-height`, `--button-height`) exactly as specified in `specs/002-task-ui-redesign/contracts/design-system.md`, plus a base reset (`* { box-sizing: border-box }`, `body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-family); }`)
- [X] T004 Import `src/frontend/src/styles/global.css` in `src/frontend/src/main.tsx` (depends on T003)

**Checkpoint**: Design tokens and font/icon dependency are in place; no visible change yet since no component styles reference them.

---

## Phase 3: User Story 1 - Modern, cohesive visual identity (Priority: P1) 🎯 MVP

**Goal**: Every screen (list, form, tabs, items) shares the new warm color palette, the Inter typeface, and visibly rounded surfaces, replacing today's unstyled browser defaults.

**Independent Test**: Load the app in a browser; confirm every screen shares the same palette/typeface/rounded-surface treatment with no unstyled elements remaining.

### Implementation for User Story 1

- [X] T005 [US1] Add page/container and heading styles to `src/frontend/src/styles/global.css` for `.tasks-page` (max-width, centered layout, padding, `h1` typography using design tokens)
- [X] T006 [US1] Add tab-nav styling to `src/frontend/src/styles/global.css` for `.tasks-page__tabs` and its `button` children, giving the active tab (`:disabled` state, per `TasksPage.tsx`) a distinct visual treatment from the inactive tab (FR-007)
- [X] T007 [US1] Add card/surface styling to `src/frontend/src/styles/global.css` for `.task-list` and `.task-item` (`--color-bg-subtle` background, `--color-border` border, `--radius-md` corners, `--space-md` internal spacing)
- [X] T008 [US1] Add alert/error message styling to `src/frontend/src/styles/global.css` for `[role="alert"]` using `--color-error-bg`/`--color-error-text` so errors stay clearly legible against the new palette (FR-008)

**Checkpoint**: App has a consistent Airbnb-inspired palette, typeface, and rounded surfaces across every screen. Inputs/buttons are still default-sized and icon-less (delivered in US2/US3).

---

## Phase 4: User Story 2 - Larger, friendlier input fields and buttons (Priority: P2)

**Goal**: Every text input and button is visibly larger and more rounded than the prior defaults, and remains fully functional.

**Independent Test**: Open the Add Task form and an Edit mode; confirm inputs/buttons render taller with generous padding and rounded corners, and still type/submit/cancel correctly.

### Implementation for User Story 2

- [X] T009 [P] [US2] Add enlarged/rounded input styling to `src/frontend/src/styles/global.css` for text `input` elements (`min-height: var(--input-height)`, horizontal padding via `--space-md`, `border-radius: var(--radius-md)`, `border: 1px solid var(--color-border)`, focus state using `--color-primary`)
- [X] T010 [P] [US2] Add enlarged/rounded button base styling to `src/frontend/src/styles/global.css` for `button` (`min-height: var(--button-height)`, horizontal padding via `--space-lg`, `border-radius: var(--radius-lg)`), plus `.btn-primary` / `.btn-secondary` / `.btn-danger` variant classes using `--color-primary`/neutral/`--color-danger` tokens (with `:disabled` and `:hover` states)
- [X] T011 [US2] Apply `btn-primary` to the "Add Task" submit button in `src/frontend/src/components/TaskForm.tsx` (className only, no behavior change)
- [X] T012 [US2] Apply button variant classNames in `src/frontend/src/components/TaskItem.tsx`: `btn-primary` for Save, `btn-secondary` for Cancel/Edit/Archive/Unarchive, `btn-danger` for Delete/Confirm (className only, no behavior change; Confirm uses danger rather than primary to more clearly signal the destructive action, per the Edge Cases note on distinguishing the delete-confirmation step)

**Checkpoint**: All inputs and buttons are visibly larger and rounded across the app; icons are still missing (delivered in US3).

---

## Phase 5: User Story 3 - Icon-labeled actions (Priority: P3)

**Goal**: Every button shows an icon representing its action alongside its existing text label, per the mapping in `contracts/design-system.md`.

**Independent Test**: Inspect every button in the app; confirm each shows the mapped icon plus its label, and that screen readers still announce a clear accessible name (FR-006).

### Implementation for User Story 3

- [X] T013 [US3] Add icon+label layout styling to `src/frontend/src/styles/global.css` (`display: inline-flex; align-items: center; gap: var(--space-sm);` on `button`, and icon `svg` sizing e.g. `width/height: 1.1em`)
- [X] T014 [P] [US3] Import `Plus` from `lucide-react` and render it before the "Add Task" label in `src/frontend/src/components/TaskForm.tsx`
- [X] T015 [P] [US3] Import `ListTodo` and `Archive` from `lucide-react` and render them before the "Active" and "Archived" tab labels respectively in `src/frontend/src/pages/TasksPage.tsx`
- [X] T016 [US3] Import `Pencil`, `Check`, `X`, `Archive`, `ArchiveRestore`, `Trash2` from `lucide-react` in `src/frontend/src/components/TaskItem.tsx` and render the mapped icon before each button's label in every state (view: Edit/Archive-Unarchive/Delete; editing: Save/Cancel; confirming: Confirm/Cancel), per the table in `contracts/design-system.md`

**Checkpoint**: All user stories complete — every button is enlarged, rounded, icon-labeled, and the whole app shares one consistent Airbnb-inspired visual system, with no functional regressions.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the redesign meets its measurable success criteria end-to-end

- [X] T017 [P] Verify each token color pair in `contracts/design-system.md` meets WCAG AA contrast (computed programmatically); adjust any failing token value (SC-004) — found `--color-primary: #FF385C` failed at 3.52:1 with white button text, darkened to `#E31C5F` (4.57:1); all other pairs already passed (danger 5.54:1, muted text 4.88:1, text 15.91:1, error text 5.72:1)
- [X] T018 [P] Reviewed `src/frontend/src/styles/global.css` for responsive safety from 375px to 1920px: `.tasks-page` uses `max-width` (not fixed width), inputs are `width: 100%`, and `.task-item__actions`/tab nav use `flex-wrap: wrap`, so no fixed-width elements can overflow or clip at narrow viewports (SC-005). Chrome browser automation was unavailable in this environment to visually confirm at each breakpoint — recommend a manual spot-check at 375px/768px/1920px before merge.
- [X] T019 Ran the functional flows against the live stack (`docker compose up`): full create → edit → archive → unarchive → delete lifecycle verified via the API (unchanged by this feature), and a production build (`tsc -b && vite build`) completed with zero errors, confirming no behavior regression (FR-009, SC-002). Chrome browser automation was unavailable to visually walk through `quickstart.md`'s UI checklist in this session — recommend opening http://localhost:5173 to confirm visually before merge.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — T001 and T002 can run in parallel
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories (T004 depends on T003)
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion; implemented in priority order P1 → P2 → P3 since each phase's CSS/markup builds on the previous phase's classes in the same shared `global.css` file
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — no dependency on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2); builds on the same `global.css` opened in US1 but does not require US1's specific rules to function — independently testable via its own Independent Test
- **User Story 3 (P3)**: Can start after Foundational (Phase 2); adds icons on top of whatever button styling exists — independently testable via its own Independent Test

### Within Each User Story

- Shared-file CSS tasks (global.css additions) before component markup tasks that rely on the new classNames
- Story complete before moving to next priority (recommended order, though stories are independently testable)

### Parallel Opportunities

- T001 and T002 (Setup) in parallel
- T009 and T010 (both add new, non-overlapping rule blocks to global.css) in parallel
- T014 and T015 (different component files) in parallel
- T017 and T018 (Polish, independent verification passes) in parallel

---

## Parallel Example: User Story 3

```bash
# Launch independent icon-import tasks together:
Task: "Import Plus from lucide-react and render it before the Add Task label in src/frontend/src/components/TaskForm.tsx"
Task: "Import ListTodo and Archive from lucide-react and render them before the Active/Archived tab labels in src/frontend/src/pages/TasksPage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Confirm the app has a consistent Airbnb-inspired look, then continue or demo as-is

### Incremental Delivery

1. Setup + Foundational → tokens/dependencies ready, no visual change yet
2. Add User Story 1 → consistent palette/typeface/rounded surfaces → demo (MVP)
3. Add User Story 2 → larger/rounder inputs and buttons → demo
4. Add User Story 3 → icons on every button → demo
5. Polish → contrast/responsive/manual-regression validation

---

## Notes

- No backend changes in this feature — all tasks are under `src/frontend/`
- `[P]` tasks touch different files (or clearly separable rule blocks within `global.css`) and have no dependency on each other
- Commit after each task or logical group
- Stop at any checkpoint to validate a story independently before moving to the next
