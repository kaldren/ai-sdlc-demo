import { useState } from "react";
import {
  Archive,
  ArchiveRestore,
  Check,
  Pencil,
  Trash2,
  X,
} from "lucide-react";
import type { Task } from "../services/taskApi";

interface TaskItemProps {
  task: Task;
  onEdit: (id: number, title: string, description: string) => Promise<void>;
  onToggleArchived: (id: number, archived: boolean) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

export default function TaskItem({
  task,
  onEdit,
  onToggleArchived,
  onDelete,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description);
  const [error, setError] = useState<string | null>(null);
  const [confirmingDelete, setConfirmingDelete] = useState(false);

  async function handleSave() {
    if (!title.trim()) {
      setError("Title is required.");
      return;
    }
    setError(null);
    try {
      await onEdit(task.id, title.trim(), description.trim());
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save.");
    }
  }

  function handleCancel() {
    setTitle(task.title);
    setDescription(task.description);
    setError(null);
    setIsEditing(false);
  }

  if (isEditing) {
    return (
      <li className="task-item task-item--editing">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          aria-label="Edit task title"
        />
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          aria-label="Edit task description"
        />
        <button className="btn-primary" onClick={handleSave}>
          <Check aria-hidden="true" />
          Save
        </button>
        <button className="btn-secondary" onClick={handleCancel}>
          <X aria-hidden="true" />
          Cancel
        </button>
        {error && <p role="alert">{error}</p>}
      </li>
    );
  }

  return (
    <li className="task-item">
      <div className="task-item__body">
        <strong>{task.title}</strong>
        {task.description && <p>{task.description}</p>}
      </div>
      <div className="task-item__actions">
        <button className="btn-secondary" onClick={() => setIsEditing(true)}>
          <Pencil aria-hidden="true" />
          Edit
        </button>
        <button
          className="btn-secondary"
          onClick={() => onToggleArchived(task.id, !task.archived)}
        >
          {task.archived ? (
            <ArchiveRestore aria-hidden="true" />
          ) : (
            <Archive aria-hidden="true" />
          )}
          {task.archived ? "Unarchive" : "Archive"}
        </button>
        {confirmingDelete ? (
          <>
            <span>Delete permanently?</span>
            <button className="btn-danger" onClick={() => onDelete(task.id)}>
              <Check aria-hidden="true" />
              Confirm
            </button>
            <button
              className="btn-secondary"
              onClick={() => setConfirmingDelete(false)}
            >
              <X aria-hidden="true" />
              Cancel
            </button>
          </>
        ) : (
          <button
            className="btn-danger"
            onClick={() => setConfirmingDelete(true)}
          >
            <Trash2 aria-hidden="true" />
            Delete
          </button>
        )}
      </div>
    </li>
  );
}
