#!/usr/bin/env python
"""
Validation harness for walkthrough templates.

For every backend/data/walkthroughs/*.json this checks that:
  1. The template has the required schema (keys, sequential steps, valid
     input_type / strict_form.type, well-formed multiple_choice).
  2. A matching generator exists and returns a dict.
  3. Hydrating 25 times leaves NO unresolved variable placeholders, every
     numeric/expression correct_answer passes the answer checker, every
     strict_form correct answer passes its own form check (and a known-bad
     probe fails it), and all multiple_choice options are unique.

Run standalone:
    python scripts/validate_walkthroughs.py
Exits nonzero if any template fails. Also importable via validate_all().
"""
import json
import os
import re
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_backend = os.path.join(_here, "..")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from app.services.walkthrough_generator import (
    generate_walkthrough,
    _load_generator,
    find_unresolved_placeholders,
)
from app.routers.walkthrough import _check_answer, _check_strict_form

WALKTHROUGHS_DIR = os.path.join(_backend, "data", "walkthroughs")

VALID_INPUT_TYPES = {"multiple_choice", "numeric", "expression", "dropdown"}
VALID_STRICT_FORM_TYPES = {
    "simplified_fraction", "log_form", "factored_form",
    "expanded_form", "exact_form", "custom_regex",
}
HYDRATION_RUNS = 25


class ValidationError(Exception):
    pass


def _schema_check(template: dict) -> None:
    for key in ("node_id", "title", "intro", "steps"):
        if key not in template:
            raise ValidationError(f"missing top-level key '{key}'")

    # Optional intro.video_id: a YouTube ID string shown above the intro body.
    # Unset in the six pilot templates; populated in FIXES-17. When present it
    # must be a non-empty string (an int/list/etc. would break the iframe embed).
    intro = template.get("intro")
    if isinstance(intro, dict) and "video_id" in intro:
        vid = intro["video_id"]
        if not isinstance(vid, str) or not vid.strip():
            raise ValidationError(
                f"intro.video_id must be a non-empty string, got {vid!r}"
            )

    steps = template["steps"]
    if not isinstance(steps, list) or not steps:
        raise ValidationError("'steps' must be a non-empty list")

    for i, step in enumerate(steps, start=1):
        for key in ("step_number", "prompt", "input_type", "correct_answer"):
            if key not in step:
                raise ValidationError(f"step {i}: missing key '{key}'")
        if step["step_number"] != i:
            raise ValidationError(
                f"step at position {i} has step_number {step['step_number']} "
                f"(steps must be sequential from 1)"
            )
        input_type = step["input_type"]
        if input_type not in VALID_INPUT_TYPES:
            raise ValidationError(f"step {i}: invalid input_type '{input_type}'")

        if input_type in ("multiple_choice", "dropdown"):
            options = step.get("options")
            if not isinstance(options, list) or len(options) < 2:
                raise ValidationError(f"step {i}: needs >= 2 options")
            if input_type == "multiple_choice":
                raw_correct = str(step["correct_answer"])
                # correct_answer may be a placeholder (e.g. "{z_star_index}")
                # that hydrates to an int — defer that check to hydration.
                if "{" not in raw_correct:
                    try:
                        idx = int(raw_correct)
                    except (ValueError, TypeError):
                        raise ValidationError(
                            f"step {i}: correct_answer must be an integer index"
                        )
                    if not (0 <= idx < len(options)):
                        raise ValidationError(
                            f"step {i}: correct_answer index {idx} out of range"
                        )

        strict_form = step.get("strict_form")
        if strict_form:
            sf_type = strict_form.get("type")
            if sf_type not in VALID_STRICT_FORM_TYPES:
                raise ValidationError(f"step {i}: invalid strict_form.type '{sf_type}'")


def _decimal_probe_for_fraction(correct: str):
    """Return the decimal string of a hydrated fraction correct answer, or None."""
    m = re.match(r'^\\frac\{(-?\d+)\}\{(-?\d+)\}$', correct.strip())
    if not m:
        m = re.match(r'^(-?\d+)\s*/\s*(-?\d+)$', correct.strip())
    if not m:
        return None
    n, d = int(m.group(1)), int(m.group(2))
    if d == 0:
        return None
    return f"{n / d:.6f}".rstrip("0").rstrip(".")


