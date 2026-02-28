"""
Practice service — per-node BKT (Bayesian Knowledge Tracing) for mastery tracking.

Flow:
1. start_practice() — get node posterior, return first problem
2. submit_answer() — BKT update, check mastery, return next or complete
3. get_hints() — return hint at requested level
4. complete_practice() — if mastered, update global state; return summary
"""
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session as DBSession

from app.config import settings
from app.models.content import Problem, Hint
from app.models.knowledge import KnowledgeNode, KnowledgeEdge
from app.models.progress import Session, StudentState, ReviewSchedule, ResponseLog
from app.services.answer_checker import check_answer
from app.kst.kst_engine import (
    get_active_graph,
    get_or_build_cache,
    compute_node_fringes,
    update_student_state,
)

logger = logging.getLogger(__name__)

LUCKY_GUESS = settings.blim_lucky_guess
CARELESS_ERROR = settings.blim_careless_error
MASTERY_THRESHOLD = settings.blim_mastery_threshold


def _bkt_update(posterior: float, is_correct: bool) -> float:
    """Per-node Bayesian Knowledge Tracing update."""
    if is_correct:
        numerator = posterior * (1 - CARELESS_ERROR)
        denominator = numerator + (1 - posterior) * LUCKY_GUESS
    else:
        numerator = posterior * CARELESS_ERROR
        denominator = numerator + (1 - posterior) * (1 - LUCKY_GUESS)

    if denominator == 0:
        return posterior
    return numerator / denominator


def _get_node_prior(user_id: str, node_id: str, db: DBSession) -> float:
    """
    Get a student's initial posterior for a node from their global state.
    Returns 0.2 if in outer_fringe (ready), 0.8 if mastered, else 0.1.
    """
    graph = get_active_graph(db)
    if not graph:
        return 0.2

    state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph.id,
    ).first()

    if not state:
        return 0.2

    if node_id in (state.mastered_nodes or []):
        return 0.8
    if node_id in (state.outer_fringe or []):
        return 0.2
    return 0.1


def _check_prereqs(node_id: str, user_id: str, db: DBSession) -> bool:
    """Return True if all prerequisites for node_id are mastered by user."""
    graph = get_active_graph(db)
    if not graph:
        return False

    prereqs = db.query(KnowledgeEdge).filter(
        KnowledgeEdge.to_node_id == node_id,
        KnowledgeEdge.graph_id == graph.id,
    ).all()

    if not prereqs:
        return True

    state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph.id,
    ).first()

    if not state:
        return False

    mastered = set(state.mastered_nodes or [])
    return all(e.from_node_id in mastered for e in prereqs)


def _get_problem(node_id: str, exclude_ids: list[str], db: DBSession) -> Optional[Problem]:
    """Get a problem for a node, excluding already-seen ones."""
    exclude_uuids = [uuid.UUID(pid) for pid in exclude_ids if pid]
    return (
        db.query(Problem)
        .filter(Problem.node_id == node_id, ~Problem.id.in_(exclude_uuids))
        .order_by(Problem.difficulty)
        .first()
    )


def start_practice(node_id: str, user_id: str, db: DBSession) -> dict:
    """Start a practice session for a node. Returns session + first problem + mastery info."""
    if not _check_prereqs(node_id, user_id, db):
        raise PermissionError(f"Prerequisites for '{node_id}' not met")

    node = db.query(KnowledgeNode).filter(KnowledgeNode.id == node_id).first()
    if not node:
        raise ValueError(f"Node '{node_id}' not found")

    problem = _get_problem(node_id, [], db)
    if not problem:
        raise ValueError(f"No problems found for node '{node_id}'")

    # Close existing active sessions for this node
    db.query(Session).filter(
        Session.user_id == user_id,
        Session.node_id == node_id,
        Session.session_type == "practice",
        Session.is_active == True,
    ).update({"is_active": False})

    posterior = _get_node_prior(user_id, node_id, db)

    session_state = {
        "posterior": posterior,
        "questions_asked": 0,
        "correct_count": 0,
        "seen_problems": [],
        "node_id": node_id,
    }

    session = Session(
        user_id=user_id,
        session_type="practice",
        node_id=node_id,
        state_snapshot=session_state,
        is_active=True,
    )
    db.add(session)
    db.commit()

    return {
        "session_id": str(session.id),
        "problem": {
            "id": str(problem.id),
            "problem_text": problem.problem_text,
            "answer_type": problem.answer_type,
        },
        "mastery": {
            "current_posterior": round(posterior, 3),
            "threshold": MASTERY_THRESHOLD,
            "min_questions": 3,
            "soft_cap": 10,
        },
    }


