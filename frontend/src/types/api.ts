// API response types matching the Plumber API

export interface RegisterResponse {
  student_id: string;
  email: string;
  name: string;
  needs_placement: boolean;
}

export interface LoginResponse {
  student_id: string;
  needs_placement: boolean;
}

export interface SessionResponse {
  session_id: string;
  student_id: string;
  started_at: string;
}

export interface SessionEndResponse {
  session_id: string;
  ended_at: string;
  problems_served: number;
  problems_correct: number;
}

export interface Intervention {
  type: "reduce_difficulty" | "route_prerequisite" | "worked_example" | "session_complete";
  message: string;
  redirect_topic?: string;
}

export interface Problem {
  problem_id: string;
  topic_id: string;
  difficulty: number;
  statement: string;
  session_id: string;
  intervention: Intervention | null;
}

export interface AnswerResult {
  correct: boolean;
  correct_answer: string;
  solution_steps: string[];
  mastery_changed: boolean;
  new_mastery: string | null;
  topic_id: string;
  difficulty: number;
}

export interface TopicProgress {
  topic_id: string;
  mastery: string;
  difficulty: number;
  accuracy: number | null;
  attempts: number;
  sessions: number;
  ease_factor: number;
  next_review: string;
}

export interface Progress {
  student_id: string;
  total_attempts: number;
  total_correct: number;
  overall_accuracy: number | null;
  topics: TopicProgress[];
}

export interface PlacementProblem {
  placement_active: boolean;
  question_number: number;
  problem_id: string | null;
  topic_id: string | null;
  difficulty: number | null;
  statement: string | null;
  total_questions: number;
  previous_correct?: boolean;
}

export interface TopicPlacement {
  status: "skip" | "placed";
  start_difficulty: number;
  estimated_accuracy: number;
  questions_asked: number;
}

export interface PlacementResult {
  placement_active: false;
  completed: true;
  questions_asked: number;
  placements: Record<string, TopicPlacement>;
}

export interface Topic {
  topic_id: string;
  title: string;
  prerequisites: string[];
  skills: string[];
}

export interface AiConfig {
  student_id: string;
  provider: "anthropic" | "openai" | null;
  configured: boolean;
  key_hint?: string;
}

export interface AiConfigSaveResponse {
  student_id: string;
  provider: string;
  configured: boolean;
}

export interface AiTestResponse {
  student_id: string;
  provider: string;
  success: boolean;
}

export interface AiExplainResponse {
  explanation: string;
  provider: string;
}

export interface ApiError {
  status: "error";
  message: string;
}
