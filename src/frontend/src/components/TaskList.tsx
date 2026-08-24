import type { Task } from "../services/taskApi";
import TaskItem from "./TaskItem";

interface TaskListProps {
  tasks: Task[];
  emptyMessage: string;
  onEdit: (id: number, title: string, description: string) => Promise<void>;
  onToggleArchived: (id: number, archived: boolean) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

export default function TaskList({
  tasks,
  emptyMessage,
  onEdit,
  onToggleArchived,
  onDelete,
}: TaskListProps) {
  if (tasks.length === 0) {
    return <p>{emptyMessage}</p>;
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onEdit={onEdit}
          onToggleArchived={onToggleArchived}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
