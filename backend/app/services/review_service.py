from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.progress import ReviewSchedule, StudentState
from app.models.content import Problem
from app.models.knowledge import KnowledgeNode
from app.services.answer_checker import check_answer
from app.config import settings

# SM-2 review schedule (FIXES-16 / 14-10): 7 → 14 → 30 → 90 days.
# Existing schedules keep their stored next_review_at / interval_days; only
# future scheduling (new masteries and advances) uses these constants.
SM2_INTERVALS = [7, 14, 30, 90]

# Escalating soft-gate enforcement (14-10).
DAILY_NEW_PRACTICE_LIMIT = 3   # once reviews are 6+ days overdue
OVERDUE_PERSISTENT_DAYS = 3    # 3-5 days: persistent banner + interstitial
OVERDUE_LIMIT_DAYS = 6         # 6+ days: cap new practice per day


def get_review_intervals(review_number: int) -> int:
    """Return interval in days for the given review number (0-indexed)."""
    if review_number < len(SM2_INTERVALS):
        return SM2_INTERVALS[review_number]
    return SM2_INTERVALS[-1]  # cap at the longest interval (90 days)


def get_due_reviews(user_id: UUID, db: Session) -> list[dict]:
    """Get all review schedule entries that are due (next_review_at <= now).
    Also apply decay to overdue reviews."""
    now = datetime.now(timezone.utc)

    schedules = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id,
        ReviewSchedule.next_review_at <= now,
    ).all()

    result = []
    for s in schedules:
        node = db.query(KnowledgeNode).filter(KnowledgeNode.id == s.node_id).first()
        if not node:
            continue

        # Calculate decay for overdue reviews
        days_overdue = 0
        overdue_threshold = s.next_review_at + timedelta(days=settings.review_grace_days)
        if now > overdue_threshold:
            days_overdue = (now - overdue_threshold).days

        # Derive review_number from interval_days for display
        review_number = _interval_to_review_number(s.interval_days)

        result.append({
            "node_id": str(s.node_id),
            "node_title": node.label,
            "topic": node.topic,
            "next_review_at": s.next_review_at.isoformat(),
            "review_number": review_number,
            "streak": s.streak,
            "days_overdue": days_overdue,
            "interval_days": s.interval_days,
        })

    return result


def get_upcoming_reviews(user_id: UUID, db: Session, days_ahead: int = 7) -> list[dict]:
    """Get reviews coming up in the next N days (not yet due)."""
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=days_ahead)

    schedules = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id,
        ReviewSchedule.next_review_at > now,
        ReviewSchedule.next_review_at <= cutoff,
    ).all()

    result = []
    for s in schedules:
        node = db.query(KnowledgeNode).filter(KnowledgeNode.id == s.node_id).first()
        if not node:
            continue

        review_number = _interval_to_review_number(s.interval_days)

        result.append({
            "node_id": str(s.node_id),
            "node_title": node.label,
            "topic": node.topic,
            "next_review_at": s.next_review_at.isoformat(),
            "review_number": review_number,
            "streak": s.streak,
            "days_until": max(0, (s.next_review_at - now).days),
        })

    return result


def start_review(user_id: UUID, node_id: str, db: Session) -> dict:
    """Start a review session for a node. Returns 1-3 review problems."""
    # Confirm review schedule exists for this node
    schedule = db.query(ReviewSchedule).filter(
        and_(ReviewSchedule.user_id == user_id, ReviewSchedule.node_id == node_id)
    ).first()
    if not schedule:
        raise ValueError(f"No review schedule found for node {node_id}")

    # Select up to 3 problems for review (random selection from node problems)
    import random
    problems = db.query(Problem).filter(
        Problem.node_id == node_id,
    ).all()

    if not problems:
        raise ValueError(f"No problems found for node {node_id}")

    count = min(3, len(problems))
    selected = random.sample(problems, count)

    review_number = _interval_to_review_number(schedule.interval_days)

    return {
        "node_id": str(node_id),
        "review_number": review_number,
        "streak": schedule.streak,
        "problems": [
            {
                "id": str(p.id),
                "statement": p.problem_text,
                "answer_type": p.answer_type,
                "choices": p.metadata_.get("choices") if p.metadata_ else None,
            }
            for p in selected
        ],
    }


def submit_review(
    user_id: UUID,
    node_id: str,
    problem_id: UUID,
    answer: str,
    db: Session,
) -> dict:
    """Submit a review answer. If correct, advance schedule. If wrong, remove schedule and reduce posterior."""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise ValueError("Problem not found")

    schedule = db.query(ReviewSchedule).filter(
        and_(ReviewSchedule.user_id == user_id, ReviewSchedule.node_id == node_id)
    ).first()
    if not schedule:
        raise ValueError("No review schedule")

    is_correct = check_answer(answer, problem.correct_answer, problem.answer_type)

    if is_correct:
        # Advance schedule using SM-2 intervals
        review_number = _interval_to_review_number(schedule.interval_days)
        next_review_number = review_number + 1
        interval = get_review_intervals(next_review_number)
        schedule.interval_days = interval
        schedule.streak += 1
        schedule.next_review_at = datetime.now(timezone.utc) + timedelta(days=interval)
        db.commit()
        return {
            "correct": True,
            "feedback": "Correct! Review scheduled.",
            "next_review_at": schedule.next_review_at.isoformat(),
            "next_interval_days": interval,
            "review_complete": True,
        }
    else:
        # Incorrect: reduce student posterior for this node and remove review schedule
        student_state = db.query(StudentState).filter(
            StudentState.user_id == user_id
        ).first()

        if student_state and student_state.mastered_nodes:
            node_id_str = str(node_id)
            if node_id_str in student_state.mastered_nodes:
                student_state.mastered_nodes = [n for n in student_state.mastered_nodes if n != node_id_str]
                from sqlalchemy.orm.attributes import flag_modified
                flag_modified(student_state, 'mastered_nodes')

        # Delete the review schedule — student must re-master
        db.delete(schedule)
        db.commit()

        return {
            "correct": False,
            "feedback": "Incorrect. This skill needs practice again.",
            "review_complete": True,
            "needs_practice": True,
        }


