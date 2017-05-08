from enum import Enum, unique


@unique
class InfoTypes(Enum):
    REVEALED_CARD = 1
    PRESIDENT_CLAIM = 2
    CHANCELLOR_CLAIM = 3

__all_ = ['InfoTypes']
