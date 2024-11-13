import pygame
import math

# Initialize pygame
pygame.init()

# Screen and game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FOV = math.pi / 3
DEPTH = 16
MOVE_SPEED = 0.1
TURN_SPEED = 0.05
MAP_WIDTH, MAP_HEIGHT = 16, 16

# Colors for sky and ground
SKY_COLOR_TOP = (135, 206, 235)
SKY_COLOR_BOTTOM = (110, 150, 200)
GROUND_COLOR = (50, 50, 50)

# Map layout (1 = wall, 0 = empty space)
MAP = (
    "################"
    "#..............#"
    "#......##......#"
    "#..####........#"
    "#..#...........#"
    "#..#....##.....#"
    "#..............#"
    "#......###.....#"
    "#......#.......#"
    "#..............#"
    "#......##......#"
    "#..............#"
    "#..............#"
    "#......#.......#"
    "#..............#"
    "################"
)

# Player attributes
player_x, player_y, player_angle = 8.0, 8.0, 0.0

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Optimized 3D Environment")
clock = pygame.time.Clock()

# Function to render the 3D scene
def render_scene():
    # Sky gradient
    for y in range(SCREEN_HEIGHT // 2):
        blend = y / (SCREEN_HEIGHT // 2)
        color = (
            int(SKY_COLOR_TOP[0] * (1 - blend) + SKY_COLOR_BOTTOM[0] * blend),
            int(SKY_COLOR_TOP[1] * (1 - blend) + SKY_COLOR_BOTTOM[1] * blend),
            int(SKY_COLOR_TOP[2] * (1 - blend) + SKY_COLOR_BOTTOM[2] * blend),
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

    # Ground
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

    # Render walls and objects
    for x in range(SCREEN_WIDTH):
        ray_angle = (player_angle - FOV / 2.0) + (x / SCREEN_WIDTH) * FOV
        distance_to_wall, hit_wall = 0, False
        eye_x, eye_y = math.sin(ray_angle), math.cos(ray_angle)

        while not hit_wall and distance_to_wall < DEPTH:
            distance_to_wall += 0.1
            test_x, test_y = int(player_x + eye_x * distance_to_wall), int(player_y + eye_y * distance_to_wall)

            if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                hit_wall, distance_to_wall = True, DEPTH
            elif MAP[test_y * MAP_WIDTH + test_x] == "#":
                hit_wall = True

        # Calculate wall slice height and shading
        wall_height = int(SCREEN_HEIGHT / (distance_to_wall + 0.1))
        wall_top, wall_bottom = (SCREEN_HEIGHT // 2) - (wall_height // 2), (SCREEN_HEIGHT // 2) + (wall_height // 2)

        shade = max(0, 255 - int(distance_to_wall * 255 / DEPTH))
        wall_color = (shade, shade, shade // 2)
        pygame.draw.line(screen, wall_color, (x, wall_top), (x, wall_bottom))

        # Floor casting with depth-based shading
        for y in range(wall_bottom, SCREEN_HEIGHT):
            depth = SCREEN_HEIGHT / (2.0 * y - SCREEN_HEIGHT)
            shade = max(0, 255 - int(depth * 255 / DEPTH))
            floor_color = (shade, shade, shade)
            pygame.draw.line(screen, floor_color, (x, y), (x, y))

# Player movement controls with mouse for rotation
def move_player():
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:  # Move forward
        new_x = player_x + math.sin(player_angle) * MOVE_SPEED
        new_y = player_y + math.cos(player_angle) * MOVE_SPEED
        if MAP[int(new_y) * MAP_WIDTH + int(new_x)] != "#":
            player_x, player_y = new_x, new_y
    if keys[pygame.K_s]:  # Move backward
        new_x = player_x - math.sin(player_angle) * MOVE_SPEED
        new_y = player_y - math.cos(player_angle) * MOVE_SPEED
        if MAP[int(new_y) * MAP_WIDTH + int(new_x)] != "#":
            player_x, player_y = new_x, new_y

    # Mouse-based rotation
    mouse_x, _ = pygame.mouse.get_pos()
    player_angle += (mouse_x - SCREEN_WIDTH // 2) * TURN_SPEED * 0.01
    pygame.mouse.set_pos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Game loop
running = True
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)  # Lock the mouse in the window

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_player()
    render_scene()
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
