"""change character limits for jobs table fields

Revision ID: 78765a73cbff
Revises: c99035135830
Create Date: 2021-05-26 12:32:08.412818-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78765a73cbff'
down_revision = 'c99035135830'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("jobs")
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("company", sa.String(100), nullable=False),
        sa.Column("link", sa.String(1000), nullable=False),
        sa.Column("description", sa.String(5000)),
        sa.Column("date_posted", sa.DateTime())
    )


def downgrade():
    pass
