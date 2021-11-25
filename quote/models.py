from typing import List, Optional

from sqlalchemy import Column, String, Integer
from postgres import Base, TimestampMixin


class Quote(Base, TimestampMixin):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    quote_text = Column(String, nullable=False)


class QuoteRepository:
    aggregate_cls = Quote

    @classmethod
    def get_by_id(cls, session, quote_id) -> Optional[Quote]:
        return session.query(cls.aggregate_cls).get(quote_id)

    @classmethod
    def get_quotes(cls, session, limit=1) -> List[Quote]:
        return session.query(cls.aggregate_cls).limit(limit).all()

    @classmethod
    def save(cls, session, aggregate) -> None:
        session.add(aggregate)
