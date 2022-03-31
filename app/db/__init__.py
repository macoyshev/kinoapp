from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

DATA_BASE_URI = 'sqlite:///app/db/primary.db'
DATA_BASE_URI_TEST = 'sqlite:///tests/app/test.db'

engine = create_engine(DATA_BASE_URI)
engine_tests = create_engine(DATA_BASE_URI_TEST)

Session = sessionmaker()

Base = declarative_base()


def create_bd(mode: Optional[str] = None) -> None:
    if mode == 'TESTING':
        Session.configure(bind=engine_tests)
        Base.metadata.create_all(engine_tests)
    else:
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)


def clear_db(mode: Optional[str] = None) -> None:
    if mode == 'TESTING':
        Base.metadata.drop_all(engine_tests)
    else:
        Base.metadata.drop_all(engine)
