"""order review_Screenshit


Revision ID: 6368f20b35f7
Revises: 
Create Date: 2023-11-05 23:25:35.690161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1212312312312"
down_revision = "6368f20b35f7"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE OrderStatus ADD VALUE 'REVIEW_ACCEPTED'")
    op.execute("ALTER TYPE OrderStatus ADD VALUE 'REVIEW_REJECTED'")
    # op.execute("ALTER TYPE OrderStatus DROP VALUE 'DETAILS_SUBMITTED'")

    # ### end Alembic commands ###


# Define the downgrade function
def downgrade():
    op.execute("ALTER TYPE OrderStatus DROP VALUE 'new_value'")

    # ### end Alembic commands ###
