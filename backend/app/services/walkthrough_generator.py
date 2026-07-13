"""
Walkthrough hydration: load a JSON template, call the matching per-node
generator to produce concrete variable values, substitute all {placeholder}
strings, and return the fully-hydrated dict.
"""
import importlib
import json
import os
import random
from typing import Optional

_WALKTHROUGHS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "walkthroughs")


def _substitute(obj, variables: dict):
    """Recursively substitute {key} placeholders throughout a JSON structure."""
    if isinstance(obj, str):
        for key, val in variables.items():
            obj = obj.replace('{' + key + '}', val)
        return obj
    elif isinstance(obj, list):
        return [_substitute(item, variables) for item in obj]
    elif isinstance(obj, dict):
        return {k: _substitute(v, variables) for k, v in obj.items()}
    return obj


def _load_generator(node_id: str):
    """
    Dynamically import walkthrough_generators/<node_id>.py (with hyphens
    converted to underscores) and return its generate() function, or None
    if no such module exists.
    """
    module_name = node_id.replace('-', '_')
    try:
        module = importlib.import_module(
            f'app.services.walkthrough_generators.{module_name}'
        )
        return getattr(module, 'generate', None)
    except ImportError:
        return None


def generate_walkthrough(node_id: str) -> Optional[dict]:
    """
    Load the walkthrough template for node_id, call the corresponding
    generator to produce fresh variable values, substitute all placeholders,
    and return the hydrated dict.

    Returns None if no template or no generator exists for node_id.
    The returned dict includes a 'variables' key (integer values) which the
    frontend passes back to the check-step endpoint.
    """
    template_path = os.path.join(_WALKTHROUGHS_DIR, f"{node_id}.json")
    if not os.path.exists(template_path):
        return None

    generator = _load_generator(node_id)
    if generator is None:
        return None

    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)

    variables = generator()
    variables_str = {k: str(v) for k, v in variables.items()}
    hydrated = _substitute(template, variables_str)

    # Shuffle multiple-choice options so the correct answer isn't always at the
    # same position (many templates have the conceptual answer at index 0).
    # The shuffle order is passed back to the client inside `variables` and used
    # by check-step to translate the student's display-index answer back to the
    # template index. This is a stateless design consistent with the existing
    # variables passback: a student could tamper with the order via devtools,
    # but walkthroughs don't affect mastery, so that's an acceptable tradeoff.
    # NOTE: if walkthrough completion ever gates anything, move MC ordering to
    # server-side session state instead of trusting the client.
    mc_orders = _shuffle_multiple_choice(hydrated)

    result_variables = dict(variables)
    result_variables.update(mc_orders)
    hydrated['variables'] = result_variables

    return hydrated


def _shuffle_multiple_choice(hydrated: dict) -> dict:
    """
    In-place shuffle the `options` of every multiple_choice step and remap its
    `correct_answer` to the new position. Returns a dict of
    {"_mc_order_{step_number}": [display_index -> template_index, ...]} so the
    check-step endpoint can translate a submitted display index back to the
    original template index.
    """
    orders = {}
    for step in hydrated.get("steps", []):
        if step.get("input_type") != "multiple_choice":
            continue
        options = step.get("options")
        if not options or len(options) < 2:
            continue

        order = list(range(len(options)))          # order[display] = template idx
        random.shuffle(order)

        step["options"] = [options[t] for t in order]

        try:
            old_correct = int(step.get("correct_answer", 0))
        except (ValueError, TypeError):
            old_correct = 0
        # New display index of the old correct option
        new_correct = order.index(old_correct) if old_correct in order else 0
        step["correct_answer"] = str(new_correct)

        orders[f"_mc_order_{step['step_number']}"] = order

    return orders