def apply_decay(user_id: UUID, db: Session) -> None:
    """Apply decay to overdue reviews (called on-the-fly during dashboard load).
    Reduces mastered status if review is overdue by more than REVIEW_GRACE_DAYS days."""
    now = datetime.now(timezone.utc)

    schedules = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id,
    ).all()

    student_state = db.query(StudentState).filter(
        StudentState.user_id == user_id
    ).first()
    if not student_state:
        return

    for s in schedules:
        overdue_threshold = s.next_review_at + timedelta(days=settings.review_grace_days)
        if now <= overdue_threshold:
            continue

        days_overdue = (now - overdue_threshold).days
        # Each day past grace period, node has a chance of dropping from mastered
        # At REVIEW_DECAY_RATE=0.02 per day, after 50 days it falls from mastered
        decay_threshold = settings.review_decay_rate * days_overdue
        if decay_threshold >= 0.5:
            # Remove from mastered
            node_id_str = str(s.node_id)
            if student_state.mastered_nodes and node_id_str in student_state.mastered_nodes:
                student_state.mastered_nodes = [n for n in student_state.mastered_nodes if n != node_id_str]
                from sqlalchemy.orm.attributes import flag_modified
                flag_modified(student_state, 'mastered_nodes')

    db.commit()


def _interval_to_review_number(interval_days: int) -> int:
    """Convert an interval_days value back to a review number index."""
    for i, days in enumerate(SM2_INTERVALS):
        if interval_days <= days:
            return i
    return len(SM2_INTERVALS)


# ── Escalating soft-gate enforcement (14-10) ──────────────────────────────────

def classify_overdue_tier(max_overdue_days: int, overdue_count: int) -> str:
    """
    Pure tier classifier for the escalating soft gate:
      none       : nothing overdue
      reminder   : 0-2 days overdue → dismissible banner
      persistent : 3-5 days overdue → non-dismissible banner + interstitial
      limit      : 6+ days overdue → new-practice daily cap
    """
    if overdue_count <= 0:
        return "none"
    if max_overdue_days >= OVERDUE_LIMIT_DAYS:
        return "limit"
    if max_overdue_days >= OVERDUE_PERSISTENT_DAYS:
        return "persistent"
    return "reminder"


def _max_overdue_days(user_id: UUID, db: Session, now: datetime) -> tuple[int, int]:
    """Return (max_days_overdue, overdue_count) across all currently-due reviews.
    Overdue is measured from next_review_at (when the review became due)."""
    due = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id,
        ReviewSchedule.next_review_at <= now,
    ).all()
    max_overdue = 0
    for s in due:
        d = (now - s.next_review_at).days
        if d > max_overdue:
            max_overdue = d
    return max_overdue, len(due)


def _count_practice_starts_today(user_id: UUID, db: Session, now: datetime) -> int:
    """Count NEW practice session starts for the user since 00:00 UTC today."""
    from app.models.progress import Session as PracticeSession
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id,
        PracticeSession.session_type == "practice",
        PracticeSession.started_at >= start_of_day,
    ).count()


def get_review_enforcement(user_id: UUID, db: Session) -> dict:
    """
    Compute the current review-enforcement state for a user.

    Tiers (by the most-overdue due review):
      - none        : no overdue reviews
      - reminder    : 0-2 days overdue  → dismissible banner
      - persistent  : 3-5 days overdue  → non-dismissible banner + interstitial
      - limit       : 6+ days overdue   → cap new practice at 3/day
    """
    now = datetime.now(timezone.utc)
    max_overdue, overdue_count = _max_overdue_days(user_id, db, now)
    tier = classify_overdue_tier(max_overdue, overdue_count)
    sessions_today = _count_practice_starts_today(user_id, db, now)
    limit_reached = (tier == "limit") and (sessions_today >= DAILY_NEW_PRACTICE_LIMIT)

    return {
        "tier": tier,
        "overdue_count": overdue_count,
        "max_overdue_days": max_overdue,
        "sessions_today": sessions_today,
        "daily_limit": DAILY_NEW_PRACTICE_LIMIT,
        "limit_reached": limit_reached,
    }


def check_practice_allowed(user_id: UUID, db: Session) -> tuple[bool, dict]:
    """
    Gate a NEW practice session start. Reviews themselves are always allowed;
    only new practice is capped once reviews are 6+ days overdue AND the daily
    limit has been reached. Returns (allowed, enforcement_info).
    """
    info = get_review_enforcement(user_id, db)
    if info["limit_reached"]:
        info = dict(info)
        info["message"] = (
            f"You have {info['overdue_count']} review(s) more than "
            f"{OVERDUE_LIMIT_DAYS} days overdue. To keep what you've learned from "
            f"slipping, new practice is limited to {DAILY_NEW_PRACTICE_LIMIT} "
            f"sessions per day until you clear them. Your reviews are always "
            f"available — finishing them lifts this limit right away."
        )
        info["cta"] = "Do reviews"
        return False, info
    return True, info
