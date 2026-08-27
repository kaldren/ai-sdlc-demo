# Quickstart: Dark Mode Toggle

## Verify locally

```bash
cd src/frontend
npm install       # no new dependency to fetch (reuses existing lucide-react)
npm run dev        # starts Vite dev server (http://localhost:5173)
```

## What to check

1. **Manual switch (US1)**: Click the theme toggle button in the header. Confirm the task list, task form, task items, tabs, and nav all immediately switch between light and dark — no page reload (watch the Network tab: no new document request), and no in-progress typed text in the task form or an item being edited is lost.
2. **Full-app coverage (FR-003)**: With dark mode active, visit both the Active and Archived tabs, open a task for editing, and trigger the delete-confirmation state. Confirm every screen/state uses dark colors with none of it still showing white/light backgrounds or unstyled elements.
3. **First-visit auto-detection (FR-002)**: Clear `localStorage` for the site (DevTools → Application → Local Storage → remove `theme-preference`) and use DevTools' "Emulate CSS media feature `prefers-color-scheme`" (Rendering tab) set to `dark`, then reload — the app should load directly in dark mode with no toggle click needed. Repeat with `prefers-color-scheme: light` (or "no preference") to confirm it loads light.
4. **No flash of wrong theme**: With `theme-preference` set to `"dark"` in `localStorage`, hard-reload the page repeatedly and watch closely (or use a screen recording) — the page should never visibly flash light before showing dark.
5. **Persistence (US2)**: Toggle to dark mode, reload the page — it should load directly in dark mode. Toggle back to light, close and reopen the tab (or restart the dev server tab) — it should load in light mode. Confirm the explicit choice persists across a real reload (not just client-side state).
6. **Explicit choice overrides auto-detection (FR-005)**: With the OS/browser emulated preference set to `dark` but an explicit `theme-preference: "light"` stored, reload — the app must load light (the explicit choice wins), not dark.
7. **Accessible contrast (FR-006, SC-005)**: In both themes, use a contrast checker (e.g. browser DevTools' contrast ratio readout when inspecting text) to spot-check the task title text, muted description text, button labels, and the error alert — all should read at or above the WCAG AA thresholds documented in `research.md`/`contracts/theming-contract.md`.
8. **Semantic color meaning preserved (FR-007)**: In dark mode, confirm the active tab is still visually distinguished the same way as light mode (filled/highlighted vs. outlined), the Delete button still reads as a destructive/red action, and a validation error (e.g. submitting an empty title) still renders as a red alert — just with dark-tuned hex values per `contracts/theming-contract.md`.
9. **Toggle discoverability & accessibility (FR-001)**: Tab to the toggle button with the keyboard and confirm it has a visible focus state and an accessible name that changes appropriately ("Switch to dark mode" / "Switch to light mode") as reported by the browser's accessibility tree.
10. **No behavior change to task CRUD**: Create, edit, archive/unarchive, and delete a task in both themes — all flows work exactly as before (same API calls in the Network tab), confirming this is purely a presentation-layer change.
