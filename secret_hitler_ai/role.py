"""
The Roles that each player can have.
"""
from enum import unique, Enum
from typing import Union


@unique
class Role(Enum):
    """
    The types of Roles.
    """
    FASCIST = 0
    LIBERAL = 1
    HITLER = 2


Prob = Union[float, int]


class RoleProbs:
    """Probability that someone is fascist or hitler."""

    def __init__(self, fascist: Prob, hitler: Prob):
        self._fascist: float = float(fascist)
        self._hitler: float = float(hitler)

    @property
    def fascist(self)->float:
        """
        The fascist probability as a float.
        
        :return: The fascist probability.
        """

        return self._fascist

    @property
    def hitler(self)->float:
        """
        The hitler probability as a float.
        
        :return: The hitler probability.
        """
        assert type(self._hitler) is float
        return self._hitler

    @fascist.setter
    def fascist(self, value: Prob):
        self._fascist = float(value)

    @hitler.setter
    def hitler(self, value: Prob):
        self._hitler = float(value)
