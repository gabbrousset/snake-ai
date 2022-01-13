import random


class Food:
    def __init__(self, grid):
        self.width = grid
        self.height = grid
        self.color = (0, 0, 255)
        self.color_border = (0, 0, 0)

    def new(self, size, grid, snake):
        width, height = size
        while len(snake) < width/grid * height/grid:
            self.x = random.randrange(0, width-self.width, grid)
            self.y = random.randrange(0, height-self.height, grid)
            if (self.x, self.y) not in snake:
                break
