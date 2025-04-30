"""add_content_column

Revision ID: 52a668bbe6eb
Revises: 5e1e8629e8fa
Create Date: 2025-04-30 20:32:02.456320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52a668bbe6eb'
down_revision: Union[str, None] = '5e1e8629e8fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
