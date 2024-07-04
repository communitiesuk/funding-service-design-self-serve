"""empty message

Revision ID: 7691cc286d3c
Revises: e88df5a3b683
Create Date: 2024-07-04 11:37:53.767253

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7691cc286d3c"
down_revision = "e88df5a3b683"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.add_column(sa.Column("index", sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("section", schema=None) as batch_op:
        batch_op.drop_column("index")

    # ### end Alembic commands ###