import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ProblemCard from "./ProblemCard";

describe("ProblemCard", () => {
  it("displays the topic label", () => {
    render(
      <ProblemCard
        topicId="fraction_arithmetic"
        difficulty={2}
        statement="Compute 1 + 1"
      />
    );
    expect(screen.getByText("Fraction Arithmetic")).toBeInTheDocument();
  });

  it("displays the difficulty label and level", () => {
    render(
      <ProblemCard
        topicId="exponent_rules"
        difficulty={3}
        statement="Simplify x^2"
      />
    );
    expect(screen.getByText("Multi-step (Lv. 3)")).toBeInTheDocument();
  });

  it("renders the problem statement", () => {
    render(
      <ProblemCard
        topicId="combinatorics"
        difficulty={1}
        statement="What is 5 factorial?"
      />
    );
    expect(screen.getByText("What is 5 factorial?")).toBeInTheDocument();
  });

  it("falls back to topic_id when label not found", () => {
    render(
      <ProblemCard
        topicId="unknown_topic"
        difficulty={1}
        statement="Test"
      />
    );
    expect(screen.getByText("unknown_topic")).toBeInTheDocument();
  });

  it("falls back to Level N for unknown difficulty", () => {
    render(
      <ProblemCard
        topicId="fraction_arithmetic"
        difficulty={9}
        statement="Test"
      />
    );
    expect(screen.getByText("Level 9 (Lv. 9)")).toBeInTheDocument();
  });
});
