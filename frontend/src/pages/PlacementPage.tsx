import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { startPlacement, submitPlacementAnswer } from "../api/client";
import ProblemCard from "../components/ProblemCard";
import AnswerInput from "../components/AnswerInput";
import PlacementProgress from "../components/PlacementProgress";
import type { PlacementProblem, PlacementResult, TopicPlacement } from "../types/api";
import { TOPIC_LABELS } from "../components/ProblemCard";

type PlacementState = "intro" | "loading" | "question" | "done" | "error";

export default function PlacementPage() {
  const { studentId } = useAuth();
  const navigate = useNavigate();
  const [state, setState] = useState<PlacementState>("intro");
  const [currentProblem, setCurrentProblem] = useState<PlacementProblem | null>(null);
  const [placements, setPlacements] = useState<Record<string, TopicPlacement> | null>(null);
  const [totalAsked, setTotalAsked] = useState(0);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const startTest = useCallback(async () => {
    if (!studentId) return;
    setState("loading");
    try {
      const result = await startPlacement(studentId);
      if (result.placement_active) {
        setCurrentProblem(result);
        setState("question");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start placement");
      setState("error");
    }
  }, [studentId]);

  const handleSubmit = async (answer: string) => {
    if (!studentId || !currentProblem?.problem_id) return;
    setSubmitting(true);
    try {
      const result = await submitPlacementAnswer(
        studentId,
        currentProblem.problem_id,
        answer
      );

      if ("placement_active" in result && result.placement_active === false) {
        // Placement complete
        const final = result as PlacementResult;
        setPlacements(final.placements);
        setTotalAsked(final.questions_asked);
        setState("done");
      } else {
        // Next question
        const next = result as PlacementProblem;
        setCurrentProblem(next);
        setState("question");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit answer");
      setState("error");
    } finally {
      setSubmitting(false);
    }
  };

  if (!studentId) {
    navigate("/login");
    return null;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {state === "intro" && (
        <div className="text-center py-16">
          <h1 className="text-3xl font-bold text-slate-900 mb-4">Placement Test</h1>
          <p className="text-slate-500 mb-2 max-w-md mx-auto">
            Answer 15–25 questions to determine your starting level across 8 algebra topics.
          </p>
          <p className="text-slate-400 text-sm mb-8">
            The test adapts to your level — difficulty increases when you answer correctly.
          </p>
          <button
            onClick={startTest}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium text-lg hover:bg-blue-700 transition-colors"
          >
            Begin Test
          </button>
        </div>
      )}

      {state === "loading" && (
        <div className="text-center py-16 text-slate-500">Starting placement test...</div>
      )}

      {state === "error" && (
        <div className="text-center py-16">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={startTest}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      )}

      {state === "question" && currentProblem && (
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Placement Test</h2>
          <PlacementProgress
            current={currentProblem.question_number}
            total={currentProblem.total_questions}
          />

          {currentProblem.previous_correct !== undefined && (
            <div className={`text-sm mb-4 ${
              currentProblem.previous_correct ? "text-green-600" : "text-red-600"
            }`}>
              Previous answer: {currentProblem.previous_correct ? "Correct" : "Incorrect"}
            </div>
          )}

          <div className="space-y-6">
            <ProblemCard
              topicId={currentProblem.topic_id!}
              difficulty={currentProblem.difficulty!}
              statement={currentProblem.statement!}
            />
            <AnswerInput onSubmit={handleSubmit} disabled={submitting} />
          </div>
        </div>
      )}

      {state === "done" && placements && (
        <div className="py-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-2 text-center">
            Placement Complete
          </h2>
          <p className="text-slate-500 text-center mb-8">
            {totalAsked} questions answered. Here are your starting levels:
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
            {Object.entries(placements).map(([topicId, placement]) => (
              <div
                key={topicId}
                className={`rounded-lg border p-4 ${
                  placement.status === "skip"
                    ? "bg-green-50 border-green-200"
                    : "bg-blue-50 border-blue-200"
                }`}
              >
                <div className="font-medium text-slate-900 text-sm">
                  {TOPIC_LABELS[topicId] || topicId}
                </div>
                <div className="text-xs text-slate-600 mt-1">
                  {placement.status === "skip"
                    ? "Already mastered"
                    : `Starting at Level ${placement.start_difficulty}`}
                  {" · "}
                  {Math.round(placement.estimated_accuracy * 100)}% accuracy
                </div>
              </div>
            ))}
          </div>

          <div className="text-center">
            <button
              onClick={() => navigate("/practice")}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium text-lg hover:bg-blue-700 transition-colors"
            >
              Start Practicing
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
