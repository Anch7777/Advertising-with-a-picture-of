import pygame as pg
import math
from settings import *
import time
class Geisha:
    def __init__(self, game, pos=(6.5, 6.5)):
        self.game = game
        self.x, self.y = pos
        self.original_image = pg.image.load('geisha.png').convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (166, 334))
        self.image = self.original_image
        self.speed = GEISHA_SPEED
        self.target = None
        self.last_seen_time = 0
        self.active = True
        self.path = None
        self.detection_range = GEISHA_VISION_RANGE * 2

    def draw(self):
        if not self.active:
            return
        dx = self.x - self.game.player.x
        dy = self.y - self.game.player.y
        distance = math.hypot(dx, dy)
        if distance < GEISHA_VISION_RANGE:
            angle = math.atan2(dy, dx) - self.game.player.angle
            if -HALF_FOV < angle < HALF_FOV:
                proj_height = SCREEN_DIST / (distance + 0.0001)
                scale = proj_height / self.image.get_height()
                scaled_width = int(self.image.get_width() * scale)
                scaled_height = int(self.image.get_height() * scale)
                scaled_image = pg.transform.scale(self.image, (scaled_width, scaled_height))
                screen_x = int((math.tan(angle) * SCREEN_DIST) + HALF_WIDTH - scaled_width // 2)
                screen_y = int(HALF_HEIGHT - scaled_height // 2)
                self.game.screen.blit(scaled_image, (screen_x, screen_y))

    def is_player_in_sight(self):
        # Проверка наличия игрока
        if not self.game.player:
            return False

        player_x, player_y = self.game.player.pos
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance > self.detection_range:
            return False

        angle_to_player = math.atan2(dy, dx)
        step = 0.1
        current_x, current_y = self.x, self.y

        # Проверка видимости игрока
        for _ in range(int(distance / step)):
            current_x += math.cos(angle_to_player) * step
            current_y += math.sin(angle_to_player) * step
            map_x = int(current_x)
            map_y = int(current_y)

            # Проверка наличия карты и наличия текущей позиции в карте
            if self.game.map and (map_x, map_y) in self.game.map.world_map:
                return False

        return True

    def move_towards_player(self):
        # Проверка наличия цели и игрока
        if not self.target or not self.game.player or not self.game.player.map_pos:
            return

        if self.path is None or self.target != self.game.player.map_pos:
            self.target = self.game.player.map_pos
            self.path = self.game.pathfinding.get_path(self.map_pos, self.target)

        if self.path and len(self.path) > 1:
            next_pos = self.path[1]
            dx = next_pos[0] + 0.5 - self.x
            dy = next_pos[1] + 0.5 - self.y
            dist = math.hypot(dx, dy)

            if dist < 0.1:
                self.x, self.y = next_pos[0] + 0.5, next_pos[1] + 0.5
                self.path.pop(0)
                return

            direction = math.atan2(dy, dx)
            speed_vector = (
                math.cos(direction) * self.speed * self.game.delta_time,
                math.sin(direction) * self.speed * self.game.delta_time
            )

            new_x = self.x + speed_vector[0]
            new_y = self.y + speed_vector[1]

            if not self.check_wall_collision(new_x - self.x, new_y - self.y):
                self.x = new_x
                self.y = new_y

    def update(self):
        if not self.active:
            return
        if self.is_player_in_sight():
            self.target = self.game.player.map_pos
            self.last_seen_time = time.time()
            self.move_towards_player()
        distance_to_player = math.hypot(self.x - self.game.player.x, self.y - self.game.player.y)
        if distance_to_player < 1:
            self.game.player.health -= 1 * self.game.delta_time
        else:
            if time.time() - self.last_seen_time > 10:
                self.active = False
                self.path = None

    def check_wall_collision(self, dx, dy):
        # Вычисление следующей позиции
        next_x = self.x + dx
        next_y = self.y + dy

        # Определение точек для проверки столкновений
        offsets = [(-0.25, -0.25), (-0.25, 0.25), (0.25, -0.25), (0.25, 0.25)]

        # Проверка столкновений
        for offset_x, offset_y in offsets:
            test_x = int(next_x + offset_x)
            test_y = int(next_y + offset_y)

            # Проверка наличия карты и наличия текущей позиции в карте
            if self.game.map and (test_x, test_y) in self.game.map.world_map:
                return False

        return True

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)