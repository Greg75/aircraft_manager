"""aircraft_type name change

Revision ID: 9048202cb7c2
Revises: ebc5478e47c1
Create Date: 2024-12-03 16:22:46.810990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9048202cb7c2'
down_revision: Union[str, None] = 'ebc5478e47c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(table_name='aircrafts_data',
                    column_name='combat_radius',
                    new_column_name='fuel_consumption',
                    type_=sa.Integer)


def downgrade() -> None:
    op.alter_column(table_name='aircrafts_data',
                    column_name='fuel_consumption',
                    new_column_name='combat_radius',
                    type_=sa.Integer)
