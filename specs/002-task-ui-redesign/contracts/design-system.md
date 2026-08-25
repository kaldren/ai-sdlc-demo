# UI Contract: Design Tokens & Icon Mapping

This is the "interface contract" for this feature: the fixed set of design tokens and the button→icon mapping that `/speckit-tasks` and `/speckit-implement` must apply consistently across every screen, so the redesign satisfies FR-001–FR-007 uniformly rather than ad hoc per component.

## Design Tokens (CSS custom properties, defined in `src/styles/global.css`)

| Token | Value | Used for |
|-------|-------|----------|
| `--color-primary` | `#E31C5F` | Primary buttons, active tab indicator, focus rings, links |
| `--color-primary-hover` | `#C81552` | Primary button/tab hover state |
| `--color-danger` | `#C13515` | Delete / destructive confirm actions |
| `--color-bg` | `#FFFFFF` | Page background |
| `--color-bg-subtle` | `#FFF8F6` | Card/panel background |
| `--color-text` | `#222222` | Primary text |
| `--color-text-muted` | `#717171` | Secondary text, placeholders, inactive tab |
| `--color-border` | `#EBEBEB` | Input/card borders, dividers |
| `--color-error-bg` | `#FDECEA` | Error/alert message background |
| `--color-error-text` | `#B3261E` | Error/alert message text |
| `--font-family` | `"Inter", "Helvetica Neue", Arial, sans-serif` | All text |
| `--radius-md` | `12px` | Inputs |
| `--radius-lg` | `999px` (pill) | Buttons |
| `--space-sm` / `--space-md` / `--space-lg` | `8px` / `16px` / `24px` | Padding/gaps |
| `--input-height` | `48px` | Text input min-height |
| `--button-height` | `48px` | Button min-height |

All colors above meet WCAG AA contrast (≥4.5:1) against the background they pair with (`--color-primary`/`--color-danger` white text on the button; `--color-text`/`--color-text-muted` on `--color-bg`/`--color-bg-subtle`), satisfying SC-004. Verified: white-on-`--color-primary` 4.57:1, white-on-`--color-danger` 5.54:1, `--color-text-muted`-on-`--color-bg` 4.88:1, `--color-text`-on-`--color-bg` 15.91:1, `--color-error-text`-on-`--color-error-bg` 5.72:1. (The initially-chosen `#FF385C` primary only reached 3.52:1 with white text and was darkened to `#E31C5F` during implementation to pass AA — see research.md.)

## Icon Mapping (`lucide-react`)

Every button below MUST render the mapped icon plus its existing text label (or an `aria-label` matching that label if the button becomes icon-only), per FR-005/FR-006.

| Button | Component | Icon (`lucide-react`) |
|--------|-----------|------------------------|
| Add Task | `TaskForm` | `Plus` |
| Active tab | `TasksPage` | `ListTodo` |
| Archived tab | `TasksPage` | `Archive` |
| Edit | `TaskItem` | `Pencil` |
| Save | `TaskItem` (editing) | `Check` |
| Cancel (edit mode) | `TaskItem` (editing) | `X` |
| Archive | `TaskItem` (not archived) | `Archive` |
| Unarchive | `TaskItem` (archived) | `ArchiveRestore` |
| Delete | `TaskItem` | `Trash2` |
| Confirm (delete) | `TaskItem` (confirming) | `Check` |
| Cancel (delete confirmation) | `TaskItem` (confirming) | `X` |

## Non-goals

- No dark theme variant (per spec Assumptions).
- No change to component props, event handlers, or any data passed to/from `taskApi.ts`.
