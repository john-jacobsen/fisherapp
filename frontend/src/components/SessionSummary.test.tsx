import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import SessionSummary from "./SessionSummary";
import type { SessionEndResponse } from "../types/api";

const mockSummary: SessionEndResponse = {
  session_id: "test-session-123",
  ended_at: "2026-02-08T12:00:00Z",
  problems_served: 10,
  problems_correct: 7,
};

describe("SessionSummary", () => {
  it("displays 'Session Complete' heading", () => {
    render(
      <SessionSummary summary={mockSummary} onDashboard={() => {}} onNewSession={() => {}} />
    );
    expect(screen.getByText("Session Complete")).toBeInTheDocument();
  });

  it("shows problems count", () => {
    render(
      <SessionSummary summary={mockSummary} onDashboard={() => {}} onNewSession={() => {}} />
    );
    expect(screen.getByText("10")).toBeInTheDocument();
    expect(screen.getByText("Problems")).toBeInTheDocument();
  });

  it("shows correct count", () => {
    render(
      <SessionSummary summary={mockSummary} onDashboard={() => {}} onNewSession={() => {}} />
    );
    expect(screen.getByText("7")).toBeInTheDocument();
    expect(screen.getByText("Correct")).toBeInTheDocument();
  });

  it("calculates and displays accuracy", () => {
    render(
      <SessionSummary summary={mockSummary} onDashboard={() => {}} onNewSession={() => {}} />
    );
    expect(screen.getByText("70%")).toBeInTheDocument();
  });

  it("calls onNewSession when Practice More clicked", async () => {
    const user = userEvent.setup();
    const handleNew = vi.fn();
    render(
      <SessionSummary summary={mockSummary} onDashboard={() => {}} onNewSession={handleNew} />
    );
    await user.click(screen.getByRole("button", { name: /practice more/i }));
    expect(handleNew).toHaveBeenCalledOnce();
  });

  it("calls onDashboard when Dashboard clicked", async () => {
    const user = userEvent.setup();
    const handleDash = vi.fn();
    render(
      <SessionSummary summary={mockSummary} onDashboard={handleDash} onNewSession={() => {}} />
    );
    await user.click(screen.getByRole("button", { name: /dashboard/i }));
    expect(handleDash).toHaveBeenCalledOnce();
  });

  it("handles zero problems gracefully", () => {
    const emptySummary: SessionEndResponse = {
      ...mockSummary,
      problems_served: 0,
      problems_correct: 0,
    };
    render(
      <SessionSummary summary={emptySummary} onDashboard={() => {}} onNewSession={() => {}} />
    );
    expect(screen.getByText("0%")).toBeInTheDocument();
  });
});
