/**
 * Convert MathLive LaTeX output to a plain-text format
 * that the R backend answer checker can compare.
 *
 * The backend already handles:
 *   - Plain fractions: "3/4", "-2/5"
 *   - LaTeX fractions: "\frac{3}{4}"
 *   - Decimals: "0.75", ".5"
 *   - Integers: "3", "-2"
 *   - Letter answers: "a", "b"
 *
 * MathLive produces LaTeX like:
 *   \frac{3}{4}         → keep as-is (backend handles it)
 *   \dfrac{3}{4}        → convert to \frac{3}{4}
 *   5^{2}               → 5^2
 *   \sqrt{16}           → sqrt(16)
 *   \log_{2}\left(8\right) → log_2(8)
 *   \ln\left(x\right)   → ln(x)
 *   \cdot               → *
 *   \times              → *
 *   \left( \right)      → ( )
 */

export function latexToPlain(latex: string): string {
  let s = latex.trim();

  // If it's already plain text (no LaTeX constructs), return as-is
  if (!s.includes("\\") && !s.includes("^{") && !s.includes("_{")) return s;

  // Convert \dfrac to \frac (backend handles \frac)
  s = s.replace(/\\dfrac/g, "\\frac");

  // Strip \left and \right delimiters
  s = s.replace(/\\left\s*/g, "");
  s = s.replace(/\\right\s*/g, "");

  // Convert \cdot and \times to *
  s = s.replace(/\\cdot/g, "*");
  s = s.replace(/\\times/g, "*");

  // Convert \sqrt{...} to sqrt(...)
  s = s.replace(/\\sqrt\{([^}]+)\}/g, "sqrt($1)");

  // Convert \ln to ln
  s = s.replace(/\\ln/g, "ln");

  // Convert \log_{base}(...) to log_base(...)
  s = s.replace(/\\log_\{([^}]+)\}/g, "log_$1");
  s = s.replace(/\\log/g, "log");

  // Convert \sum_{...}^{...} to sum notation
  s = s.replace(/\\sum_\{([^}]+)\}\^\{([^}]+)\}/g, "sum_{$1}^{$2}");
  s = s.replace(/\\sum/g, "sum");

  // Remove braces around exponents: x^{2} → x^2, x^{15} → x^15
  s = s.replace(/\^\{([^}]+)\}/g, "^$1");

  // Remove parentheses around numeric exponents: x^(15) → x^15
  s = s.replace(/\^\((\d+)\)/g, "^$1");

  // Remove braces around subscripts: x_{1} → x_1
  s = s.replace(/_\{([^}]+)\}/g, "_$1");

  // Strip remaining LaTeX formatting commands that might slip through
  s = s.replace(/\\,/g, "");     // thin space
  s = s.replace(/\\;/g, "");     // medium space
  s = s.replace(/\\!/g, "");     // negative thin space
  s = s.replace(/\\ /g, " ");    // explicit space
  s = s.replace(/\\text\{([^}]*)\}/g, "$1"); // \text{...}

  // Remove unnecessary spaces
  s = s.replace(/\s+/g, " ").trim();

  return s;
}
