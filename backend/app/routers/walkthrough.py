import json
import logging
import os
import re
from math import gcd
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.routers.auth import get_current_user
from app.models.user import User
from app.services.walkthrough_generator import generate_walkthrough
from app.services.walkthrough_conditions import evaluate_condition, ConditionError
from app.services.answer_checker import check_answer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/walkthrough", tags=["walkthrough"])

_WALKTHROUGHS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "walkthroughs")


def _load_raw_template(node_id: str) -> Optional[dict]:
    path = os.path.join(_WALKTHROUGHS_DIR, f"{node_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/{node_id}")
def get_walkthrough(
    node_id: str,
    current_user: User = Depends(get_current_user),
):
    """Return a freshly generated (hydrated) walkthrough instance for the given node."""
    result = generate_walkthrough(node_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No walkthrough template for '{node_id}'")
    return result


class CheckStepRequest(BaseModel):
    step_number: int
    answer: str
    variables: dict  # The variables dict returned by GET (e.g. {"numerator": 18, ...})


@router.post("/{node_id}/check-step")
def check_step(
    node_id: str,
    body: CheckStepRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Validate a student's answer for a single walkthrough step.

    Flow:
      1. Check mathematical correctness.
      2. If correct AND the step has a strict_form, check the form.
         Return wrong-answer feedback if the form is rejected.
      3. If correct and form OK, return correct=True.
      4. If mathematically wrong, return wrong-answer feedback.

    The client passes back the 'variables' dict from GET so the backend
    can evaluate the correct answer without server-side sessions.
    """
    template = _load_raw_template(node_id)
    if template is None:
        raise HTTPException(status_code=404, detail=f"No walkthrough template for '{node_id}'")

    steps = template.get("steps", [])
    step = next((s for s in steps if s["step_number"] == body.step_number), None)
    if step is None:
        raise HTTPException(status_code=400, detail=f"Step {body.step_number} not found")

    # Hydrate the correct_answer template with the supplied variables
    variables_str = {k: str(v) for k, v in body.variables.items()}
    correct_answer = step["correct_answer"]
    for key, val in variables_str.items():
        correct_answer = correct_answer.replace('{' + key + '}', val)

    input_type = step.get("input_type", "numeric")

    # For multiple_choice, the client submits a *display* index into the shuffled
    # options. Translate it back to the *template* index (the order the raw JSON
    # lists options in) before comparing to the template's correct_answer and
    # before evaluating position-based feedback conditions ("answer == 2").
    # The order list is passed back by the client in `variables` (see
    # walkthrough_generator._shuffle_multiple_choice). Stateless by design —
    # tampering is possible but walkthroughs don't affect mastery.
    answer_for_check = body.answer
    if input_type == "multiple_choice":
        order = body.variables.get(f"_mc_order_{body.step_number}")
        if order:
            try:
                answer_for_check = str(order[int(body.answer)])
            except (ValueError, IndexError, TypeError):
                answer_for_check = body.answer  # malformed → falls through as wrong

    is_correct = _check_answer(answer_for_check, correct_answer, input_type)

    if is_correct:
        # Check strict_form if present on this step
        strict_form_raw = step.get("strict_form")
        if strict_form_raw and input_type in ("expression", "numeric"):
            # Hydrate any variable placeholders in the strict_form values
            strict_form = _hydrate_dict(strict_form_raw, variables_str)
            form_ok, form_feedback = _check_strict_form(body.answer, strict_form)
            if not form_ok:
                return {"correct": False, "feedback": form_feedback}
        return {"correct": True, "feedback": None}

    feedback_list = step.get("wrong_answer_feedback", [])
    feedback_text = _evaluate_feedback(feedback_list, answer_for_check, body.variables, variables_str)
    return {"correct": False, "feedback": feedback_text}


# ── Strict form checking ───────────────────────────────────────────────────────

def _hydrate_dict(d: dict, variables_str: dict) -> dict:
    """Replace {key} placeholders in all string values of a flat dict."""
    result = {}
    for k, v in d.items():
        if isinstance(v, str):
            for var, val in variables_str.items():
                v = v.replace('{' + var + '}', val)
        result[k] = v
    return result


def _check_strict_form(student: str, strict_form: dict) -> tuple:
    """
    Verify that a mathematically-correct answer is in the required form.

    Returns (True, "") if the form is acceptable.
    Returns (False, rejection_feedback) if the form is wrong.

    Supported types:
      simplified_fraction — GCD of numerator and denominator must be 1
      log_form            — answer must contain log/ln notation
      factored_form       — answer must have balanced parens with factor structure
      expanded_form       — answer must NOT look like a product of factor groups
      exact_form          — answer must not contain decimal points
      custom_regex        — answer must match the provided regex pattern
    """
    form_type = strict_form.get("type", "")
    rejection = strict_form.get(
        "rejection_feedback", "Please write your answer in the required form."
    )
    s = student.strip()

    if form_type == "simplified_fraction":
        # ALLOWLIST: the answer MUST match a fraction pattern. Anything else
        # (decimals like 0.75, bare integers, malformed input) is rejected as
        # wrong form — a decimal that happens to equal the fraction must not
        # slip through. Anchored patterns (^...$) prevent trailing garbage.
        m = re.match(r'^\\frac\{(-?\d+)\}\{(-?\d+)\}$', s)
        if not m:
            m = re.match(r'^(-?\d+)\s*/\s*(-?\d+)$', s)
        if not m:
            return False, rejection          # no fraction match = wrong form
        n, d = int(m.group(1)), int(m.group(2))
        g = gcd(abs(n), abs(d))
        if g > 1:
            return False, rejection
        return True, ""

    if form_type == "log_form":
        # Require log/ln as a token: a word boundary BEFORE the token (so a bare
        # backslash or string start qualifies, but a variable like "catalog" or
        # "kiln" does not). No boundary AFTER, so log_3, log2, \log_{2} all pass.
        if not re.search(r'\b(log|ln)', s):
            return False, rejection
        return True, ""

    if form_type == "factored_form":
        # Must have balanced parentheses with a multiplication-like structure.
        # Strip function heads first so \sin(x)/f(x)-style input isn't
        # misclassified as a product of factors.
        stripped = re.sub(r'\\?(sin|cos|tan|log|ln|exp|sqrt|frac)\s*', '', s)
        open_count = stripped.count('(')
        close_count = stripped.count(')')
        if open_count == 0 or open_count != close_count:
            return False, rejection
        factor_pattern = re.compile(
            r'\)\s*\(|\d\s*\(|[a-zA-Z]\s*\(|\)\s*[a-zA-Z]|\)\s*\d'
        )
        if not factor_pattern.search(stripped):
            return False, rejection
        return True, ""

    if form_type == "expanded_form":
        # Must NOT look like a product of factors. Strip function heads first
        # so \sin(x) etc. isn't misread as a factor group and wrongly rejected.
        stripped = re.sub(r'\\?(sin|cos|tan|log|ln|exp|sqrt|frac)\s*', '', s)
        open_count = stripped.count('(')
        close_count = stripped.count(')')
        if open_count == close_count and open_count > 0:
            factor_pattern = re.compile(
                r'\)\s*\(|\d\s*\(|[a-zA-Z]\s*\(|\)\s*[a-zA-Z]|\)\s*\d'
            )
            if factor_pattern.search(stripped):
                return False, rejection
        return True, ""

    if form_type == "exact_form":
        # Reject decimal points AND scientific notation (e.g. 1.5e3, 2E-4).
        if '.' in s:
            return False, rejection
        if re.search(r'\d[eE][+-]?\d', s):
            return False, rejection
        return True, ""

    if form_type == "custom_regex":
        pattern = strict_form.get("pattern", "")
        if not pattern:
            return True, ""
        try:
            if not re.search(pattern, s):
                return False, rejection
        except re.error:
            # A bad (possibly hydrated) pattern must never 500 the endpoint;
            # log and accept rather than crash the student's submission.
            logger.warning("Invalid custom_regex pattern %r; accepting answer", pattern)
            return True, ""
        return True, ""

    # Unknown type — allow through
    return True, ""


# ── Answer checking ────────────────────────────────────────────────────────────

def _check_answer(student: str, correct: str, input_type: str) -> bool:
    student = student.strip()
    if input_type == "numeric":
        try:
            return abs(float(student) - float(correct)) <= 0.01
        except (ValueError, TypeError):
            return False
    elif input_type == "multiple_choice":
        try:
            return int(student) == int(correct)
        except (ValueError, TypeError):
            return student.lower() == correct.lower()
    elif input_type == "expression":
        # Normalize "x = value" form: strip the leading "var =" so students
        # can write either the bare value or "x = value" for solution steps.
        normalized = re.sub(r'^[a-zA-Z]\s*=\s*', '', student)
        if normalized != student:
            if check_answer(normalized, correct, "symbolic"):
                return True
        return check_answer(student, correct, "symbolic")
    elif input_type == "dropdown":
        return student.lower() == correct.strip().lower()
    return False


# ── Feedback evaluation ────────────────────────────────────────────────────────

def _evaluate_feedback(
    feedback_list: list,
    student_answer: str,
    variables: dict,
    variables_str: dict,
) -> Optional[str]:
    """Return the first matching feedback text, with all placeholders substituted."""
    for item in feedback_list:
        condition = item.get("condition", "default")
        if _eval_condition(condition, student_answer, variables):
            raw = item.get("feedback", "")
            for key, val in variables_str.items():
                raw = raw.replace('{' + key + '}', val)
            raw = raw.replace('{answer}', student_answer.strip())
            return raw
    return None


def _eval_condition(condition: str, student_answer: str, variables: dict) -> bool:
    """
    Evaluate a wrong-answer feedback condition against the student's answer and
    the walkthrough's variables.

    Conditions are safe boolean expressions (see walkthrough_conditions.py).
    Two named conditions are reserved and handled specially:
      - "default" always matches (fallthrough feedback).
      - "answer == original fraction" is a symbolic equivalence check (SymPy),
        which the expression grammar can't express — documented in
        walkthrough-schema.md.
    A small set of legacy named conditions is still supported as a fallback so
    any un-migrated template keeps working; new templates must use expressions.
    """
    cond = condition.strip()

    if cond == "default":
        return True

    # Reserved symbolic helper — needs SymPy, not arithmetic over variables.
    if cond == "answer == original fraction":
        try:
            num = int(variables.get("numerator", 0))
            den = int(variables.get("denominator", 0))
            return check_answer(student_answer, f"\\frac{{{num}}}{{{den}}}", "symbolic")
        except Exception:
            return False

    # Legacy no-op kept for backwards compatibility (superseded by strict_form).
    if cond == "answer is equivalent but not fully simplified":
        return False

    # Primary path: safe expression evaluator. Malicious or malformed input
    # raises ConditionError (never executes) and falls through to the legacy
    # branches below, which don't match hostile strings either → False.
    try:
        return evaluate_condition(cond, student_answer, variables)
    except ConditionError:
        pass

    return _eval_legacy_condition(cond, student_answer, variables)


def _eval_legacy_condition(cond: str, student_answer: str, variables: dict) -> bool:
    """Backwards-compatible named-condition handling for un-migrated templates."""
    try:
        ans_float = float(student_answer.strip())
        ans_int = int(ans_float) if ans_float == int(ans_float) else None
    except (ValueError, AttributeError):
        ans_int = None

    num = int(variables.get("numerator", 0))
    den = int(variables.get("denominator", 0))
    g = int(variables.get("gcf", 0))

    if cond == "answer divides numerator but not denominator":
        if ans_int and ans_int > 1:
            return num % ans_int == 0 and den % ans_int != 0
        return False

    if cond == "answer divides denominator but not numerator":
        if ans_int and ans_int > 1:
            return den % ans_int == 0 and num % ans_int != 0
        return False

    if cond == "answer divides both but is not the greatest":
        if ans_int and ans_int > 1:
            return num % ans_int == 0 and den % ans_int == 0 and ans_int < g
        return False

    return False
