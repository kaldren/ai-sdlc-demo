# Quickstart: Task Tracker Visual Redesign

## Verify locally

```bash
cd src/frontend
npm install       # picks up the new lucide-react dependency
npm run dev       # starts Vite dev server (http://localhost:5173)
```

## What to check

1. **Visual identity (US1)**: Page background, buttons, tabs, and input borders use the warm coral/neutral palette from `contracts/design-system.md`; all text renders in Inter (check DevTools → Computed → font-family falls back correctly if the Google Fonts request is blocked).
2. **Larger, rounder controls (US2)**: Title/description inputs and every button are visibly taller and more rounded than plain browser defaults; buttons/inputs remain fully usable (typing, focus, submit) with mouse and keyboard.
3. **Icons on every button (US3)**: Add Task, Active/Archived tabs, Edit, Save, Cancel, Archive/Unarchive, Delete, and the delete-confirm Confirm/Cancel buttons each show the icon from the mapping table alongside their label.
4. **No behavior change**: Create, edit, archive/unarchive, and delete a task — all flows work exactly as before (same number of clicks/steps, same API calls in the Network tab).
5. **Responsiveness**: Resize the browser from ~375px to full desktop width — no overlapping or clipped controls.
6. **Accessibility**: Tab through the page with the keyboard; every button has a visible focus state and an accessible name (inspect via browser accessibility tree or screen reader).
