"""Init DB

Revision ID: 37394f735b32
Revises: 
Create Date: 2019-09-29 18:27:43.083034+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37394f735b32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('profile_id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('profile_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('document',
    sa.Column('document_id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('profile_id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('title', sa.VARCHAR(length=128), nullable=True),
    sa.Column('filename', sa.VARCHAR(length=256), nullable=False),
    sa.Column('filesize', sa.INTEGER(), nullable=False),
    sa.Column('digest', sa.VARCHAR(length=32), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.profile_id'], ),
    sa.PrimaryKeyConstraint('document_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document')
    op.drop_table('profile')
    # ### end Alembic commands ###