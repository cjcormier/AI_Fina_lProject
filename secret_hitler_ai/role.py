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
        self._fascist: float = fascist
        self._hitler: float = hitler

    @property
    def fascist(self)->float:
        """
        Return the fascist probability as a float.
        :return: The fascist probability.
        """
        return self._fascist

    @property
    def hitler(self)->float:
        """
        Return the hitler probability as a float.
        :return: The hitler probability.
        """
        return self._hitler

    @fascist.setter
    def fascist(self, value: Prob):
        self._fascist = float(value)


    @hitler.setter
    def hitler(self, value: Prob):
        self._hitler = float(value)
