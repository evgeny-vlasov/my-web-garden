"""Add Phase 1 CRM fields to contact submissions.

Revision ID: c1a4f2e8b7d3
Revises: 05d9d55a08f1
Create Date: 2026-07-04 21:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "c1a4f2e8b7d3"
down_revision = "05d9d55a08f1"
branch_labels = None
depends_on = None


ALLOWED_STATUSES = "'new', 'contacted', 'booked', 'closed', 'spam'"


def upgrade():
    op.add_column(
        "contact_submissions",
        sa.Column(
            "is_read",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "contact_submissions",
        sa.Column("follow_up_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "contact_submissions",
        sa.Column("last_contacted_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "contact_submissions",
        sa.Column("archived_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "contact_submissions",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    # Preserve the known meaning of legacy values: read/responded records were
    # viewed, but neither value reliably proves that the client was contacted.
    op.execute(
        """UPDATE contact_submissions
           SET is_read = true
           WHERE status IN ('read', 'responded')"""
    )
    op.execute(
        """UPDATE contact_submissions
           SET status = CASE
               WHEN is_spam IS TRUE THEN 'spam'
               WHEN status IN ('read', 'responded') OR status IS NULL THEN 'new'
               ELSE status
           END"""
    )

    op.alter_column(
        "contact_submissions",
        "status",
        existing_type=sa.String(length=20),
        nullable=False,
        server_default="new",
    )
    op.create_check_constraint(
        "ck_contact_submissions_status",
        "contact_submissions",
        f"status IN ({ALLOWED_STATUSES})",
    )
    op.create_index(
        "ix_contact_submissions_status",
        "contact_submissions",
        ["status"],
    )
    op.create_index(
        "ix_contact_submissions_follow_up_at",
        "contact_submissions",
        ["follow_up_at"],
    )
    op.create_index(
        "ix_contact_submissions_archived_at",
        "contact_submissions",
        ["archived_at"],
    )


def downgrade():
    op.drop_index("ix_contact_submissions_archived_at", table_name="contact_submissions")
    op.drop_index("ix_contact_submissions_follow_up_at", table_name="contact_submissions")
    op.drop_index("ix_contact_submissions_status", table_name="contact_submissions")
    op.drop_constraint(
        "ck_contact_submissions_status",
        "contact_submissions",
        type_="check",
    )
    op.execute(
        """UPDATE contact_submissions
           SET status = CASE
               WHEN status = 'spam' THEN 'new'
               WHEN status IN ('contacted', 'booked', 'closed') THEN 'responded'
               ELSE status
           END"""
    )
    op.alter_column(
        "contact_submissions",
        "status",
        existing_type=sa.String(length=20),
        nullable=True,
        server_default=None,
    )
    op.drop_column("contact_submissions", "updated_at")
    op.drop_column("contact_submissions", "archived_at")
    op.drop_column("contact_submissions", "last_contacted_at")
    op.drop_column("contact_submissions", "follow_up_at")
    op.drop_column("contact_submissions", "is_read")

