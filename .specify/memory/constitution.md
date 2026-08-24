<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.0.1
Modified principles: Reformatted all principles from prose+Rationale into
  intro sentence + MUST/MUST NOT bullet lists (no principle added, removed,
  or redefined)
Added sections: None (Technology Stack and Development Workflow replace the
  prior Additional Constraints / Development Workflow & Quality Gates
  sections with equivalent content, restructured as a table and subsections)
Removed sections: "Additional Constraints" and "Development Workflow &
  Quality Gates" headings (content preserved, moved into "Technology Stack"
  and "Development Workflow")
Templates requiring updates: ✅ No updates required (structure-only change;
  plan/spec/tasks templates read this file dynamically)
Follow-up TODOs: None
-->

# Task Tracker Constitution

## Core Principles

### I. Fixed Technology Stack

The application MUST be built on the stack defined in the Technology Stack
table below.

- No additional frontend framework, backend framework, or primary datastore
  MAY be introduced without a constitution amendment
- Supporting libraries (state management, ORM, test runners, etc.) are
  permitted as long as they serve this stack rather than replace a piece
  of it
- A single, fixed stack keeps onboarding, tooling, and operational
  knowledge concentrated instead of fragmented across competing
  technologies chosen ad hoc per feature

### II. REST API Contract

All APIs exposed by the backend MUST follow REST conventions and exchange
data as JSON.

- Endpoints MUST be resource-oriented and use standard HTTP methods and
  status codes
- All request/response bodies MUST be JSON
- Non-RESTful protocols (GraphQL, gRPC, ad hoc RPC-style endpoints) and
  non-JSON payloads (XML, form-encoded API responses, etc.) MUST NOT be
  used for application APIs
- A single, predictable API style keeps client integration, documentation,
  and tooling (OpenAPI/FastAPI auto-docs) simple and consistent

### III. Backend Test Coverage (NON-NEGOTIABLE)

Every backend feature, endpoint, and non-trivial function MUST be
accompanied by unit tests.

- A pull request that adds or changes backend behavior without
  corresponding unit tests MUST NOT be merged
- Tests MUST exercise business logic directly (not only through
  end-to-end flows) so failures are localized and fast to diagnose
- Unit tests are the cheapest, fastest way to keep FastAPI business logic
  correct as the codebase evolves

### IV. Frontend/Backend Separation

The React frontend MUST NOT access PostgreSQL, or any other datastore,
directly.

- All data reads and writes from the frontend MUST go through the FastAPI
  backend's REST API
- The frontend MUST NOT embed database credentials, connection strings, or
  database client libraries
- Routing all data access through the backend preserves a single point of
  validation, authorization, and business-rule enforcement, and keeps the
  database topology and credentials out of client-delivered code

### V. Simplicity First (YAGNI)

Implementations MUST start with the simplest design that satisfies the
current requirement.

- Abstractions (interfaces, plugin systems, generic frameworks, extra
  service layers, design patterns applied preemptively) MUST NOT be
  introduced unless a concrete, current need justifies them
- Speculative flexibility for hypothetical future requirements is NOT a
  valid justification
- Simplicity can always be relaxed later when a real need appears; the
  reverse (removing entrenched complexity) is far more expensive

## Technology Stack

The following technology decisions are binding for this project:

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend | React | Consumes the backend REST API only; no direct data access (Principle IV) |
| Backend / API | FastAPI | Async support, auto-generated OpenAPI docs, native REST/JSON fit (Principle II) |
| Database | PostgreSQL | Sole system of record; only the backend holds credentials or a database client |
| Backend Testing | Unit test framework appropriate to the backend language | Enforces Principle III on every backend change |

Any deviation from this table, or from the boundaries in Principle IV,
requires an explicit, documented constitution amendment before
implementation begins.

## Development Workflow

### Code Review Requirements

- All changes MUST be submitted via Pull Request
- Reviewers MUST verify compliance with Principles I, II, and IV (correct
  stack usage, REST/JSON APIs, no direct frontend database access)
- Any added abstraction or new dependency MUST be justified in the PR
  description against Principle V (Simplicity First); reviewers MAY
  request simplification before merge

### Testing Requirements

- Pull requests changing backend code MUST include unit tests covering the
  new or changed behavior (Principle III)
- A PR MUST NOT be merged if backend behavior changed without
  corresponding unit tests

### Quality Gates

1. **API contract check**: New or changed endpoints MUST be reflected in
   FastAPI's request/response models so the generated OpenAPI schema stays
   accurate and REST/JSON conventions are honored
2. **Test gate**: Backend unit tests MUST pass before merge
3. **Boundary check**: No frontend code may reference a database
   connection string, ORM, or DB client library

## Governance

This constitution supersedes any conflicting team practice, template
default, or prior informal convention.

- **Authority**: Amendments to this constitution require explicit
  agreement from the project owner before merge
- **Amendment Process**: Proposed changes MUST be documented in a PR that
  edits this file, state the version bump and rationale, and be approved
  before merge; merging ratifies the amendment and updates `Last Amended`
  to the merge date
- **Compliance**: All plans, specs, and PR reviews MUST verify adherence
  to these principles; every `/speckit-plan` run MUST re-check the
  Constitution Check gate against this file after Phase 1 design
- **Exceptions**: Any deviation from these principles MUST be documented
  with justification in the relevant plan's Complexity Tracking section or
  the PR description

**Versioning policy**: This constitution follows semantic versioning:
- MAJOR: Backward-incompatible governance changes, or removal/redefinition
  of an existing principle
- MINOR: A new principle or section is added, or guidance is materially
  expanded
- PATCH: Wording, formatting, clarification, or typo fixes with no
  semantic change

**Version**: 1.0.1 | **Ratified**: 2026-08-24 | **Last Amended**: 2026-08-24
