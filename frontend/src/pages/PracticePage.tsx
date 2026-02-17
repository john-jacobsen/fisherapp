import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { startSession, endSession, getNextProblem, checkAnswer, getTopics } from "../api/client";
import ProblemCard from "../components/ProblemCard";
import AnswerInput from "../components/AnswerInput";
import FeedbackPanel from "../components/FeedbackPanel";
import InterventionBanner from "../components/InterventionBanner";
import SessionSummary from "../components/SessionSummary";
import type { Problem, AnswerResult, SessionEndResponse, Intervention, Topic } from "../types/api";

type PracticeState = "topic-select" | "loading" | "problem" | "feedback" | "ended" | "error" | "complete";

export default function PracticePage() {
  const { studentId } = useAuth();
  const navigate = useNavigate();
  const [state, setState] = useState<PracticeState>("topic-select");
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

  // Topic selection
  const [allTopics, setAllTopics] = useState<Topic[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [topicsLoading, setTopicsLoading] = useState(true);

  // Load available topics on mount
  useEffect(() => {
    getTopics()
      .then((topics) => {
        setAllTopics(topics);
        setSelectedTopics(topics.map((t) => t.topic_id));
      })
      .catch(() => {})
      .finally(() => setTopicsLoading(false));
  }, []);

  const toggleTopic = (topicId: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topicId)
        ? prev.filter((id) => id !== topicId)
        : [...prev, topicId]
    );
  };

  const selectAll = () => setSelectedTopics(allTopics.map((t) => t.topic_id));
  const selectNone = () => setSelectedTopics([]);

  const initSession = useCallback(async () => {
    if (!studentId) return;
    setState("loading");
    try {
      const sess = await startSession(studentId);
      setSessionId(sess.session_id);
      const topics = selectedTopics.length === allTopics.length ? undefined : selectedTopics;
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
  }, [studentId, selectedTopics, allTopics.length]);

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
      const topics = selectedTopics.length === allTopics.length ? undefined : selectedTopics;
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

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Topic selection screen */}
      {state === "topic-select" && (
        <div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">Practice</h1>
          <p className="text-sm text-slate-500 mb-6">
            Select which topics you want to practice, then start your session.
          </p>

          {topicsLoading ? (
            <div className="text-center py-8 text-slate-500">Loading topics...</div>
          ) : (
            <>
              <div className="flex items-center gap-3 mb-4">
                <button
                  onClick={selectAll}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Select All
                </button>
                <span className="text-slate-300">|</span>
                <button
                  onClick={selectNone}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Deselect All
                </button>
                <span className="ml-auto text-sm text-slate-500">
                  {selectedTopics.length}/{allTopics.length} selected
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
                {allTopics.map((topic) => {
                  const isSelected = selectedTopics.includes(topic.topic_id);
                  return (
                    <button
                      key={topic.topic_id}
                      onClick={() => toggleTopic(topic.topic_id)}
                      className={`text-left p-4 rounded-lg border-2 transition-colors ${
                        isSelected
                          ? "border-blue-500 bg-blue-50"
                          : "border-slate-200 bg-white hover:border-slate-300"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                            isSelected
                              ? "border-blue-500 bg-blue-500 text-white"
                              : "border-slate-300"
                          }`}
                        >
                          {isSelected && (
                            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </div>
                        <span className={`text-sm font-medium ${isSelected ? "text-slate-900" : "text-slate-600"}`}>
                          {topic.title}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>

              <button
                onClick={initSession}
                disabled={selectedTopics.length === 0}
                className="w-full px-5 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Start Practice Session
              </button>
            </>
          )}
        </div>
      )}

      {/* Session stats bar */}
      {state !== "ended" && state !== "error" && state !== "topic-select" && (
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
          onNewSession={() => {
            setProblemCount(0);
            setCorrectCount(0);
            setSessionId(null);
            setState("topic-select");
          }}
        />
      )}
    </div>
  );
}
