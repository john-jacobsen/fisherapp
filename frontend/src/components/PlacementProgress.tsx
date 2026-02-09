interface PlacementProgressProps {
  current: number;
  total: number;
}

export default function PlacementProgress({ current, total }: PlacementProgressProps) {
  const pct = Math.min(100, Math.round((current / total) * 100));

  return (
    <div className="mb-6">
      <div className="flex justify-between text-sm text-slate-500 mb-2">
        <span>Question {current} of {total}</span>
        <span>{pct}%</span>
      </div>
      <div className="w-full bg-slate-200 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
