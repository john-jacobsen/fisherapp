from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database import get_db
from app.routers.auth import get_current_user
from app.models.user import User
from app.models.progress import StudentState, ReviewSchedule, Session as SessionModel, ResponseLog
from app.models.knowledge import KnowledgeGraph
from app.services.auth_service import hash_password, verify_password

router = APIRouter(prefix="/settings", tags=["settings"])


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "created_at": current_user.created_at.isoformat(),
    }


@router.patch("/profile")
def update_profile(
    body: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.name is not None:
        current_user.name = body.name
    if body.email is not None:
        # Check uniqueness
        existing = db.query(User).filter(User.email == body.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = body.email
    db.commit()
    return {"id": str(current_user.id), "email": current_user.email, "name": current_user.name}


@router.post("/change-password")
def change_password(
    body: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(body.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password_hash = hash_password(body.new_password)
    db.commit()
    return {"message": "Password updated"}


@router.post("/reset-progress")
def reset_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete all student progress: state, sessions, logs, review schedules."""
    # Delete review schedules
    db.query(ReviewSchedule).filter(ReviewSchedule.user_id == current_user.id).delete()
    # Delete response logs
    db.query(ResponseLog).filter(ResponseLog.user_id == current_user.id).delete()
    # Delete sessions
    db.query(SessionModel).filter(SessionModel.user_id == current_user.id).delete()
    # Delete student state
    db.query(StudentState).filter(StudentState.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Progress reset successfully"}
