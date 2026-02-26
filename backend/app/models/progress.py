import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.user import utcnow


class StudentState(Base):
    __tablename__ = "student_states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    graph_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_graphs.id"), nullable=False)
    graph_version: Mapped[int] = mapped_column(Integer, nullable=False)
    state_distribution: Mapped[dict] = mapped_column(JSONB, nullable=False)
    mastered_nodes: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    outer_fringe: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    inner_fringe: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    placement_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="student_states")
    graph = relationship("KnowledgeGraph", back_populates="student_states")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_type: Mapped[str] = mapped_column(String(20), nullable=False)
    node_id: Mapped[str] = mapped_column(String(50), ForeignKey("knowledge_nodes.id"), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    state_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")
    response_logs = relationship("ResponseLog", back_populates="session")


class ResponseLog(Base):
    __tablename__ = "response_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    node_id: Mapped[str] = mapped_column(String(50), ForeignKey("knowledge_nodes.id"), nullable=False)
    problem_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    session_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    used_hint: Mapped[bool] = mapped_column(Boolean, default=False)
    hint_level: Mapped[int] = mapped_column(Integer, default=0)
    used_ai: Mapped[bool] = mapped_column(Boolean, default=False)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    student_answer: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user = relationship("User", back_populates="response_logs")
    session = relationship("Session", back_populates="response_logs")


class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    node_id: Mapped[str] = mapped_column(String(50), ForeignKey("knowledge_nodes.id"), nullable=False)
    mastered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    next_review_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    interval_days: Mapped[int] = mapped_column(Integer, default=1)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="review_schedules")
