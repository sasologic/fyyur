"""empty message

Revision ID: 130a092fed01
Revises: 
Create Date: 2022-07-31 03:32:24.325368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '130a092fed01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """empty message

Revision ID: c7105644dc55
Revises: 
Create Date: 2022-07-31 02:56:54.215236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7105644dc55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('venue',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('seeking_description', sa.VARCHAR(length=300), autoincrement=False, nullable=False),
    sa.Column('website', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('genres', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='venue_pkey')
    )

    op.create_table('artist',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('artist_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('website_link', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='artist_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('show',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('start_time', sa.DATE, autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='show_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='show_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='show_pkey')
    )



def downgrade():
   pass


