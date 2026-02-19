import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getProgress } from "../api/client";
import MasteryGrid from "../components/MasteryGrid";
import type { Progress } from "../types/api";

export default function DashboardPage() {
  const { studentId } = useAuth();
  const navigate = useNavigate();
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);

  useEffect(() => {
    if (!studentId) return;
    setLoading(true);
    getProgress(studentId)
      .then(setProgress)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load progress"))
      .finally(() => setLoading(false));
  }, [studentId]);

  if (!studentId) {
    navigate("/login");
    return null;
  }

  if (loading) {
    return <div className="text-center py-16 text-slate-500">Loading progress...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-16">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!progress) return null;

  const mastered = progress.topics.filter((t) => t.mastery === "mastered").length;
  const inProgress = progress.topics.filter((t) => t.mastery === "in_progress").length;
  const accuracy = progress.overall_accuracy != null
    ? Math.round(progress.overall_accuracy * 100)
    : null;

  const toggleTopic = (topicId: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topicId)
        ? prev.filter((id) => id !== topicId)
        : [...prev, topicId]
    );
  };

  const handlePractice = () => {
    if (selectedTopics.length === 0) return;
    navigate(`/practice?topics=${selectedTopics.join(",")}`);
  };

  const handleSmartPractice = () => {
    navigate("/practice?smart=true");
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <div className="flex items-center gap-3">
          <button
            onClick={handlePractice}
            disabled={selectedTopics.length === 0}
            className="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Practice{selectedTopics.length > 0 ? ` (${selectedTopics.length})` : ""}
          </button>
          <button
            onClick={handleSmartPractice}
            className="px-5 py-2.5 bg-emerald-600 text-white rounded-lg font-medium hover:bg-emerald-700 transition-colors"
          >
            Smart Practice
          </button>
        </div>
      </div>

      {/* Stats overview */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <StatCard label="Topics Mastered" value={`${mastered}/8`} />
        <StatCard label="In Progress" value={String(inProgress)} />
        <StatCard label="Total Problems" value={String(progress.total_attempts)} />
        <StatCard label="Accuracy" value={accuracy != null ? `${accuracy}%` : "\u2014"} />
      </div>

      {/* Topic mastery grid */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900">Topic Progress</h2>
        <p className="text-xs text-slate-400">
          Click topics to select, then press Practice. Or use Smart Practice for auto-selection.
        </p>
      </div>
      <MasteryGrid
        topics={progress.topics}
        selectedTopics={selectedTopics}
        onToggleTopic={toggleTopic}
      />
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white rounded-lg border border-slate-200 p-4 text-center">
      <div className="text-2xl font-bold text-slate-900">{value}</div>
      <div className="text-sm text-slate-500">{label}</div>
    </div>
  );
}
