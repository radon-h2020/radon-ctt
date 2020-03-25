import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from util.configuration import BasePath, DBFile

if not os.path.exists(BasePath):
    os.makedirs(BasePath)

engine = create_engine('sqlite:///' + os.path.join(BasePath, DBFile))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import project, testartifact, deployment, execution, result
    Base.metadata.create_all(bind=engine)
