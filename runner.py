import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from snake import Snake, SnakeAI
from food import Food
import random
import stat


DATA = os.path.join('scores.json')


class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1280, 720      # Size of the screen
        self.grid = 20      # Size of the each box (snake, food, ...)
        self.borders = True    # Enable or disable border collisions
        self._display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption('snake ai')
        self.speed = 0     # Game delay between each frame in milliseconds (speed)
        self.color = (0, 0, 0)
        self.font = pygame.font.Font(None, 40)

        with open(DATA, 'r') as f:
            self.best = int(f.read())
        self.high_score = self.best
        self.current_score = 0

    def on_init(self):
        self._running = True
        self.snake = Snake(self.grid)
        self.snakeAI = SnakeAI(self.size, self.grid)
        self.food = Food(self.grid)
        self.food.new(self.size, self.grid, self.snake.tail)
        self.solution = []

    def on_event(self):
        events = pygame.event.get()

        # Listens to window closing
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False

        # Gets new AI solution when needed
        if not len(self.solution):
            print('new solution')
            self.solution = self.snakeAI.shortest_path((self.snake.x, self.snake.y), (self.food.x, self.food.y), self.snake.tail)
            print(self.solution)

            # Safety check
            if self.solution == None:
                self.solution = []
                return

        move = self.solution.pop()

        # Executes the AI moves
        if move == 'up':
            self.snake.move_up()

        if move == 'down':
            self.snake.move_down()

        if move == 'right':
            self.snake.move_right()

        if move == 'left':
            self.snake.move_left()

    def on_loop(self):
        # Logic of game
        self.snake.move()

        if self.snake.collision_trail():
            self.dead()

        if self.borders:
            if self.snake.borders(self.size):
                self.dead()
        else:
            self.snake.wrap(self.size)

        if self.snake.eat((self.food.x, self.food.y)):
            self.current_score += 1
            self.food.new(self.size, self.grid, self.snake.tail)

        if self.current_score > self.high_score:
            self.high_score = self.current_score

    def dead(self):
        pygame.time.delay(4000)
        self.solution = []
        self.snake.died()
        self.current_score = 0
        print('\nDEAD\n')

    def on_render(self):
        self._display_surf.fill(self.color)

        # Scores
        current_score = self.font.render(f'score: {self.current_score}', True, (255, 255, 255))
        high_score = self.font.render(f'high score: {self.high_score}', True, (255, 255, 255))
        self._display_surf.blit(current_score, (10, 10))
        self._display_surf.blit(high_score, (250, 10))

        # Draws the food
        food_rect = ((self.food.x, self.food.y), (self.food.width, self.food.height))
        self._display_surf.fill(self.food.color, food_rect, special_flags=0)
        pygame.draw.rect(self._display_surf, self.food.color_border, food_rect, 1)

        # Draws the tail of the snake
        for n in self.snake.tail:
            body_rect = (n, (self.snake.width, self.snake.height))
            self._display_surf.fill(self.snake.color_tail, body_rect, special_flags=0)
            pygame.draw.rect(self._display_surf, self.snake.color_border, body_rect, 1)

        # Draws the head of the snake
        head_rect = ((self.snake.x, self.snake.y), (self.snake.width, self.snake.height))
        self._display_surf.fill(self.snake.color_head, head_rect, special_flags=0)
        pygame.draw.rect(self._display_surf, self.snake.color_border, head_rect, 1)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
        if self.high_score > self.best:
            with open(DATA, 'w') as f:
                f.write(str(self.high_score))

    def on_execute(self):
        self.on_init()

        while self._running:
            pygame.time.delay(self.speed)
            self.on_event()
            self.on_loop()
            self.on_render()
        self.on_cleanup()


def setup():
    if not os.path.exists(DATA):
        with open(DATA, 'w') as f:
            f.write('0')
        f.close()
    os.chflags(DATA, stat.UF_HIDDEN)


def main():
    setup()
    game = Game()
    game.on_execute()


main()
