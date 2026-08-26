# AI SDLC Demo

A demo of an AI-driven software development lifecycle: this repo uses [Spec Kit](https://github.com/github/spec-kit)
and Claude Code skills/agents to spec, plan, task-break, and implement features with an AI
assistant end-to-end. The sample application built through that process is **Task Tracker**, a
web app for tracking tasks.

## Structure

- `docs/` — supporting documentation.
- `src/` — source code.
- `specs/` — Spec Kit feature specs, plans, and tasks.
- `.claude/` — Claude Code skills (`skills/speckit-*`) and agents (`agents/`) that drive the Spec Kit workflow.

This project is being built from scratch — expect its structure and contents to evolve as work begins.

## Spec Kit workflow

Feature work follows Spec Kit's spec → plan → tasks → implement flow, implemented as the
`speckit-*` skills under `.claude/skills/`. Rather than invoking each skill by hand,
`.claude/agents/` provides one subagent per stage:

| Agent | Wraps | Role |
|---|---|---|
| `spec-author` | speckit-specify, speckit-clarify | Draft or refine a feature's `spec.md` |
| `planner` | speckit-plan | Turn an approved spec into `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` |
| `task-breaker` | speckit-tasks | Break an approved plan into `tasks.md` |
| `qa-reviewer` | speckit-analyze, speckit-checklist | Read-only cross-artifact consistency check, plus optional acceptance checklists |
| `implementer` | speckit-implement | Execute `tasks.md` and write the code |
| `spec-flow` | — (orchestrator) | Runs the stages above end-to-end, pausing for human approval after spec and after plan, and confirming before implementation starts |

Ask for `spec-flow` to drive a whole feature through the flow, or invoke a stage agent by name
for a single step. `speckit-constitution` and `speckit-taskstoissues` remain manually-invoked
skills rather than agents — constitution changes need explicit project-owner sign-off, and
taskstoissues creates real GitHub issues.
