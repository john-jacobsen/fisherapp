import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  registerStudent,
  loginStudent,
  getProgress,
  startSession,
  endSession,
  getNextProblem,
  checkAnswer,
  startPlacement,
  submitPlacementAnswer,
  getTopics,
} from "./client";

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

function mockResponse(data: unknown, ok = true, status = 200) {
  mockFetch.mockResolvedValueOnce({
    ok,
    status,
    json: () => Promise.resolve(data),
  });
}

beforeEach(() => {
  mockFetch.mockReset();
});

describe("API client", () => {
  it("registerStudent sends POST to /students", async () => {
    mockResponse({ student_id: "s1", email: "a@b.com", name: "Test" });
    const result = await registerStudent("a@b.com", "pw", "Test");
    expect(result.student_id).toBe("s1");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/students"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("loginStudent sends POST to /students/login", async () => {
    mockResponse({ student_id: "s1" });
    const result = await loginStudent("a@b.com", "pw");
    expect(result.student_id).toBe("s1");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/students/login"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("getProgress sends GET to /students/:id/progress", async () => {
    mockResponse({ student_id: "s1", total_attempts: 10, total_correct: 7, overall_accuracy: 0.7, topics: [] });
    const result = await getProgress("s1");
    expect(result.total_attempts).toBe(10);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/students/s1/progress"),
      expect.any(Object)
    );
  });

  it("startSession sends POST to /sessions", async () => {
    mockResponse({ session_id: "sess1", student_id: "s1", started_at: "2026-01-01" });
    const result = await startSession("s1");
    expect(result.session_id).toBe("sess1");
  });

  it("endSession sends POST to /sessions/:id/end", async () => {
    mockResponse({ session_id: "sess1", ended_at: "2026-01-01", problems_served: 5, problems_correct: 3 });
    const result = await endSession("sess1");
    expect(result.problems_served).toBe(5);
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/sessions/sess1/end"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("getNextProblem sends GET with student_id query param", async () => {
    mockResponse({ problem_id: "p1", topic_id: "fraction_arithmetic", difficulty: 2, statement: "x", session_id: "s1", intervention: null });
    const result = await getNextProblem("s1");
    expect(result.problem_id).toBe("p1");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("student_id=s1"),
      expect.any(Object)
    );
  });

  it("checkAnswer sends POST to /problems/check", async () => {
    mockResponse({ correct: true, correct_answer: "42", solution_steps: [], mastery_changed: false, new_mastery: null, topic_id: "t", difficulty: 1 });
    const result = await checkAnswer("s1", "sess1", "p1", "42");
    expect(result.correct).toBe(true);
    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.student_id).toBe("s1");
    expect(body.problem_id).toBe("p1");
    expect(body.answer).toBe("42");
  });

  it("startPlacement sends POST to /placement/start", async () => {
    mockResponse({ placement_active: true, question_number: 1, problem_id: "p1", topic_id: "t", difficulty: 1, statement: "x", total_questions: 15 });
    const result = await startPlacement("s1");
    expect(result.placement_active).toBe(true);
  });

  it("submitPlacementAnswer sends POST to /placement/answer", async () => {
    mockResponse({ placement_active: true, question_number: 2, problem_id: "p2", topic_id: "t", difficulty: 2, statement: "y", total_questions: 15 });
    const result = await submitPlacementAnswer("s1", "p1", "42");
    expect(result.placement_active).toBe(true);
  });

  it("getTopics sends GET to /topics", async () => {
    mockResponse([{ topic_id: "t1", title: "T1", prerequisites: [], skills: [] }]);
    const result = await getTopics();
    expect(result).toHaveLength(1);
  });

  it("throws ApiError on non-ok response", async () => {
    mockResponse({ message: "Not found" }, false, 404);
    await expect(registerStudent("a@b.com", "pw", "Test")).rejects.toThrow("Not found");
  });
});
