from enum import Enum, unique
from src.cards import Cards

@unique
class BoardStates(Enum):
    NORMAL = 0
    FASCIST_WIN = 1
    LIBERAL_WIN = 2
    HITLER_CHANCELLOR = 3
    HITLER_SHOT = 4


class Board:
    def __init__(self):
        self.fascist_board = 0
        self.liberal_board = 0

    def increment_board(self, policy):
        if policy is Cards.FASCIST:
            self.fascist_board += 1
            if self.fascist_board >= 6:
                return BoardStates.FASCIST_WIN
        else:
            self.liberal_board += 1
            if self.liberal_board >= 5:
                return BoardStates.LIBERAL_WIN

        return BoardStates.NORMAL

__all__ = ['BoardStates', 'Board']

