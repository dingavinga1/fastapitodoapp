"""Fixed pwd

Revision ID: eb5e6a501324
Revises: ee9044ef9202
Create Date: 2024-08-26 11:29:00.633455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb5e6a501324'
down_revision: Union[str, None] = 'ee9044ef9202'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=300),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###