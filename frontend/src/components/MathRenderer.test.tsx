import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import MathRenderer from "./MathRenderer";

describe("MathRenderer", () => {
  it("renders plain text without modification", () => {
    render(<MathRenderer text="Hello world" />);
    expect(screen.getByText("Hello world")).toBeInTheDocument();
  });

  it("renders empty string without error", () => {
    const { container } = render(<MathRenderer text="" />);
    expect(container.querySelector("span")).toBeInTheDocument();
  });

  it("renders LaTeX commands as math (no delimiters)", () => {
    const { container } = render(<MathRenderer text="\\frac{3}{4}" />);
    // KaTeX wraps output in katex class spans
    expect(container.querySelector(".katex")).toBeInTheDocument();
  });

  it("renders inline math with $ delimiters", () => {
    const { container } = render(<MathRenderer text="Compute $\\frac{1}{2}$ please" />);
    expect(container.querySelector(".katex")).toBeInTheDocument();
    expect(container.innerHTML).toContain("Compute");
  });

  it("renders display math with $$ delimiters", () => {
    const { container } = render(<MathRenderer text="$$\\sum_{i=1}^{n} i$$" />);
    expect(container.querySelector(".katex-display")).toBeInTheDocument();
  });

  it("handles mixed text and math", () => {
    const { container } = render(<MathRenderer text="Solve $x + 1 = 3$ for x." />);
    expect(container.querySelector(".katex")).toBeInTheDocument();
    expect(container.innerHTML).toContain("Solve");
    expect(container.innerHTML).toContain("for x.");
  });

  it("applies className prop", () => {
    const { container } = render(<MathRenderer text="test" className="my-class" />);
    expect(container.querySelector("span.my-class")).toBeInTheDocument();
  });

  it("converts single newline to <br> tag", () => {
    const { container } = render(<MathRenderer text={"line1\nline2"} />);
    expect(container.innerHTML).toContain("<br>");
  });

  it("converts double newline to two <br> tags", () => {
    const { container } = render(<MathRenderer text={"paragraph1\n\nparagraph2"} />);
    expect(container.innerHTML).toContain("<br><br>");
  });

  it("converts newlines between multiple-choice options", () => {
    const { container } = render(
      <MathRenderer text={"Which is correct?\n\n(a) option one\n(b) option two\n(c) option three"} />
    );
    // Each option should be on its own line (separated by <br>)
    expect(container.innerHTML).toContain("<br>");
    expect(container.innerHTML).toContain("(a) option one");
    expect(container.innerHTML).toContain("(b) option two");
  });
});
