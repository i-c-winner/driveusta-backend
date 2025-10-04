"""First

Revision ID: e52e9111db30
Revises: 4dad747bdd17_create_schemas
Create Date: 2025-10-03 23:34:26.056478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e52e9111db30'
down_revision: Union[str, Sequence[str], None] = '4dad747bdd17_create_schemas'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
