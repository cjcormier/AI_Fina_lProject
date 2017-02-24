from enum import Enum, unique

@unique
class Info_Types(Enum):
    REVEALED_CARD = 1
    PRESIDENT_CLAIM = 2
    CHANCELLOR_CLAIM = 3
