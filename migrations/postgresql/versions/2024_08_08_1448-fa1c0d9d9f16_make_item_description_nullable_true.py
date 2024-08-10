"""make item.description nullable=True

Revision ID: fa1c0d9d9f16
Revises: 1fde873990a3
Create Date: 2024-08-08 14:48:40.335147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa1c0d9d9f16'
down_revision: Union[str, None] = '1fde873990a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###