# ai-sdlc-demo — reference framework

This repo demonstrates an **AI-led SDLC**: AI agents drive most of the lifecycle
(spec → plan → implement → review → deploy → operate), humans set direction and
approve at checkpoints. Reference architecture:

> Microsoft Tech Community — "An AI led SDLC: Building an End-to-End Agentic
> Software Development Lifecycle with Azure and GitHub"
> https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896

## The 5-step flow

1. **Spec-driven development (Spec Kit)** — plain-English request →
   `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` →
   `/speckit.implement`, gated by the project constitution.
2. **GitHub Coding Agent** — takes a scoped issue, works on its own branch,
   opens a PR. No mid-run steering, so it needs a tight task breakdown, not
   one big prompt.
3. **GitHub Code Quality review** — CodeQL/PMD/ESLint + AI-assisted review;
   augments human PR review, doesn't replace it.
4. **GitHub Actions for build & deploy** — deliberately non-agentic. CI/CD
   and infra deployment stay deterministic even though an agent could do
   them; agent-produced code runs sandboxed before a human trusts it.
5. **SRE Agent** — proactive day-2 ops: watches logs/metrics/traces,
   proposes or (within an explicit scope) takes remediation.

## Toolchain

Azure + GitHub native by default: Spec Kit, GitHub Copilot coding agent,
GitHub Code Quality, GitHub Actions, Azure Container Apps (sandboxed
execution), Azure SRE Agent. Substitute only if the user says otherwise.

## Governing principles

The rules for how work actually happens in this repo (spec-first, test-first,
deterministic build/deploy, human checkpoints, scoped task breakdowns) live in
the project constitution — **`.specify/memory/constitution.md`**. Read it
before planning or implementing a feature; if it and this file ever disagree,
the constitution wins.

# Skills
You will find required skills inside `.claude/skills` folder. Use them when needed.
