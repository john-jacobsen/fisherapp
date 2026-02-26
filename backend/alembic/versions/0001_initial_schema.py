"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-02-25

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # knowledge_graphs first (no deps)
    op.create_table('knowledge_graphs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('graph_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # users (no deps)
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # knowledge_nodes (depends on knowledge_graphs)
    op.create_table('knowledge_nodes',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('graph_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic', sa.String(100), nullable=False),
        sa.Column('label', sa.String(255), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('display_x', sa.Float(), nullable=True),
        sa.Column('display_y', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['graph_id'], ['knowledge_graphs.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # knowledge_edges (depends on knowledge_nodes)
    op.create_table('knowledge_edges',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('graph_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('from_node_id', sa.String(50), nullable=False),
        sa.Column('to_node_id', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['from_node_id'], ['knowledge_nodes.id']),
        sa.ForeignKeyConstraint(['graph_id'], ['knowledge_graphs.id']),
        sa.ForeignKeyConstraint(['to_node_id'], ['knowledge_nodes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('graph_id', 'from_node_id', 'to_node_id')
    )

    # courses (depends on users, knowledge_graphs)
    op.create_table('courses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('instructor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('graph_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['graph_id'], ['knowledge_graphs.id']),
        sa.ForeignKeyConstraint(['instructor_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # course_enrollments
    op.create_table('course_enrollments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('course_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.ForeignKeyConstraint(['student_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'course_id')
    )

    # student_states
    op.create_table('student_states',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('graph_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('graph_version', sa.Integer(), nullable=False),
        sa.Column('state_distribution', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('mastered_nodes', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('outer_fringe', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('inner_fringe', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('placement_completed', sa.Boolean(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['graph_id'], ['knowledge_graphs.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # sessions
    op.create_table('sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_type', sa.String(20), nullable=False),
        sa.Column('node_id', sa.String(50), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('state_snapshot', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['knowledge_nodes.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # problems
    op.create_table('problems',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('node_id', sa.String(50), nullable=False),
        sa.Column('problem_text', sa.Text(), nullable=False),
        sa.Column('correct_answer', sa.Text(), nullable=False),
        sa.Column('answer_type', sa.String(20), nullable=True),
        sa.Column('difficulty', sa.Float(), nullable=True),
        sa.Column('source', sa.String(50), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['knowledge_nodes.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # hints
    op.create_table('hints',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('problem_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('hint_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('problem_id', 'level')
    )

    # lessons
    op.create_table('lessons',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('node_id', sa.String(50), nullable=False),
        sa.Column('video_url', sa.Text(), nullable=True),
        sa.Column('content_markdown', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['knowledge_nodes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('node_id')
    )

    # worked_examples
    op.create_table('worked_examples',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('node_id', sa.String(50), nullable=False),
        sa.Column('problem_text', sa.Text(), nullable=False),
        sa.Column('steps', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['knowledge_nodes.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # response_logs (depends on problems and sessions)
    op.create_table('response_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('node_id', sa.String(50), nullable=False),
        sa.Column('problem_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_type', sa.String(20), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('used_hint', sa.Boolean(), nullable=True),
        sa.Column('hint_level', sa.Integer(), nullable=True),
        sa.Column('used_ai', sa.Boolean(), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('student_answer', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['knowledge_nodes.id']),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id']),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # review_schedules
    op.create_table('review_schedules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('node_id', sa.String(50), nullable=False),
        sa.Column('mastered_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('next_review_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('interval_days', sa.Integer(), nullable=True),
        sa.Column('streak', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['node_id'], ['knowledge_nodes.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'node_id')
    )


def downgrade() -> None:
    op.drop_table('review_schedules')
    op.drop_table('response_logs')
    op.drop_table('worked_examples')
    op.drop_table('lessons')
    op.drop_table('hints')
    op.drop_table('problems')
    op.drop_table('sessions')
    op.drop_table('student_states')
    op.drop_table('course_enrollments')
    op.drop_table('courses')
    op.drop_table('knowledge_edges')
    op.drop_table('knowledge_nodes')
    op.drop_table('users')
    op.drop_table('knowledge_graphs')
