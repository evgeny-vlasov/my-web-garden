"""Add private client chat rooms and messages.

Revision ID: f8a4b2c6d913
Revises: e7f3a9b1c402
Create Date: 2026-07-05 14:05:00
"""

from alembic import op
import sqlalchemy as sa


revision = "f8a4b2c6d913"
down_revision = "e7f3a9b1c402"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat_rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("invite_token_hash", sa.String(length=64), nullable=True),
        sa.Column("invite_created_at", sa.DateTime(), nullable=True),
        sa.Column("invite_last_used_at", sa.DateTime(), nullable=True),
        sa.Column("client_access_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("access_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("archived_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("status IN ('active', 'closed', 'archived')", name="ck_chat_rooms_status"),
        sa.CheckConstraint("access_version >= 1", name="ck_chat_rooms_access_version_positive"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invite_token_hash"),
    )
    op.create_index("ix_chat_rooms_client_id", "chat_rooms", ["client_id"])
    op.create_index("ix_chat_rooms_status", "chat_rooms", ["status"])
    op.create_index("ix_chat_rooms_invite_token_hash", "chat_rooms", ["invite_token_hash"])
    op.create_index("ix_chat_rooms_created_by_user_id", "chat_rooms", ["created_by_user_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("sender_type", sa.String(length=20), nullable=False),
        sa.Column("sender_user_id", sa.Integer(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("read_by_admin_at", sa.DateTime(), nullable=True),
        sa.Column("read_by_client_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("sender_type IN ('admin', 'client')", name="ck_chat_messages_sender_type"),
        sa.CheckConstraint("length(trim(body)) > 0", name="ck_chat_messages_body_not_blank"),
        sa.CheckConstraint(
            "(sender_type = 'admin' AND sender_user_id IS NOT NULL) OR "
            "(sender_type = 'client' AND sender_user_id IS NULL)",
            name="ck_chat_messages_sender_user",
        ),
        sa.ForeignKeyConstraint(["room_id"], ["chat_rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_chat_messages_room_id", "chat_messages", ["room_id"])
    op.create_index("ix_chat_messages_sender_user_id", "chat_messages", ["sender_user_id"])
    op.create_index("ix_chat_messages_created_at", "chat_messages", ["created_at"])
    op.create_index("ix_chat_messages_room_created", "chat_messages", ["room_id", "created_at", "id"])


def downgrade():
    op.drop_index("ix_chat_messages_room_created", table_name="chat_messages")
    op.drop_index("ix_chat_messages_created_at", table_name="chat_messages")
    op.drop_index("ix_chat_messages_sender_user_id", table_name="chat_messages")
    op.drop_index("ix_chat_messages_room_id", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index("ix_chat_rooms_created_by_user_id", table_name="chat_rooms")
    op.drop_index("ix_chat_rooms_invite_token_hash", table_name="chat_rooms")
    op.drop_index("ix_chat_rooms_status", table_name="chat_rooms")
    op.drop_index("ix_chat_rooms_client_id", table_name="chat_rooms")
    op.drop_table("chat_rooms")
