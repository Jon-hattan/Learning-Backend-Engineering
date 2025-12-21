"""baseline

Revision ID: 3a6db02afba9
Revises: 
Create Date: 2025-12-21 17:31:10.733030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel #ADD THIS HERE


# revision identifiers, used by Alembic.
revision: str = '3a6db02afba9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
