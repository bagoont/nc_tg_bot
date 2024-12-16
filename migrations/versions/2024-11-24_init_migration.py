"""Init migration.

Revision ID: 1a06c7f821a2
Revises:
Create Date: 2024-11-24 14:58:12.522011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a06c7f821a2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('language', sa.String(length=3), nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=False),
    sa.Column('tg_name', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('app_password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('tg_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###