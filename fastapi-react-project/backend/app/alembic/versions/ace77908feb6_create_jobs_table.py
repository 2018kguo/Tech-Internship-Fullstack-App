"""create_jobs_table

Revision ID: ace77908feb6
Revises: 91979b40eb38
Create Date: 2021-04-24 12:50:19.077881-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ace77908feb6'
down_revision = '91979b40eb38'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("company", sa.String(50), nullable=False),
        sa.Column("link", sa.String(300), nullable=False),
        sa.Column("description", sa.String(1000))
    )


def downgrade():
    op.drop_table("jobs")
