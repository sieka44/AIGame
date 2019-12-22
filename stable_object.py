import numpy as np
import pygame as pg
from collision_circle import CollisionCircle
from collision_handler import CircleCollisionHandler
from bot import Behaviour

COLOUR = (255, 255, 255)
ATTACK_AREA = 100
GROUP_SIZE = 4


class StableObject(CollisionCircle):
    def __init__(self, x_position, y_position, r, center_point):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, 0)
        self.asylum = self.calculate_asylum(center_point)

    def calculate_asylum(self, center):
        vector = self._position - center
        vector[0] = vector[0] / vector[0] * 1 if vector[0] > 0 else -1
        vector[1] = vector[1] / vector[1] * 1 if vector[1] > 0 else -1
        return self._position + (vector * 2 * self._radius)

    def get_asylum_point(self):
        return self.asylum

    def draw(self, window):
        pg.draw.circle(window, self._colour, self._position.astype(np.int),
                       self._radius)
        pg.draw.circle(window, self._colour, self.asylum.astype(np.int), 5)

    def update(self, delta):
        self._delta += delta
        pass

    def handle_group_attack(self, bots_true, player_position):
        if self._delta > 5000:
            bots_in_area = []
            bots = bots_true.copy()
            for b in bots:
                if CircleCollisionHandler.is_in_area(b, self.asylum, ATTACK_AREA):
                    bots_in_area.append(b)
                    bots.remove(b)
            self.check_group_size(bots_in_area, player_position)
            self._delta = 0

    def check_group_size(self, unit, player_pos):
        if len(unit) > GROUP_SIZE:
            for u in unit:
                u.behavior = Behaviour.Attack
                u.direction = player_pos
