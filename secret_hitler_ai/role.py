"""
The Roles that each player can have.
"""
from enum import unique, Enum


@unique
class Role(Enum):
    """
    The types of Roles.
    """
    FASCIST = 0
    LIBERAL = 1
    HITLER = 2
