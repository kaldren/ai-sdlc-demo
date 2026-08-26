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

## GitHub integration

Feature work can start from a GitHub issue instead of free text, and the pipeline reports
status back to that issue as it runs — mirroring how an enterprise team tracks feature work on
a board:

- **Setup (one-time per environment)**: this repo registers the official
  [`github/github-mcp-server`](https://github.com/github/github-mcp-server) as a project-scoped
  MCP server in `.mcp.json` (committed, no secret inside it). Each environment must export its
  own `GITHUB_PERSONAL_ACCESS_TOKEN` before starting Claude Code — the simplest way, if you
  already use `gh`, is `setx GITHUB_PERSONAL_ACCESS_TOKEN (gh auth token)` (PowerShell) or
  `export GITHUB_PERSONAL_ACCESS_TOKEN=$(gh auth token)` (bash), reusing your existing `repo`-
  scoped token. Restart Claude Code afterward and approve the `github` server when prompted
  (project-scoped MCP servers require explicit trust approval on first use). Board-status moves
  (below) additionally need `gh` itself authenticated with the `project` scope — run
  `gh auth refresh -s project,read:project` once per environment and re-export the token as
  above afterward.
- **Intake**: give `spec-flow` (or `spec-author` directly) a GitHub issue reference — `#123`, a
  bare number, or a full issue URL — instead of a feature description. `spec-author` fetches the
  issue's title/body from the same repo as the git remote and uses it as the feature description.
- **Progress comments**: as each spec-flow gate is approved (spec, then plan), it posts a short
  status comment back on the source issue.
- **Closing the loop**: once `implementer` finishes, it posts a completion summary comment and
  closes the issue if every task succeeded, or leaves it open (comment only) if something failed.
- **Task issues**: `speckit-taskstoissues` (still manually invoked) links any task issues it
  creates back to the source issue (`Part of #N`) when one is known.
- **Board status**: if the source issue is also tracked on a GitHub Projects (v2) board,
  `spec-flow` and `implementer` move its card across the `Status` field as the pipeline
  progresses — `Ready` on spec approval, `In progress` through planning/tasks/implementation,
  `In review` while `qa-reviewer` runs, `Done` when `implementer` closes the issue (or left at
  `In progress` if a task failed). This uses `scripts/move-board-status.sh <issue-number>
  "<status-name>"`, a thin wrapper over `gh project item-edit` — the GitHub MCP server has no
  Projects-v2 tools, so this goes through the `gh` CLI directly. The script defaults to the
  `kaldren` / project `3` board (`ai-sdlc-demo-v1`); override with the `PROJECT_OWNER` /
  `PROJECT_NUMBER` env vars if you're pointing at a different board.

All GitHub writes are guarded the same way: they only ever target the repository resolved from
`git config --get remote.origin.url`, never a different one.
