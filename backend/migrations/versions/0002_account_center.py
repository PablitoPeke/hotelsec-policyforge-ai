"""Editable profiles and safe public session identifiers."""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("organization_name", sa.String(120), nullable=False, server_default=""))
    op.add_column("users", sa.Column("job_title", sa.String(120), nullable=False, server_default=""))
    op.add_column("users", sa.Column("email_verified_at", sa.DateTime(timezone=True)))
    op.add_column("login_sessions", sa.Column("public_id", sa.String(36)))
    # Legacy session creation times are unknown; do not invent them during migration.
    op.add_column("login_sessions", sa.Column("created_at", sa.DateTime(timezone=True)))
    op.add_column("login_sessions", sa.Column("device_label", sa.String(80), nullable=False, server_default="Sesion anterior"))
    connection = op.get_bind()
    sessions = sa.table("login_sessions", sa.column("token_hash", sa.String), sa.column("public_id", sa.String))
    for token_hash in connection.execute(sa.select(sessions.c.token_hash)).scalars().all():
        connection.execute(sessions.update().where(sessions.c.token_hash == token_hash).values(public_id=str(uuid4())))
    with op.batch_alter_table("login_sessions") as batch:
        fallback = sa.text("gen_random_uuid()::text") if connection.dialect.name == "postgresql" else sa.text("(lower(hex(randomblob(16))))")
        batch.alter_column("public_id", existing_type=sa.String(36), nullable=False, server_default=fallback)
        batch.create_index("ix_login_sessions_public_id", ["public_id"], unique=True)


def downgrade():
    with op.batch_alter_table("login_sessions") as batch:
        batch.drop_index("ix_login_sessions_public_id")
        for column in ("device_label", "created_at", "public_id"):
            batch.drop_column(column)
    for column in ("email_verified_at", "job_title", "organization_name"):
        op.drop_column("users", column)
