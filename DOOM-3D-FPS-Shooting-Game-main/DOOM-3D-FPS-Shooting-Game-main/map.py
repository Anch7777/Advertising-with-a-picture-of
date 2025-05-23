mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, "S", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2, 2, 2, 0, 3, 3, 3, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 4, 4, 4, 0, 1, 0, 2, 0, 3, 3, 3, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 3, 3, 3, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, "G", 1],
    [1, 0, 4, 4, 4, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2, 3, 3, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 4, 4, 4, 0, 1, 0, 3, 0, 1, 1, 1, 0, 2, 2, 2, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 4, 0, 1, 0, 3, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 4, 0, 1, 0, 3, 0, 1, 0, 1, 1, 2, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 5, 1],  # Exit (5)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.player_start_pos = None
        self.geisha_start_pos = None
        self.get_map()

    def get_map(self):
        player_start_set = False
        geisha_start_set = False
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value == "G" and not geisha_start_set:
                    self.geisha_start_pos = (i + 0.5, j + 0.5)
                    self.mini_map[j][i] = 0
                    geisha_start_set = True
                elif value == "S" and not player_start_set:
                    self.player_start_pos = (i + 0.5, j + 0.5)
                    self.mini_map[j][i] = 0
                    player_start_set = True
                elif value != 0 and value != "G" and value != "S":
                    self.world_map[(i, j)] = value

        # Проверка, что начальные позиции установлены
        if not self.player_start_pos:
            raise ValueError("Player start position not set")
        if not self.geisha_start_pos:
            raise ValueError("Geisha start position not set")

        # Проверка, что world_map корректно заполнен
        if not self.world_map:
            raise ValueError("World map is empty")