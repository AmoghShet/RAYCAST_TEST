import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple DOOM-inspired Raycast")

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
num_rays = screen_width // 2  # Reduced number of rays for performance
max_depth = 8
delta_angle = fov / num_rays
dist_proj_plane = (screen_width / 2) / math.tan(half_fov)
wall_height = screen_height / 2

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Function to cast a ray and find the distance to the wall
def cast_ray(px, py, angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    for depth in range(max_depth * 100):
        x = px + depth * cos_a / 100.0
        y = py + depth * sin_a / 100.0
        if game_map[int(x)][int(y)] == 1:
            return depth / 100.0
    return max_depth

# Function to check for collision
def is_colliding(nx, ny):
    if game_map[int(nx)][int(ny)] == 1:
        return True
    return False

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        new_x = player_x + math.cos(player_angle) * player_speed
        new_y = player_y + math.sin(player_angle) * player_speed
        if not is_colliding(new_x, new_y):
            player_x = new_x
            player_y = new_y
    if keys[pygame.K_s]:
        new_x = player_x - math.cos(player_angle) * player_speed
        new_y = player_y - math.sin(player_angle) * player_speed
        if not is_colliding(new_x, new_y):
            player_x = new_x
            player_y = new_y
    if keys[pygame.K_a]:
        player_angle -= player_turn_speed
    if keys[pygame.K_d]:
        player_angle += player_turn_speed
    if keys[pygame.K_q]:
        new_x = player_x + math.sin(player_angle) * player_speed
        new_y = player_y - math.cos(player_angle) * player_speed
        if not is_colliding(new_x, new_y):
            player_x = new_x
            player_y = new_y
    if keys[pygame.K_e]:
        new_x = player_x - math.sin(player_angle) * player_speed
        new_y = player_y + math.cos(player_angle) * player_speed
        if not is_colliding(new_x, new_y):
            player_x = new_x
            player_y = new_y

    # Raycasting
    screen.fill(black)
    for ray in range(num_rays):
        angle = player_angle - half_fov + ray * delta_angle
        depth = cast_ray(player_x, player_y, angle)
        depth *= math.cos(player_angle - angle)
        wall_height_proj = wall_height / (depth + 0.0001)
        color = (255 / (1 + depth * depth * 0.1),) * 3
        pygame.draw.rect(screen, color, (ray * 2, screen_height / 2 - wall_height_proj / 2, 2, wall_height_proj))

    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
