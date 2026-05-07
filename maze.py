import random
import collections
import heapq
import time

class Maze:
    def __init__(self, rows=21, cols=21):
        # Keep odd dimensions for proper maze generation
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.grid = []
        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)
        self.generate()

    def generate(self):
        # Fill with walls
        self.grid = [[1] * self.cols for _ in range(self.rows)]

        def carve(r, c):
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows and 0 < nc < self.cols and self.grid[nr][nc] == 1:
                    self.grid[r + dr // 2][c + dc // 2] = 0  # Remove wall between
                    self.grid[nr][nc] = 0
                    carve(nr, nc)

        self.grid[1][1] = 0
        carve(1, 1)
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.end[0]][self.end[1]] = 0

    def bfs(self):
        start_time = time.time()
        queue = collections.deque([(self.start, [self.start])])
        visited = {self.start}
        explored = []

        while queue:
            (r, c), path = queue.popleft()
            explored.append((r, c))
            if (r, c) == self.end:
                return path, explored, time.time() - start_time

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == 0 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(((nr, nc), path + [(nr, nc)]))

        return [], explored, time.time() - start_time

    def dfs(self):
        start_time = time.time()
        stack = [(self.start, [self.start])]
        visited = {self.start}
        explored = []

        while stack:
            (r, c), path = stack.pop()
            explored.append((r, c))
            if (r, c) == self.end:
                return path, explored, time.time() - start_time

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == 0 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        stack.append(((nr, nc), path + [(nr, nc)]))

        return [], explored, time.time() - start_time

    def astar(self):
        start_time = time.time()

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        heap = [(0 + heuristic(self.start, self.end), 0, self.start, [self.start])]
        visited = {}
        explored = []

        while heap:
            f, g, (r, c), path = heapq.heappop(heap)
            if (r, c) in visited:
                continue
            visited[(r, c)] = True
            explored.append((r, c))

            if (r, c) == self.end:
                return path, explored, time.time() - start_time

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == 0 and (nr, nc) not in visited:
                        new_g = g + 1
                        new_f = new_g + heuristic((nr, nc), self.end)
                        heapq.heappush(heap, (new_f, new_g, (nr, nc), path + [(nr, nc)]))

        return [], explored, time.time() - start_time

    def solve(self, algorithm="bfs"):
        if algorithm == "bfs":
            return self.bfs()
        elif algorithm == "dfs":
            return self.dfs()
        elif algorithm == "astar":
            return self.astar()