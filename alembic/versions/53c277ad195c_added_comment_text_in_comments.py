"""added comment text in comments

Revision ID: 53c277ad195c
Revises: f4ac83a4f517
Create Date: 2023-06-01 18:34:43.814444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53c277ad195c'
down_revision = 'f4ac83a4f517'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('comment', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'comment')
    # ### end Alembic commands ###
