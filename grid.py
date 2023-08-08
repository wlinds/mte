import pygame
import numpy as np
import math

pygame.init()
n = 17
cell_size = 30
movement_speed = 20

screen_size = (n * cell_size, n * cell_size)
screen = pygame.display.set_mode(screen_size)
font = pygame.font.Font(None, 16)
text_color = (140, 140, 250)

player_pos = np.array([n // 2, n // 2])
player_color = (145, 120, 40)

v1 = np.array([n - 1, n // 2])
random_player_color = (255, 0, 0)

arrow_color = (0, 255, 0)
def generate_random_unit_vector():
    angle = np.random.uniform(0, 2 * np.pi)  # Random angle in radians
    unit_vector = np.array([math.cos(angle), math.sin(angle)])
    return unit_vector

arrow_vector = None
show_arrow = False

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button clicked
            arrow_vector = generate_random_unit_vector()
            show_arrow = True

    v1[0] -= 1
    if v1[0] < 0:
        v1[0] = n - 1

    # Key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= 1
    if keys[pygame.K_d] and player_pos[0] < n - 1:
        player_pos[0] += 1
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= 1
    if keys[pygame.K_s] and player_pos[1] < n - 1:
        player_pos[1] += 1

    screen.fill((0, 22, 37))

    # Draw the grid
    for row in range(n):
        for col in range(n):
            pygame.draw.rect(screen, (0, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

    # Origin lines
    pygame.draw.line(screen, (34, 34, 57), (0, n * cell_size // 2), (screen_size[0], n * cell_size // 2), 2)
    pygame.draw.line(screen, (34, 34, 57), (n * cell_size // 2, 0), (n * cell_size // 2, screen_size[1]), 2)

    # Draw the player square and translate text position
    pygame.draw.rect(screen, player_color, (player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size))

    player_vector_text = font.render(f"({player_pos[0] - n // 2}, {n // 2 - player_pos[1]})", True, text_color)
    text_x = player_pos[0] * cell_size
    text_y = (player_pos[1] - 1/2) * cell_size
    screen.blit(player_vector_text, (text_x, text_y))

    # Draw v1
    pygame.draw.rect(screen, random_player_color, (v1[0] * cell_size, v1[1] * cell_size, cell_size, cell_size))
    v1_text = font.render(f"({v1[0] - n // 2}, {n // 2 - v1[1]})", True, text_color)
    text_x = v1[0] * cell_size
    text_y = (v1[1] - 1/2) * cell_size
    screen.blit(v1_text, (text_x, text_y))

    # Weird vector
    if show_arrow and arrow_vector is not None:
        arrow_start = v1 * cell_size
        arrow_end = player_pos * cell_size
        pygame.draw.line(screen, arrow_color, arrow_start, arrow_end, 2)

    pygame.display.flip()

    clock.tick(movement_speed)  # Control frame rate

pygame.quit()
