# Phase 1 Data Model: Dark Mode Toggle

**No backend/database entities are introduced or modified.** This feature does not touch `specs/001-task-management/data-model.md`'s `Task` entity, add any new table, field, or API payload shape, or require any migration. It is a client-side, presentation-only concern (per spec Assumptions).

## Client-side "entity": Theme Preference

The spec's Key Entities section defines this conceptually; it is realized purely in the browser, not in any backend store:

| Attribute | Detail |
|-----------|--------|
| Storage location | Browser `localStorage`, scoped per browser/device (never sent to the backend) |
| Key | `theme-preference` |
| Values | `"light"` \| `"dark"` — set only once the user makes an explicit choice (FR-005) |
| Absent state | No key present means "not yet chosen"; the app falls back to the auto-detected value from `prefers-color-scheme` (FR-002), which is *not* written to `localStorage` until an explicit toggle happens |
| Written by | `useTheme.ts`'s `toggleTheme()`, on every explicit toggle |
| Read by | The inline `<script>` in `index.html` (at first paint, to set `document.documentElement.dataset.theme`) and `useTheme.ts` (on mount, to initialize React state from the already-set DOM attribute) |
| Lifecycle / state transitions | `(absent) → "light"` or `(absent) → "dark"` on first explicit toggle; thereafter `"light" ⇄ "dark"` on every subsequent toggle. There is no transition back to "absent" — once chosen, a preference always exists for that browser/device (no "reset to system default" control is in scope per spec Assumptions) |

No relationships to any other entity; no validation rules beyond the two-value enum above (an unrecognized/corrupted stored value is treated the same as "absent" — falls back to auto-detection — so a malformed `localStorage` value cannot break rendering).
