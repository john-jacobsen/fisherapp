"""
Pytest wrapper around the walkthrough validation harness. Runs the full
schema + hydration validation over every template so it executes with the
rest of the suite.

    python -m pytest backend/tests/test_walkthrough_validation.py -q
"""
import os
import sys

import pytest

_here = os.path.dirname(os.path.abspath(__file__))
_backend = os.path.join(_here, "..")
for p in (_backend, os.path.join(_backend, "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)

from validate_walkthroughs import validate_all, validate_node, validate_all as _va  # noqa: E402


def _node_ids():
    all_passed, rows = validate_all()
    return [node_id for node_id, _, _ in rows]


@pytest.mark.parametrize("node_id", _node_ids())
def test_walkthrough_template_valid(node_id):
    ok, msg = validate_node(node_id)
    assert ok, f"{node_id}: {msg}"


def test_all_templates_pass():
    all_passed, rows = validate_all()
    failures = [f"{n}: {m}" for n, ok, m in rows if not ok]
    assert all_passed, "Walkthrough validation failures:\n" + "\n".join(failures)


if __name__ == "__main__":
    from validate_walkthroughs import main
    sys.exit(main())
