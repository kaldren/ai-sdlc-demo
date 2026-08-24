# Feature Specification: Task Management

**Feature Branch**: `001-task-management`

**Created**: 2026-08-24

**Status**: Draft

**Input**: User description: "Task management: users can create a task with a title and description, edit a task's title/description, archive a task (soft-hide it from the default/active task list without deleting it, with the ability to view archived tasks and unarchive them), and permanently delete a task (irreversible removal, allowed on both active and archived tasks). There is no user authentication — this is a single shared task list visible to everyone. Each task should track its creation and last-updated timestamps in addition to title, description, and archived status."

## Clarifications

### Session 2026-08-24

- Q: Should task changes propagate to other users in real time (e.g., within 1 second, via push/polling), or is it sufficient for changes to appear the next time a user loads/refreshes the list? → A: Refresh-based is sufficient; no real-time push/polling infrastructure is required for v1.
- Q: Should the task list API support pagination in this first version? → A: No; return the full active (or archived) list unpaginated for v1. Pagination can be added later if the list grows large.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Task (Priority: P1)

A user adds a new task to the shared list by providing a title and, optionally, a description, so the task is tracked and visible to everyone using the list.

**Why this priority**: Without the ability to create a task, there is nothing to edit, archive, or delete — this is the foundational capability and the smallest possible MVP.

**Independent Test**: Can be fully tested by submitting a title (with or without a description) and verifying the task appears in the active task list with the correct title, description, and a creation timestamp.

**Acceptance Scenarios**:

1. **Given** the active task list, **When** a user submits a new task with a title and a description, **Then** the task appears in the active list with that title, description, and a creation/last-updated timestamp set to the current time.
2. **Given** the active task list, **When** a user submits a new task with a title only, **Then** the task is created successfully with an empty description.
3. **Given** the active task list, **When** a user attempts to submit a task with an empty or blank title, **Then** the system rejects the submission and no task is created.

---

### User Story 2 - Edit a Task (Priority: P2)

A user updates an existing task's title and/or description to correct or refine its details.

**Why this priority**: Tasks change after creation; editing is the next most common action after creating one, and depends on a task already existing.

**Independent Test**: Can be fully tested by creating a task, changing its title and/or description, and verifying the stored values and last-updated timestamp reflect the change while the creation timestamp stays the same.

**Acceptance Scenarios**:

1. **Given** an existing task, **When** a user changes its title, description, or both, **Then** the task reflects the new values and its last-updated timestamp advances, while its creation timestamp remains unchanged.
2. **Given** an existing task, **When** a user attempts to clear the title entirely, **Then** the system rejects the edit and the task's title remains unchanged.
3. **Given** an archived task, **When** a user edits its title or description, **Then** the edit succeeds and the task remains archived.

---

### User Story 3 - Archive and Unarchive a Task (Priority: P3)

A user archives a task to hide it from the default/active task list without losing it, and can later view archived tasks or restore (unarchive) one back to the active list.

**Why this priority**: Archiving lets users declutter the active list without the permanence of deletion; it's valuable but secondary to basic create/edit.

**Independent Test**: Can be fully tested by creating a task, archiving it, verifying it disappears from the active list but appears in an archived-tasks view, then unarchiving it and verifying it reappears in the active list.

**Acceptance Scenarios**:

1. **Given** an active task, **When** a user archives it, **Then** the task no longer appears in the default/active task list, its archived status is set, and its last-updated timestamp advances.
2. **Given** an archived task, **When** a user views archived tasks, **Then** the task is visible there with its title, description, and timestamps.
3. **Given** an archived task, **When** a user unarchives it, **Then** the task reappears in the default/active task list and its last-updated timestamp advances.

---

### User Story 4 - Delete a Task (Priority: P4)

A user permanently removes a task — active or archived — from the system when it is no longer needed at all.

**Why this priority**: Permanent deletion is destructive and irreversible, so it is the least frequently needed and highest-risk action; it depends on a task already existing.

**Independent Test**: Can be fully tested by creating a task (active or archived), deleting it, and verifying it no longer appears in either the active or archived views and cannot be retrieved.

**Acceptance Scenarios**:

