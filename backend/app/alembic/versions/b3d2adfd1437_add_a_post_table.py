"""Add a post table

Revision ID: b3d2adfd1437
Revises: 91979b40eb38
Create Date: 2020-11-19 12:17:01.026418-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3d2adfd1437'
down_revision = '91979b40eb38'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "post",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(256)),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("image_url", sa.String, nullable=False),
        sa.Column("source_url", sa.String),
        sa.Column("content", sa.String),
        sa.Column("created", sa.DateTime),
    )


def downgrade():
    op.drop_table("post")
