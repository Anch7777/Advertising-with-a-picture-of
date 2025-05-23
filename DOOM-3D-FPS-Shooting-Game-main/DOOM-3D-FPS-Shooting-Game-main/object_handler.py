import time

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.npc_list = []
        self.npc_positions = {}
        self.geisha_visible = False
        self.last_seen_time = time.time()
        if hasattr(self.game, 'geisha'):
            self.geisha = self.game.geisha
        else:
            self.geisha = None

    def add_npc(self, npc):
        self.npc_list.append(npc)
        self.npc_positions[npc.map_pos] = npc

    def update(self):
        for npc in self.npc_list:
            if npc.active:  # Отображаем только активных NPC
                npc.update()
        self.check_geisha_visibility()
        self.check_geisha_disappearance()

    def check_geisha_visibility(self):
        if self.geisha and self.geisha.is_player_in_sight():
            self.geisha_visible = True
            self.last_seen_time = time.time()
        else:
            self.geisha_visible = False

    def check_geisha_disappearance(self):
        if not self.geisha_visible and time.time() - self.last_seen_time > 10:
            if self.geisha:
                self.geisha.active = False