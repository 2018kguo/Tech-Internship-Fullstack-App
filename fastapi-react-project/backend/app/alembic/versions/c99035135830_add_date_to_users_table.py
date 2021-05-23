"""add_date_to_users_table

Revision ID: c99035135830
Revises: ace77908feb6
Create Date: 2021-05-22 11:37:37.663329-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c99035135830'
down_revision = 'ace77908feb6'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("jobs")
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("company", sa.String(50), nullable=False),
        sa.Column("link", sa.String(300), nullable=False),
        sa.Column("description", sa.String(1000)),
        sa.Column("date_posted", sa.DateTime())
    )


def downgrade():
    pass
