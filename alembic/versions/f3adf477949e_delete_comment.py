"""delete comment

Revision ID: f3adf477949e
Revises: e49d90e01d5f
Create Date: 2023-07-09 11:07:20.099127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3adf477949e'
down_revision = 'e49d90e01d5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='comments_post_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='comments_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_id', 'post_id', name='comments_pkey')
    )
    # ### end Alembic commands ###