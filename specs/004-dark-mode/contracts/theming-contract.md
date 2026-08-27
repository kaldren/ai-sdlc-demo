# UI Contract: Theme Attribute, Dark Tokens & Toggle Behavior

This is the "interface contract" for this feature — the fixed mechanism, dark token values, and toggle behavior that `/speckit-tasks` and `/speckit-implement` must apply, so dark mode covers 100% of the app (FR-003) consistently rather than ad hoc per component. It extends, and does not modify, `specs/002-task-ui-redesign/contracts/design-system.md` — every token *name* below already exists there; only new dark *values* are introduced.

## Theme attribute

- **Attribute**: `data-theme` on `<html>` (`document.documentElement`)
- **Values**: `"light"` | `"dark"` (always one of these two once the app has run its init script; no third value)
- **Set by**: an inline `<script>` in `index.html`'s `<head>`, executed synchronously before first paint, and thereafter by `useTheme.ts`'s `toggleTheme()`

## Resolution order (on load)

1. `localStorage.getItem('theme-preference')` — if `"light"` or `"dark"`, use it.
2. Otherwise, `window.matchMedia('(prefers-color-scheme: dark)').matches` — if `true`, use `"dark"`.
3. Otherwise (no stored preference and no readable OS preference, e.g. `matchMedia` unsupported), use `"light"`.

This order is evaluated once, synchronously, in the `index.html` inline script, and mirrored by `useTheme.ts` on mount to set its initial React state (it does not re-run the detection — it reads the attribute the inline script already set, to avoid a second, possibly-inconsistent decision).

## `useTheme` hook surface (`src/frontend/src/hooks/useTheme.ts`)

```ts
function useTheme(): {
  theme: "light" | "dark";
  toggleTheme: () => void;
};
```

- `toggleTheme()` flips `theme`, updates `document.documentElement.dataset.theme` immediately (synchronously, in the same event handler — no `useEffect` round-trip that could introduce a visible delay), and writes the new value to `localStorage['theme-preference']`.
- Calling `toggleTheme()` MUST NOT cause the task list to re-fetch, the form inputs to reset, or any component to remount — it only changes the `data-theme` attribute and re-renders the (single) `ThemeToggle` button for its own icon/label swap (FR-004).

## `ThemeToggle` component (`src/frontend/src/components/ThemeToggle.tsx`)

| State | Icon (`lucide-react`) | `aria-label` |
|-------|------------------------|----------------|
| Current theme is light | `Moon` | "Switch to dark mode" |
| Current theme is dark | `Sun` | "Switch to light mode" |

Rendered once, in `TasksPage`'s header, next to the `<h1>`. Uses the existing `.btn-secondary` button styling (no new button variant needed).

## Dark token values (`src/frontend/src/styles/global.css`, under `[data-theme="dark"]`)

| Token | Light value (unchanged, `:root`) | Dark value (new) |
|-------|-----------------------------------|-------------------|
| `--color-primary` | `#E31C5F` | `#E31C5F` |
| `--color-primary-hover` | `#C81552` | `#C81552` |
| `--color-danger` | `#C13515` | `#F0674C` |
| `--color-danger-hover` | `#A32C11` | `#A52B12` |
| `--color-bg` | `#FFFFFF` | `#121212` |
| `--color-bg-subtle` | `#FFF8F6` | `#1E1E1E` |
| `--color-text` | `#222222` | `#F2F2F2` |
| `--color-text-muted` | `#717171` | `#B8B8B8` |
| `--color-border` | `#EBEBEB` | `#3A3A3A` |
| `--color-error-bg` | `#FDECEA` | `#3A1712` |
| `--color-error-text` | `#B3261E` | `#F4877B` |

`--font-family`, `--radius-md`, `--radius-lg`, `--space-sm`/`--space-md`/`--space-lg`, `--input-height`, `--button-height` are unchanged in dark mode (colors only change, per spec Assumptions).

WCAG AA contrast verification (≥4.5:1 for normal text) for every text/background pairing above is documented in `research.md`.

### CSS rule change required alongside the token table

`.btn-danger:hover` in `global.css` currently sets `background: var(--color-danger)` (reusing the same token used for its resting-state text color). Under dark mode this pairing fails AA (a value legible as text on `#121212` cannot also give white text ≥4.5:1 as a background — see `research.md`). Implementation MUST change `.btn-danger:hover`'s background to `var(--color-danger-hover)` in **both** themes (giving the previously-unused `--color-danger-hover` token its first real consumer), rather than introducing a third, dark-only-only rule — this keeps one CSS rule serving both themes via token overrides, consistent with the rest of the stylesheet.

## Non-goals

- No "system"/auto third mode persisted as an ongoing selectable option — system preference is only ever the *first-visit default* (FR-002), never a persisted third value of `theme-preference` (per spec Assumptions: only light and dark are in scope).
- No live re-theming in response to OS `prefers-color-scheme` changes after the app has loaded (see `research.md`).
- No per-component theme props or React Context — theming is entirely CSS-variable-driven off the single `data-theme` attribute.
- No high-contrast mode or scheduled/time-of-day switching (out of scope per spec Assumptions).
