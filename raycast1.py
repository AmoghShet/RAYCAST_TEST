import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple DOOM-inspired FPS")

# Map (1 - wall, 0 - empty space)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

# Player attributes
player_x = 2.0
player_y = 2.0
player_angle = 0.0
player_speed = 0.05
player_turn_speed = 0.03

# Raycasting parameters
fov = math.pi / 3
half_fov = fov / 2
num_rays = screen_width
max_depth = 8
delta_angle = fov / num_rays
dist_proj_plane = (screen_width / 2) / math.tan(half_fov)
wall_height = screen_height / 2

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_x += math.cos(player_angle) * player_speed
        player_y += math.sin(player_angle) * player_speed
    if keys[pygame.K_s]:
        player_x -= math.cos(player_angle) * player_speed
        player_y -= math.sin(player_angle) * player_speed
    if keys[pygame.K_a]:
        player_angle -= player_turn_speed
    if keys[pygame.K_d]:
        player_angle += player_turn_speed

    # Raycasting
    screen.fill(black)
    for ray in range(num_rays):
        angle = player_angle - half_fov + ray * delta_angle
        for depth in range(max_depth):
            target_x = player_x + depth * math.cos(angle)
            target_y = player_y + depth * math.sin(angle)

            if game_map[int(target_x)][int(target_y)] == 1:
                depth *= math.cos(player_angle - angle)
                wall_height_proj = wall_height / (depth + 0.0001)
                color = (255 / (1 + depth * depth * 0.1),) * 3
                pygame.draw.rect(screen, color, (ray, screen_height / 2 - wall_height_proj / 2, 1, wall_height_proj))
                break

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
