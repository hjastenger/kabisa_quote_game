from typing import List, Optional

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm.session import Session as SessionType
from postgres import Base, TimestampMixin, Session


class Quote(Base, TimestampMixin):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    quote_text = Column(String, nullable=False)


class QuoteRepository:
    aggregate_cls = Quote

    @classmethod
    def _current_session(cls) -> SessionType:
        return Session()

    @classmethod
    def get_by_id(cls, quote_id) -> Optional[Quote]:
        return cls._current_session().query(cls.aggregate_cls).get(quote_id)

    @classmethod
    def get_quotes(cls, limit=1) -> List[Quote]:
        return cls._current_session().query(cls.aggregate_cls).limit(limit).all()

    @classmethod
    def save(cls, aggregate) -> None:
        cls._current_session().add(aggregate)
