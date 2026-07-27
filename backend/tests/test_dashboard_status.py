"""
Unit tests for dashboard node-status derivation (FIXES-16 Item 8 / 14-9).

"ready" must be computed directly from prerequisite edges so it does not depend
on the truncated KST outer-fringe enumeration. These run without a database.

    python -m pytest backend/tests/test_dashboard_status.py -q
"""
import os
import sys
from types import SimpleNamespace

_here = os.path.dirname(os.path.abspath(__file__))
_backend = os.path.join(_here, "..")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from app.routers.dashboard import get_node_status


# A small chain: a -> b -> c, plus d with two prereqs (a, b).
CACHE = {"relations": [("a", "b"), ("b", "c"), ("a", "d"), ("b", "d")]}


def _state(mastered):
    return SimpleNamespace(mastered_nodes=list(mastered), outer_fringe=[], inner_fringe=[])


def test_no_state_root_is_ready():
    assert get_node_status("a", None, CACHE) == "ready"


def test_no_state_node_with_prereqs_is_available():
    assert get_node_status("b", None, CACHE) == "available"


def test_mastered_node():
    assert get_node_status("a", _state({"a"}), CACHE) == "mastered"


def test_ready_when_all_prereqs_mastered():
    # b's only prereq is a → mastering a makes b ready.
    assert get_node_status("b", _state({"a"}), CACHE) == "ready"


def test_available_when_a_prereq_is_unmet():
    # d needs both a and b; only a mastered → still available.
    assert get_node_status("d", _state({"a"}), CACHE) == "available"
    # c needs b (mastered a only) → available.
    assert get_node_status("c", _state({"a"}), CACHE) == "available"


def test_deep_node_ready_after_all_prereqs():
    # The 14-9 regression: a node deep in the chain must become ready once all
    # its direct prerequisites are mastered, regardless of KST state truncation.
    assert get_node_status("d", _state({"a", "b"}), CACHE) == "ready"
    assert get_node_status("c", _state({"a", "b"}), CACHE) == "ready"
