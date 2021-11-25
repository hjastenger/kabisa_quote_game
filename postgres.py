from datetime import datetime

from sqlalchemy import DateTime, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("postgresql://admin:password@localhost:5432/kabisa_db", echo=False)

session_factory = sessionmaker(bind=engine)


class TimestampMixin:
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now)

    def __repr__(self):
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys())
        return "%s(%s)" % (self.__class__.__name__, values)


def get_transactional_db_session():
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
