import MathRenderer from "./MathRenderer";
import type { AnswerResult } from "../types/api";

interface FeedbackPanelProps {
  result: AnswerResult;
  onNext: () => void;
}

export default function FeedbackPanel({ result, onNext }: FeedbackPanelProps) {
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

      {result.mastery_changed && result.new_mastery === "mastered" && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
          <p className="text-yellow-800 font-medium">
            🎓 Topic mastered: {result.topic_id.replace(/_/g, " ")}!
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
