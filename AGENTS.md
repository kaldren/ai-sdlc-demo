# ai-sdlc-demo — reference framework

This repo demonstrates an **AI-led SDLC**: AI agents drive most of the lifecycle
(spec → plan → implement → review → deploy → operate), humans set direction and
approve at checkpoints. For all work in this workspace, use the following article
as the reference architecture and vocabulary unless the user says otherwise:

> Microsoft Tech Community — "An AI led SDLC: Building an End-to-End Agentic
> Software Development Lifecycle with Azure and GitHub"
> https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896

## The 5-step flow described in the article

1. **Spec-driven development (Spec Kit)** — "spec first, code second." A plain
   English problem statement (e.g. "As a user I want to view real time weather
   data for my city so that I can plan my day.") is fed to GitHub's open-source
   **Spec Kit** (`/speckit.specify ...`), which produces requirements, a plan,
   and a task breakdown. A **"constitution"** file encodes org/tech-stack
   standards (e.g. TDD required, coverage thresholds, "Azure-native only") so
   every generated plan respects them. The article's author bridges Spec Kit's
   output into GitHub Issues with a custom **"spec-to-issue"** tool, auto-
   assigning the coding agent — because Spec Kit's own `implement` step
   otherwise expects to run inside an IDE/local agent.

2. **GitHub Coding Agent** — an autonomous agent that takes a scoped issue,
   works in the background on its own branch, opens a PR, runs tests, and (for
   UI changes) drives Playwright MCP to screenshot the result into the PR.
   Reasoning/steps are visible in the Agents tab; the underlying run is visible
   in Actions. Feeding it a Spec Kit task breakdown (rather than one big
   prompt) markedly improves its output quality, since GitHub.com's coding
   agent — unlike an IDE agent — gets no mid-run human steering, only a
   PR-review checkpoint.

3. **GitHub Code Quality review (human-in-the-loop + AI assist)** — Copilot
   layers on top of CodeQL/PMD/ESLint with in-context quality findings,
   autofixes, and change summaries, at PR level and repo-wide scoreboards.
   Cited stats: Qodo 2025 report — AI code review lifted quality-improvement
   rate from 55%→81%; Atlassian RovoDev 2026 — 38.7% of AI review comments led
   to further fixes. Framed as raising review coverage/confidence, not
   replacing human review — and as a plausible place for a future
   supply-chain-focused sub-agent (e.g. catching XZ-Utils-style hidden
   malicious commits).

4. **GitHub Actions for build & deploy — deliberately non-agentic.** CI/CD,
   promotion through dev→prod, and infra deployment stay **deterministic**.
   The article's stated principle: some processes are deterministic just
   because that's all that was available (candidates for going agentic — IVR
   trees, scripted retention flows); others (financial transactions, policy
   engines, document ingestion, and — per the author — CI/CD/infra deploy)
   should *stay* deterministic even though an agent *could* do them, because
   the risk/benefit doesn't favor non-determinism there. Untrusted agent-
   produced code is run in an isolated sandbox (Azure Container Apps "Dynamic
   Sessions") before a human evaluates it via a surfaced revision URL.

5. **SRE Agent — proactive day-2 operations.** Watches logs/metrics/traces on
   the running service, correlates incidents, and proposes/takes remediation
   (restart pods, shift traffic, alert on secret expiry), in either a
   read-only "propose" mode or a privileged "act autonomously within scope"
   mode. Supports **sub-agents** for narrow tasks — e.g. a GitHub sub-agent
   invoked after incident resolution to file a summarizing issue — which
   closes the loop back to step 2 (coding agent picks up the fix).

## Cross-cutting principles worth carrying into this repo's work

- **Spec is the versioned source of truth** ("version control for your
  thinking"), not a stale doc — treat specs/plans as living, executable
  artifacts alongside code.
- **Deterministic vs. agentic is a deliberate choice per process**, not a
  default-to-agentic stance. Prefer deterministic CI/CD and infra even when an
  agent could technically do it.
- **Humans stay at the checkpoints**: PR review, deploy approval, incident
  remediation approval (per the SRE agent's permission model) — agents do the
  legwork in between.
- **Tight, structured task breakdowns beat single large prompts** for
  autonomous/background agents specifically because they get no mid-run
  steering.
- The article is explicit that this is Azure + GitHub flavored (Spec Kit,
  GitHub Copilot coding agent, GitHub Code Quality, Azure Container Apps,
  Azure SRE Agent) — treat those as the reference toolchain for this demo
  unless told to substitute alternatives.
