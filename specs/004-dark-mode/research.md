# Phase 0 Research: Dark Mode Toggle

## Decision: Theme application mechanism — `data-theme` attribute + CSS custom-property overrides

- **Decision**: Set `data-theme="light"` or `data-theme="dark"` on `document.documentElement` (`<html>`). `src/frontend/src/styles/global.css` gains a single `[data-theme="dark"] { ... }` block that redefines the exact same custom-property names `002-task-ui-redesign` already declared on `:root` (`--color-primary`, `--color-bg`, `--color-text`, etc.), with dark-tuned values. The light values already in `:root` remain the default (used when `data-theme="light"` or, defensively, when the attribute is absent).
- **Rationale**: `002-task-ui-redesign` already centralized every color used across `TaskForm`, `TaskItem`, `TaskList`, and `TasksPage` behind CSS custom properties (`contracts/design-system.md`). Because every component already renders exclusively via those tokens (verified by inspection of `global.css` and all four components — no inline hex colors or hard-coded styles exist outside the stylesheet), redefining the token *values* under a `[data-theme="dark"]` selector re-themes 100% of the app (FR-003) with zero component code changes. This directly satisfies constitution Principle V (Simplicity First) — no CSS-in-JS, no theming library (e.g. `styled-components` `ThemeProvider`, `next-themes`), and no new build dependency.
- **Alternatives considered**: A `.dark` class toggled on `<body>` (rejected — functionally equivalent to the attribute approach but `data-theme` is more idiomatic for a two-value enum and reads better in DevTools); duplicating every component's className with light/dark variants (rejected — would require touching every component, contradicting FR-003's "no screen left unstyled" and directly undoing the whole point of `002-task-ui-redesign`'s token system); a CSS-in-JS theming library (rejected — new runtime dependency disproportionate to swapping ~11 token values, violates Principle V).

## Decision: First-visit default — `prefers-color-scheme`, read once, no live OS-change listener

- **Decision**: On first visit (no `theme-preference` in `localStorage`), read `window.matchMedia('(prefers-color-scheme: dark)').matches` once to pick the initial theme; if `matchMedia` is unavailable or the media query can't be evaluated, default to light. This value is *not* persisted to `localStorage` (persistence only happens on an explicit user toggle, per FR-005) and is *not* re-evaluated live if the OS preference changes later in the same session while still unset — the spec's edge cases and FR-002 only describe first-visit detection, not continuous OS-preference syncing.
- **Rationale**: FR-002 requires only a one-time detection at first visit with a documented light fallback; FR-005 requires the *explicit* choice to override auto-detection going forward. Adding a `matchMedia` `change` listener that keeps re-theming an already-unset session would be speculative behavior not requested by any acceptance scenario — out of scope per Principle V (YAGNI). This was a pre-resolved judgment call per the approved spec, not a new one introduced here.
- **Alternatives considered**: Live-syncing to OS preference changes via a `matchMedia` `change` event listener even before an explicit choice is made (rejected — not required by any FR/SC, adds an event-listener lifecycle to manage for no requested behavior); reading the preference lazily inside a `useEffect` after mount (rejected — see next decision, this causes a visible flash of the wrong theme).

## Decision: Flash-of-wrong-theme avoidance — inline synchronous `<script>` in `index.html`

- **Decision**: Add a small inline (non-module, non-deferred) `<script>` at the top of `index.html`'s `<head>`, executed synchronously during HTML parsing, that reads `localStorage.getItem('theme-preference')` (falling back to `prefers-color-scheme` per the decision above) and sets `document.documentElement.dataset.theme` before the React bundle loads or the app mounts. `src/hooks/useTheme.ts` then reads that already-set attribute for its initial React state instead of re-deciding the theme.
- **Rationale**: If the theme were instead set inside a React `useEffect` after mount, there would be a visible frame (or more) where the page renders with the default light tokens before flipping to dark for a returning dark-mode user — a poor experience and arguably a violation of "instant, no perceptible delay" (SC-004) at load time. Setting the attribute synchronously before the stylesheet's rules are applied (the CSS is bundled via `main.tsx`'s `import "./styles/global.css"`, so it only takes effect once the module script runs/paints) means the correct theme is already selected by the time any paint happens, with no separate network request or dependency needed.
- **Alternatives considered**: Setting the theme inside a `useEffect`/`useLayoutEffect` in `App.tsx` (rejected — causes the flash described above); server-side rendering the initial theme (rejected — this is a static Vite SPA with no server-rendering step, out of scope and disproportionate).

