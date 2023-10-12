"""Create initial tables

Revision ID: 0361a1290b7a
Revises: 
Create Date: 2023-10-12 16:19:38.735164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0361a1290b7a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE items (
            id serial PRIMARY KEY,
            name TEXT,
            price NUMERIC(16,2)
        );
    """
    )
    pass


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE items;
        """
    )
    pass
