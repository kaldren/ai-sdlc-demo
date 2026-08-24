import { FormEvent, useState } from "react";

interface TaskFormProps {
  onCreate: (title: string, description: string) => Promise<void>;
}

export default function TaskForm({ onCreate }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim()) {
      setError("Title is required.");
      return;
    }
    setError(null);
    setSubmitting(true);
    try {
      await onCreate(title.trim(), description.trim());
      setTitle("");
      setDescription("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        type="text"
        placeholder="Task title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        aria-label="Task title"
      />
      <input
        type="text"
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        aria-label="Task description"
      />
      <button type="submit" disabled={submitting}>
        Add Task
      </button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
