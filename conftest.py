import pytest
from sqlalchemy.orm import sessionmaker

from postgres import engine


@pytest.fixture()
def db_session_fixture():
    session_factory = sessionmaker(bind=engine)
    return session_factory()


@pytest.fixture(autouse=True, scope='function')
def run_around_tests(db_session_fixture):
    db_session_fixture.begin(subtransactions=True)
    session = db_session_fixture
    session.begin(nested=True)

    try:
        yield
    except Exception:
        raise
    finally:
        session.rollback()
    session.close()
