import pygame
import random

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Tetris:
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 500
        self.block_size = 20
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.speed = 500
        self.running = True
        self.paused = False
        self.blocks = []
        self.current_block = self.get_random_block()

    def get_random_block(self):
        shapes = [
            [[1, 1, 1],
             [0, 1, 0]],

            [[0, 1, 1],
             [1, 1, 0]],

            [[1, 1, 0],
             [0, 1, 1]],

            [[1, 0, 0],
             [1, 1, 1]],

            [[0, 0, 1],
             [1, 1, 1]],

            [[1, 1, 1, 1]],

            [[1, 1],
             [1, 1]]
        ]
        return random.choice(shapes)

    def draw_block(self, block, x, y):
        for i, row in enumerate(block):
            for j, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(self.screen, WHITE, (x + j * self.block_size, y + i * self.block_size, self.block_size, self.block_size))

    def move_block(self, dx, dy):
        x, y = self.get_block_position()
        new_x, new_y = x + dx, y + dy
        if self.is_valid_position(self.current_block, new_x, new_y):
            self.blocks[-1] = (new_x, new_y)
        else:
            if dy == 1:
                self.blocks.pop()
                self.add_block_to_grid()
                self.check_for_lines()
                self.current_block = self.get_random_block()
                self.blocks.append((self.screen_width // 2, 0))

    def is_valid_position(self, block, x, y):
        for i, row in enumerate(block):
            for j, val in enumerate(row):
                if val == 1:
                    if x + j * self.block_size < 0 or x + j * self.block_size >= self.screen_width:
                        return False
                    if y + i * self.block_size >= self.screen_height:
                        return False
                    for grid_x, grid_y in self.blocks[:-1]:
                        if grid_x == x + j * self.block_size and grid_y == y + i * self.block_size:
                            return False
        return True

    def add_block_to_grid(self):
        x, y = self.get_block_position()
        for i, row in enumerate(self.current_block):
            for j, val in enumerate(row):
                if val == 1:
                    self.blocks.insert(0, (x + j * self.block_size, y + i * self.block_size))

    def check_for_lines(self):
        lines = []
        for y in range(self.screen_height // self.block_size):
            line = True
            for x in range(self.screen_width // self.block_size):
                if (x * self.block_size, y * self.block_size) not in self.blocks:
                    line = False
                    break
            if line:
                lines.append(y)
        if lines:
            self.lines_cleared += len(lines)
            self.score += len(lines) * 100
            for line in lines:
                for x in range(self.screen_width // self.block_size):
                    self.blocks.remove((x * self.block_size, line * self.block_size))
                for i, (x, y) in enumerate(self.blocks):
                    if y < line * self.block_size:
                        self.blocks[i] = (x, y + self.block_size)

    def get_block_position(self):
        return self.blocks[-1]

    def draw_grid(self):
        for y in range(self.screen_height // self.block_size):
            for x in range(self.screen_width // self.block_size):
                pygame.draw.rect(self.screen, GRAY, (x * self.block_size, y * self.block_size, self.block_size, self.block_size), 1)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x, y))

    def run(self):
        self.blocks.append((self.screen_width // 2, 0))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_block(-self.block_size, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_block(self.block_size, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_block(0, self.block_size)
                    elif event.key == pygame.K_UP:
                        self.move_block(0, -self.block_size)
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
            if not self.paused:
                self.move_block(0, self.block_size)
            self.screen.fill(BLACK)
            self.draw_grid()
            for x, y in self.blocks[:-1]:
                pygame.draw.rect(self.screen, WHITE, (x, y, self.block_size, self.block_size))
            self.draw_block(self.current_block, *self.get_block_position())
            self.draw_text(f"Score: {self.score}", 10, 10)
            self.draw_text(f"Lines: {self.lines_cleared}", 10, 40)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
