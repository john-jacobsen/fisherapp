"""
Tests for review enforcement (FIXES-16 Item 9 / 14-10): SM-2 interval
constants and the escalating soft-gate tier classifier. DB-free (CI-safe).

    python -m pytest backend/tests/test_review_enforcement.py -q
"""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_backend = os.path.join(_here, "..")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from app.services.review_service import (
    SM2_INTERVALS,
    get_review_intervals,
    classify_overdue_tier,
    DAILY_NEW_PRACTICE_LIMIT,
    OVERDUE_PERSISTENT_DAYS,
    OVERDUE_LIMIT_DAYS,
)


# ── SM-2 interval schedule: 7 → 14 → 30 → 90 ──────────────────────────────────

def test_interval_constants():
    assert SM2_INTERVALS == [7, 14, 30, 90]


def test_interval_progression():
    assert get_review_intervals(0) == 7
    assert get_review_intervals(1) == 14
    assert get_review_intervals(2) == 30
    assert get_review_intervals(3) == 90


def test_interval_caps_at_90():
    # Beyond the last index, scheduling caps at the longest interval.
    assert get_review_intervals(4) == 90
    assert get_review_intervals(10) == 90


# ── Escalating soft-gate tiers ────────────────────────────────────────────────

def test_tier_none_when_nothing_overdue():
    assert classify_overdue_tier(0, 0) == "none"
    assert classify_overdue_tier(99, 0) == "none"  # count 0 dominates


def test_tier_reminder_0_to_2_days():
    assert classify_overdue_tier(0, 1) == "reminder"
    assert classify_overdue_tier(2, 3) == "reminder"


def test_tier_persistent_3_to_5_days():
    assert classify_overdue_tier(3, 1) == "persistent"
    assert classify_overdue_tier(5, 2) == "persistent"


def test_tier_limit_6_plus_days():
    assert classify_overdue_tier(6, 1) == "limit"
    assert classify_overdue_tier(30, 4) == "limit"


def test_thresholds_are_the_documented_values():
    assert OVERDUE_PERSISTENT_DAYS == 3
    assert OVERDUE_LIMIT_DAYS == 6
    assert DAILY_NEW_PRACTICE_LIMIT == 3
