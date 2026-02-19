import { useState, useEffect, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { startSession, endSession, getNextProblem, checkAnswer, getProgress } from "../api/client";
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
  const [searchParams] = useSearchParams();
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
  const [lastAnswer, setLastAnswer] = useState("");

  // Parse topics from URL params
  const topicsParam = searchParams.get("topics");
  const isSmartMode = searchParams.get("smart") === "true";
  const selectedTopics = topicsParam ? topicsParam.split(",").filter(Boolean) : [];

  // For smart mode, we compute topics from progress data
  const [smartTopics, setSmartTopics] = useState<string[] | null>(null);

  // Resolve smart practice topics
  useEffect(() => {
    if (!isSmartMode || !studentId) return;
    getProgress(studentId).then((progress) => {
      // Pick topics with lowest accuracy or most overdue reviews
      const ranked = [...progress.topics]
        .filter((t) => t.mastery !== "not_started" || t.attempts === 0)
        .sort((a, b) => {
          // Prioritize not_started (never practiced) first
          if (a.mastery === "not_started" && b.mastery !== "not_started") return -1;
          if (b.mastery === "not_started" && a.mastery !== "not_started") return 1;
          // Then by lowest accuracy
          const accA = a.accuracy ?? 0;
          const accB = b.accuracy ?? 0;
          return accA - accB;
        });
      // Select the top half (at least 2, at most all)
      const count = Math.max(2, Math.ceil(ranked.length / 2));
      setSmartTopics(ranked.slice(0, count).map((t) => t.topic_id));
    }).catch(() => {
      // Fallback: no topic filter (practice everything)
      setSmartTopics([]);
    });
  }, [isSmartMode, studentId]);

  const getTopicFilter = useCallback((): string[] | undefined => {
    if (isSmartMode) {
      return smartTopics && smartTopics.length > 0 ? smartTopics : undefined;
    }
    return selectedTopics.length > 0 ? selectedTopics : undefined;
  }, [isSmartMode, smartTopics, selectedTopics]);

  const initSession = useCallback(async () => {
    if (!studentId) return;
    setState("loading");
    try {
      const sess = await startSession(studentId);
      setSessionId(sess.session_id);
      const topics = getTopicFilter();
      const prob = await getNextProblem(studentId, topics);
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
  }, [studentId, getTopicFilter]);

  // Auto-start session when component mounts (or when smart topics resolve)
  useEffect(() => {
    if (!studentId) return;
    if (isSmartMode && smartTopics === null) return; // Wait for smart topics to resolve
    initSession();
  }, [studentId, isSmartMode, smartTopics]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSubmit = async (answer: string) => {
    if (!studentId || !sessionId || !problem) return;
    setSubmitting(true);
    setLastAnswer(answer);
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
      const topics = getTopicFilter();
      const prob = await getNextProblem(studentId, topics);
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

  // Redirect to dashboard if no topics specified and not smart mode
  if (!isSmartMode && selectedTopics.length === 0) {
    navigate("/dashboard");
    return null;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Session stats bar */}
      {state !== "ended" && state !== "error" && (
        <div className="flex items-center justify-between mb-6">
          <div className="text-sm text-slate-500">
            {isSmartMode && <span className="text-emerald-600 font-medium mr-3">Smart Practice</span>}
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
          <FeedbackPanel
            result={feedback}
            problemStatement={problem?.statement || ""}
            studentAnswer={lastAnswer}
            onNext={handleNext}
          />
        </div>
      )}

      {state === "complete" && (
        <div className="text-center py-16">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">No problems available</h2>
          <p className="text-slate-500 mb-6">
            No problems could be generated for the selected topics. Try selecting different topics or starting a new session.
          </p>
          <div className="flex justify-center gap-3">
            <button
              onClick={() => navigate("/dashboard")}
              className="px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
            >
              Back to Dashboard
            </button>
            <button
              onClick={handleEndSession}
              className="px-6 py-2.5 bg-slate-200 text-slate-700 rounded-lg font-medium hover:bg-slate-300"
            >
              End Session
            </button>
          </div>
        </div>
      )}

      {state === "ended" && sessionSummary && (
        <SessionSummary
          summary={sessionSummary}
          onDashboard={() => navigate("/dashboard")}
          onNewSession={() => navigate("/dashboard")}
        />
      )}
    </div>
  );
}
