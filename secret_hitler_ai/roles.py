from enum import Enum, unique


@unique
class Role(Enum):
    FASCIST = 1
    LIBERAL = 2
    HITLER = 3

__all__ = ['Role']
