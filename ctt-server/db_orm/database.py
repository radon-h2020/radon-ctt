import os

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from util.configuration import BasePath, DBFile

if not os.path.exists(BasePath):
    os.makedirs(BasePath)

engine = create_engine('sqlite:///' + os.path.join(BasePath, DBFile), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import project, testartifact, deployment, execution, result
    Base.metadata.create_all(bind=engine)


# Explicitly enable ForeignKey support for SQLite
# https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#foreign-key-support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
