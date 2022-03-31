from contextlib import contextmanager
from typing import Any

from sqlalchemy.orm.session import Session as SessionType

from app.db import Session


@contextmanager
def create_session(**kwargs: Any) -> SessionType:
    session = Session(**kwargs)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
