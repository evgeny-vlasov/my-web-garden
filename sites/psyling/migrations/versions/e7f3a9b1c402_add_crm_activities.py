"""Add private CRM activities and follow-up tasks.

Revision ID: e7f3a9b1c402
Revises: d4e6a8c2f901
Create Date: 2026-07-05 13:55:00
"""

from alembic import op
import sqlalchemy as sa


revision = "e7f3a9b1c402"
down_revision = "d4e6a8c2f901"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "crm_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.Column("contact_submission_id", sa.Integer(), nullable=True),
        sa.Column("actor_user_id", sa.Integer(), nullable=True),
        sa.Column("activity_type", sa.String(length=20), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("due_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "(client_id IS NOT NULL) <> (contact_submission_id IS NOT NULL)",
            name="ck_crm_activities_exactly_one_parent",
        ),
        sa.CheckConstraint(
            "activity_type IN ('note', 'call', 'email', 'voicemail', "
            "'appointment', 'follow_up', 'other')",
            name="ck_crm_activities_type",
        ),
        sa.CheckConstraint(
            "length(trim(body)) > 0", name="ck_crm_activities_body_not_blank"
        ),
        sa.CheckConstraint(
            "completed_at IS NULL OR due_at IS NOT NULL OR activity_type = 'follow_up'",
            name="ck_crm_activities_completion_relevant",
        ),
        sa.ForeignKeyConstraint(
            ["client_id"], ["clients.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["contact_submission_id"], ["contact_submissions.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["actor_user_id"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crm_activities_client_id", "crm_activities", ["client_id"])
    op.create_index(
        "ix_crm_activities_contact_submission_id", "crm_activities",
        ["contact_submission_id"],
    )
    op.create_index(
        "ix_crm_activities_actor_user_id", "crm_activities", ["actor_user_id"]
    )
    op.create_index("ix_crm_activities_due_at", "crm_activities", ["due_at"])
    op.create_index(
        "ix_crm_activities_open_followups",
        "crm_activities",
        ["due_at"],
        postgresql_where=sa.text(
            "completed_at IS NULL AND (due_at IS NOT NULL OR activity_type = 'follow_up')"
        ),
    )


def downgrade():
    op.drop_index("ix_crm_activities_open_followups", table_name="crm_activities")
    op.drop_index("ix_crm_activities_due_at", table_name="crm_activities")
    op.drop_index("ix_crm_activities_actor_user_id", table_name="crm_activities")
    op.drop_index(
        "ix_crm_activities_contact_submission_id", table_name="crm_activities"
    )
    op.drop_index("ix_crm_activities_client_id", table_name="crm_activities")
    op.drop_table("crm_activities")
