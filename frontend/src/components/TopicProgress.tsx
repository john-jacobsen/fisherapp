import type { TopicProgress as TopicProgressType } from "../types/api";
import { TOPIC_LABELS } from "./ProblemCard";

interface TopicProgressProps {
  topic: TopicProgressType;
  selectable?: boolean;
  selected?: boolean;
  onToggle?: () => void;
}

const MASTERY_STYLES: Record<string, { bg: string; text: string; label: string }> = {
  mastered: { bg: "bg-green-100 border-green-300", text: "text-green-700", label: "Mastered" },
  in_progress: { bg: "bg-blue-50 border-blue-200", text: "text-blue-700", label: "In Progress" },
  not_started: { bg: "bg-slate-50 border-slate-200", text: "text-slate-400", label: "Not Started" },
};

export default function TopicProgress({ topic, selectable, selected, onToggle }: TopicProgressProps) {
  const style = MASTERY_STYLES[topic.mastery] || MASTERY_STYLES.not_started;
  const accuracy = topic.accuracy != null ? Math.round(topic.accuracy * 100) : null;
  const label = TOPIC_LABELS[topic.topic_id] || topic.topic_id;

  const selectedStyles = selected
    ? "ring-2 ring-blue-500 ring-offset-1 border-blue-500"
    : "";

  const content = (
    <>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {selectable && (
            <div
              className={`w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                selected
                  ? "border-blue-500 bg-blue-500 text-white"
                  : "border-slate-300"
              }`}
            >
              {selected && (
                <svg className="w-2.5 h-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>
          )}
          <h3 className="font-medium text-slate-900 text-sm">{label}</h3>
        </div>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${style.text} ${style.bg}`}>
          {style.label}
        </span>
      </div>

      {topic.mastery !== "not_started" && (
        <div className="grid grid-cols-3 gap-2 text-xs text-slate-600">
          <div>
            <div className="font-semibold text-slate-800">{accuracy != null ? `${accuracy}%` : "\u2014"}</div>
            <div>Accuracy</div>
          </div>
          <div>
            <div className="font-semibold text-slate-800">Lv. {topic.difficulty}</div>
            <div>Difficulty</div>
          </div>
          <div>
            <div className="font-semibold text-slate-800">{topic.attempts}</div>
            <div>Attempts</div>
          </div>
        </div>
      )}
    </>
  );

  if (selectable) {
    return (
      <button
        type="button"
        onClick={onToggle}
        className={`rounded-lg border p-4 ${style.bg} ${selectedStyles} text-left transition-all hover:shadow-sm`}
      >
        {content}
      </button>
    );
  }

  return (
    <div className={`rounded-lg border p-4 ${style.bg}`}>
      {content}
    </div>
  );
}
