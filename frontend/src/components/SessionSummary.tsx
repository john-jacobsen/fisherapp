import type { SessionEndResponse } from "../types/api";

interface SessionSummaryProps {
  summary: SessionEndResponse;
  onDashboard: () => void;
  onNewSession: () => void;
}

export default function SessionSummary({ summary, onDashboard, onNewSession }: SessionSummaryProps) {
  const accuracy = summary.problems_served > 0
    ? Math.round((summary.problems_correct / summary.problems_served) * 100)
    : 0;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-8 text-center max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-slate-900 mb-6">Session Complete</h2>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div>
          <div className="text-3xl font-bold text-blue-600">{summary.problems_served}</div>
          <div className="text-sm text-slate-500">Problems</div>
        </div>
        <div>
          <div className="text-3xl font-bold text-green-600">{summary.problems_correct}</div>
          <div className="text-sm text-slate-500">Correct</div>
        </div>
        <div>
          <div className="text-3xl font-bold text-slate-700">{accuracy}%</div>
          <div className="text-sm text-slate-500">Accuracy</div>
        </div>
      </div>

      <div className="flex gap-3 justify-center">
        <button
          onClick={onNewSession}
          className="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Practice More
        </button>
        <button
          onClick={onDashboard}
          className="px-5 py-2.5 bg-slate-100 text-slate-700 rounded-lg font-medium hover:bg-slate-200 transition-colors"
        >
          Dashboard
        </button>
      </div>
    </div>
  );
}
