from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.services import placement_service

router = APIRouter(prefix="/api/placement", tags=["placement"])


class SubmitRequest(BaseModel):
    session_id: str
    problem_id: str
    answer: str


@router.post("/start")
def start_placement(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return placement_service.start_placement(str(current_user.id), db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submit")
def submit_answer(
    req: SubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return placement_service.submit_answer(
            req.session_id, req.problem_id, req.answer, str(current_user.id), db
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/results")
def get_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return placement_service.get_results(str(current_user.id), db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