1. **Given** an active task, **When** a user deletes it, **Then** the task is permanently removed and no longer appears in the active list.
2. **Given** an archived task, **When** a user deletes it, **Then** the task is permanently removed and no longer appears in the archived list.
3. **Given** a task has been deleted, **When** any user attempts to retrieve it, **Then** the system reports it as not found; the task cannot be recovered.

---

### Edge Cases

- What happens when a user tries to edit, archive, or delete a task that has already been deleted (e.g., by another user moments earlier)? System MUST report it as not found rather than silently succeeding.
- What happens when a user tries to archive a task that is already archived, or unarchive a task that is already active? System MUST treat this as a no-op success rather than an error, leaving the task in its current state (last-updated timestamp does not advance for a no-op).
- What happens when a title consists only of whitespace? Treated the same as an empty title and rejected.
- What happens when two users edit or archive the same task at nearly the same time? The last write wins; no conflict-resolution UI is required for this feature.
- What happens when a user submits an unreasonably long title or description? System MUST enforce a reasonable maximum length and reject submissions that exceed it, rather than truncating silently.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow any user to create a task by providing a title and an optional description.
- **FR-002**: System MUST require a non-empty (non-whitespace-only) title to create or update a task, and MUST reject the operation otherwise.
- **FR-003**: System MUST allow any user to view the list of active (non-archived) tasks.
- **FR-004**: System MUST allow any user to edit an existing task's title and/or description, regardless of whether the task is active or archived.
- **FR-005**: System MUST allow any user to archive an active task, which removes it from the default/active task list without deleting its data.
- **FR-006**: System MUST allow any user to view the list of archived tasks, separately from the active task list.
- **FR-007**: System MUST allow any user to unarchive an archived task, restoring it to the active task list.
- **FR-008**: System MUST allow any user to permanently delete a task, whether it is currently active or archived.
- **FR-009**: System MUST make deletion irreversible — once deleted, a task's data MUST NOT be retrievable or recoverable through the system.
- **FR-010**: System MUST record a creation timestamp for each task at the time it is created, and MUST NOT change it afterward.
- **FR-011**: System MUST record a last-updated timestamp for each task and MUST advance it whenever the task's title, description, or archived status changes.
- **FR-012**: System MUST make all tasks visible to and editable by anyone using the application, since no user authentication or per-user ownership exists in this feature.
- **FR-013**: System MUST treat archiving an already-archived task, or unarchiving an already-active task, as a no-op that does not error and does not advance the last-updated timestamp.
- **FR-014**: System MUST reject attempts to edit, archive, unarchive, or delete a task that does not exist (e.g., already deleted), reporting it as not found.

### Key Entities *(include if feature involves data)*

- **Task**: A single to-do item on the shared list. Attributes: title (required, non-empty text), description (optional text), archived status (boolean, defaults to not archived), creation timestamp (set once, at creation), last-updated timestamp (advances on any create/edit/archive/unarchive change). Tasks have no owner and are not related to any other entity in this feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can create a new task in under 10 seconds from the moment they start entering a title.
- **SC-002**: 100% of archived tasks are excluded from the default/active task list until explicitly unarchived.
- **SC-003**: 100% of deleted tasks are permanently unrecoverable and absent from both active and archived views immediately after deletion.
- **SC-004**: A new user, with no prior instruction, can successfully create, edit, archive, and delete a task on their first attempt at least 95% of the time.
- **SC-005**: Task edits (title, description, archive/unarchive) are reflected the next time any user loads or refreshes the task list — no real-time push is required for this feature.

## Assumptions

- Title is required and must be non-blank; description is optional free-form text.
- No user authentication or per-user task ownership exists for this feature; the task list is shared and globally visible/editable, consistent with the project constitution's current scope (auth may be introduced later as a separate feature).
- No additional task attributes (due date, priority, tags, completion/done status) are in scope for this feature — only title, description, archived status, and timestamps, per explicit user direction.
- Maximum length is enforced for title (200 characters) and description (2000 characters), pinned during planning (see `data-model.md`); these are implementation-level limits, not a user-facing product decision.
- "Last write wins" is an acceptable conflict resolution strategy for concurrent edits to the same task; no locking or merge UI is required.
- The active and archived task lists are returned unpaginated (full list) in this version; pagination is out of scope until the list is shown to grow large enough to need it.
