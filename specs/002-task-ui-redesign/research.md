# Phase 0 Research: Task Tracker Visual Redesign

## Decision: Typography — Inter via Google Fonts

- **Decision**: Use "Inter" as the single application-wide typeface, loaded via a Google Fonts `<link>` in `index.html`, with a system-font fallback stack (`Inter, "Helvetica Neue", Arial, sans-serif`).
- **Rationale**: Inter is free (SIL Open Font License), extremely widely used in modern product UI, and is explicitly minimalist/geometric — matching the spec's "well-known and used, minimalistic" requirement and the user's own example. A `<link>` tag avoids adding a font-loading npm package.
- **Alternatives considered**: Self-hosting font files (rejected — adds build complexity for no benefit at this scale, violates Simplicity First); system font stack only (rejected — doesn't satisfy "well-known... font" intent as clearly as a deliberately chosen typeface); "Circular" (rejected — Airbnb's actual proprietary typeface, not freely licensed, and spec Assumptions explicitly rule out reusing Airbnb's proprietary assets).

## Decision: Icons — `lucide-react`

- **Decision**: Add `lucide-react` (npm-confirmed available) as the icon library for every button (Add Task, Active/Archived tabs, Edit, Save, Cancel, Archive/Unarchive, Delete, Confirm).
- **Rationale**: MIT-licensed, tree-shakable (only imported icons ship), actively maintained, consistent stroke-based icon style that reads as clean/minimal — fits the Airbnb-inspired aesthetic. It is a small, focused "supporting library" under constitution Principle I, not a competing frontend framework.
- **Alternatives considered**: Hand-rolled inline SVGs (rejected — more code to maintain for the same result, no meaningful simplicity gain since a small icon library is a normal, low-risk dependency); `react-icons` (rejected — bundles multiple icon families and is heavier than needed for a single consistent style); Font Awesome (rejected — icon-font approach is heavier and less accessible than inline SVG components).

## Decision: Styling approach — plain CSS + design tokens

- **Decision**: One global stylesheet (`src/styles/global.css`) defining CSS custom properties (color, radius, spacing, font tokens) plus base/reset rules, imported once in `main.tsx`. Components keep their existing `className` hooks (`task-form`, `task-item`, etc.) and get corresponding rules in the same stylesheet; no CSS Modules, CSS-in-JS, or utility-CSS framework is introduced.
- **Rationale**: The app currently ships with zero CSS. Plain CSS with custom-property tokens is the simplest option that satisfies "consistent palette/typeface/rounding everywhere" (FR-001–004) without adding a build-time dependency or a new styling paradigm — directly aligned with constitution Principle V (Simplicity First / YAGNI).
- **Alternatives considered**: Tailwind CSS (rejected — adds a build-tool dependency and a new authoring convention for a 4-component app; disproportionate to scope); styled-components/Emotion (rejected — CSS-in-JS runtime cost and new dependency not justified for a static visual redesign); CSS Modules per component (rejected — unnecessary indirection when there is one small, shared design system to apply consistently across just four files).

## Decision: Color palette (Airbnb-inspired, not Airbnb's trademarked assets)

- **Decision**: Primary accent `#E31C5F` (a coral/pink in the same family as Airbnb's brand color) on a warm neutral background (`#FFFFFF` / `#FFF8F6`), warm gray text (`#222222` / `#717171`), and a soft warm border/divider gray (`#EBEBEB`).
- **Rationale**: Satisfies "colors like Airbnb" (warm coral primary + neutral supporting palette) while remaining a generic, freely-usable color value — not a reused logo, wordmark, or other trademarked brand asset, consistent with the spec's Assumptions section.
- **Alternatives considered**: Exact legacy Airbnb "Rausch" `#FF5A5F` (rejected — more directly identified with Airbnb's specific historical branding than needed to satisfy "inspired by"); a non-coral warm palette, e.g. amber/orange (rejected — less clearly reads as "Airbnb-like" per the explicit user request); the brighter `#FF385C` (rejected during Polish/SC-004 verification — white button text on `#FF385C` only reaches 3.52:1 contrast, below WCAG AA's 4.5:1 for normal-size text; `#E31C5F` keeps the same coral family and reaches 4.57:1).

## Open Questions

None — no `NEEDS CLARIFICATION` markers remain from the Technical Context.
