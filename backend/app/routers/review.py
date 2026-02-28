from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.services.review_service import (
    get_due_reviews,
    get_upcoming_reviews,
    start_review,
    submit_review,
)

router = APIRouter(prefix="/api/review", tags=["review"])


class ReviewSubmit(BaseModel):
    node_id: str
    problem_id: str
    answer: str


@router.get("/due")
def list_due_reviews(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_due_reviews(current_user.id, db)


@router.get("/upcoming")
def list_upcoming_reviews(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_upcoming_reviews(current_user.id, db)


@router.post("/{node_id}/start")
def start_node_review(
    node_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return start_review(current_user.id, node_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/submit")
def submit_review_answer(
    body: ReviewSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        from uuid import UUID
        return submit_review(
            current_user.id,
            body.node_id,
            UUID(body.problem_id),
            body.answer,
            db,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
