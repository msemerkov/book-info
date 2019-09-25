"""create book table

Revision ID: 23cfc5ce4383
Revises: 
Create Date: 2019-09-15 16:34:40.803789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23cfc5ce4383'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('author', sa.String),
        sa.Column('rating', sa.Integer),
        sa.Column('date_reading', sa.Date),
    )


def downgrade():
    op.drop_table('books')
