import factory

from quote.models import Quote


def quote_factory(session):
    class QuoteFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Quote
            sqlalchemy_session = session
            sqlalchemy_session_persistence = 'flush'

        id = factory.Sequence(lambda n: n)
        author = factory.Sequence(lambda n: f'Quote Author {n}')
        quote_text = factory.Sequence(lambda n: f'Quote text {n}')

    return QuoteFactory
