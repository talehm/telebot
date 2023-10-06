from alembic import op
import sqlalchemy as sa
from webapp.enums import OrderStatus  # Import your enum class

revision = 'asddsfnu3274af'  # Replace with your desired identifier
down_revision = 'ef1e65011d8c'
def upgrade():
    # Add the new enum values to the existing enum type
    op.execute("COMMIT")  # Needed for PostgreSQL
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'ORDER_SCREENSHOT_SENT' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'ORDER_WAITING_SCREENSHOT' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'ORDER_SCREENSHOT_ACCEPTED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'ORDER_SCREENSHOT_REJECTED' BEFORE 'COMPLETED'")
def downgrade():
    # Downgrade is not implemented as it's not straightforward to remove enum values
    pass
