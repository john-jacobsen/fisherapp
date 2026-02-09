import MathRenderer from "./MathRenderer";

const DIFFICULTY_LABELS = ["", "Recognition", "Routine", "Multi-step", "Transfer", "Synthesis"];

const TOPIC_LABELS: Record<string, string> = {
  fraction_arithmetic: "Fraction Arithmetic",
  exponent_rules: "Exponent Rules",
  order_of_operations: "Order of Operations",
  summation_notation: "Summation Notation",
  solving_equations: "Solving Equations",
  logarithms_exponentials: "Logarithms & Exponentials",
  combinatorics: "Combinatorics",
  geometric_series: "Geometric Series",
};

interface ProblemCardProps {
  topicId: string;
  difficulty: number;
  statement: string;
}

export default function ProblemCard({ topicId, difficulty, statement }: ProblemCardProps) {
  const topicLabel = TOPIC_LABELS[topicId] || topicId;
  const diffLabel = DIFFICULTY_LABELS[difficulty] || `Level ${difficulty}`;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-sm font-medium text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
          {topicLabel}
        </span>
        <span className="text-sm text-slate-500">
          {diffLabel} (Lv. {difficulty})
        </span>
      </div>

      <div className="text-lg text-slate-900 leading-relaxed">
        <MathRenderer text={statement} />
      </div>
    </div>
  );
}

export { TOPIC_LABELS };
