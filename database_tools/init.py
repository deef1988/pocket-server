from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy import create_engine
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE
from database_tools.category_group import add_category
from database_tools.status import add_status

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))
meta = MetaData(bind=engine)

users = Table('users', meta,
              Column('uid', Integer, primary_key=True),
              Column('username', String),
              Column('password', String),
              Column('email', String),
              Column('token', String),
              Column('tokenexp', DateTime),
              Column('status_id', Integer, ForeignKey('status_of_user.usid')))

messages = Table('messages', meta,
                 Column('mid', Integer, primary_key=True),
                 Column('to_id', Integer, ForeignKey('users.uid')),
                 Column('from_id', Integer, ForeignKey('users.uid')),
                 Column('message', String),
                 Column('dtime', DateTime))

contacts = Table('contacts', meta,
                 Column('cid', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey('users.uid')),
                 Column('contact', Integer, ForeignKey('users.uid')))

#-------------------------------------------------------------------
groups = Table('groups', meta,
                Column('gid', Integer, primary_key=True),
                Column('group_name', String),
                Column('creation_date', DateTime),
                Column('creater_user_id', Integer),
                Column('category_group', Integer, ForeignKey('category_group.category_id')))


user_groups = Table('user_groups', meta,
                    Column('user_id', Integer, ForeignKey('users.uid'), primary_key=True),
                    Column('group_id', Integer, ForeignKey('groups.gid')))

#---------------------------------------------------roles
user_roles = Table('user_roles', meta,
              Column('roleid', primary_key=True),
              Column('role_name'))

status_of_user = Table('status_of_user', meta,
                       Column('usid', Integer, primary_key=True),
                       Column('status_name', String))


coll_group = Table('coll_group', meta,
                   Column('clid', Integer, primary_key=True),
                   Column('collgroup_id', Integer, ForeignKey('groups.gid')),
                   Column('group_id', Integer, ForeignKey('groups.gid')))


category_group = Table('category_group', meta,
                       Column('category_id', Integer, primary_key=True),
                       Column('category_name', String))

meta.create_all(engine)

add_status(engine)
add_category(engine)
