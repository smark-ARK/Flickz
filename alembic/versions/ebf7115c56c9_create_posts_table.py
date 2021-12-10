"""create posts table

Revision ID: ebf7115c56c9
Revises: 
Create Date: 2021-12-10 15:26:52.463758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ebf7115c56c9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
