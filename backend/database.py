import json
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models  # import models to register with Base
    Base.metadata.create_all(bind=engine)
