import pygame as pg
from collision_circle import CollisionCircle

CONST_VELOCITY = 1
COLOUR = (255, 0, 0)
RAY_SIZE = 4


class Player(CollisionCircle):
    def __init__(self, x_position, y_position, r, colour_setter):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, CONST_VELOCITY,
                                 colour_setter=colour_setter)

    def draw_with_laser(self, window, mouse_position):
        self.draw(window)
        pg.draw.line(window, COLOUR, self._position, mouse_position, RAY_SIZE)
