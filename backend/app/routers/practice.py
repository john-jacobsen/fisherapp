from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.services import practice_service

router = APIRouter(prefix="/api/practice", tags=["practice"])


class SubmitRequest(BaseModel):
    session_id: str
    problem_id: str
    answer: str


class CompleteRequest(BaseModel):
    session_id: str


@router.post("/{node_id}/start")
def start_practice(
    node_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return practice_service.start_practice(node_id, str(current_user.id), db)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{node_id}/submit")
def submit_answer(
    node_id: str,
    req: SubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return practice_service.submit_practice_answer(
            node_id, req.session_id, req.problem_id, req.answer, str(current_user.id), db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{node_id}/hints/{problem_id}")
def get_hint(
    node_id: str,
    problem_id: str,
    level: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return practice_service.get_hint(node_id, problem_id, level, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{node_id}/complete")
def complete_practice(
    node_id: str,
    req: CompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return practice_service.complete_practice(
            node_id, req.session_id, str(current_user.id), db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
