import pygame as pg
import math
from settings import *

class Player:
    def __init__(self, game, pos=(1.5, 1.5)):
        self.game = game
        self.x, self.y = pos
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.base_speed = PLAYER_SPEED
        self.sprint_speed = PLAYER_SPEED * 2
        self.rot_speed = PLAYER_ROT_SPEED
        self.collision_radius = 0.1
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

    # Обновите метод process_input:
    def process_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_UP):
                self.forward = True
            elif event.key in (pg.K_s, pg.K_DOWN):
                self.backward = True
            elif event.key in (pg.K_a, pg.K_LEFT):
                self.left = True
            elif event.key in (pg.K_d, pg.K_RIGHT):
                self.right = True

        elif event.type == pg.KEYUP:
            if event.key in (pg.K_w, pg.K_UP):
                self.forward = False
            elif event.key in (pg.K_s, pg.K_DOWN):
                self.backward = False
            elif event.key in (pg.K_a, pg.K_LEFT):
                self.left = False
            elif event.key in (pg.K_d, pg.K_RIGHT):
                self.right = False

    # В методе movement исправьте боковое движение:
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = self.sprint_speed if pg.key.get_pressed()[pg.K_LSHIFT] else self.base_speed
        speed *= self.game.delta_time

        dx, dy = 0, 0
        if self.forward:
            dx += speed * cos_a
            dy += speed * sin_a
        if self.backward:
            dx -= speed * cos_a
            dy -= speed * sin_a
        if self.left:
            self.rotate(-1)
        if self.right:
            self.rotate(1)

        if self.check_wall_collision(dx, dy):
            self.x += dx
            self.y += dy

    def rotate(self, direction):
        self.angle += direction * self.rot_speed * self.game.delta_time

    def check_wall_collision(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy
        offsets = [(-0.1, -0.1), (-0.1, 0.1), (0.1, -0.1), (0.1, 0.1)]
        for offset_x, offset_y in offsets:
            test_x = int(next_x + offset_x)
            test_y = int(next_y + offset_y)
            if (test_x, test_y) in self.game.map.world_map:
                return False
        return True

    def draw_health(self):
        width = int(200 * (self.health / PLAYER_MAX_HEALTH))
        pg.draw.rect(self.game.screen, 'red', (20, 20, 200, 30))
        pg.draw.rect(self.game.screen, 'green', (20, 20, width, 30))

    def update(self):
        self.movement()
        self.draw_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)