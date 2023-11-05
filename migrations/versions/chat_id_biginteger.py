from alembic import op
import sqlalchemy as sa
from webapp.enums import OrderStatus  # Import your enum class

revision = "sdfdsfdsfsdfs"  # Replace with your desired identifier
down_revision = "sdfsdfsddssdf"


def upgrade():
    op.alter_column(
        "account_buyer", "chat_id", existing_type=sa.Integer(), type_=sa.BigInteger
    )


def downgrade():
    # Downgrade is not implemented as it's not straightforward to remove enum values
    pass
