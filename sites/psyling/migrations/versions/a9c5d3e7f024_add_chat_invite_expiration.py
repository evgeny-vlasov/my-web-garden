"""Add expiration to private chat invites.

Revision ID: a9c5d3e7f024
Revises: f8a4b2c6d913
Create Date: 2026-07-05 14:20:00
"""

from alembic import op
import sqlalchemy as sa


revision = "a9c5d3e7f024"
down_revision = "f8a4b2c6d913"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "chat_rooms", sa.Column("invite_expires_at", sa.DateTime(), nullable=True)
    )
    op.execute(
        """
        UPDATE chat_rooms
        SET invite_expires_at = COALESCE(invite_created_at, CURRENT_TIMESTAMP)
                                + INTERVAL '14 days'
        WHERE invite_token_hash IS NOT NULL
        """
    )
    op.create_index(
        "ix_chat_rooms_invite_expires_at", "chat_rooms", ["invite_expires_at"]
    )


def downgrade():
    op.drop_index("ix_chat_rooms_invite_expires_at", table_name="chat_rooms")
    op.drop_column("chat_rooms", "invite_expires_at")
