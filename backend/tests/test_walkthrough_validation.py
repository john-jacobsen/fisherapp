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

from validate_walkthroughs import (  # noqa: E402
    validate_all,
    validate_node,
    _schema_check,
    ValidationError,
)


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


# ── Item 5: optional intro.video_id ───────────────────────────────────────────

def _minimal_template(intro: dict) -> dict:
    return {
        "node_id": "x",
        "title": "X",
        "intro": intro,
        "steps": [
            {"step_number": 1, "prompt": "p", "input_type": "numeric", "correct_answer": "1"},
        ],
    }


def test_schema_check_accepts_missing_video_id():
    # The six pilot templates leave video_id unset — must still pass.
    _schema_check(_minimal_template({"body": "b"}))


def test_schema_check_accepts_valid_video_id():
    _schema_check(_minimal_template({"body": "b", "video_id": "dQw4w9WgXcQ"}))


def test_schema_check_rejects_non_string_video_id():
    for bad in (123, "", "   ", ["id"], None):
        with pytest.raises(ValidationError):
            _schema_check(_minimal_template({"body": "b", "video_id": bad}))


if __name__ == "__main__":
    from validate_walkthroughs import main
    sys.exit(main())
