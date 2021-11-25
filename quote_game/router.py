from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from quote_game.models import SquarePosition
from quote_game.service import QuoteGameService

router = APIRouter(prefix="/game")


class CreateGameResponse(BaseModel):
    success: bool
    game_id: Optional[int] = None
    error_msg: Optional[str] = None


@router.get("/", response_model=CreateGameResponse)
async def create_game():
    success, response_data = await QuoteGameService.create_new_game()
    if success:
        return CreateGameResponse(success=True, game_id=response_data)
    else:
        return CreateGameResponse(success=False, error_msg=response_data)


class PostGameGuessRequest(BaseModel):
    game_id: int
    position_a: SquarePosition
    position_b: SquarePosition


class PostGameGuessResponse(BaseModel):
    msg: str
    success: bool
    game_id: Optional[int] = None
    game_state: Optional[int] = None


@router.post(
    "/guess",
    response_model=PostGameGuessResponse,
    description="Post a guess to discover whether 2 coordinates contain the same quote",
)
async def post_game_guess(post_data: PostGameGuessRequest):
    game_guess_res, msg = await QuoteGameService.check_guess(
        game_id=post_data.game_id, pos_a=post_data.position_a, pos_b=post_data.position_b
    )
    if game_guess_res:
        return {
            "success": game_guess_res.success,
            "game_state": game_guess_res.game_state,
            "msg": game_guess_res.msg,
            "game_id": post_data.game_id,
        }

    return {"success": False, "msg": msg}
