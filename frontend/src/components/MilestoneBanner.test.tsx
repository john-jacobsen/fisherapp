import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, test, expect, vi } from "vitest";
import MilestoneBanner from "./MilestoneBanner";

describe("MilestoneBanner", () => {
  test("renders the milestone count", () => {
    render(<MilestoneBanner milestone={100} onDismiss={() => {}} />);
    expect(screen.getByText(/100/)).toBeInTheDocument();
  });

  test("renders a placement test recommendation", () => {
    render(<MilestoneBanner milestone={200} onDismiss={() => {}} />);
    expect(screen.getByText(/placement test/i)).toBeInTheDocument();
  });

  test("calls onDismiss when dismiss button is clicked", async () => {
    const user = userEvent.setup();
    const onDismiss = vi.fn();
    render(<MilestoneBanner milestone={100} onDismiss={onDismiss} />);
    await user.click(screen.getByRole("button", { name: /dismiss/i }));
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });
});
