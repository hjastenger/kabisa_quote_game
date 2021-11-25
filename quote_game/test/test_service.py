import pytest

from postgres import Session
from quote.seed import quote_factory
from quote_game.service import QuoteGameService


@pytest.mark.asyncio
@pytest.fixture(autouse=True, scope='function')
async def run_around_tests():
    session = Session()
    session.begin(subtransactions=True)
    yield
    session.rollback()
    session.close()


@pytest.mark.asyncio
async def test_create_new_game_insufficient_quotes():
    success, create_game_res = await QuoteGameService.create_new_game()

    assert not success


@pytest.mark.asyncio
async def test_create_new_game():
    factory = quote_factory()
    [factory() for i in range(8)]

    success, create_game_res = await QuoteGameService.create_new_game()

    assert success
