import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import AnswerInput from "./AnswerInput";

describe("AnswerInput", () => {
  it("renders input and submit button", () => {
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
});
