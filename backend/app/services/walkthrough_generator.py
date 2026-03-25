"""
Walkthrough hydration: load a JSON template, call the matching per-node
generator to produce concrete variable values, substitute all {placeholder}
strings, and return the fully-hydrated dict.
"""
import importlib
import json
import os
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
    hydrated['variables'] = variables

    return hydrated
