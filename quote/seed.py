import factory

from postgres import Session
from quote.models import Quote


def quote_factory():
    class QuoteFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Quote
            sqlalchemy_session = Session
            sqlalchemy_session_persistence = 'flush'

        id = factory.Sequence(lambda n: n)
        author = factory.Sequence(lambda n: f'Quote Author {n}')
        quote_text = factory.Sequence(lambda n: f'Quote text {n}')

    return QuoteFactory
