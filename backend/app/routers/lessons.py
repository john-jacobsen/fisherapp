from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.knowledge import KnowledgeNode, KnowledgeEdge
from app.models.content import Lesson, WorkedExample
from app.models.progress import StudentState
from app.kst.kst_engine import get_active_graph

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


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
    examples = db.query(WorkedExample).filter(
        WorkedExample.node_id == node_id
    ).order_by(WorkedExample.display_order).all()

    prereqs_met = _prereqs_met(node_id, db, str(current_user.id), graph.id)

    return {
        "node": {"id": node.id, "label": node.label, "topic": node.topic},
        "lesson": {
            "video_url": lesson.video_url if lesson else None,
            "content_markdown": lesson.content_markdown if lesson else f"# {node.label}\n\nLesson content coming soon.",
        } if lesson else None,
        "worked_examples": [
            {
                "id": str(e.id),
                "problem_text": e.problem_text,
                "steps": e.steps,
            }
            for e in examples
        ],
        "is_prerequisites_met": prereqs_met,
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
