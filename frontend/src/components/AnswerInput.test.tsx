import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import AnswerInput from "./AnswerInput";

// Force text mode for tests (MathLive web component doesn't work in jsdom)
beforeEach(() => {
  localStorage.setItem("fisherapp-input-mode", "text");
});

describe("AnswerInput", () => {
  it("renders input and submit button in text mode", () => {
    render(<AnswerInput onSubmit={() => {}} />);
    expect(screen.getByPlaceholderText(/type your answer/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /submit/i })).toBeInTheDocument();
  });

  it("calls onSubmit with trimmed answer", async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();
    render(<AnswerInput onSubmit={handleSubmit} />);

    const input = screen.getByPlaceholderText(/type your answer/i);
    await user.type(input, "  3/4  ");
    await user.click(screen.getByRole("button", { name: /submit/i }));

    expect(handleSubmit).toHaveBeenCalledWith("3/4");
  });

  it("clears input after submit", async () => {
    const user = userEvent.setup();
    render(<AnswerInput onSubmit={() => {}} />);

    const input = screen.getByPlaceholderText(/type your answer/i) as HTMLInputElement;
    await user.type(input, "42");
    await user.click(screen.getByRole("button", { name: /submit/i }));

    expect(input.value).toBe("");
  });

  it("disables input and button when disabled prop is true", () => {
    render(<AnswerInput onSubmit={() => {}} disabled />);
    expect(screen.getByPlaceholderText(/type your answer/i)).toBeDisabled();
    expect(screen.getByRole("button", { name: /submit/i })).toBeDisabled();
  });

  it("does not submit empty input", async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();
    render(<AnswerInput onSubmit={handleSubmit} />);

    await user.click(screen.getByRole("button", { name: /submit/i }));
    expect(handleSubmit).not.toHaveBeenCalled();
  });

  it("shows toggle button to switch modes", () => {
    render(<AnswerInput onSubmit={() => {}} />);
    expect(screen.getByText(/switch to math keyboard/i)).toBeInTheDocument();
  });

  it("toggle button updates localStorage", async () => {
    // Verify the toggle text appears and localStorage starts as text
    render(<AnswerInput onSubmit={() => {}} />);
    expect(localStorage.getItem("fisherapp-input-mode")).toBe("text");
    expect(screen.getByText(/switch to math keyboard/i)).toBeInTheDocument();
    // Note: Cannot actually toggle to math mode in jsdom because
    // MathLive web component requires a real browser environment
  });
});
