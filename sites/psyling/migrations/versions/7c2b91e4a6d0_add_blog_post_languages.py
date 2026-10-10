"""Add language and linked translation fields to blog posts.

Revision ID: 7c2b91e4a6d0
Revises: b6e2d4f8a105
Create Date: 2026-10-10 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "7c2b91e4a6d0"
down_revision = "b6e2d4f8a105"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "blog_posts",
        sa.Column("language", sa.String(length=2), server_default="en", nullable=False),
    )
    op.add_column(
        "blog_posts", sa.Column("translation_id", sa.Integer(), nullable=True)
    )
    op.create_check_constraint(
        "ck_blog_posts_language", "blog_posts", "language IN ('en', 'ru')"
    )
    op.create_check_constraint(
        "ck_blog_posts_translation_not_self",
        "blog_posts",
        "translation_id IS NULL OR translation_id <> id",
    )
    op.create_foreign_key(
        "fk_blog_posts_translation_id",
        "blog_posts",
        "blog_posts",
        ["translation_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_blog_posts_language", "blog_posts", ["language"])
    op.create_index(
        "ix_blog_posts_translation_id",
        "blog_posts",
        ["translation_id"],
        unique=True,
    )


def downgrade():
    op.drop_index("ix_blog_posts_translation_id", table_name="blog_posts")
    op.drop_index("ix_blog_posts_language", table_name="blog_posts")
    op.drop_constraint(
        "fk_blog_posts_translation_id", "blog_posts", type_="foreignkey"
    )
    op.drop_constraint(
        "ck_blog_posts_translation_not_self", "blog_posts", type_="check"
    )
    op.drop_constraint("ck_blog_posts_language", "blog_posts", type_="check")
    op.drop_column("blog_posts", "translation_id")
    op.drop_column("blog_posts", "language")
