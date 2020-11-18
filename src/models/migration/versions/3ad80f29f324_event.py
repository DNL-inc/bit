"""Event

Revision ID: 3ad80f29f324
Revises: 28e3ab1a0e03
Create Date: 2020-11-18 14:20:40.614779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad80f29f324'
down_revision = '28e3ab1a0e03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.Column('faculty', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faculty'], ['faculties.id'], ),
    sa.ForeignKeyConstraint(['group'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###