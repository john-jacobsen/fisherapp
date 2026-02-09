import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import MasteryGrid from "./MasteryGrid";
import type { TopicProgress } from "../types/api";

const mockTopics: TopicProgress[] = [
  {
    topic_id: "fraction_arithmetic",
    mastery: "mastered",
    difficulty: 4,
    accuracy: 0.92,
    attempts: 25,
    sessions: 3,
    ease_factor: 2.5,
    next_review: "2026-03-01",
  },
  {
    topic_id: "exponent_rules",
    mastery: "in_progress",
    difficulty: 2,
    accuracy: 0.65,
    attempts: 10,
    sessions: 2,
    ease_factor: 2.3,
    next_review: "2026-02-15",
  },
  {
    topic_id: "combinatorics",
    mastery: "not_started",
    difficulty: 1,
    accuracy: null,
    attempts: 0,
    sessions: 0,
    ease_factor: 2.5,
    next_review: "2026-02-10",
  },
];

describe("MasteryGrid", () => {
  it("renders a card for each topic", () => {
    render(<MasteryGrid topics={mockTopics} />);
    expect(screen.getByText("Fraction Arithmetic")).toBeInTheDocument();
    expect(screen.getByText("Exponent Rules")).toBeInTheDocument();
    expect(screen.getByText("Combinatorics")).toBeInTheDocument();
  });

  it("shows mastery status labels", () => {
    render(<MasteryGrid topics={mockTopics} />);
    expect(screen.getByText("Mastered")).toBeInTheDocument();
    expect(screen.getByText("In Progress")).toBeInTheDocument();
    expect(screen.getByText("Not Started")).toBeInTheDocument();
  });

  it("shows accuracy for non-started topics as missing", () => {
    render(<MasteryGrid topics={mockTopics} />);
    // Mastered topic shows 92%
    expect(screen.getByText("92%")).toBeInTheDocument();
    // In-progress topic shows 65%
    expect(screen.getByText("65%")).toBeInTheDocument();
  });

  it("shows attempt count for active topics", () => {
    render(<MasteryGrid topics={mockTopics} />);
    expect(screen.getByText("25")).toBeInTheDocument();
    expect(screen.getByText("10")).toBeInTheDocument();
  });

  it("renders empty grid without error", () => {
    const { container } = render(<MasteryGrid topics={[]} />);
    expect(container.firstChild).toBeInTheDocument();
  });
});
