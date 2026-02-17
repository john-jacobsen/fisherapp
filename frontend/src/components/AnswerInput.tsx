import { useState, useCallback } from "react";
import MathInput from "./MathInput";
import { latexToPlain } from "../utils/latexToPlain";

interface AnswerInputProps {
  onSubmit: (answer: string) => void;
  disabled?: boolean;
}

type InputMode = "math" | "text";

const MODE_STORAGE_KEY = "fisherapp-input-mode";

function getStoredMode(): InputMode {
  try {
    const stored = localStorage.getItem(MODE_STORAGE_KEY);
    if (stored === "text" || stored === "math") return stored;
  } catch {}
  return "math";
}

export default function AnswerInput({ onSubmit, disabled = false }: AnswerInputProps) {
  const [answer, setAnswer] = useState("");
  const [mode, setMode] = useState<InputMode>(getStoredMode);

  const handleSubmit = useCallback((e?: React.FormEvent) => {
    e?.preventDefault();
    const raw = answer.trim();
    if (!raw || disabled) return;

    // Convert LaTeX to plain text if in math mode
    const submittedAnswer = mode === "math" ? latexToPlain(raw) : raw;
    onSubmit(submittedAnswer);
    setAnswer("");
  }, [answer, disabled, mode, onSubmit]);

  const handleMathSubmit = useCallback(() => {
    handleSubmit();
  }, [handleSubmit]);

  const toggleMode = () => {
    const next = mode === "math" ? "text" : "math";
    setMode(next);
    setAnswer("");
    try {
      localStorage.setItem(MODE_STORAGE_KEY, next);
    } catch {}
  };

  return (
    <div className="space-y-2">
      <form onSubmit={handleSubmit} className="flex gap-3">
        {mode === "math" ? (
          <MathInput
            value={answer}
            onChange={setAnswer}
            onSubmit={handleMathSubmit}
            disabled={disabled}
            placeholder="Type your answer..."
            autoFocus
          />
        ) : (
          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            disabled={disabled}
            placeholder="Type your answer (e.g., 3/4, 0.75, \frac{3}{4})"
            className="flex-1 px-4 py-3 border border-slate-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-slate-100 disabled:cursor-not-allowed"
            autoFocus
          />
        )}
        <button
          type="submit"
          disabled={disabled || !answer.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Submit
        </button>
      </form>
      <div className="flex items-center justify-end">
        <button
          type="button"
          onClick={toggleMode}
          className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
        >
          {mode === "math" ? "Switch to plain text input" : "Switch to math keyboard"}
        </button>
      </div>
    </div>
  );
}
