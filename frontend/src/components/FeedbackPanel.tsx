import { useState } from "react";
import { Link } from "react-router-dom";
import MathRenderer from "./MathRenderer";
import { useAuth } from "../context/AuthContext";
import { getAiExplanation } from "../api/client";
import type { AnswerResult } from "../types/api";

interface FeedbackPanelProps {
  result: AnswerResult;
  problemStatement: string;
  studentAnswer: string;
  onNext: () => void;
}

export default function FeedbackPanel({ result, problemStatement, studentAnswer, onNext }: FeedbackPanelProps) {
  const { studentId, hasAiKey } = useAuth();
  const [aiExplanation, setAiExplanation] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  const handleShowAiSolution = async () => {
    if (!studentId) return;
    setAiLoading(true);
    setAiError("");
    try {
      const response = await getAiExplanation(
        studentId,
        result.topic_id,
        problemStatement,
        studentAnswer,
        result.correct_answer
      );
      setAiExplanation(response.explanation);
    } catch (err) {
      setAiError(err instanceof Error ? err.message : "Failed to get AI explanation");
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className={`rounded-xl border p-6 ${
      result.correct
        ? "bg-green-50 border-green-200"
        : "bg-red-50 border-red-200"
    }`}>
      <div className="flex items-center gap-3 mb-4">
        {result.correct ? (
          <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
            ✓
          </div>
        ) : (
          <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center text-white font-bold">
            ✗
          </div>
        )}
        <h3 className={`text-lg font-semibold ${
          result.correct ? "text-green-800" : "text-red-800"
        }`}>
          {result.correct ? "Correct!" : "Incorrect"}
        </h3>
      </div>

      {!result.correct && (
        <div className="mb-4">
          <p className="text-sm font-medium text-slate-700 mb-1">Correct answer:</p>
          <div className="text-lg text-slate-900">
            <MathRenderer text={result.correct_answer} />
          </div>
        </div>
      )}

      {result.solution_steps && result.solution_steps.length > 0 && (
        <div className="mb-4">
          <p className="text-sm font-medium text-slate-700 mb-2">Solution:</p>
          <ol className="space-y-2">
            {result.solution_steps.map((step, i) => (
              <li key={i} className="text-slate-800 pl-2">
                <MathRenderer text={step} />
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* AI Solution section — only on incorrect answers */}
      {!result.correct && (
        <div className="mb-4">
          {aiExplanation ? (
            <div className="bg-white rounded-lg border border-slate-200 p-4 mt-3">
              <p className="text-sm font-medium text-purple-700 mb-2">AI Explanation:</p>
              <div className="text-sm text-slate-800 whitespace-pre-wrap leading-relaxed">
                <MathRenderer text={aiExplanation} />
              </div>
            </div>
          ) : aiLoading ? (
            <div className="text-sm text-slate-500 mt-2">
              Getting AI explanation...
            </div>
          ) : aiError ? (
            <div className="text-sm text-red-600 mt-2">{aiError}</div>
          ) : hasAiKey ? (
            <button
              onClick={handleShowAiSolution}
              className="text-sm text-purple-600 hover:text-purple-800 font-medium mt-2 transition-colors"
            >
              Show AI Solution
            </button>
          ) : (
            <Link
              to="/settings"
              className="text-sm text-purple-600 hover:text-purple-800 font-medium mt-2 inline-block transition-colors"
            >
              Connect AI in Settings
            </Link>
          )}
        </div>
      )}

      {result.mastery_changed && result.new_mastery === "mastered" && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
          <p className="text-yellow-800 font-medium">
            Topic mastered: {result.topic_id.replace(/_/g, " ")}!
          </p>
        </div>
      )}

      <button
        onClick={onNext}
        className="mt-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
      >
        Next Problem
      </button>
    </div>
  );
}
