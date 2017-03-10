from enum import Enum, unique

@unique
class Cards(Enum):
    FASCIST = 1
    LIBERAL = 2

__all__ = ['Cards']
