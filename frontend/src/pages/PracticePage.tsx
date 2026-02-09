import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { startSession, endSession, getNextProblem, checkAnswer } from "../api/client";
import ProblemCard from "../components/ProblemCard";
import AnswerInput from "../components/AnswerInput";
import FeedbackPanel from "../components/FeedbackPanel";
import InterventionBanner from "../components/InterventionBanner";
import SessionSummary from "../components/SessionSummary";
import type { Problem, AnswerResult, SessionEndResponse, Intervention } from "../types/api";

type PracticeState = "loading" | "problem" | "feedback" | "ended" | "error" | "complete";

export default function PracticePage() {
  const { studentId } = useAuth();
  const navigate = useNavigate();
  const [state, setState] = useState<PracticeState>("loading");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [problem, setProblem] = useState<Problem | null>(null);
  const [feedback, setFeedback] = useState<AnswerResult | null>(null);
  const [intervention, setIntervention] = useState<Intervention | null>(null);
  const [sessionSummary, setSessionSummary] = useState<SessionEndResponse | null>(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [problemCount, setProblemCount] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  const initSession = useCallback(async () => {
    if (!studentId) return;
    setState("loading");
    try {
      const sess = await startSession(studentId);
      setSessionId(sess.session_id);
      const prob = await getNextProblem(studentId);
      if (prob.problem_id) {
        setProblem(prob);
        setIntervention(prob.intervention);
        setState("problem");
      } else {
        setState("complete");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start session");
      setState("error");
    }
  }, [studentId]);

  useEffect(() => {
    initSession();
  }, [initSession]);

  const handleSubmit = async (answer: string) => {
    if (!studentId || !sessionId || !problem) return;
    setSubmitting(true);
    try {
      const result = await checkAnswer(studentId, sessionId, problem.problem_id, answer);
      setFeedback(result);
      setProblemCount((c) => c + 1);
      if (result.correct) setCorrectCount((c) => c + 1);
      setState("feedback");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer");
      setState("error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = async () => {
    if (!studentId) return;
    setState("loading");
    try {
      const prob = await getNextProblem(studentId);
      if (prob.problem_id) {
        setProblem(prob);
        setIntervention(prob.intervention);
        setFeedback(null);
        setState("problem");
      } else {
        setState("complete");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get next problem");
      setState("error");
    }
  };

  const handleEndSession = async () => {
    if (!sessionId) return;
    try {
      const summary = await endSession(sessionId);
      setSessionSummary(summary);
      setState("ended");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to end session");
      setState("error");
    }
  };

  if (!studentId) {
    navigate("/login");
    return null;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Session stats bar */}
      {state !== "ended" && state !== "error" && (
        <div className="flex items-center justify-between mb-6">
          <div className="text-sm text-slate-500">
            Problems: {problemCount} | Correct: {correctCount}
            {problemCount > 0 && ` (${Math.round((correctCount / problemCount) * 100)}%)`}
          </div>
          <button
            onClick={handleEndSession}
            className="text-sm text-slate-500 hover:text-red-600 transition-colors"
          >
            End Session
          </button>
        </div>
      )}

      {state === "loading" && (
        <div className="text-center py-16 text-slate-500">Loading...</div>
      )}

      {state === "error" && (
        <div className="text-center py-16">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={initSession}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      )}

      {state === "problem" && problem && (
        <div className="space-y-6">
          {intervention && <InterventionBanner intervention={intervention} />}
          <ProblemCard
            topicId={problem.topic_id}
            difficulty={problem.difficulty}
            statement={problem.statement}
          />
          <AnswerInput onSubmit={handleSubmit} disabled={submitting} />
        </div>
      )}

      {state === "feedback" && feedback && (
        <div className="space-y-6">
          {problem && (
            <ProblemCard
              topicId={problem.topic_id}
              difficulty={problem.difficulty}
              statement={problem.statement}
            />
          )}
          <FeedbackPanel result={feedback} onNext={handleNext} />
        </div>
      )}

      {state === "complete" && (
        <div className="text-center py-16">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">All caught up!</h2>
          <p className="text-slate-500 mb-6">
            All topics mastered and none are due for review.
          </p>
          <button
            onClick={handleEndSession}
            className="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
          >
            End Session
          </button>
        </div>
      )}

      {state === "ended" && sessionSummary && (
        <SessionSummary
          summary={sessionSummary}
          onDashboard={() => navigate("/dashboard")}
          onNewSession={initSession}
        />
      )}
    </div>
  );
}
