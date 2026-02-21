interface MilestoneBannerProps {
  milestone: number;
  onDismiss: () => void;
}

export default function MilestoneBanner({ milestone, onDismiss }: MilestoneBannerProps) {
  return (
    <div className="rounded-lg border bg-emerald-50 border-emerald-200 text-emerald-800 p-4 mb-6 flex items-start justify-between gap-4">
      <div>
        <p className="font-semibold">You've completed {milestone} practice problems!</p>
        <p className="text-sm mt-1">
          Consider taking a new placement test to see how much you've improved and
          update your personalized study plan.
        </p>
      </div>
      <button
        onClick={onDismiss}
        aria-label="Dismiss"
        className="text-emerald-600 hover:text-emerald-800 font-medium text-sm shrink-0"
      >
        Dismiss
      </button>
    </div>
  );
}
