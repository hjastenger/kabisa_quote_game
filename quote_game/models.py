import itertools
import random
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session as SessionType

from postgres import Base, TimestampMixin, Session
from quote.models import Quote


class SquarePosition(BaseModel):
    x: int
    y: int


class QuoteGame(Base, TimestampMixin):
    __tablename__ = 'quote_game'

    random_seed_lower, random_seed_upper = 1, 100

    id = Column(Integer, primary_key=True)
    seed = Column(Integer, nullable=False)
    squares = relationship("GameSquare")

    def game_state_to_int(self):
        game_state = sorted(self.squares, key=lambda x: (x.x_pos, x.y_pos))
        return int(''.join(['1' if g.guessed else '0' for g in game_state]), 2)

    def _get_square_by_position(self, pos: SquarePosition):
        return next((s for s in self.squares if s.x_pos == pos.x and s.y_pos == pos.y), None)

    def quote_id_on_square(self, pos: SquarePosition):
        return next((s.quote_id for s in self.squares if s.x_pos == pos.x and s.y_pos == pos.y), None)

    def guess(self, pos_a: SquarePosition, pos_b: SquarePosition):
        square_a, square_b = self._get_square_by_position(pos_a), self._get_square_by_position(pos_b)

        if square_a and square_b and square_a.quote_id == square_b.quote_id:
            square_a.guessed, square_b.guessed = True, True
            return True

    @property
    def is_finished(self):
        return all([s.guessed for s in self.squares])

    @classmethod
    def construct_game(cls, quote_list, len_x_axis, len_y_axis, seed=random.randint(random_seed_lower, random_seed_upper)):
        if len(quote_list) != len_x_axis * len_y_axis:
            pass

        game_squares = list(itertools.chain.from_iterable([[(x,y)for y in range(len_y_axis)] for x in range(len_x_axis)]))
        random.Random(seed).shuffle(game_squares)

        square_couples = [(game_squares[i], game_squares[i+1]) for i in range(0, len(game_squares), 2)]

        new_game = QuoteGame(seed=seed)
        for i, couple in enumerate(square_couples):
            quote_id = quote_list[i].id
            pos_square_a, pos_square_b = couple[0], couple[1]
            new_game.squares.append(GameSquare(quote_id=quote_id, x_pos=pos_square_a[0], y_pos=pos_square_a[1]))
            new_game.squares.append(GameSquare(quote_id=quote_id, x_pos=pos_square_b[0], y_pos=pos_square_b[1]))

        return new_game


class GameSquare(Base, TimestampMixin):
    __tablename__ = 'game_square'

    id = Column(Integer, primary_key=True)
    quote_game_id = Column(Integer, ForeignKey(QuoteGame.id), nullable=False)
    quote_id = Column(Integer, ForeignKey(Quote.id), nullable=False)
    x_pos = Column(Integer, nullable=False)
    y_pos = Column(Integer, nullable=False)
    guessed = Column(Boolean, nullable=False, default=False)


class QuoteGameRepository:
    aggregate_cls = QuoteGame

    @classmethod
    def _current_session(cls) -> SessionType:
        return Session()

    @classmethod
    def get_by_id(cls, game_id) -> Optional[QuoteGame]:
        return cls._current_session().query(cls.aggregate_cls).get(game_id)

    @classmethod
    def save(cls, aggregate) -> None:
        cls._current_session().add(aggregate)
        cls._current_session().flush()