def submit_practice_answer(
    node_id: str,
    session_id: str,
    problem_id: str,
    answer: str,
    user_id: str,
    db: DBSession,
    mode: str = "test",
) -> dict:
    """Process a practice answer. Returns feedback + mastery + next problem."""
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.user_id == user_id,
        Session.is_active == True,
    ).first()
    if not session:
        raise ValueError("Session not found or already completed")

    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise ValueError("Problem not found")

    state = session.state_snapshot.copy()
    posterior = state["posterior"]
    questions_asked = state["questions_asked"]
    correct_count = state["correct_count"]
    seen_problems = state["seen_problems"]

    is_correct = check_answer(answer, problem.correct_answer, problem.answer_type)
    is_learning_mode = (mode == "learning")

    # In learning mode: record answer but do NOT update BKT posterior or mastery
    if not is_learning_mode:
        posterior = _bkt_update(posterior, is_correct)
        if is_correct:
            correct_count += 1
        questions_asked += 1

    seen_problems.append(str(problem.id))

    # Log response for analytics
    graph = get_active_graph(db)
    if graph:
        log = ResponseLog(
            user_id=user_id,
            session_id=session.id,
            node_id=node_id,
            problem_id=problem.id,
            session_type="practice",
            is_correct=is_correct,
            student_answer=answer,
        )
        db.add(log)

    # Check termination (only in test mode)
    is_mastered = (not is_learning_mode) and posterior >= MASTERY_THRESHOLD and questions_asked >= 3
    soft_cap = (not is_learning_mode) and questions_asked >= 10
    low_posterior = (not is_learning_mode) and posterior <= 0.15 and questions_asked >= 3

    state.update({
        "posterior": posterior,
        "questions_asked": questions_asked,
        "correct_count": correct_count,
        "seen_problems": seen_problems,
        "is_mastered": is_mastered,
    })

    next_problem = None
    if not is_mastered and not soft_cap and not low_posterior:
        np = _get_problem(node_id, seen_problems, db)
        if np:
            next_problem = {
                "id": str(np.id),
                "problem_text": np.problem_text,
                "answer_type": np.answer_type,
            }
        else:
            # No more unseen problems — recycle
            np = _get_problem(node_id, [], db)
            if np:
                next_problem = {
                    "id": str(np.id),
                    "problem_text": np.problem_text,
                    "answer_type": np.answer_type,
                }

    session.state_snapshot = state
    db.commit()

    return {
        "is_correct": is_correct,
        "correct_answer": problem.correct_answer,
        "mastery": {
            "current_posterior": round(posterior, 3),
            "questions_answered": questions_asked,
            "is_mastered": is_mastered,
        },
        "next_problem": next_problem,
        "suggest_review_lesson": low_posterior,
    }


def get_hint(node_id: str, problem_id: str, level: int, db: DBSession) -> dict:
    """Return hint at the requested level for a problem."""
    hint = db.query(Hint).filter(
        Hint.problem_id == problem_id,
        Hint.level == level,
    ).first()

    if not hint:
        raise ValueError(f"No hint at level {level} for this problem")

    max_level = db.query(Hint).filter(Hint.problem_id == problem_id).count()

    return {
        "hint_text": hint.hint_text,
        "level": level,
        "max_level": max_level,
    }


def complete_practice(
    node_id: str,
    session_id: str,
    user_id: str,
    db: DBSession,
) -> dict:
    """
    Complete a practice session.
    If mastered, update global StudentState and schedule review.
    Returns summary + fringe for next topic selection.
    """
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.user_id == user_id,
    ).first()
    if not session:
        raise ValueError("Session not found")

    state = session.state_snapshot or {}
    posterior = state.get("posterior", 0.0)
    questions_asked = state.get("questions_asked", 0)
    correct_count = state.get("correct_count", 0)
    is_mastered = state.get("is_mastered", False) or (
        posterior >= MASTERY_THRESHOLD and questions_asked >= 3
    )

    session.is_active = False
    session.completed_at = datetime.now(timezone.utc)

    graph = get_active_graph(db)
    outer_fringe = []
    inner_fringe = []

    if is_mastered and graph:
        graph_id = str(graph.id)
        student_state = db.query(StudentState).filter(
            StudentState.user_id == user_id,
            StudentState.graph_id == graph.id,
        ).first()

        mastered_set = set(student_state.mastered_nodes or []) if student_state else set()
        mastered_set.add(node_id)

        # Recompute fringes
        inner, outer = compute_node_fringes(db, graph_id, mastered_set)
        outer_fringe = outer
        inner_fringe = inner

        # Update StudentState
        if student_state:
            student_state.mastered_nodes = list(mastered_set)
            student_state.outer_fringe = outer
            student_state.inner_fringe = inner
        else:
            new_state = StudentState(
                user_id=user_id,
                graph_id=graph.id,
                graph_version=graph.version,
                state_distribution={},
                mastered_nodes=list(mastered_set),
                outer_fringe=outer,
                inner_fringe=inner,
                placement_completed=False,
            )
            db.add(new_state)
            db.flush()
            student_state = new_state

        # Schedule review
        now = datetime.now(timezone.utc)
        existing_review = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id,
            ReviewSchedule.node_id == node_id,
        ).first()
        if existing_review:
            existing_review.mastered_at = now
            existing_review.next_review_at = now + timedelta(days=1)
            existing_review.interval_days = 1
            existing_review.streak = 0
        else:
            db.add(ReviewSchedule(
                user_id=user_id,
                node_id=node_id,
                mastered_at=now,
                next_review_at=now + timedelta(days=1),
                interval_days=1,
                streak=0,
            ))

    db.commit()

    # Fetch node labels for fringe
    def node_info(nid):
        n = db.query(KnowledgeNode).filter(KnowledgeNode.id == nid).first()
        return {"node_id": nid, "label": n.label if n else nid, "topic": n.topic if n else ""}

    accuracy = round(correct_count / questions_asked, 3) if questions_asked > 0 else 0.0

    return {
        "summary": {
            "questions": questions_asked,
            "correct": correct_count,
            "accuracy": accuracy,
            "mastery_posterior": round(posterior, 3),
        },
        "is_mastered": is_mastered,
        "outer_fringe": [node_info(n) for n in outer_fringe],
        "inner_fringe": [node_info(n) for n in inner_fringe],
    }
