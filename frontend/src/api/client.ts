import type {
  RegisterResponse,
  LoginResponse,
  SessionResponse,
  SessionEndResponse,
  Problem,
  AnswerResult,
  Progress,
  PlacementProblem,
  PlacementResult,
  Topic,
  AiConfig,
  AiConfigSaveResponse,
  AiTestResponse,
  AiExplainResponse,
} from "../types/api";

const BASE_URL = import.meta.env.VITE_API_URL || "/api";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const data = await res.json();

  if (!res.ok) {
    throw new ApiError(data?.message || `Request failed: ${res.status}`, res.status);
  }

  return data as T;
}

// --- Students ---

export function registerStudent(
  email: string,
  password: string,
  name: string
): Promise<RegisterResponse> {
  return request("/students", {
    method: "POST",
    body: JSON.stringify({ email, password, name }),
  });
}

export function loginStudent(
  email: string,
  password: string
): Promise<LoginResponse> {
  return request("/students/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function getProgress(studentId: string): Promise<Progress> {
  return request(`/students/${studentId}/progress`);
}

// --- Sessions ---

export function startSession(studentId: string): Promise<SessionResponse> {
  return request("/sessions", {
    method: "POST",
    body: JSON.stringify({ student_id: studentId }),
  });
}

export function endSession(sessionId: string): Promise<SessionEndResponse> {
  return request(`/sessions/${sessionId}/end`, {
    method: "POST",
  });
}

// --- Problems ---

export function getNextProblem(studentId: string): Promise<Problem> {
  return request(`/problems/next?student_id=${studentId}`);
}

export function checkAnswer(
  studentId: string,
  sessionId: string,
  problemId: string,
  answer: string
): Promise<AnswerResult> {
  return request("/problems/check", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      session_id: sessionId,
      problem_id: problemId,
      answer,
    }),
  });
}

// --- Placement ---

export function startPlacement(
  studentId: string,
  maxQuestions?: number
): Promise<PlacementProblem> {
  return request("/placement/start", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      max_questions: maxQuestions,
    }),
  });
}

export function skipPlacement(
  studentId: string
): Promise<{ student_id: string; skipped: boolean }> {
  return request("/placement/skip", {
    method: "POST",
    body: JSON.stringify({ student_id: studentId }),
  });
}

export function resetPlacement(
  studentId: string
): Promise<{ student_id: string; needs_placement: boolean }> {
  return request("/placement/reset", {
    method: "POST",
    body: JSON.stringify({ student_id: studentId }),
  });
}

export function submitPlacementAnswer(
  studentId: string,
  problemId: string,
  answer: string
): Promise<PlacementProblem | PlacementResult> {
  return request("/placement/answer", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      problem_id: problemId,
      answer,
    }),
  });
}

// --- AI Configuration ---

export function getAiConfig(studentId: string): Promise<AiConfig> {
  return request(`/students/${studentId}/ai-config`);
}

export function saveAiConfig(
  studentId: string,
  provider: "anthropic" | "openai",
  apiKey: string
): Promise<AiConfigSaveResponse> {
  return request(`/students/${studentId}/ai-config`, {
    method: "POST",
    body: JSON.stringify({ provider, api_key: apiKey }),
  });
}

export function deleteAiConfig(studentId: string): Promise<{ student_id: string; configured: boolean }> {
  return request(`/students/${studentId}/ai-config`, {
    method: "DELETE",
  });
}

export function testAiConnection(studentId: string): Promise<AiTestResponse> {
  return request(`/students/${studentId}/ai-config/test`, {
    method: "POST",
  });
}

export function getAiExplanation(
  studentId: string,
  topicId: string,
  statement: string,
  studentAnswer: string,
  correctAnswer: string
): Promise<AiExplainResponse> {
  return request("/ai/explain", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      topic_id: topicId,
      statement,
      student_answer: studentAnswer,
      correct_answer: correctAnswer,
    }),
  });
}

// --- Topics ---

export function getTopics(): Promise<Topic[]> {
  return request("/topics");
}
