import pytest

from quote.seed import quote_factory
from quote_game.service import QuoteGameService


@pytest.mark.asyncio
async def test_create_new_game_insufficient_quotes(db_session_fixture):
    success, create_game_res = await QuoteGameService.create_new_game(db_session_fixture)

    assert not success


@pytest.mark.asyncio
async def test_create_new_game(db_session_fixture):
    factory = quote_factory(db_session_fixture)
    [factory() for i in range(8)]

    success, create_game_res = await QuoteGameService.create_new_game(db_session_fixture)

    assert success
