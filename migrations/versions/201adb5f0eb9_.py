"""empty message

Revision ID: 201adb5f0eb9
Revises: 1f59b60711b6
Create Date: 2024-08-05 22:25:50.603906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '201adb5f0eb9'
down_revision: Union[str, None] = '1f59b60711b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proofShot', sa.Column('photoName', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proofShot', 'photoName')
    # ### end Alembic commands ###
