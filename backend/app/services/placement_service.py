"""
Placement test service — adaptive assessment using BLIM.

Flow:
1. start_placement() — uniform prior, select first item, return first problem
2. submit_answer() — BLIM update, check termination, return next problem or completion
3. get_results() — return categorized node statuses
"""
import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session as DBSession

from app.kst.kst_engine import (
    get_active_graph,
    get_or_build_cache,
    initialize_uniform_prior,
    run_blim_update,
    get_distribution_entropy,
    get_mastered_nodes_from_distribution,
    compute_node_fringes,
    select_next_assessment_item,
    update_student_state,
)
from app.models.content import Problem
from app.models.knowledge import KnowledgeNode
from app.models.progress import Session, ReviewSchedule, StudentState
from app.services.answer_checker import check_answer
from app.config import settings

logger = logging.getLogger(__name__)


def _get_problem_for_node(
    db: DBSession,
    node_id: str,
    exclude_ids: list[str],
) -> Optional[Problem]:
    """Get a random problem for the given node, excluding already-seen problems."""
    query = db.query(Problem).filter(
        Problem.node_id == node_id,
        ~Problem.id.in_([uuid.UUID(pid) for pid in exclude_ids if pid]),
    )
    return query.order_by(Problem.difficulty).first()


def start_placement(user_id: str, db: DBSession) -> dict:
    """
    Initialize a placement test session.
    Returns: { session_id, first_question: { problem_id, node_id, problem_text, topic } }
    """
    graph = get_active_graph(db)
    if not graph:
        raise ValueError("No active knowledge graph found")

    graph_id = str(graph.id)
    distribution = initialize_uniform_prior(db, graph_id)
    initial_entropy = get_distribution_entropy(distribution)

    # Close any existing active placement sessions for this user
    db.query(Session).filter(
        Session.user_id == user_id,
        Session.session_type == "placement",
        Session.is_active == True,
    ).update({"is_active": False})

    # Create new session with state snapshot
    session_state = {
        "distribution": distribution,
        "asked_items": [],
        "asked_problems": [],
        "initial_entropy": initial_entropy,
        "questions_answered": 0,
        "correct_count": 0,
        "graph_id": graph_id,
    }

    session = Session(
        user_id=user_id,
        session_type="placement",
        state_snapshot=session_state,
        is_active=True,
    )
    db.add(session)
    db.flush()

    # Select first item
    item_id = select_next_assessment_item(db, graph_id, distribution, [])
    if not item_id:
        raise ValueError("Could not select first assessment item")

    # Get a problem for that item
    problem = _get_problem_for_node(db, item_id, [])
    if not problem:
        # Try another item
        cache = get_or_build_cache(db, graph_id)
        for alt_item in cache["items"]:
            if alt_item != item_id:
                problem = _get_problem_for_node(db, alt_item, [])
                if problem:
                    item_id = alt_item
                    break

    if not problem:
        raise ValueError("No problems found. Run seed_problems.py first.")

    # Get topic
    node = db.query(KnowledgeNode).filter(KnowledgeNode.id == item_id).first()

    db.commit()

    return {
        "session_id": str(session.id),
        "first_question": {
            "problem_id": str(problem.id),
            "node_id": item_id,
            "problem_text": problem.problem_text,
            "topic": node.topic if node else "",
        },
    }


def submit_answer(
    session_id: str,
    problem_id: str,
    answer: str,
    user_id: str,
    db: DBSession,
) -> dict:
    """
    Process a placement test answer.
    Returns:
    {
        is_correct, correct_answer,
        next_question: {...} | null,
        progress: { questions_answered, estimated_remaining },
        is_complete: bool
    }
    """
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
    distribution = state["distribution"]
    asked_items = state["asked_items"]
    asked_problems = state["asked_problems"]
    initial_entropy = state["initial_entropy"]
    questions_answered = state["questions_answered"]
    correct_count = state["correct_count"]
    graph_id = state["graph_id"]

    # Check answer
    is_correct = check_answer(answer, problem.correct_answer, problem.answer_type)
    if is_correct:
        correct_count += 1

    # BLIM update
    distribution = run_blim_update(
        db, graph_id, distribution, problem.node_id, is_correct
    )

    # Track progress
    asked_items.append(problem.node_id)
    asked_problems.append(str(problem.id))
    questions_answered += 1

    # Check termination conditions
    current_entropy = get_distribution_entropy(distribution)
    entropy_ratio = current_entropy / initial_entropy if initial_entropy > 0 else 1.0

    is_complete = (
        entropy_ratio <= settings.blim_entropy_termination
        or questions_answered >= 20
    )

    next_question = None
    if not is_complete:
        # Select next item
        next_item_id = select_next_assessment_item(db, graph_id, distribution, asked_items)
        if next_item_id:
            next_problem = _get_problem_for_node(db, next_item_id, asked_problems)
            if next_problem:
                node = db.query(KnowledgeNode).filter(KnowledgeNode.id == next_item_id).first()
                next_question = {
                    "problem_id": str(next_problem.id),
                    "node_id": next_item_id,
                    "problem_text": next_problem.problem_text,
                    "topic": node.topic if node else "",
                }
            else:
                # No problem for next item, try to complete
                is_complete = True
        else:
            is_complete = True

    # Update session state
    state.update({
        "distribution": distribution,
        "asked_items": asked_items,
        "asked_problems": asked_problems,
        "questions_answered": questions_answered,
        "correct_count": correct_count,
    })

    if is_complete:
        _finalize_placement(user_id, state, db, graph_id)
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)
        session.state_snapshot = state
    else:
        session.state_snapshot = state

    db.commit()

    return {
        "is_correct": is_correct,
        "correct_answer": problem.correct_answer,
        "next_question": next_question,
        "progress": {
            "questions_answered": questions_answered,
            "estimated_remaining": max(0, 15 - questions_answered),
        },
        "is_complete": is_complete,
    }


