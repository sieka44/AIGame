# import pygame
#
# import player
#
# window_x = 500
# window_y = 500
#
# # init
# pygame.init()
# window = pygame.display.set_mode((window_x, window_y))
# pygame.display.set_caption("FIRST")
#
# p = player.Player(r=10)
#
# while p.isRunning:
#     pygame.time.delay(100)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             p.isRunning = False
#     keys = pygame.key.get_pressed()
#     p.move(keys, window_x, window_y)
#     p.draw(window)
# pygame.quit()


import math
import random
from colorsys import hsv_to_rgb

import pygame as pg
from numpy import array as Vector

from collision_circle import CollisionCircle
from collision_handler import CircleCollisionHandler
from player import Player

BACKGROUND_COLOUR = (0, 0, 0)
WINDOW_SIZE_X = 500
WINDOW_SIZE_Y = 500
DEFAULT_BOT_COUNT = 8
DEFAULT_BALL_COLOUR = (45, 173, 60)
DEFAULT_INERTIA = 1
DEFAULT_BOT_SIZE = 15
DEFAULT_USER_SIZE = 25
VISIBLE_FPS = False


def rgb_ball_colour_setter(colour, mass):
    return colour


def spawn_bots(no_of_balls):
    bots = []
    i = 0
    while i < no_of_balls:
        radius = DEFAULT_BOT_SIZE
        x = random.randrange(radius + 5, WINDOW_SIZE_X - radius - 5)
        y = random.randrange(radius + 5, WINDOW_SIZE_Y - radius - 5)
        rotation = random.uniform(0.0, math.pi)
        ang_velocity = random.uniform(-math.pi * 0.5, math.pi * 0.5)
        velocity = Vector([random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)])
        c_setter = rgb_ball_colour_setter
        b = CollisionCircle(x, y, DEFAULT_BOT_SIZE, DEFAULT_BALL_COLOUR, colour_setter=c_setter)
        b.set_angular_velocity(ang_velocity)
        b.set_velocity(velocity * 10)
        if CircleCollisionHandler.detect_any_collision(bots, b):
            i -= 1
        else:
            bots.append(b)
        i += 1
    return bots


def spawn_additional_bots(position, velocity):
    radius = random.randrange(10, 50)
    c_setter = rgb_ball_colour_setter
    bot = CollisionCircle(position[0], position[1], radius, DEFAULT_BALL_COLOUR,
                          colour_setter=c_setter)
    bot.set_velocity(velocity)
    return bot


def spawn_user(position):
    p = Player(position[0], position[1], DEFAULT_USER_SIZE,
               colour_setter=rgb_ball_colour_setter)
    p.set_velocity(0)
    return p


def calculate(player_position, mouse_position, r=0):
    dx = player_position[0] - mouse_position[0]
    dy = player_position[1] - mouse_position[1]

    reversed_sign_x = 1 if dx < 0 else -1
    slope = dy / dx if dx != 0 else 1
    x_new = reversed_sign_x * WINDOW_SIZE_X
    y_new = player_position[1] + slope * (x_new - player_position[0])

    return x_new, y_new


if __name__ == "__main__":
    random.seed()
    pg.init()

    window = pg.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))

    pg.display.set_caption("AI Game 2D")

    previous_time = pg.time.get_ticks()

    bots = spawn_bots(DEFAULT_BOT_COUNT)
    stable_objects = []
    user = spawn_user((WINDOW_SIZE_X / 2, WINDOW_SIZE_Y / 2))
    stable_objects.append(user)
    collision_handler = CircleCollisionHandler((WINDOW_SIZE_X, WINDOW_SIZE_Y), DEFAULT_INERTIA)

    new_bot_position = None
    mouse_position = (0, 0)
    should_run = True

    while should_run:
        window.fill(BACKGROUND_COLOUR)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_run = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                new_bot_position = Vector(event.pos)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if new_bot_position is not None:
                    new_bot_velocity = Vector(event.pos) - new_bot_position
                    bots.append(spawn_additional_bots(new_bot_position, new_bot_velocity))
                    new_bot_position = None

        mouse_position = calculate(user.get_position(), pg.mouse.get_pos())
        current_time = pg.time.get_ticks()
        dt = float(current_time - previous_time) / 1000.0
        previous_time = current_time

        collision_handler.handle_boundaries(bots)
        collision_handler.handle_collisions(bots)
        collision_handler.handle_stable_objects(bots, stable_objects)

        for b in bots:
            b.draw(window)
            b.update(dt)
        user.draw_with_laser(window, mouse_position)
        pg.display.update()
        if VISIBLE_FPS and dt > 0.0:
            print(1.0 / dt)
