from enum import Enum, unique


@unique
class Role(Enum):
    FASCIST = auto()
    LIBERAL = 2
    HITLER = 3