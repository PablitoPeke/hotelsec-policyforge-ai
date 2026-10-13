"""Persistent global daily and per-user hourly AI ceilings."""
from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("ai_usage",
        sa.Column("bucket", sa.String(100), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("used", sa.Integer, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_ai_usage_owner_id", "ai_usage", ["owner_id"])
    op.create_index("ix_ai_usage_expires_at", "ai_usage", ["expires_at"])


def downgrade():
    op.drop_table("ai_usage")
