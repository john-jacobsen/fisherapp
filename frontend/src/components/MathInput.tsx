import { useRef, useEffect, useCallback } from "react";
import type { MathfieldElement } from "mathlive";
import "mathlive";

interface MathInputProps {
  value: string;
  onChange: (latex: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
  placeholder?: string;
  autoFocus?: boolean;
}

export default function MathInput({
  value,
  onChange,
  onSubmit,
  disabled = false,
  placeholder = "Type your answer...",
  autoFocus = true,
}: MathInputProps) {
  const ref = useRef<MathfieldElement>(null);

  // Sync value into the mathfield when it changes externally (e.g. cleared)
  useEffect(() => {
    const mf = ref.current;
    if (mf && mf.getValue() !== value) {
      mf.setValue(value);
    }
  }, [value]);

  // Set up event listeners
  useEffect(() => {
    const mf = ref.current;
    if (!mf) return;

    const handleInput = () => {
      onChange(mf.getValue());
    };

    mf.addEventListener("input", handleInput);
    return () => mf.removeEventListener("input", handleInput);
  }, [onChange]);

  // Handle Enter key to submit
  useEffect(() => {
    const mf = ref.current;
    if (!mf || !onSubmit) return;

    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        onSubmit();
      }
    };

    mf.addEventListener("keydown", handleKeydown);
    return () => mf.removeEventListener("keydown", handleKeydown);
  }, [onSubmit]);

  // Auto-focus
  useEffect(() => {
    if (autoFocus && ref.current) {
      // Small delay to let the web component initialize
      const timer = setTimeout(() => ref.current?.focus(), 100);
      return () => clearTimeout(timer);
    }
  }, [autoFocus]);

  // Handle disabled state
  useEffect(() => {
    const mf = ref.current;
    if (mf) {
      mf.readOnly = disabled;
    }
  }, [disabled]);

  const setRef = useCallback((el: MathfieldElement | null) => {
    (ref as React.MutableRefObject<MathfieldElement | null>).current = el;
    if (el) {
      // Configure the mathfield
      el.mathVirtualKeyboardPolicy = "auto";
      el.smartFence = true;
      el.smartSuperscript = false;
      if (value) el.setValue(value);
    }
  }, []);

  return (
    <math-field
      ref={setRef}
      placeholder={placeholder}
      class={[
        "math-input-field",
        "flex-1 px-4 py-3 border border-slate-300 rounded-lg text-lg",
        "focus-within:outline-none focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-transparent",
        disabled ? "bg-slate-100 cursor-not-allowed" : "",
      ].join(" ")}
    />
  );
}

// Extend JSX for the math-field web component
declare global {
  namespace JSX {
    interface IntrinsicElements {
      "math-field": React.DetailedHTMLProps<
        React.HTMLAttributes<MathfieldElement> & {
          placeholder?: string;
          "read-only"?: boolean;
          "virtual-keyboard-mode"?: string;
        },
        MathfieldElement
      >;
    }
  }
}
