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

SM2_INTERVALS = [1, 3, 7, 14, 30]


def get_review_intervals(review_number: int) -> int:
    """Return interval in days for the given review number (0-indexed)."""
    if review_number < len(SM2_INTERVALS):
        return SM2_INTERVALS[review_number]
    return 30  # Every 30 days after max


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