def _finalize_placement(user_id: str, state: dict, db: DBSession, graph_id: str):
    """
    After placement: compute mastered/ready/locked, create StudentState,
    and schedule reviews for all mastered nodes.
    """
    distribution = state["distribution"]

    # Get active graph
    from app.models.knowledge import KnowledgeGraph
    graph = db.query(KnowledgeGraph).filter(
        KnowledgeGraph.id == graph_id,
    ).first()
    if not graph:
        return

    # Compute mastered nodes from most probable state
    mastered = get_mastered_nodes_from_distribution(distribution)
    inner, outer = compute_node_fringes(db, graph_id, set(mastered))

    # Update or create StudentState
    student_state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph.id,
    ).first()

    if student_state:
        student_state.state_distribution = distribution
        student_state.mastered_nodes = mastered
        student_state.outer_fringe = outer
        student_state.inner_fringe = inner
        student_state.placement_completed = True
    else:
        student_state = StudentState(
            user_id=user_id,
            graph_id=graph.id,
            graph_version=graph.version,
            state_distribution=distribution,
            mastered_nodes=mastered,
            outer_fringe=outer,
            inner_fringe=inner,
            placement_completed=True,
        )
        db.add(student_state)

    db.flush()

    # Schedule reviews for mastered nodes
    now = datetime.now(timezone.utc)
    for node_id in mastered:
        existing = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id,
            ReviewSchedule.node_id == node_id,
        ).first()
        if not existing:
            review = ReviewSchedule(
                user_id=user_id,
                node_id=node_id,
                mastered_at=now,
                next_review_at=now + timedelta(days=1),
                interval_days=1,
                streak=0,
            )
            db.add(review)


def get_results(user_id: str, db: DBSession) -> dict:
    """Return placement results for the user."""
    graph = get_active_graph(db)
    if not graph:
        raise ValueError("No active graph")

    student_state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph.id,
    ).first()

    if not student_state:
        return {
            "mastered_nodes": [],
            "ready_nodes": [],
            "locked_nodes": [],
            "questions_answered": 0,
            "accuracy": 0,
        }

    # Get all nodes
    all_nodes = db.query(KnowledgeNode).filter(
        KnowledgeNode.graph_id == graph.id
    ).all()
    node_map = {n.id: n for n in all_nodes}

    mastered = student_state.mastered_nodes or []
    outer = student_state.outer_fringe or []
    locked = [
        n.id for n in all_nodes
        if n.id not in mastered and n.id not in outer
    ]

    # Find the most recent completed placement session
    session = db.query(Session).filter(
        Session.user_id == user_id,
        Session.session_type == "placement",
        Session.is_active == False,
    ).order_by(Session.completed_at.desc()).first()

    questions_answered = 0
    accuracy = 0.0
    if session and session.state_snapshot:
        snap = session.state_snapshot
        questions_answered = snap.get("questions_answered", 0)
        correct = snap.get("correct_count", 0)
        accuracy = round(correct / questions_answered, 3) if questions_answered > 0 else 0.0

    def node_info(nid):
        n = node_map.get(nid)
        return {"node_id": nid, "label": n.label if n else nid, "topic": n.topic if n else ""}

    return {
        "mastered_nodes": [node_info(n) for n in mastered],
        "ready_nodes": [node_info(n) for n in outer],
        "locked_nodes": [node_info(n) for n in locked],
        "questions_answered": questions_answered,
        "accuracy": accuracy,
    }
