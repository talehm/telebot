"""product properties

Revision ID: d439b342d45d
Revises: 357ab64c0cdb
Create Date: 2023-05-09 00:14:17.139428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd439b342d45d'
down_revision = '357ab64c0cdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_buyer', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['chat_id'])

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('properties', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('properties')

    with op.batch_alter_table('account_buyer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
