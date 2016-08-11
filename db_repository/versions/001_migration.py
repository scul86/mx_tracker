from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
gas_stop = Table('gas_stop', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('gallons', DECIMAL),
    Column('price', DECIMAL),
    Column('trip', DECIMAL),
    Column('mpg', DECIMAL),
    Column('location', String(length=140)),
    Column('timestamp', DateTime),
    Column('vehicle_id', Integer),
)

vehicle = Table('vehicle', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('passwd', String(length=128)),
    Column('mileage', DECIMAL),
    Column('last_updated', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['gas_stop'].create()
    post_meta.tables['vehicle'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['gas_stop'].drop()
    post_meta.tables['vehicle'].drop()
