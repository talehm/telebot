from alembic import op
import sqlalchemy as sa
from webapp.enums import OrderStatus  # Import your enum class

revision = 'sdfsdfsddssdf'  # Replace with your desired identifier
down_revision = 'vdfvfdnjfdsddsf'    

def upgrade():
    # Add the new enum values to the existing enum type
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'ORDER_SCREENSHOT_SENT' BEFORE 'COMPLETED'")

def downgrade():
    # Downgrade is not implemented as it's not straightforward to revert enum changes
    pass
