from abc import ABC, abstractmethod
from board.Board import Board

class Player(ABC):
    @abstractmethod
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def make_move(self, game_board: Board, player_id: int) -> None:
        pass