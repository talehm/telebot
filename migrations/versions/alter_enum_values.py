from alembic import op
import sqlalchemy as sa
from webapp.enums import OrderStatus  # Import your enum class

revision = 'vdfvfdnjfdsddsf'  # Replace with your desired identifier
down_revision = 'asddsfnu3274af'    

def upgrade():
    # Add the new enum values to the existing enum type
    op.execute("COMMIT")  # Needed for PostgreSQL
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'SS_SENT' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'WAITING_SS' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'SS_ACCEPTED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'SS_REJECTED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'CONFIRMED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'REJECTED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'DETAILS_SUBMITTED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'REVIEW_SUBMITTED' BEFORE 'COMPLETED'")
    op.execute(f"ALTER TYPE orderstatus ADD VALUE 'ORDER_SCREENSHOT_SENT' BEFORE 'COMPLETED'")

def downgrade():
    # Downgrade is not implemented as it's not straightforward to revert enum changes
    pass
