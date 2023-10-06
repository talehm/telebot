"""empty message

Revision ID: d6b4f2845335
Revises: 4d785a64914f
Create Date: 2023-05-13 13:54:37.954147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6b4f2845335'
down_revision = '4d785a64914f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_seller', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chat_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_seller', schema=None) as batch_op:
        batch_op.drop_column('chat_id')

    # ### end Alembic commands ###
