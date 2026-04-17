"""retirando campo da tabela

Revision ID: 3f04961c2df6
Revises: f59f75b4f547
Create Date: 2026-04-16 23:48:32.519951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f04961c2df6'
down_revision: Union[str, Sequence[str], None] = 'f59f75b4f547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("files", "mime_type")


def downgrade() -> None:
    op.add_column(
        "files",
        sa.Column("file_hash", sa.String(length=64), nullable=True)
    )
