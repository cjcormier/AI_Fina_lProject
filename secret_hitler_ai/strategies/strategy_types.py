"""
Contains the basic class to define the types of strategies.
"""
from enum import unique, Enum


@unique
class StrategyTypes(Enum):
    """
    The types of strategies.
    """
    CHOOSE_CHANCELLOR = 1
    CHANCELLOR_CARDS = 2
    PRESIDENT_CARDS = 3
    VOTE = 4
    VOTE_RESULTS = 5
    ANALYZE_REVEALED_CARD = 6
    ANALYZE_CHANCELLOR_CARD = 7
    SHOOT = 8

__all__ = ["StrategyTypes"]
