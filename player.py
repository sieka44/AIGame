import pygame
from collision_circle import CollisionCircle

CONST_VELOCITY = 1
COLOUR = (255, 0, 0)


class Player(CollisionCircle):
    def __init__(self, x_position, y_position, r, colour_setter):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, CONST_VELOCITY,
                                 colour_setter=colour_setter)

    def get_colour(self):
        return COLOUR
    # def move(self, keys, maxX, maxY):
    #     if keys[pygame.K_LEFT] and self.x > self.r:
    #         self._position -= self.vel
    #     if keys[pygame.K_RIGHT] and self.x < maxX - self.r:
    #         self.x += self.vel
    #     if keys[pygame.K_UP] and self.y > self.r:
    #         self.y -= self.vel
    #     if keys[pygame.K_DOWN] and self.y < maxY - self.r:
    #         self.y += self.vel
