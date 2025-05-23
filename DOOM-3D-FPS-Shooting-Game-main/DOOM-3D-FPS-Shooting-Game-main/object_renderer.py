import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('sky.png', (WIDTH, HALF_HEIGHT))
        self.floor_texture = self.get_texture('floor.png', (WIDTH, HALF_HEIGHT))

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        self.screen.blit(self.sky_image, (0, 0))
        self.screen.blit(self.floor_texture, (0, HALF_HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            if image:
                self.screen.blit(image, pos)
        if self.game.geisha and self.game.geisha.active:
            self.game.geisha.draw()

    @staticmethod
    def get_texture(path, res=None):
        try:
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res) if res else texture
        except Exception as e:
            print(f"Error loading texture {path}: {e}")
            return None

    def load_wall_textures(self):
        return {
            1: self._load_scaled_texture('wall_1.png', 1520, 1800),
            2: self._load_scaled_texture('wall_2.png', 1536, 1800),
            3: self._load_scaled_texture('wall_3.png', 501, 560),
            4: self._load_scaled_texture('wall_4.png', 493, 562),
            5: self._load_scaled_texture('exit_door.png', 370, 482),
        }

    def _load_scaled_texture(self, name, orig_w, orig_h):
        texture = pg.image.load(name).convert_alpha()
        scale_factor = TEXTURE_SIZE / orig_h
        new_w = int(orig_w * scale_factor)
        return pg.transform.scale(texture, (new_w, TEXTURE_SIZE))