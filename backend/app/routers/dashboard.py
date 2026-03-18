from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.knowledge import KnowledgeGraph, KnowledgeNode, KnowledgeEdge
from app.models.progress import StudentState, ReviewSchedule
from app.routers.auth import get_current_user
from app.models.user import User
from app.kst.kst_engine import get_active_graph, get_or_build_cache
from app.services.review_service import apply_decay

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def get_node_status(node_id: str, student_state: StudentState | None, graph_cache: dict) -> str:
    """
    Compute status for a node given student state.
    - mastered: in mastered_nodes
    - ready: in outer fringe (all prerequisites mastered — recommended next)
    - available: prerequisites not yet met, but still accessible (advisory only)
    """
    if student_state is None:
        # Before placement: outer-fringe nodes (no prereqs) are ready, others are available
        relations = graph_cache.get("relations", [])
        has_prereqs = any(target == node_id for _, target in relations)
        return "available" if has_prereqs else "ready"

    if node_id in student_state.mastered_nodes:
        return "mastered"
    if node_id in student_state.outer_fringe:
        return "ready"
    return "available"


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    apply_decay(current_user.id, db)

    graph = get_active_graph(db)
    if not graph:
        raise HTTPException(status_code=503, detail="No active knowledge graph found")

    graph_id = str(graph.id)
    cache = get_or_build_cache(db, graph_id)

    nodes = db.query(KnowledgeNode).filter(KnowledgeNode.graph_id == graph.id).all()
    edges = db.query(KnowledgeEdge).filter(KnowledgeEdge.graph_id == graph.id).all()

    student_state = db.query(StudentState).filter(
        StudentState.user_id == current_user.id,
        StudentState.graph_id == graph.id,
    ).first()

    # Build node list with status
    node_list = []
    for node in nodes:
        status = get_node_status(node.id, student_state, cache)
        node_list.append({
            "id": node.id,
            "label": node.label,
            "topic": node.topic,
            "status": status,
            "display_x": node.display_x,
            "display_y": node.display_y,
        })

    edge_list = [{"from_node_id": e.from_node_id, "to_node_id": e.to_node_id} for e in edges]

    # Stats
    mastered = [n for n in node_list if n["status"] == "mastered"]
    ready = [n for n in node_list if n["status"] == "ready"]
    total = len(node_list)
    mastered_count = len(mastered)
    ready_count = len(ready)
    overall_progress = round(mastered_count / total, 3) if total > 0 else 0

    # Recommended next: fallback chain so this is never empty
    recommended_next = None

    # 1. Outer fringe (ready to learn)
    if ready:
        rn = ready[0]
        prereq_ids = [rel[0] for rel in cache.get("relations", []) if rel[1] == rn["id"]]
        recommended_next = {
            "node_id": rn["id"],
            "label": rn["label"],
            "topic": rn["topic"],
            "prereqs_met": prereq_ids,
        }

    # 2. Any accessible node (prerequisites not yet met but available)
    if not recommended_next and student_state:
        available_nodes = [n for n in node_list if n["status"] == "available"]
        if available_nodes:
            an = available_nodes[0]
            recommended_next = {
                "node_id": an["id"],
                "label": an["label"],
                "topic": an["topic"],
                "prereqs_met": [],
            }

    # 3. Review due node
    if not recommended_next and reviews_due:
        rd = reviews_due[0]
        rd_node = next((n for n in node_list if n["id"] == rd["node_id"]), None)
        if rd_node:
            recommended_next = {
                "node_id": rd["node_id"],
                "label": rd["label"],
                "topic": rd_node.get("topic", ""),
                "prereqs_met": [],
            }

    # 4. First unmastered node in curriculum order
    if not recommended_next:
        unmastered = [n for n in node_list if n["status"] != "mastered"]
        if unmastered:
            un = unmastered[0]
            recommended_next = {
                "node_id": un["id"],
                "label": un["label"],
                "topic": un["topic"],
                "prereqs_met": [],
            }

    # Reviews due
    now = datetime.now(timezone.utc)
    reviews_due = []
    if student_state:
        due = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.next_review_at <= now,
        ).all()
        for r in due:
            node = next((n for n in node_list if n["id"] == r.node_id), None)
            if node:
                reviews_due.append({
                    "node_id": r.node_id,
                    "label": node["label"],
                    "mastered_at": r.mastered_at.isoformat(),
                    "interval": r.interval_days,
                    "streak": r.streak,
                })

    return {
        "knowledge_map": {
            "nodes": node_list,
            "edges": edge_list,
        },
        "stats": {
            "mastered_count": mastered_count,
            "ready_count": ready_count,
            "total_count": total,
            "overall_progress": overall_progress,
        },
        "recommended_next": recommended_next,
        "reviews_due": reviews_due,
        "placement_completed": student_state.placement_completed if student_state else False,
    }
