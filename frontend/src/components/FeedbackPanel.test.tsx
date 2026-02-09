import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import FeedbackPanel from "./FeedbackPanel";
import type { AnswerResult } from "../types/api";

const correctResult: AnswerResult = {
  correct: true,
  correct_answer: "42",
  solution_steps: ["Step 1: Compute 40 + 2", "Step 2: Result is 42"],
  mastery_changed: false,
  new_mastery: null,
  topic_id: "fraction_arithmetic",
  difficulty: 2,
};

const incorrectResult: AnswerResult = {
  correct: false,
  correct_answer: "\\frac{3}{4}",
  solution_steps: ["Step 1: Find common denominator", "Step 2: Simplify"],
  mastery_changed: false,
  new_mastery: null,
  topic_id: "fraction_arithmetic",
  difficulty: 2,
};

describe("FeedbackPanel", () => {
  it("shows 'Correct!' for correct answers", () => {
    render(<FeedbackPanel result={correctResult} onNext={() => {}} />);
    expect(screen.getByText("Correct!")).toBeInTheDocument();
  });

  it("shows 'Incorrect' for wrong answers", () => {
    render(<FeedbackPanel result={incorrectResult} onNext={() => {}} />);
    expect(screen.getByText("Incorrect")).toBeInTheDocument();
  });

  it("shows correct answer when incorrect", () => {
    render(<FeedbackPanel result={incorrectResult} onNext={() => {}} />);
    expect(screen.getByText("Correct answer:")).toBeInTheDocument();
  });

  it("renders solution steps", () => {
    render(<FeedbackPanel result={incorrectResult} onNext={() => {}} />);
    expect(screen.getByText("Solution:")).toBeInTheDocument();
  });

  it("shows Next Problem button", async () => {
    const user = userEvent.setup();
    const handleNext = vi.fn();
    render(<FeedbackPanel result={correctResult} onNext={handleNext} />);

    await user.click(screen.getByRole("button", { name: /next problem/i }));
    expect(handleNext).toHaveBeenCalledOnce();
  });

  it("shows mastery notification when topic mastered", () => {
    const masteredResult: AnswerResult = {
      ...correctResult,
      mastery_changed: true,
      new_mastery: "mastered",
      topic_id: "fraction_arithmetic",
    };
    render(<FeedbackPanel result={masteredResult} onNext={() => {}} />);
    expect(screen.getByText(/topic mastered/i)).toBeInTheDocument();
  });
});
