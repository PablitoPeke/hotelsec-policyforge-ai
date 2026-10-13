"""Hashed, expiring, single-use account email tokens."""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("account_tokens",
        sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(30), nullable=False),
        sa.Column("issued_email", sa.String(254), nullable=False),
        sa.Column("target_email", sa.String(254), nullable=False),
        sa.Column("change_id", sa.String(36)),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True)))
    for column in ("user_id", "change_id", "expires_at"):
        op.create_index(f"ix_account_tokens_{column}", "account_tokens", [column])


def downgrade():
    op.drop_table("account_tokens")
