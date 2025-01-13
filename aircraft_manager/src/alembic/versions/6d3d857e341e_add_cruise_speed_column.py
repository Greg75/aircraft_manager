"""add cruise_speed column

Revision ID: 6d3d857e341e
Revises: c6f01ba61cf8
Create Date: 2024-12-03 21:06:28.132479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d3d857e341e'
down_revision: Union[str, None] = 'c6f01ba61cf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(table_name='aircrafts_data', column=sa.Column(name='cruise_speed', type_=sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column(table_name='aircrafts_data', column_name='cruise_speed')
