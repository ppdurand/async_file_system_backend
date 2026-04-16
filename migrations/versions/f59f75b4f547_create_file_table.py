"""Create File Table

Revision ID: f59f75b4f547
Revises: 
Create Date: 2026-04-14 10:44:37.409574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f59f75b4f547'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'files',
        sa.Column('id', sa.String(length=36), primary_key=True, index=True),
        sa.Column('filename', sa.String(), index=True),
        sa.Column('filepath', sa.String(), index=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('file_hash', sa.String(length=64), nullable=True),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), default='uploaded'),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now())
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('files')
