export interface Task {
  id: number;
  title: string;
  description: string;
  archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
}

export interface TaskCreateInput {
  title: string;
  description?: string;
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  archived?: boolean;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

declare global {
  interface Window {
    __RUNTIME_CONFIG__?: { API_BASE_URL?: string };
  }
}

const BASE_URL =
  window.__RUNTIME_CONFIG__?.API_BASE_URL ||
  (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      message = body.detail ? JSON.stringify(body.detail) : message;
    } catch {
      // response had no JSON body; keep default message
    }
    throw new ApiError(response.status, message);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export function listTasks(archived: boolean): Promise<TaskListResponse> {
  return request<TaskListResponse>(`/api/tasks?archived=${archived}`);
}

export function getTask(id: number): Promise<Task> {
  return request<Task>(`/api/tasks/${id}`);
}

export function createTask(input: TaskCreateInput): Promise<Task> {
  return request<Task>("/api/tasks", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function updateTask(id: number, input: TaskUpdateInput): Promise<Task> {
  return request<Task>(`/api/tasks/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export function archiveTask(id: number): Promise<Task> {
  return updateTask(id, { archived: true });
}

export function unarchiveTask(id: number): Promise<Task> {
  return updateTask(id, { archived: false });
}

export function deleteTask(id: number): Promise<void> {
  return request<void>(`/api/tasks/${id}`, { method: "DELETE" });
}
