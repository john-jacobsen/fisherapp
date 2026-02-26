import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Integer, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.user import utcnow


class KnowledgeGraph(Base):
    __tablename__ = "knowledge_graphs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    graph_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    nodes = relationship("KnowledgeNode", back_populates="graph")
    edges = relationship("KnowledgeEdge", back_populates="graph")
    student_states = relationship("StudentState", back_populates="graph")


class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    graph_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_graphs.id"), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    display_x: Mapped[float] = mapped_column(Float, nullable=True)
    display_y: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    graph = relationship("KnowledgeGraph", back_populates="nodes")
    outgoing_edges = relationship("KnowledgeEdge", foreign_keys="KnowledgeEdge.from_node_id", back_populates="from_node")
    incoming_edges = relationship("KnowledgeEdge", foreign_keys="KnowledgeEdge.to_node_id", back_populates="to_node")
    problems = relationship("Problem", back_populates="node")
    lesson = relationship("Lesson", back_populates="node", uselist=False)
    worked_examples = relationship("WorkedExample", back_populates="node")


class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"
    __table_args__ = (UniqueConstraint("graph_id", "from_node_id", "to_node_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    graph_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("knowledge_graphs.id"), nullable=False)
    from_node_id: Mapped[str] = mapped_column(String(50), ForeignKey("knowledge_nodes.id"), nullable=False)
    to_node_id: Mapped[str] = mapped_column(String(50), ForeignKey("knowledge_nodes.id"), nullable=False)

    graph = relationship("KnowledgeGraph", back_populates="edges")
    from_node = relationship("KnowledgeNode", foreign_keys=[from_node_id], back_populates="outgoing_edges")
    to_node = relationship("KnowledgeNode", foreign_keys=[to_node_id], back_populates="incoming_edges")
