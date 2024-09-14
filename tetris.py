import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Initialize font
font = pygame.font.Font(None, 36)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Screen dimensions
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris Test")

# Block size
block_size = 30

# Tetris grid
grid = [[0 for _ in range(10)] for _ in range(20)]

# Tetromino shapes
shapes = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]],  # O-shape
    [[0, 1, 0], [1, 1, 1]],  # T-shape
    [[1, 1, 0], [0, 1, 1]],  # S-shape
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 0, 0], [1, 1, 1]],  # L-shape
    [[0, 0, 1], [1, 1, 1]],  # J-shape
]

# Tetromino colors
colors = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
]

# Current tetromino
current_shape = None
current_color = None
current_x = 3
current_y = 0

# Global score variable
score = 0

# Functions
def draw_grid():
    for x in range(0, screen_width, block_size):
        pygame.draw.line(screen, gray, (x, 0), (x, screen_height))
    for y in range(0, screen_height, block_size):
        pygame.draw.line(screen, gray, (0, y), (screen_width, y))

def draw_shape():
    for y in range(len(current_shape)):
        for x in range(len(current_shape[y])):
            if current_shape[y][x] == 1:
                pygame.draw.rect(screen, current_color, (
                    (current_x + x) * block_size, (current_y + y) * block_size, block_size, block_size))

def check_collision(shape=None, offset_x=0, offset_y=0):
    if shape is None:
        shape = current_shape
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x] == 1:
                if (current_y + y + offset_y >= len(grid) or 
                    current_x + x + offset_x < 0 or 
                    current_x + x + offset_x >= len(grid[0]) or 
                    grid[current_y + y + offset_y][current_x + x + offset_x] != 0):
                    return True
    return False

def lock_shape():
    for y in range(len(current_shape)):
        for x in range(len(current_shape[y])):
            if current_shape[y][x] == 1:
                grid[current_y + y][current_x + x] = current_color  # Lock the color in the grid

def new_shape():
    global current_shape, current_color, current_x, current_y
    current_shape = random.choice(shapes)  # Randomly select a new shape
    current_color = colors[shapes.index(current_shape)]  # Get the corresponding color
    current_x = 3  # Reset horizontal position
    current_y = 0  # Reset vertical position

    if check_collision():  # If the new shape collides immediately, game over
        game_over_sequence()
        pygame.quit()
        exit()

def draw_locked_pieces():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, grid[y][x], (
                    x * block_size, y * block_size, block_size, block_size))

def rotate_shape():
    global current_shape, current_x, current_y
    rotated_shape = list(zip(*current_shape[::-1]))
    kick_offsets = [(0, 0), (-1, 0), (1, 0), (0, -1)]  # Basic wall kick offsets

    for offset_x, offset_y in kick_offsets:
        if not check_collision(rotated_shape, offset_x, offset_y):
            current_shape = rotated_shape
            current_x += offset_x
            current_y += offset_y
            return True
    return False

def clear_rows():
    global grid
    full_rows = []
    for y in range(len(grid)):
        if all(cell != 0 for cell in grid[y]):
            full_rows.append(y)
    
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0 for _ in range(10)])
    
    return len(full_rows)

def update_score(cleared_rows):
    global score
    points = [0, 40, 100, 300, 1200]  # Points for 0, 1, 2, 3, 4 rows
    score += points[cleared_rows]

def draw_score():
    score_surface = font.render(f"Score: {score}", True, white)
    screen.blit(score_surface, (10, 10))

def game_over_sequence():
    game_over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 36)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    score_text = score_font.render(f"Final Score: {score}", True, white)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    blink_timer = 0
    show_text = True

    for _ in range(10):  # Blink 5 times (on and off)
        screen.fill(black)
        if show_text:
            screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        pygame.display.flip()
        
        time.sleep(0.5)  # Wait for 0.5 seconds
        show_text = not show_text

    # Wait for a key press or 3 seconds before exiting
    start_time = time.time()
    while time.time() - start_time < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                return
        pygame.display.flip()
        clock.tick(60)

# Game loop
clock = pygame.time.Clock()
fall_speed = 0.5
fall_time = 0
fast_fall = False

# Start with a new shape
new_shape()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(offset_x=-1):
                    current_x -= 1
            if event.key == pygame.K_RIGHT:
                if not check_collision(offset_x=1):
                    current_x += 1
            if event.key == pygame.K_SPACE:
                rotate_shape()
            if event.key == pygame.K_DOWN:
                fast_fall = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fast_fall = False

    # Tetromino falling
    fall_time += clock.get_time()
    if fast_fall:
        fall_speed = 0.05
    else:
        fall_speed = 0.5
    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        current_y += 1
        if check_collision():
            current_y -= 1
            lock_shape()
            cleared_rows = clear_rows()  # Clear completed rows
            update_score(cleared_rows)  # Update the score
            new_shape()

    # Drawing
    screen.fill(black)
    draw_grid()
    draw_locked_pieces()  # Add this line to draw the locked pieces
    draw_shape()
    draw_score()  # Add this line to draw the score

    # Update display
    pygame.display.update()

    # Control game speed
    clock.tick(60)

