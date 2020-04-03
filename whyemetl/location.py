"""
Location contains utility classes to represents geopositions and continents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Position:
    latitude: float
    longitude: float


class Continent(ABC):
    """ Continent interface that represents a geographical Continent area. """

    @abstractmethod
    def contains(self, position):
        """ Returns True if the given position is in the Continent area. """
        pass


class Rectangle(Continent):
    """A Continent area is approximated by a rectangle, defined by 2 positions:
    upperleft and bottomright"""

    def __init__(self, name, upperleft, bottomright):
        self.name = name
        self.upperleft = upperleft
        self.bottomright = bottomright

    def contains(self, position):
        """ Returns True if the given position is within the Continent. """

        if position.latitude is None or position.longitude is None:
            return False
        longitude_in_range = (
            self.upperleft.longitude <= position.longitude <= self.bottomright.longitude
        )
        latitude_in_range = (
            self.bottomright.latitude <= position.latitude <= self.upperleft.latitude
        )
        if longitude_in_range and latitude_in_range:
            return True
        return False


def get_continent(position, continents):
    """
    Checks in which continent the position is.
    Returns the continent name that contains it.
    """

    for continent in continents:
        if continent.contains(position):
            return continent.name
    return "OTHERS"
