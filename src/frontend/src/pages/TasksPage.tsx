import { useCallback, useEffect, useState } from "react";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import * as taskApi from "../services/taskApi";
import type { Task } from "../services/taskApi";

export default function TasksPage() {
  const [view, setView] = useState<"active" | "archived">("active");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const response = await taskApi.listTasks(view === "archived");
      setTasks(response.tasks);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks.");
    }
  }, [view]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function handleCreate(title: string, description: string) {
    await taskApi.createTask({ title, description });
    await refresh();
  }

  async function handleEdit(id: number, title: string, description: string) {
    await taskApi.updateTask(id, { title, description });
    await refresh();
  }

  async function handleToggleArchived(id: number, archived: boolean) {
    await taskApi.updateTask(id, { archived });
    await refresh();
  }

  async function handleDelete(id: number) {
    await taskApi.deleteTask(id);
    await refresh();
  }

  return (
    <main className="tasks-page">
      <h1>Task Tracker</h1>

      <TaskForm onCreate={handleCreate} />

      <nav className="tasks-page__tabs">
        <button
          disabled={view === "active"}
          onClick={() => setView("active")}
        >
          Active
        </button>
        <button
          disabled={view === "archived"}
          onClick={() => setView("archived")}
        >
          Archived
        </button>
      </nav>

      {error && <p role="alert">{error}</p>}

      <TaskList
        tasks={tasks}
        emptyMessage={
          view === "active" ? "No active tasks." : "No archived tasks."
        }
        onEdit={handleEdit}
        onToggleArchived={handleToggleArchived}
        onDelete={handleDelete}
      />
    </main>
  );
}
