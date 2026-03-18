import json
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.knowledge import KnowledgeNode, KnowledgeEdge
from app.models.content import Lesson, WorkedExample
from app.models.progress import StudentState, ReviewSchedule
from app.kst.kst_engine import get_active_graph

router = APIRouter(prefix="/api/lessons", tags=["lessons"])

_VIDEOS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "lesson_videos.json")
_LESSONS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "lessons")


def _load_lesson_file(node_id: str):
    """Load lesson markdown from file, returns None if not found."""
    path = os.path.join(_LESSONS_DIR, f"{node_id}.md")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def _load_videos() -> dict:
    """Load lesson_videos.json fresh each call so edits take effect without restart."""
    try:
        with open(_VIDEOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _prereqs_met(node_id: str, db: Session, user_id: str, graph_id) -> bool:
    """Check if all prerequisites for a node are mastered by the user."""
    prereqs = db.query(KnowledgeEdge).filter(
        KnowledgeEdge.to_node_id == node_id,
        KnowledgeEdge.graph_id == graph_id,
    ).all()

    if not prereqs:
        return True  # No prerequisites

    state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph_id,
    ).first()

    if not state:
        return False

    mastered = set(state.mastered_nodes or [])
    return all(e.from_node_id in mastered for e in prereqs)


@router.get("/{node_id}")
def get_lesson(
    node_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    graph = get_active_graph(db)
    if not graph:
        raise HTTPException(status_code=503, detail="No active knowledge graph")

    node = db.query(KnowledgeNode).filter(KnowledgeNode.id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")

    lesson = db.query(Lesson).filter(Lesson.node_id == node_id).first()
    file_content = _load_lesson_file(node_id)
    examples = db.query(WorkedExample).filter(
        WorkedExample.node_id == node_id
    ).order_by(WorkedExample.display_order).all()

    prereqs_met = _prereqs_met(node_id, db, str(current_user.id), graph.id)

    # Compute mastery from StudentState
    state = db.query(StudentState).filter(
        StudentState.user_id == str(current_user.id),
        StudentState.graph_id == graph.id,
    ).first()
    mastery = 0.0
    if state:
        if node_id in (state.mastered_nodes or []):
            mastery = 1.0
        elif node_id in (state.inner_fringe or []):
            mastery = 0.6

    return {
        "node": {"id": node.id, "label": node.label, "topic": node.topic},
        "lesson": {
            "video_url": lesson.video_url if lesson else None,
            "content_markdown": (
                lesson.content_markdown if lesson and lesson.content_markdown
                else file_content
                or f"# {node.label}\n\nLesson content coming soon."
            ),
        },
        "worked_examples": [
            {
                "id": str(e.id),
                "problem_text": e.problem_text,
                "steps": e.steps,
            }
            for e in examples
        ],
        "is_prerequisites_met": prereqs_met,
        "mastery": mastery,
    }


@router.get("/{node_id}/examples")
def get_examples(
    node_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    examples = db.query(WorkedExample).filter(
        WorkedExample.node_id == node_id
    ).order_by(WorkedExample.display_order).all()

    return {
        "worked_examples": [
            {
                "id": str(e.id),
                "problem_text": e.problem_text,
                "steps": e.steps,
            }
            for e in examples
        ]
    }


@router.get("/{node_id}/videos")
def get_videos(
    node_id: str,
    current_user: User = Depends(get_current_user),
):
    """Return curated videos for a node from lesson_videos.json."""
    data = _load_videos()
    entry = data.get(node_id, {})
    return {"videos": entry.get("videos", [])}
