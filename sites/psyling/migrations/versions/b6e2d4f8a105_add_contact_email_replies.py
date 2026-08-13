"""Add stored admin email replies for contact submissions.

Revision ID: b6e2d4f8a105
Revises: a9c5d3e7f024
Create Date: 2026-08-13 21:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "b6e2d4f8a105"
down_revision = "a9c5d3e7f024"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "contact_email_replies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("contact_submission_id", sa.Integer(), nullable=False),
        sa.Column("sender_user_id", sa.Integer(), nullable=True),
        sa.Column("subject", sa.String(length=200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("recipient", sa.String(length=120), nullable=False),
        sa.Column(
            "status", sa.String(length=20), nullable=False,
            server_default="pending",
        ),
        sa.Column("idempotency_key", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "status IN ('pending', 'sent', 'failed')",
            name="ck_contact_email_replies_status",
        ),
        sa.CheckConstraint(
            "length(trim(subject)) > 0",
            name="ck_contact_email_replies_subject_not_blank",
        ),
        sa.CheckConstraint(
            "length(trim(body)) > 0",
            name="ck_contact_email_replies_body_not_blank",
        ),
        sa.CheckConstraint(
            "(status = 'sent' AND sent_at IS NOT NULL) OR "
            "(status <> 'sent' AND sent_at IS NULL)",
            name="ck_contact_email_replies_sent_timestamp",
        ),
        sa.ForeignKeyConstraint(
            ["contact_submission_id"], ["contact_submissions.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sender_user_id"], ["users.id"], ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "idempotency_key", name="uq_contact_email_replies_idempotency_key"
        ),
    )
    op.create_index(
        "ix_contact_email_replies_contact_submission_id",
        "contact_email_replies", ["contact_submission_id"],
    )
    op.create_index(
        "ix_contact_email_replies_sender_user_id",
        "contact_email_replies", ["sender_user_id"],
    )
    op.create_index(
        "ix_contact_email_replies_status",
        "contact_email_replies", ["status"],
    )
    op.create_index(
        "ix_contact_email_replies_created_at",
        "contact_email_replies", ["created_at"],
    )
    op.create_index(
        "ix_contact_email_replies_contact_created",
        "contact_email_replies", ["contact_submission_id", "created_at", "id"],
    )


def downgrade():
    op.drop_index(
        "ix_contact_email_replies_contact_created",
        table_name="contact_email_replies",
    )
    op.drop_index(
        "ix_contact_email_replies_created_at", table_name="contact_email_replies"
    )
    op.drop_index(
        "ix_contact_email_replies_status", table_name="contact_email_replies"
    )
    op.drop_index(
        "ix_contact_email_replies_sender_user_id",
        table_name="contact_email_replies",
    )
    op.drop_index(
        "ix_contact_email_replies_contact_submission_id",
        table_name="contact_email_replies",
    )
    op.drop_table("contact_email_replies")
