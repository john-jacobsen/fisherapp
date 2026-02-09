import type { Intervention } from "../types/api";

interface InterventionBannerProps {
  intervention: Intervention;
}

export default function InterventionBanner({ intervention }: InterventionBannerProps) {
  const bgColor = intervention.type === "worked_example"
    ? "bg-purple-50 border-purple-200 text-purple-800"
    : intervention.type === "route_prerequisite"
    ? "bg-orange-50 border-orange-200 text-orange-800"
    : "bg-blue-50 border-blue-200 text-blue-800";

  return (
    <div className={`rounded-lg border p-4 mb-4 ${bgColor}`}>
      <p className="font-medium">{intervention.message}</p>
    </div>
  );
}
