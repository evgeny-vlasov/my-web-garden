"""Add client records and contact-to-client linking.

Revision ID: d4e6a8c2f901
Revises: c1a4f2e8b7d3
Create Date: 2026-07-05 00:15:00
"""

from alembic import op
import sqlalchemy as sa


revision = "d4e6a8c2f901"
down_revision = "c1a4f2e8b7d3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column(
            "preferred_contact_method",
            sa.String(length=20),
            nullable=False,
            server_default="none",
        ),
        sa.Column(
            "language",
            sa.String(length=20),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="active",
        ),
        sa.Column("private_notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "preferred_contact_method IN ('email', 'phone', 'text', 'none')",
            name="ck_clients_preferred_contact_method",
        ),
        sa.CheckConstraint(
            "language IN ('en', 'ru', 'other', 'unknown')",
            name="ck_clients_language",
        ),
        sa.CheckConstraint(
            "status IN ('active', 'inactive', 'archived')",
            name="ck_clients_status",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_clients_status", "clients", ["status"])

    op.add_column(
        "contact_submissions",
        sa.Column("client_id", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_contact_submissions_client_id",
        "contact_submissions",
        ["client_id"],
    )
    op.create_foreign_key(
        "fk_contact_submissions_client_id_clients",
        "contact_submissions",
        "clients",
        ["client_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    op.drop_constraint(
        "fk_contact_submissions_client_id_clients",
        "contact_submissions",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_contact_submissions_client_id",
        table_name="contact_submissions",
    )
    op.drop_column("contact_submissions", "client_id")
    op.drop_index("ix_clients_status", table_name="clients")
    op.drop_table("clients")

