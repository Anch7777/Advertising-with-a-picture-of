import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.load_textures()

    def load_textures(self):
        # Загрузка текстур для стен
        return {
            1: pg.image.load('wall_1.png').convert_alpha(),
            2: pg.image.load('wall_2.png').convert_alpha(),
            3: pg.image.load('wall_3.png').convert_alpha(),
            4: pg.image.load('wall_4.png').convert_alpha(),
            5: pg.image.load('exit_door.png').convert_alpha(),
        }

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if proj_height > HEIGHT * 2 or texture not in self.textures:
                continue
            texture_surface = self.textures[texture]
            tex_width = texture_surface.get_width()
            tex_height = texture_surface.get_height()

            offset = max(0, min(offset, 1))
            texture_offset = int(offset * (tex_width - SCALE))
            wall_column = texture_surface.subsurface(texture_offset, 0, SCALE, tex_height)
            wall_column = pg.transform.scale(wall_column, (SCALE, int(proj_height)))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            depth_hor, texture_hor = MAX_DEPTH, None
            depth_vert, texture_vert = MAX_DEPTH, None

            # Горизонтальные проверки
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Вертикальные проверки
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Определение ближайшей стены
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.game.player.angle - ray_angle)
            proj_height = SCREEN_DIST / (depth + 0.0001)
            self.ray_casting_result.append((depth, proj_height, texture, offset))
            ray_angle += DELTA_ANGLE


    def update(self):
        self.ray_cast()
        self.get_objects_to_render()