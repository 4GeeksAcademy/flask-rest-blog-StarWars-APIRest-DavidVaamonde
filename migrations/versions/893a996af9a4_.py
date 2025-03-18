"""empty message

Revision ID: 893a996af9a4
Revises: 6e5ee30b33f6
Create Date: 2025-03-18 22:20:49.432143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '893a996af9a4'
down_revision = '6e5ee30b33f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('homeworld', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('population', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))

    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('model', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('model')
        batch_op.drop_column('name')

    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('type')
        batch_op.drop_column('name')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('population')
        batch_op.drop_column('name')

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('homeworld')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
