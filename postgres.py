from asyncio import current_task
from datetime import datetime

from sqlalchemy import DateTime, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

engine = create_engine("postgresql://admin:password@localhost:5432/kabisa_db", echo=False)
# session_factory = sessionmaker(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory, scopefunc=current_task)


class TimestampMixin:
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now)

    def __repr__(self):
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys())
        return "%s(%s)" % (self.__class__.__name__, values)


def transactional(expire_on_commit=False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            bounded_session = Session()
            try:
                result = await func(*args, **kwargs)
                bounded_session.commit()
                return result
            except:
                bounded_session.rollback()
                raise
            finally:
                bounded_session.close()
                Session.remove()
        return wrapper
    return decorator
