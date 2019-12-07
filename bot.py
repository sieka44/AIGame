import pygame
import enum
from collision_circle import CollisionCircle

CONST_VELOCITY = 1
COLOUR = (255, 0, 0)


class Behaviour(enum.Enum):
    Explore = 0
    Flee = 1,
    Risk = 2,
    Attack = 3


class Player(CollisionCircle):
    def __init__(self, x_position, y_position, r, colour_setter):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, CONST_VELOCITY,
                                 colour_setter=colour_setter)
