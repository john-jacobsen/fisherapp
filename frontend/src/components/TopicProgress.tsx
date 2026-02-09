import type { TopicProgress as TopicProgressType } from "../types/api";
import { TOPIC_LABELS } from "./ProblemCard";

interface TopicProgressProps {
  topic: TopicProgressType;
}

const MASTERY_STYLES: Record<string, { bg: string; text: string; label: string }> = {
  mastered: { bg: "bg-green-100 border-green-300", text: "text-green-700", label: "Mastered" },
  in_progress: { bg: "bg-blue-50 border-blue-200", text: "text-blue-700", label: "In Progress" },
  not_started: { bg: "bg-slate-50 border-slate-200", text: "text-slate-400", label: "Not Started" },
};

export default function TopicProgress({ topic }: TopicProgressProps) {
  const style = MASTERY_STYLES[topic.mastery] || MASTERY_STYLES.not_started;
  const accuracy = topic.accuracy != null ? Math.round(topic.accuracy * 100) : null;
  const label = TOPIC_LABELS[topic.topic_id] || topic.topic_id;

  return (
    <div className={`rounded-lg border p-4 ${style.bg}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-medium text-slate-900 text-sm">{label}</h3>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${style.text} ${style.bg}`}>
          {style.label}
        </span>
      </div>

      {topic.mastery !== "not_started" && (
        <div className="grid grid-cols-3 gap-2 text-xs text-slate-600">
          <div>
            <div className="font-semibold text-slate-800">{accuracy != null ? `${accuracy}%` : "—"}</div>
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
    </div>
  );
}
