# Simple DOOM-inspired Raycasting Testing in Pygame
 
## Overview

This project is a simple raycasting engine inspired by classics such as DOOM & Wolfenstein 3D, created using Pygame. The engine casts rays from the player's position to detect walls in a 2D map and renders a 3D view of the environment.

## Features

- Basic player movement (forward, backward, strafe left, strafe right, rotate left, rotate right).
- Simple collision detection.
- Real-time 3D rendering of a 2D map using raycasting.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install Pygame using pip:
    ```sh
    pip install pygame
    ```

## Usage

1. Save the script  `strafe.py`.
2. Run the script:
    ```sh
    python3 strafe.py
    ```

## Code Description

### Initialization

The script starts by importing the necessary libraries, initializing Pygame, and setting up the screen dimensions and display.

```python
import pygame
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple DOOM-inspired Raycast")
```

### Map and Player Setup

A 2D map is defined using a nested list where `1` represents walls and `0` represents empty space. The player's initial position, angle, speed, and turn speed are also defined.

```python
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

player_x = 2.0
player_y = 2.0
player_angle = 0.0
player_speed = 0.05
player_turn_speed = 0.03
```

### Raycasting Parameters

Parameters for the field of view, number of rays, and depth of the projection plane are defined to control the raycasting process.

```python
fov = math.pi / 3
half_fov = fov / 2
num_rays = screen_width // 2
max_depth = 8
delta_angle = fov / num_rays
dist_proj_plane = (screen_width / 2) / math.tan(half_fov)
wall_height = screen_height / 2
```

### Main Functions

#### `cast_ray(px, py, angle)`

This function casts a ray from the player's position at a given angle and returns the distance to the nearest wall.

```python
def cast_ray(px, py, angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    for depth in range(max_depth * 100):
        x = px + depth * cos_a / 100.0
        y = py + depth * sin_a / 100.0
        if game_map[int(x)][int(y)] == 1:
            return depth / 100.0
    return max_depth
```

#### `is_colliding(nx, ny)`

This function checks if the new position `(nx, ny)` would collide with a wall.

```python
def is_colliding(nx, ny):
    if game_map[int(nx)][int(ny)] == 1:
        return True
    return False
```

### Main Loop

The main loop handles player input, movement, raycasting, and rendering.

```python
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    screen.fill((0, 0, 0))
    for ray in range(num_rays):
        angle = player_angle - half_fov + ray * delta_angle
        depth = cast_ray(player_x, player_y, angle)
        depth *= math.cos(player_angle - angle)
        wall_height_proj = wall_height / (depth + 0.0001)
        color = (255 / (1 + depth * depth * 0.1),) * 3
        pygame.draw.rect(screen, color, (ray * 2, screen_height / 2 - wall_height_proj / 2, 2, wall_height_proj))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

## Controls

- `W`: Move forward
- `S`: Move backward
- `A`: Rotate left
- `D`: Rotate right
- `Q`: Strafe left
- `E`: Strafe right

## Notes

- The number of rays has been reduced for performance optimization. Adjust `num_rays` for higher quality at the cost of performance.
- Collision detection is rudimentary and may be improved for more complex maps.

Enjoy exploring the raycasting engine!
