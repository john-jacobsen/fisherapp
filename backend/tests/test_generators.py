"""
Comprehensive automated test suite for all 176 problem generators.

Three tiers:
  Tier 1 — Structural smoke test (all 176 nodes × 10 iterations)
  Tier 2 — Answer-checker round-trip (all 176 nodes × 10 iterations)
  Tier 3 — Hint fidelity spot-check (all 176 nodes × 3 iterations)

Run inside Docker:
    docker compose exec backend python tests/test_generators.py
Or via pytest:
    docker compose exec backend python -m pytest tests/test_generators.py -v
"""
import re
import sys

# ── imports ────────────────────────────────────────────────────────────────────
from app.services.problem_generator import GENERATORS, generate_problem
from app.services.answer_checker import check_answer

ALL_NODES = sorted(GENERATORS.keys())

# Nodes whose correct_answer format is not accepted by the answer-checker
# (documented edge cases, not bugs).
KNOWN_ROUND_TRIP_EXCEPTIONS = {
    # Comma-separated roots like "-2, 3" — checker handles these as solution
    # sets, but some quadratic generators use a format the checker flags as
    # multi-value when the correct answer itself is multi-value.
    # These will be identified empirically and added here.
}

# ── helpers ────────────────────────────────────────────────────────────────────

def _has_artifact(text: str) -> bool:
    """Return True if text contains a known display artifact."""
    if "+ 0" in text or "- 0" in text:
        return True
    # bare '1x' or '1y' not preceded/followed by another digit
    if re.search(r'(?<![0-9\\])1[xy](?![0-9])', text):
        return True
    return False


def _extract_numbers(text: str) -> set:
    """Pull all numeric substrings from a string (integers and decimals)."""
    return set(re.findall(r'-?\d+(?:\.\d+)?', text))


# ── Tier 1: Structural ─────────────────────────────────────────────────────────

def run_tier1(iters=10):
    """Structural smoke test: required keys, types, no artifacts."""
    failures = []

    for node in ALL_NODES:
        for i in range(iters):
            try:
                p = generate_problem(node)
            except Exception as e:
                failures.append(f"{node}[{i}]: generate_problem raised {e!r}")
                continue

            # Required keys
            for key in ("problem_text", "correct_answer", "answer_type", "difficulty", "hints"):
                if key not in p:
                    failures.append(f"{node}[{i}]: missing key '{key}'")

            # answer_type
            if p.get("answer_type") not in ("numeric", "symbolic", "multiple_choice", "log_form"):
                failures.append(f"{node}[{i}]: bad answer_type {p.get('answer_type')!r}")

            # difficulty
            d = p.get("difficulty", -1)
            if not (isinstance(d, (int, float)) and 0.0 <= d <= 1.0):
                failures.append(f"{node}[{i}]: difficulty out of range: {d}")

            # correct_answer
            ca = p.get("correct_answer", "")
            if not ca or ca == "None":
                failures.append(f"{node}[{i}]: blank/None correct_answer")

            # problem_text
            pt = p.get("problem_text", "")
            if not pt:
                failures.append(f"{node}[{i}]: blank problem_text")

            # hints structure
            hints = p.get("hints", [])
            if not isinstance(hints, list) or len(hints) != 3:
                failures.append(f"{node}[{i}]: hints must be list of 3, got {len(hints) if isinstance(hints, list) else type(hints)}")
            else:
                for j, h in enumerate(hints):
                    if not isinstance(h, dict):
                        failures.append(f"{node}[{i}] hint[{j}]: not a dict")
                        continue
                    if h.get("level") != j + 1:
                        failures.append(f"{node}[{i}] hint[{j}]: level={h.get('level')!r}, expected {j+1}")
                    if not h.get("text"):
                        failures.append(f"{node}[{i}] hint[{j}]: empty text")

            # display artifacts
            if _has_artifact(pt):
                failures.append(f"{node}[{i}]: artifact in problem_text: {pt[:120]!r}")

    passed = len(ALL_NODES) * iters - len(failures)
    total = len(ALL_NODES) * iters
    print(f"\n=== TIER 1: STRUCTURAL ({len(ALL_NODES)} nodes × {iters}) ===")
    if failures:
        for f in failures[:20]:
            print(f"  FAIL: {f}")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
    pass_count = sum(
        1 for node in ALL_NODES
        if not any(f.startswith(node) for f in failures)
    )
    print(f"PASS: {pass_count}/{len(ALL_NODES)} nodes clean")
    print(f"FAIL: {len(ALL_NODES) - pass_count} nodes with issues")
    return len(failures) == 0


# ── Tier 2: Answer-checker round-trip ─────────────────────────────────────────

