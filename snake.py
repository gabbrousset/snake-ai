from util import *


class Snake:
    def __init__(self, grid):
        self.initial_position = (grid * 4, grid * 4)
        self.x, self.y = self.initial_position
        self.width = grid
        self.height = grid
        self.tail = []
        self.initial_size = 3
        self.size = self.initial_size
        self.speed = grid
        self.x_vel = self.speed
        self.y_vel = 0
        self.color_head = (255, 0, 0)
        self.color_tail = (200, 200, 200)
        self.color_border = (0, 0, 0)

    def eat(self, food):
        x, y = food
        if self.x == x and self.y == y:
            self.size += 1
            return True
        return False

    def borders(self, size):
        width, height = size
        if self.x < 0 or self.y < 0:
            return True
        if self.x + self.width > width or self.y + self.height > height:
            return True
        return False

    def wrap(self, size):
        width, height = size
        if self.x < 0:
            self.x = width - self.width
        if self.x + self.width > width:
            self.x = 0
        if self.y < 0:
            self.y = height - self.height
        if self.y + self.height > height:
            self.y = 0

    def collision_trail(self):
        if (self.x, self.y) in self.tail:
            return True
        return False

    def move(self):
        self.tail.insert(0, (self.x, self.y))
        while len(self.tail) > self.size:
            self.tail.pop()
        self.x += self.x_vel
        self.y += self.y_vel

    def move_up(self):
        self.x_vel = 0
        self.y_vel = -self.speed

    def move_down(self):
        self.x_vel = 0
        self.y_vel = +self.speed

    def move_right(self):
        self.x_vel = self.speed
        self.y_vel = 0

    def move_left(self):
        self.x_vel = -self.speed
        self.y_vel = 0

    def died(self):
        self.x, self.y = self.initial_position
        self.tail = []
        self.size = self.initial_size
        self.x_vel = self.speed
        self.y_vel = 0


class SnakeAI:
    def __init__(self, size, grid):
        self.width, self.height = size
        self.grid = grid

    def shortest_path(self, source, goal, initial_tail):
        initial_tail.insert(0, source)
        start = Node(source, None, None, 0, initial_tail)
        frontier = QueueFrontier()
        frontier.add(start)

        explored = set()

        while True:
            if frontier.empty():
                return None

            node = frontier.remove()

            explored.add(node.state)

            for action, state in self.neighbors(node.state):
                tail = node.tail.copy()
                tail.insert(0, state)
                tail.pop()
                if not frontier.contains_state(state) and state not in explored:
                    if not self.obstacles(state, tail):
                        child = Node(state, node, action, node.count + 1, tail)
                        frontier.add(child)

                        if child.state == goal:
                            solution = []
                            while child.parent is not None:
                                solution.append(child.action)
                                child = child.parent
                            return solution

    def neighbors(self, state):
        x, y = state
        moves = set()

        if y >= self.grid:
            moves.add(('up', (x, y - self.grid)))
        if y < self.height - self.grid - 1:
            moves.add(('down', (x, y + self.grid)))
        if x < self.width - self.grid - 1:
            moves.add(('right', (x + self.grid, y)))
        if x >= self.grid:
            moves.add(('left', (x - self.grid, y)))

        return moves

    def obstacles(self, state, tail):
        if state in tail[1:]:
            return True
        return False
