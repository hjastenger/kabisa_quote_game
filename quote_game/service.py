import logging
from typing import Tuple, Optional

from pydantic import BaseModel

from quote.models import QuoteRepository
from quote_game.models import QuoteGame, SquarePosition, QuoteGameRepository

log = logging.getLogger(__name__)


class GameGuessResponse(BaseModel):
    success: bool
    game_state: int
    msg: str = []


class QuoteGameService:
    @staticmethod
    async def create_new_game(session) -> Tuple[bool, str]:
        quotes = QuoteRepository.get_quotes(session, limit=8)
        if len(quotes) == 8:
            new_game = QuoteGame.construct_game(quote_list=quotes, len_y_axis=4, len_x_axis=4)

            QuoteGameRepository.save(session, new_game)
            log.info(f"New quote game created {new_game.id} ")
            return True, new_game.id
        else:
            log.warning(f"Game creation aborted due to insufficient available quotes, have {len(quotes)} but require 8")
            return (
                False,
                "Could not create game due to insufficient available quotes",
            )

    @staticmethod
    async def check_guess(
        session, game_id: int, pos_a: SquarePosition, pos_b: SquarePosition
    ) -> Tuple[Optional[GameGuessResponse], Optional[str]]:
        if game := QuoteGameRepository.get_by_id(session, game_id):
            if game.is_finished:
                return (
                    GameGuessResponse(
                        success=False,
                        game_state=game.game_state_to_int(),
                        msg=f"Game {game_id} is already finished",
                    ),
                    None,
                )

            if pos_a == pos_b:
                return (
                    GameGuessResponse(
                        success=False,
                        game_state=game.game_state_to_int(),
                        msg=f"Position A and B can not be identical",
                    ),
                    None,
                )

            correct_guess = game.guess(pos_a, pos_b)
            if correct_guess:
                QuoteGameRepository.save(session, game)

                if game.is_finished:
                    msg = f"Congratulations you have beaten the game!"
                else:
                    msg = f"Square {pos_a} and {pos_b} contained the same quote!"

                return GameGuessResponse(success=True, game_state=game.game_state_to_int(), msg=msg), None

            else:
                quote_on_position = [(game.quote_id_on_square(pos), pos) for pos in [pos_a, pos_b]]

                msg_hints = []
                for (quote_id, pos) in quote_on_position:
                    if not quote_id:
                        msg_hints.append(f"No square at location {pos}")
                    else:
                        quote_on_pos = QuoteRepository.get_by_id(session, game.quote_id_on_square(pos))
                        msg_hints.append(f"Quote at {pos} is '{quote_on_pos.quote_text}'")

                return (
                    GameGuessResponse(
                        success=False,
                        game_state=game.game_state_to_int(),
                        msg=". ".join(msg_hints),
                    ),
                    None,
                )
        return None, f"No game found for id '{game_id}'"
