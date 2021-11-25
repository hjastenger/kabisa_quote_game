import asyncio
import pytest

from quote.models import QuoteRepository
from quote.seed import quote_factory
from quote_game.models import QuoteGame, SquarePosition


@pytest.mark.asyncio
async def test_create_game():
    factory = quote_factory()
    quote_fixtures = [factory() for i in range(8)]

    game = QuoteGame.construct_game(
        quote_list=quote_fixtures,
        len_x_axis=4,
        len_y_axis=4,
        seed=1
    )

    # Test game validity by verifying 2 predicates:
    # - Board should contain 8 unique quotes.
    # - These unique quotes should be distributed over 16 unique (x,y) game squares.
    assert len(set([s.quote_id for s in game.squares])) == 8, 'does not contain exact 8 unique quotes'
    assert len(set([(s.x_pos, s.y_pos) for s in game.squares])) == 16, 'does not contain exact 16 unique squares'

    assert not game.is_finished, 'game state after init was already finished'

    # Game state is serialized to int by converting whether each square is guessed to base 2
    # example of new game: 0000000000000000 (16 unguessed squares) => 0
    assert game.game_state_to_int() == 0


@pytest.mark.asyncio
async def test_play_full_game():
    factory = quote_factory()
    quote_fixtures = [factory() for i in range(8)]

    game = QuoteGame.construct_game(
        quote_list=quote_fixtures,
        len_x_axis=4,
        len_y_axis=4,
        seed=1
    )

    assert game.guess(SquarePosition(x=0, y=2), SquarePosition(x=2, y=2))
    # After right guess: 0010 0000 0010 0000 => 2^13 + 2^5 => 8224
    assert game.game_state_to_int() == 8224
    assert not game.is_finished

    assert game.guess(SquarePosition(x=0, y=0), SquarePosition(x=3, y=2))
    # After guess: 1010 0000 0010 0010 => 2^15 + 2^13 + 2^5 + 2 => 40994
    assert game.game_state_to_int() == 40994

    assert game.guess(SquarePosition(x=1, y=2), SquarePosition(x=1, y=1))

    assert game.guess(SquarePosition(x=0, y=3), SquarePosition(x=2, y=0))
    assert game.guess(SquarePosition(x=1, y=3), SquarePosition(x=2, y=3))
    assert game.guess(SquarePosition(x=3, y=3), SquarePosition(x=0, y=1))
    assert game.guess(SquarePosition(x=3, y=0), SquarePosition(x=3, y=1))
    assert game.guess(SquarePosition(x=2, y=1), SquarePosition(x=1, y=0))
    assert game.is_finished
    assert game.game_state_to_int() == (2**16)-1


@pytest.mark.asyncio
async def test_play_wrong_guess():
    factory = quote_factory()
    quote_fixtures = [factory() for i in range(8)]

    game = QuoteGame.construct_game(
        quote_list=quote_fixtures,
        len_x_axis=4,
        len_y_axis=4,
        seed=1
    )

    assert not game.guess(SquarePosition(x=0, y=2), SquarePosition(x=1, y=2))
    assert game.game_state_to_int() == 0

