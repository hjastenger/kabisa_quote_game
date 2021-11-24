import pytest
from aioresponses import aioresponses

from quote.infra.storm_quote_api import QuoteAPI


@pytest.mark.asyncio
async def test_200_response():
    with aioresponses() as m:
        quote_author_fixt, quote_fixt = 'henk', 'henk is great, henk is life'
        m.get(
            'http://quotes.stormconsultancy.co.uk/random.json',
            payload={'author': quote_author_fixt, 'quote': quote_fixt},
        )
        res = await QuoteAPI.fetch_random_quote()

        assert res[0] == 200 and res[1]['author'] == quote_author_fixt and res[1]['quote'] == quote_fixt

@pytest.mark.asyncio
async def test_500_response():
    with aioresponses() as m:
        quote_author_fixt, quote_fixt = 'henk', 'henk is great, henk is life'
        m.get(
            'http://quotes.stormconsultancy.co.uk/random.json',
            payload={'author': quote_author_fixt, 'quote': quote_fixt},
            status=500
        )
        res = await QuoteAPI.fetch_random_quote()

        assert res[0] == 500 and res[1]['error_msg'] == 'Failed to fetch quote, API returned 500'