## Decision: Persistence — a single `localStorage` key, written only on explicit choice

- **Decision**: Use one `localStorage` key, `theme-preference`, holding exactly `"light"` or `"dark"`. The key is absent until the user's first explicit toggle (matching the spec's Key Entity: "not yet chosen" state). `useTheme.ts` is the sole reader/writer.
- **Rationale**: The spec's Assumptions explicitly rule out cross-device sync (no accounts/auth) and require only per-browser/device persistence across reloads/visits — `localStorage` is the simplest built-in web API that satisfies this with no new dependency, consistent with Principle V. A single string key needs no schema/versioning.
- **Alternatives considered**: Cookies (rejected — this app has no backend rendering step or server-side need to read the theme, so a cookie's server-visibility is pure unused overhead versus `localStorage`); `sessionStorage` (rejected — explicitly wrong, since the spec requires persistence *across* visits/reloads, which `sessionStorage` does not provide); IndexedDB (rejected — massive overkill for one string value).

## Decision: State management — a plain custom hook, no React Context

- **Decision**: `src/hooks/useTheme.ts` is a plain hook (`useState` + a couple of effects) that exposes `{ theme: "light" | "dark", toggleTheme: () => void }`. It is called directly by the new `ThemeToggle` component. No `React.Context`/provider is introduced.
- **Rationale**: There is exactly one consumer of theme state in this feature — the toggle button itself, rendered once in `TasksPage`. Theme *application* to the rest of the app happens entirely through the DOM attribute + CSS (no component needs to read the current theme as a prop/value), so there is no prop-drilling problem to solve. Introducing Context now would be exactly the kind of "abstraction introduced ahead of a concrete need" Principle V prohibits; if a second consumer appears later (e.g. a theme-aware chart), Context can be added then.
- **Alternatives considered**: `React.Context` + provider wrapping `App` (rejected per above — YAGNI); a global module-level mutable variable outside React (rejected — `useState` is simpler and gives the toggle button correct re-renders with equivalent code size).

## Decision: Toggle control — icon button reusing `lucide-react`'s `Sun`/`Moon`, placed in the page header

- **Decision**: `ThemeToggle.tsx` renders a single `<button>` in `TasksPage`'s header area (next to the `<h1>`), showing the `Moon` icon (offering to switch to dark) when the current theme is light, and the `Sun` icon (offering to switch to light) when the current theme is dark, with an `aria-label` that states the action ("Switch to dark mode" / "Switch to light mode"), consistent with the icon-per-button convention `002-task-ui-redesign` established (`contracts/design-system.md`).
- **Rationale**: `lucide-react` (already a dependency) ships both `Sun` and `Moon` icons, so no new dependency is needed. A single header-level control satisfies FR-001 (visible, discoverable) and SC-001 (one action from anywhere — the app has only one screen/route, so the header control is reachable from every view) without duplicating the control per-tab/per-screen.
- **Alternatives considered**: A text-only toggle (rejected — inconsistent with `002-task-ui-redesign`'s "icon on every button" convention); a three-way switch (light/dark/system) control (rejected — spec Assumptions explicitly scope this feature to two selectable themes, light and dark, with system preference used only as the first-visit default, not as a persistent third mode).

## Decision: Dark palette values, re-tuned from `002-task-ui-redesign`'s tokens, WCAG AA-verified

- **Decision**: Reuse every token *name* from `contracts/design-system.md` unchanged; override these *values* under `[data-theme="dark"]`:

  | Token | Light (existing) | Dark (new) |
  |-------|-------------------|------------|
  | `--color-primary` | `#E31C5F` | `#E31C5F` (unchanged — already passes AA on white text and reads clearly on dark backgrounds) |
  | `--color-primary-hover` | `#C81552` | `#C81552` (unchanged — reused as-is) |
  | `--color-danger` | `#C13515` | `#F0674C` (brightened so it remains legible as text on the dark background) |
  | `--color-danger-hover` | `#A32C11` (defined but currently unused in any CSS rule) | `#A52B12` (now actively used as the `.btn-danger:hover` background in dark mode — see contract) |
  | `--color-bg` | `#FFFFFF` | `#121212` |
  | `--color-bg-subtle` | `#FFF8F6` | `#1E1E1E` |
  | `--color-text` | `#222222` | `#F2F2F2` |
  | `--color-text-muted` | `#717171` | `#B8B8B8` |
  | `--color-border` | `#EBEBEB` | `#3A3A3A` |
  | `--color-error-bg` | `#FDECEA` | `#3A1712` |
  | `--color-error-text` | `#B3261E` | `#F4877B` |

  All other tokens (`--font-family`, `--radius-md`, `--radius-lg`, `--space-*`, `--input-height`, `--button-height`) are layout/typography, not color, and are left unchanged in both themes (per the spec Assumption that dark mode is a re-tuned counterpart, not a new visual identity — same layout/typography/shapes, only colors change).

- **Rationale — contrast verification** (WCAG AA, ≥4.5:1 for normal text, computed via the standard relative-luminance formula):
  - `#F2F2F2` text on `#121212` bg: 16.73:1; on `#1E1E1E` card bg: 14.89:1
  - `#B8B8B8` muted text on `#121212` bg: 9.44:1; on `#1E1E1E` card bg: 8.40:1
  - White on `--color-primary` (`#E31C5F`): 4.57:1 (same value already verified in `002-task-ui-redesign`'s research)
  - White on `--color-primary-hover` (`#C81552`): 5.70:1
  - `--color-danger` (`#F0674C`) text on `#121212` bg: 6.02:1
  - White on `--color-danger-hover` (`#A52B12`) background (`.btn-danger:hover`): 7.11:1
  - `--color-error-text` (`#F4877B`) on `--color-error-bg` (`#3A1712`): 6.56:1
  - All ≥4.5:1, satisfying FR-006/SC-005. (Non-text decorative contrasts — e.g. `--color-border` against `--color-bg`, `--color-bg-subtle` against `--color-bg` — are not held to the 4.5:1 text threshold; they were chosen to remain visually distinguishable, consistent with WCAG's non-text 3:1 UI-component guidance: border-vs-bg 1.65:1 is intentionally subtle since it's a hairline divider, not a required-to-perceive boundary, matching the equally subtle light-mode `#EBEBEB` on `#FFFFFF` divider.)
  - A single hex value cannot simultaneously (a) read clearly as *text* directly on the dark page background and (b) provide ≥4.5:1 contrast for *white text placed on top of it* as a hover background — these are opposing lightness requirements. This is why `--color-danger` (text role) and `--color-danger-hover` (hover-background role) are distinct values in dark mode, whereas in light mode `.btn-danger:hover` happened to reuse `--color-danger` directly as the hover background. `--color-danger-hover` was already declared as an unused token in `002-task-ui-redesign`'s `global.css`; this feature is the first to give it an actual CSS rule (`.btn-danger:hover` background, dark theme only).
- **Alternatives considered**: A single shared danger color reused for both text and hover-background roles in dark mode, as light mode currently does (rejected — verified computationally that no red hue/lightness in the appropriate family clears 4.5:1 in both roles simultaneously against a `#121212` background); a pure grayscale/desaturated dark palette instead of a warm near-black (rejected — `#121212`-family "true dark" is the widely-adopted baseline (e.g. Material Design's dark theme guidance) that keeps the warm coral accent from `002-task-ui-redesign` reading clearly, versus a colder dark gray that would clash with the warm palette).

## Decision: Semantic color-coded elements preserved (FR-007)

- **Decision**: The only color-coded-for-meaning elements that currently exist in the codebase are: the active tab indicator (filled with `--color-primary`), destructive actions (`.btn-danger`, using `--color-danger`/`--color-danger-hover`), and error/validation alerts (`[role="alert"]`, using `--color-error-bg`/`--color-error-text`). Each keeps its role (brand/selected = primary hue family, destructive = red/orange hue family, error = red hue family) in dark mode; only the exact hex values change per the table above.
- **Rationale**: Satisfies FR-007 directly — "preserve the visual meaning... even where the specific color values differ." No status/priority-labeled task fields exist in the current `Task` data model (`specs/001-task-management/data-model.md`) or UI, so there is no additional semantic color mapping to re-tune beyond these three.
- **Alternatives considered**: None needed — this is a direct inventory of the existing codebase's color-coded elements, not a design choice with alternatives.

## Open Questions

None — no `NEEDS CLARIFICATION` markers remain from the Technical Context. The one judgment call the spec flagged (first-visit default theme source) was already resolved by the human before this plan was authored (spec Edge Cases / FR-002).
