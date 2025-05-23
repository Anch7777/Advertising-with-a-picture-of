from collections import deque

class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.graph = {}
        self.get_graph()

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, value in enumerate(row):
                if value == 0:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if self.is_valid_node(x + dx, y + dy)]

    def is_valid_node(self, x, y):
        if 0 <= x < len(self.map[0]) and 0 <= y < len(self.map):
            return self.map[y][x] == 0
        return False

    def bfs(self, start, goal):
        queue = deque([start])
        visited = {start: None}
        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = self.graph.get(cur_node, [])
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_path(self, start, goal):
        visited = self.bfs(start, goal)
        path = []
        current = goal
        while current != start and current is not None:
            path.append(current)
            current = visited[current]
        if current == start:
            path.append(current)
        return path[::-1]