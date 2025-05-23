import pygame as pg
import sys
from settings import *
from map import Map
from player import Player
from raycasting import RayCasting
from object_renderer import ObjectRenderer
from object_handler import ObjectHandler
from pathfinding import PathFinding
from geisha import Geisha

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.font = pg.font.Font(None, 45)
        self.paused = False
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        player_start_pos = self.map.player_start_pos if self.map.player_start_pos else (1.5, 1.5)
        geisha_start_pos = self.map.geisha_start_pos if self.map.geisha_start_pos else (6.5, 6.5)
        self.player = Player(self, pos=player_start_pos)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.pathfinding = PathFinding(self)
        self.geisha = Geisha(self, pos=geisha_start_pos)
        self.object_handler = ObjectHandler(self)
        self.object_handler.add_npc(self.geisha)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.geisha.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS) / 1000
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.check_win_condition()

    def check_win_condition(self):
        player_pos = (int(self.player.x), int(self.player.y))
        if self.map.world_map.get(player_pos) == 5:  # Exit door
            text = self.font.render("Press E to exit", True, (255, 255, 255))
            text_rect = text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
            self.screen.blit(text, text_rect)
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                print("Exiting the game!")
                pg.quit()
                sys.exit()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.player.process_input(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()