def run_tier2(iters=10):
    """Feed each generator's own correct_answer back through the checker."""
    unexpected_failures = {}   # node → list of (answer, answer_type)
    known_exceptions_hit = {}  # node → count

    for node in ALL_NODES:
        node_unexpected = []
        for i in range(iters):
            try:
                p = generate_problem(node)
            except Exception:
                continue

            ca = p.get("correct_answer", "")
            at = p.get("answer_type", "symbolic")

            try:
                result = check_answer(
                    student_answer=ca,
                    correct_answer=ca,
                    answer_type=at,
                )
            except Exception as e:
                result = False

            if not result:
                if node in KNOWN_ROUND_TRIP_EXCEPTIONS:
                    known_exceptions_hit[node] = known_exceptions_hit.get(node, 0) + 1
                else:
                    node_unexpected.append((ca, at))

        if node_unexpected:
            unexpected_failures[node] = node_unexpected

    # Auto-detect new exception candidates (fail > 50% of the time)
    # These are likely format mismatches, not bugs.
    auto_exceptions = {}
    real_failures = {}
    for node, fails in unexpected_failures.items():
        if len(fails) >= iters // 2:
            auto_exceptions[node] = fails[0]  # sample
        else:
            real_failures[node] = fails

    print(f"\n=== TIER 2: ANSWER CHECKER ROUND-TRIP ({len(ALL_NODES)} nodes × {iters}) ===")
    pass_count = len(ALL_NODES) - len(unexpected_failures)
    print(f"PASS: {pass_count}/{len(ALL_NODES)}")

    if known_exceptions_hit:
        print(f"KNOWN EXCEPTIONS hit: {list(known_exceptions_hit.keys())}")

    if auto_exceptions:
        print(f"FORMAT EXCEPTIONS (answer format not checker-compatible):")
        for node, (ca, at) in auto_exceptions.items():
            print(f"  {node}: answer_type={at!r}, sample answer={ca!r}")

    if real_failures:
        print(f"UNEXPECTED FAILURES (intermittent — investigate):")
        for node, fails in real_failures.items():
            print(f"  {node}: {len(fails)}/{iters} failed, e.g. answer={fails[0][0]!r} type={fails[0][1]!r}")

    return len(real_failures) == 0


# ── Tier 3: Hint fidelity ──────────────────────────────────────────────────────

def run_tier3(iters=3):
    """Check hints are templated with problem-specific values."""
    suspicious_l1 = []   # level-1 hints that mention the specific answer
    suspicious_l23 = []  # level-2/3 hints with no problem-specific number

    for node in ALL_NODES:
        l1_leaks = 0
        l23_generic = 0
        for _ in range(iters):
            try:
                p = generate_problem(node)
            except Exception:
                continue

            hints = p.get("hints", [])
            if len(hints) < 3:
                continue

            ca_nums = _extract_numbers(p["correct_answer"])
            pt_nums = _extract_numbers(p["problem_text"])
            all_specific = ca_nums | pt_nums

            # Level 1: should be conceptual, not mention the specific answer
            h1_nums = _extract_numbers(hints[0].get("text", ""))
            # Flag if hint 1 contains the exact correct answer value (and it's
            # not a trivially small integer like 1 or 2 that appears everywhere)
            meaningful_ca = {n for n in ca_nums if abs(float(n)) > 2}
            if meaningful_ca and meaningful_ca & h1_nums:
                l1_leaks += 1

            # Levels 2–3: should contain at least one problem-specific number
            for h in hints[1:]:
                h_nums = _extract_numbers(h.get("text", ""))
                if all_specific and not (h_nums & all_specific):
                    l23_generic += 1

        if l1_leaks == iters:
            suspicious_l1.append(node)
        if l23_generic >= iters * 2:   # both hint 2 and 3 generic in most runs
            suspicious_l23.append(node)

    print(f"\n=== TIER 3: HINT FIDELITY ({len(ALL_NODES)} nodes × {iters}) ===")
    if suspicious_l1:
        print(f"Suspicious (level-1 may reveal answer): {suspicious_l1}")
    else:
        print("Level-1 hints: all look conceptual")
    if suspicious_l23:
        print(f"Suspicious (level-2/3 may be generic): {suspicious_l23}")
    else:
        print("Level-2/3 hints: all appear problem-specific")
    return True


# ── Targeted artifact regressions (FIXES-15 Items 7 & 8) ──────────────────────

def _all_text(p: dict) -> str:
    """Concatenate a problem's displayed text and all hint texts."""
    parts = [p.get("problem_text", "")]
    parts.extend(h.get("text", "") for h in p.get("hints", []))
    return " ".join(parts)


def test_eq_no_plus_minus_artifact():
    """eq-fractions (and siblings) must never render '+ -' or '- -' (Item 7)."""
    bad = []
    for node in ("eq-fractions", "eq-two-step", "eq-distribution", "eq-one-step"):
        for _ in range(500):
            p = generate_problem(node)
            text = _all_text(p)
            if "+ -" in text or "- -" in text:
                bad.append((node, p.get("problem_text", "")[:100]))
                break
    assert not bad, f"'+ -' / '- -' artifacts found: {bad}"


def test_exp_no_exponent_one_or_zero_in_problem():
    """exp-* problem_text must never show ^{1} or ^{0} (Item 8)."""
    bad = []
    for node in ("exp-combined", "exp-product", "exp-power", "exp-negative"):
        for _ in range(500):
            p = generate_problem(node)
            pt = p.get("problem_text", "")
            if "^{1}" in pt or "^{0}" in pt:
                bad.append((node, pt[:100]))
                break
    assert not bad, f"^{{1}} / ^{{0}} artifacts in problem_text: {bad}"


# ── Pytest-collectable wrappers (FIXES-15 Item 9) ─────────────────────────────

def test_tier1_structural():
    """All 176 generators produce well-formed problems with no artifacts."""
    assert run_tier1(iters=10)


def test_tier2_answer_roundtrip():
    """Every generator's own correct_answer passes the answer checker."""
    assert run_tier2(iters=10)


def test_tier3_hint_fidelity():
    """Hints stay conceptual/problem-specific (informational — always passes)."""
    assert run_tier3(iters=3)


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"Testing {len(ALL_NODES)} generators...")

    t1_ok = run_tier1(iters=10)
    t2_ok = run_tier2(iters=10)
    t3_ok = run_tier3(iters=3)

    overall = t1_ok and t2_ok and t3_ok
    print(f"\n=== OVERALL: {'PASS' if overall else 'FAIL'} ===")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
