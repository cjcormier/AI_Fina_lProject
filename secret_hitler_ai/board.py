"""
Contains the basic classes to control and retrieve information about the Facist and 
Liberal Policy tracks and the status of the win condition.
"""
from enum import Enum, unique
from secret_hitler_ai.deck import Card


@unique
class BoardStates(Enum):
    """Status of the win condition."""
    NORMAL = 0
    FASCIST_WIN = 1
    LIBERAL_WIN = 2
    HITLER_CHANCELLOR = 3
    HITLER_SHOT = 4


class Board:
    """Information about the Fascist and Liberal Policy tracks."""
    def __init__(self):
        self.fascist_board = 0
        self.liberal_board = 0

    def increment_board(self, policy: Card)->BoardStates:
        """Increments the relevent policy track for the given policy.
        
        :param policy: The policy that was enacted.
        :return: The win condition based on the played card.
        """
        if policy is Card.FASCIST:
            self.fascist_board += 1
            if self.fascist_board >= 6:
                return BoardStates.FASCIST_WIN
        else:
            self.liberal_board += 1
            if self.liberal_board >= 5:
                return BoardStates.LIBERAL_WIN

        return BoardStates.NORMAL

__all__ = ['BoardStates', 'Board']