def _hydration_checks(node_id: str, run_idx: int) -> None:
    hydrated = generate_walkthrough(node_id)
    if hydrated is None:
        raise ValidationError("generate_walkthrough returned None")

    variables = hydrated.get("variables", {})

    # 1. No unresolved variable placeholders anywhere.
    unresolved = find_unresolved_placeholders(hydrated, variables)
    if unresolved:
        raise ValidationError(
            f"run {run_idx}: unresolved placeholders {sorted(set(unresolved))}"
        )

    for step in hydrated.get("steps", []):
        n = step["step_number"]
        input_type = step["input_type"]
        correct = str(step["correct_answer"])

        # 2. numeric / expression correct answers self-check.
        if input_type in ("numeric", "expression"):
            if not _check_answer(correct, correct, input_type):
                raise ValidationError(
                    f"run {run_idx} step {n}: correct_answer {correct!r} "
                    f"does not pass the {input_type} checker"
                )

        # 3. strict_form: correct passes, known-bad probe fails.
        strict_form = step.get("strict_form")
        if strict_form and input_type in ("numeric", "expression"):
            ok, _ = _check_strict_form(correct, strict_form)
            if not ok:
                raise ValidationError(
                    f"run {run_idx} step {n}: correct_answer {correct!r} "
                    f"fails its own strict_form {strict_form.get('type')}"
                )
            sf_type = strict_form.get("type")
            probe = None
            if sf_type == "simplified_fraction":
                probe = _decimal_probe_for_fraction(correct)
            elif sf_type == "exact_form":
                probe = re.sub(r'(\d+)', lambda mm: mm.group(1) + ".0", correct, count=1)
                if "." not in probe:
                    probe = None
            elif sf_type == "log_form":
                probe = "42"
            # factored_form / expanded_form / custom_regex: no generic probe.
            if probe is not None and probe != correct:
                bad_ok, _ = _check_strict_form(probe, strict_form)
                if bad_ok:
                    raise ValidationError(
                        f"run {run_idx} step {n}: bad probe {probe!r} wrongly "
                        f"PASSED strict_form {sf_type}"
                    )

        # 4. multiple_choice: options unique and correct_answer is a valid index.
        if input_type == "multiple_choice":
            options = step.get("options", [])
            if len(set(options)) != len(options):
                dupes = [o for o in options if options.count(o) > 1]
                raise ValidationError(
                    f"run {run_idx} step {n}: duplicate MC options {sorted(set(dupes))}"
                )
            try:
                idx = int(correct)
            except (ValueError, TypeError):
                raise ValidationError(
                    f"run {run_idx} step {n}: hydrated correct_answer {correct!r} "
                    f"is not an integer index"
                )
            if not (0 <= idx < len(options)):
                raise ValidationError(
                    f"run {run_idx} step {n}: correct index {idx} out of range "
                    f"(len={len(options)})"
                )


def validate_node(node_id: str) -> tuple:
    """Return (passed: bool, message: str) for one template."""
    path = os.path.join(WALKTHROUGHS_DIR, f"{node_id}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            template = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"could not load template: {exc}"

    try:
        _schema_check(template)
    except ValidationError as exc:
        return False, f"schema: {exc}"

    if _load_generator(node_id) is None:
        return False, "no generator found"

    try:
        for run_idx in range(1, HYDRATION_RUNS + 1):
            _hydration_checks(node_id, run_idx)
    except ValidationError as exc:
        return False, str(exc)
    except Exception as exc:  # generator/hydration crash
        return False, f"hydration raised {type(exc).__name__}: {exc}"

    return True, f"ok ({HYDRATION_RUNS} hydrations)"


def validate_all() -> tuple:
    """Validate every template. Return (all_passed: bool, rows: list[(node, ok, msg)])."""
    node_ids = sorted(
        os.path.splitext(f)[0]
        for f in os.listdir(WALKTHROUGHS_DIR)
        if f.endswith(".json")
    )
    rows = []
    all_passed = True
    for node_id in node_ids:
        ok, msg = validate_node(node_id)
        rows.append((node_id, ok, msg))
        if not ok:
            all_passed = False
    return all_passed, rows


def main() -> int:
    all_passed, rows = validate_all()
    width = max((len(n) for n, _, _ in rows), default=10)
    print(f"\nWalkthrough validation ({len(rows)} templates)\n")
    for node_id, ok, msg in rows:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {node_id.ljust(width)}  {msg}")
    print()
    if all_passed:
        print(f"All {len(rows)} templates passed.")
        return 0
    n_fail = sum(1 for _, ok, _ in rows if not ok)
    print(f"{n_fail} of {len(rows)} templates FAILED.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
