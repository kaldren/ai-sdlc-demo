<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles: trimmed all five to short, gate-checkable statements;
  dropped standalone rationale paragraphs (rationale now lives in AGENTS.md,
  linked below) and the Technology/Workflow prose sections
- Added sections: none
- Removed sections: Technology & Tooling Constraints, Development Workflow &
  Quality Gates (folded into a short Toolchain line + Governance)
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — generic Constitution Check gate,
    still reads fine against the shortened principles
  - ✅ .specify/templates/spec-template.md — no changes needed
  - ✅ .specify/templates/tasks-template.md — no changes needed
- Follow-up TODOs: none
-->

# AI-Led SDLC Demo Constitution

Short by design — this is a demo repo. Full context and rationale for these
principles live in **AGENTS.md**; if the two ever disagree, this file wins.

## Core Principles

### I. Spec-First (NON-NEGOTIABLE)

Every feature goes through Spec Kit (`specify` → `plan` → `tasks` →
`implement`) before code is written. `spec.md`/`plan.md`/`tasks.md` stay in
sync with what's actually built.

### II. Test-First

Tests are written before the implementation they cover and must fail first.
Task breakdowns include test tasks ahead of implementation tasks.

### III. Deterministic Build & Deploy

CI/CD, environment promotion, and infra deployment stay deterministic
(GitHub Actions) even when an agent could do them. Agent-produced code runs
sandboxed before a human trusts it with production traffic.

### IV. Humans Own the Checkpoints

Agents stop for human approval at PR review, deploy approval, and privileged
incident remediation. Read-only "propose" mode doesn't need a human in the
loop; anything irreversible or externally visible does.

### V. Scoped Work for Background Agents

Work handed to an autonomous coding agent arrives as a scoped issue from a
Spec Kit task breakdown, not a single free-form prompt.

## Toolchain

Azure + GitHub native (Spec Kit, GitHub Copilot coding agent, GitHub Code
Quality, GitHub Actions, Azure Container Apps, Azure SRE Agent) — see
AGENTS.md. Substitute only if the user asks.

## Governance

This constitution supersedes ad hoc practice. Amendments: edit this file,
bump the version below, note the change in the Sync Impact Report. Semver:
MAJOR = principle removed/redefined, MINOR = principle added, PATCH =
wording only.

**Version**: 1.1.0 | **Ratified**: 2026-08-24 | **Last Amended**: 2026-08-24
