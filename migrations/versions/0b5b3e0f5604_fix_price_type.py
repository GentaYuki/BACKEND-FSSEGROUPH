"""fix price type

Revision ID: 0b5b3e0f5604
Revises: 4dbaf5ec8dc9
Create Date: 2024-12-18 13:58:36.307119

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0b5b3e0f5604'
down_revision = '4dbaf5ec8dc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=mysql.DECIMAL(precision=10, scale=2),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Integer(),
               type_=mysql.DECIMAL(precision=10, scale=2),
               existing_nullable=False)

    # ### end Alembic commands ###