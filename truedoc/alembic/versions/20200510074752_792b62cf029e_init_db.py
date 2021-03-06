"""Init DB

Revision ID: 792b62cf029e
Revises:
Create Date: 2020-05-10 07:47:52.123440+00:00

"""
from alembic import op
import sqlalchemy as sa

import truedoc.config
from truedoc.db import db

# revision identifiers, used by Alembic.
revision = '792b62cf029e'
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
    sa.PrimaryKeyConstraint('profile_id', name=op.f('pk_profile')),
    sa.UniqueConstraint('email', name=op.f('uq_profile_email'))
    )
    op.create_table('document',
    sa.Column('document_id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('profile_id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('title', sa.VARCHAR(length=128), nullable=True),
    sa.Column('filename', sa.VARCHAR(length=256), nullable=False),
    sa.Column('filesize', sa.INTEGER(), nullable=False),
    sa.Column('digest', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.profile_id'], name=op.f('fk_document_profile_id_profile')),
    sa.PrimaryKeyConstraint('document_id', name=op.f('pk_document'))
    )

    if truedoc.config.IS_DEVELOPMENT:
        profile = db.models.Profile(email=truedoc.config.DEVELOPMENT.EMAIL)
        profile.set_password(truedoc.config.DEVELOPMENT.PASSWORD)
        profile.profile_id = truedoc.config.DEVELOPMENT.PROFILE_ID  # TODO: think about add method 'set_id' to Profile class

        db.Profile.create(profile)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if truedoc.config.IS_DEVELOPMENT:
        profile = db.Profile.load(truedoc.config.DEVELOPMENT.PROFILE_ID)
        db.Profile.delete(profile)

    op.drop_table('document')
    op.drop_table('profile')
    # ### end Alembic commands ###
