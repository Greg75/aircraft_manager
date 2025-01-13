"""armament_weight name change

Revision ID: c6f01ba61cf8
Revises: 9048202cb7c2
Create Date: 2024-12-03 16:59:33.727391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c6f01ba61cf8'
down_revision: Union[str, None] = '9048202cb7c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(table_name='aircrafts_data',
                    column_name='armament_weight',
                    new_column_name='fuel',
                    type_=sa.Integer)


def downgrade() -> None:
    op.alter_column(table_name='aircrafts_data',
                    column_name='fuel',
                    new_column_name='armament_weight',
                    type_=sa.Integer)
