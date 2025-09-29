"""Initial schema

Revision ID: 20240528_01
Revises: 
Create Date: 2024-05-28
"""

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.create_table(
        "applicants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("target_schools", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_applicants_email", "applicants", ["email"])
    op.create_index("ix_applicants_id", "applicants", ["id"])

    op.create_table(
        "academic_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("applicant_id", sa.Integer(), nullable=False),
        sa.Column("school_name", sa.String(), nullable=False),
        sa.Column("gpa", sa.Float(), nullable=True),
        sa.Column("test_scores", sa.String(), nullable=True),
        sa.Column("coursework", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["applicant_id"], ["applicants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_academic_records_id", "academic_records", ["id"])

    op.create_table(
        "extracurriculars",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("applicant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("impact", sa.String(), nullable=True),
        sa.Column("duration", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["applicant_id"], ["applicants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_extracurriculars_id", "extracurriculars", ["id"])

    op.create_table(
        "essays",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("applicant_id", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["applicant_id"], ["applicants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_essays_id", "essays", ["id"])

    op.create_table(
        "evaluations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("applicant_id", sa.Integer(), nullable=False),
        sa.Column("essay_id", sa.Integer(), nullable=True),
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("scores", sa.JSON(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("recommendations", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["applicant_id"], ["applicants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["essay_id"], ["essays.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_evaluations_id", "evaluations", ["id"])

    op.create_table(
        "milestones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("applicant_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["applicant_id"], ["applicants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_milestones_id", "milestones", ["id"])

    op.create_table(
        "suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("evaluation_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("impact", sa.String(), nullable=True),
        sa.Column("effort", sa.String(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
        sa.ForeignKeyConstraint(["evaluation_id"], ["evaluations.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_suggestions_id", "suggestions", ["id"])


def downgrade() -> None:
    op.drop_index("ix_suggestions_id", table_name="suggestions")
    op.drop_table("suggestions")
    op.drop_index("ix_milestones_id", table_name="milestones")
    op.drop_table("milestones")
    op.drop_index("ix_evaluations_id", table_name="evaluations")
    op.drop_table("evaluations")
    op.drop_index("ix_essays_id", table_name="essays")
    op.drop_table("essays")
    op.drop_index("ix_extracurriculars_id", table_name="extracurriculars")
    op.drop_table("extracurriculars")
    op.drop_index("ix_academic_records_id", table_name="academic_records")
    op.drop_table("academic_records")
    op.drop_index("ix_applicants_id", table_name="applicants")
    op.drop_index("ix_applicants_email", table_name="applicants")
    op.drop_table("applicants")
