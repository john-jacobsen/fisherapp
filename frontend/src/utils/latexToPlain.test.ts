import { describe, it, expect } from "vitest";
import { latexToPlain } from "./latexToPlain";

describe("latexToPlain", () => {
  it("passes through plain text unchanged", () => {
    expect(latexToPlain("3/4")).toBe("3/4");
    expect(latexToPlain("42")).toBe("42");
    expect(latexToPlain("a")).toBe("a");
    expect(latexToPlain("-5")).toBe("-5");
    expect(latexToPlain("0.75")).toBe("0.75");
  });

  it("keeps \\frac as-is (backend handles it)", () => {
    expect(latexToPlain("\\frac{3}{4}")).toBe("\\frac{3}{4}");
    expect(latexToPlain("\\frac{-2}{5}")).toBe("\\frac{-2}{5}");
  });

  it("converts \\dfrac to \\frac", () => {
    expect(latexToPlain("\\dfrac{3}{4}")).toBe("\\frac{3}{4}");
  });

  it("strips \\left and \\right", () => {
    expect(latexToPlain("\\left(x+1\\right)")).toBe("(x+1)");
  });

  it("converts \\cdot and \\times to *", () => {
    expect(latexToPlain("2\\cdot 3")).toBe("2* 3");
    expect(latexToPlain("2\\times 3")).toBe("2* 3");
  });

  it("converts \\sqrt{} to sqrt()", () => {
    expect(latexToPlain("\\sqrt{16}")).toBe("sqrt(16)");
    expect(latexToPlain("\\sqrt{x+1}")).toBe("sqrt(x+1)");
  });

  it("converts \\ln to ln", () => {
    expect(latexToPlain("\\ln x")).toBe("ln x");
  });

  it("converts \\log with subscript", () => {
    expect(latexToPlain("\\log_{2}")).toBe("log_2");
    expect(latexToPlain("\\log_{10}\\left(x\\right)")).toBe("log_10(x)");
  });

  it("simplifies exponent braces", () => {
    expect(latexToPlain("x^{2}")).toBe("x^2");
    expect(latexToPlain("x^{n+1}")).toBe("x^n+1");
  });

  it("simplifies subscript braces", () => {
    expect(latexToPlain("x_{1}")).toBe("x_1");
  });

  it("strips LaTeX spacing commands", () => {
    expect(latexToPlain("3\\,000")).toBe("3000");
    expect(latexToPlain("a\\;b")).toBe("ab");
  });

  it("handles \\text{}", () => {
    expect(latexToPlain("\\text{hello}")).toBe("hello");
  });

  it("handles summation notation", () => {
    expect(latexToPlain("\\sum_{i=1}^{n}i")).toBe("sum_i=1^ni");
  });

  it("handles negative fractions from MathLive", () => {
    expect(latexToPlain("-\\frac{3}{4}")).toBe("-\\frac{3}{4}");
  });

  it("handles empty and whitespace input", () => {
    expect(latexToPlain("")).toBe("");
    expect(latexToPlain("   ")).toBe("");
  });
});
