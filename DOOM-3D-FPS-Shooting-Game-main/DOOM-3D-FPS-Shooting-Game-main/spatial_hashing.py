class SpatialHashing:
    def __init__(self, cell_size=1):
        self.cell_size = cell_size
        self.grid = {}

    def hash_position(self, pos):
        return tuple(int(x // self.cell_size) for x in pos)

    def insert(self, obj, pos):
        key = self.hash_position(pos)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(obj)

    def query(self, pos):
        key = self.hash_position(pos)
        return self.grid.get(key, [])