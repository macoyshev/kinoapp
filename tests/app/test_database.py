import pytest
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.database import create_session


def test_create_session_invalid_entity():
    with pytest.raises(UnmappedInstanceError):
        with create_session() as session:
            session.add('tet')
