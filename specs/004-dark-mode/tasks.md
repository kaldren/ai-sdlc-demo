---

description: "Task list for Dark Mode Toggle"
---

# Tasks: Dark Mode Toggle

**Input**: Design documents from `/specs/004-dark-mode/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md (client-side
`theme-preference` only — no backend entities), contracts/theming-contract.md, quickstart.md

**Tests**: Not requested for this feature (frontend-only, presentation-layer change); verified
manually per `quickstart.md`'s 10-point checklist, consistent with `002-task-ui-redesign`'s
approach — no dedicated frontend test framework exists in this project (see `001-task-management`
plan's Complexity Tracking). No automated test tasks are included; each `quickstart.md` check is
instead mapped to an explicit verification task below.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing
of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

## Path Conventions

All paths are under `src/frontend/` (existing web app frontend from `001-task-management` /
`002-task-ui-redesign`); no backend changes (plan.md Project Structure).

---

## Phase 1: Setup (Shared Infrastructure)

**Not applicable.** No new project, dependency, or scaffolding is needed — `lucide-react` is
already an installed dependency (added in `002-task-ui-redesign`) and its existing `Sun`/`Moon`
icons are reused directly, with no new npm package added (plan.md Primary Dependencies). Work
begins directly at Phase 2.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the dark theme's CSS token values and the initial-theme resolution
mechanism that both user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T001 [P] Add a `[data-theme="dark"]` override block to `src/frontend/src/styles/global.css`, redefining the existing token names (`--color-primary`, `--color-primary-hover`, `--color-danger`, `--color-danger-hover`, `--color-bg`, `--color-bg-subtle`, `--color-text`, `--color-text-muted`, `--color-border`, `--color-error-bg`, `--color-error-text`) with the dark values from `contracts/theming-contract.md`'s token table; leave the `:root` light values and all non-color tokens (`--font-family`, `--radius-md`, `--radius-lg`, `--space-sm/md/lg`, `--input-height`, `--button-height`) unchanged (FR-003, FR-006, FR-007)
- [X] T002 [P] Fix `.btn-danger:hover` in `src/frontend/src/styles/global.css` to set `background: var(--color-danger-hover)` (currently `background: var(--color-danger)`) so the rule works in **both** themes — required because reusing `--color-danger` for both its resting-state text color and its hover-state background cannot satisfy WCAG AA in both roles against the dark `--color-bg` (`contracts/theming-contract.md` "CSS rule change required alongside the token table"; `research.md` contrast verification); this gives the previously-declared-but-unused `--color-danger-hover` token its first real consumer
- [X] T003 [P] Add an inline, synchronous `<script>` at the top of `<head>` in `src/frontend/index.html`, executed before the React bundle loads, that resolves the initial theme per `contracts/theming-contract.md`'s resolution order — `localStorage.getItem('theme-preference')` if it is `"light"` or `"dark"`; otherwise `window.matchMedia('(prefers-color-scheme: dark)').matches` → `"dark"`; otherwise `"light"` — and sets `document.documentElement.dataset.theme` to the result before first paint, so no visible flash of the wrong theme occurs (FR-002, SC-004)

**Checkpoint**: Dark token values exist and are selectable via `data-theme="dark"`, `.btn-danger:hover` passes AA contrast in both themes, and the correct initial theme is resolved and set before first paint on every load. Nothing yet lets the user change `data-theme` interactively — that arrives in User Story 1.

---

## Phase 3: User Story 1 - Manually switch between light and dark mode (Priority: P1) 🎯 MVP

**Goal**: A visible, discoverable control lets the user flip the entire app between the light and
dark color schemes instantly, with no reload and no lost in-progress input.

**Independent Test**: Open the app, activate the theme control, and confirm every visible screen
(task list, task form, task items, tabs) immediately re-renders in the dark color scheme, then
switch back and confirm it returns to light — all without a page reload or any data/input loss.

### Implementation for User Story 1

- [X] T004 [US1] Create the `useTheme` hook in `src/frontend/src/hooks/useTheme.ts` exposing `{ theme: "light" | "dark"; toggleTheme: () => void }` per `contracts/theming-contract.md`: initialize React state by reading the `data-theme` attribute the inline script (T003) already set on `document.documentElement` (do not re-run detection); `toggleTheme()` synchronously flips `theme`, updates `document.documentElement.dataset.theme`, and writes the new value to `localStorage['theme-preference']` — all within the same event handler, with no `useEffect` round-trip that could introduce a visible delay (FR-004, FR-005)
- [X] T005 [US1] Create the `ThemeToggle` component in `src/frontend/src/components/ThemeToggle.tsx`: a single button using the existing `.btn-secondary` styling and the `useTheme` hook (T004) — shows the `Moon` icon (`lucide-react`) with `aria-label="Switch to dark mode"` when `theme === "light"`, and the `Sun` icon with `aria-label="Switch to light mode"` when `theme === "dark"` (FR-001; depends on T004)
- [X] T006 [US1] Render `<ThemeToggle />` in `src/frontend/src/pages/TasksPage.tsx`'s header, next to the `<h1>` (depends on T005)
- [X] T007 [US1] Manually verify per `quickstart.md` checks 1, 2, and 9: clicking the toggle immediately switches every visible screen/state (task list, task form, task items, Active/Archived tabs, an item being edited, the delete-confirmation state) between light and dark with no page reload (confirm via the Network tab: no new document request) and no lost in-progress form input (FR-003, FR-004); the toggle is reachable by keyboard, shows a visible focus state, and its accessible name updates correctly between "Switch to dark mode" / "Switch to light mode" (FR-001) (depends on T004–T006)

**Checkpoint**: The app has a fully working, discoverable dark-mode toggle covering every screen. Reloading still defaults to auto-detection each time (no persistence yet) — that arrives in User Story 2.

---

## Phase 4: User Story 2 - Theme preference is remembered (Priority: P2)

**Goal**: A user's explicitly chosen theme stays in effect on every future visit to the app in the
same browser, without needing to re-select it.

**Independent Test**: Switch the theme, reload the page (or close and reopen the tab), and confirm
the previously selected theme is still applied on load.

### Implementation for User Story 2

- [X] T008 [P] [US2] Manually verify per `quickstart.md` check 5: toggle to dark mode and reload the page — it loads directly in dark mode; toggle to light mode and reload again (or reopen the tab) — it loads directly in light mode. Confirms the explicit choice written by `toggleTheme` (T004) and read back by the inline script (T003) persists across a real reload, not just in-memory client state (FR-005, SC-003) (depends on Phase 2 + T004–T006)
- [X] T009 [P] [US2] Manually verify per `quickstart.md` check 6: with the browser's emulated `prefers-color-scheme` set to `dark` (DevTools Rendering tab) but an explicit `theme-preference: "light"` already stored in `localStorage`, reload the page and confirm it loads light — the explicit stored choice overrides auto-detection, per the resolution order set up in T003 (FR-005) (depends on Phase 2 + T004–T006)

**Checkpoint**: Both user stories are complete — the toggle works instantly across the whole app (US1) and the chosen theme survives reloads and new visits (US2), with system-preference auto-detection only ever applying before any explicit choice exists.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate the remaining `quickstart.md` checks that cut across both stories — first-visit
auto-detection, flash prevention, accessibility contrast, preserved semantic meaning, and no
regression to existing task behavior.

- [X] T010 [P] Verify per `quickstart.md` check 7 and `research.md`'s computed contrast values: spot-check WCAG AA contrast (≥4.5:1 for normal text) in both themes for task title text, muted description text, button labels, and the error alert, using the browser DevTools contrast-ratio readout (FR-006, SC-005) (depends on T001, T002)
- [X] T011 [P] Verify per `quickstart.md` check 3: clear `localStorage` for the site, emulate `prefers-color-scheme: dark` (DevTools Rendering tab), reload — the app loads directly in dark mode with no toggle click needed; repeat with `light` (or no preference) and confirm it loads light (FR-002) (depends on T003)
- [X] T012 [P] Verify per `quickstart.md` check 4: with `theme-preference` set to `"dark"` in `localStorage`, hard-reload the page repeatedly and confirm it never visibly flashes light before showing dark — directly validates the inline script added in T003 (SC-004) (depends on T003)
- [X] T013 [P] Verify per `quickstart.md` check 8: in dark mode, confirm the active tab is still visually distinguished the same way as in light mode, the Delete button still reads as a destructive/red action, and a validation error (e.g. submitting an empty title) still renders as a red alert — just with the dark-tuned hex values from T001/T002 (FR-007) (depends on T001, T002, T004–T006)
- [X] T014 Run the full task CRUD regression per `quickstart.md` check 10: create, edit, archive/unarchive, and delete a task in both light and dark mode, confirming identical API calls in the Network tab and identical behavior to before this feature — this is purely a presentation-layer change (depends on all prior phases)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A — nothing to build.
- **Foundational (Phase 2)**: No dependencies — T001, T002, and T003 touch different files (or non-overlapping rule blocks within `global.css`) and can run in parallel. BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion (T001–T003). T004 → T005 → T006 → T007 are sequential (each builds on the previous file).
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) and User Story 1 (Phase 3) — persistence relies on `toggleTheme` (T004) writing `localStorage` and the inline script (T003) reading it back on load. T008 and T009 are independent verification passes and can run in parallel.
- **Polish (Phase 5)**: Depends on the phases each task references (see individual task dependencies above); T014 depends on all prior phases being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — no dependency on other stories.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2), but is only meaningfully testable once User Story 1's toggle exists (there is no way to make an "explicit choice" to persist without it) — implemented and verified after US1 in practice, though its acceptance scenarios are independently defined in spec.md.

### Within Each User Story

- User Story 1: T004 (hook) → T005 (component, imports the hook) → T006 (wiring into `TasksPage.tsx`) → T007 (manual verification of the built toggle).
- User Story 2: T008 and T009 are both read-only manual verification passes against the already-built mechanism — no file edits, no ordering dependency between them.

### Parallel Opportunities

- T001, T002, and T003 (Foundational) in parallel — different files/non-overlapping rule blocks, no shared dependency.
- T008 and T009 (User Story 2) in parallel — independent manual checks against the same running app.
- T010, T011, T012, and T013 (Polish) in parallel — independent verification passes covering different `quickstart.md` checks.

---

## Parallel Example: Foundational Phase

```bash
# Launch independent foundational tasks together:
Task: "Add [data-theme=\"dark\"] override block to src/frontend/src/styles/global.css"
Task: "Fix .btn-danger:hover in src/frontend/src/styles/global.css to use --color-danger-hover"
Task: "Add inline theme-init <script> to src/frontend/index.html's <head>"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (dark tokens, `.btn-danger:hover` fix, inline resolution script).
2. Complete Phase 3: User Story 1 (the toggle itself).
3. **STOP and VALIDATE**: Confirm the toggle instantly switches every screen with no reload/data loss, then continue or demo as-is. At this point the theme still resets to auto-detected on every reload (no persistence) — acceptable as a standalone MVP per spec.md's priority ordering.

### Incremental Delivery

1. Foundational → dark palette and flash-free initial-theme resolution are in place, but nothing is user-triggerable yet.
2. Add User Story 1 → working, discoverable dark-mode toggle across the whole app → demo (MVP).
3. Add User Story 2 → explicit choice survives reloads/new visits → demo.
4. Polish → auto-detection, no-flash, contrast, semantic-meaning, and CRUD-regression checks confirm every success criterion (SC-001–SC-005).

---

## Notes

- No backend changes in this feature — all tasks are under `src/frontend/`.
- `[P]` tasks touch different files (or clearly separable rule blocks within `global.css`) and have no dependency on each other.
- Both items flagged in the plan as needing their own task are represented above: initial-theme flash prevention is T003 (Foundational, verified in T012); the `.btn-danger:hover` → `--color-danger-hover` fix is T002 (Foundational, verified in T010/T013).
- Commit after each task or logical group.
- Stop at any checkpoint to validate a story independently before moving to the next.
