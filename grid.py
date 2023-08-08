import pygame
import numpy as np
import math

pygame.init()
n = 17
cell_size = 30
movement_speed = 40

screen_size = (n * cell_size, n * cell_size)
screen = pygame.display.set_mode(screen_size)
font = pygame.font.Font(None, 16)
text_color = (140, 140, 250)

player_pos = np.array([n // 2, n // 2])
player_color = (145, 120, 40)

arrow_color = (0, 255, 0)

clock = pygame.time.Clock()

def generate_random_unit_vector():
    angle = np.random.uniform(0, 2 * np.pi)  # Random angle in radians
    unit_vector = np.array([math.cos(angle), math.sin(angle)])
    return unit_vector

arrow_vector = None
show_arrow = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button clicked
            arrow_vector = generate_random_unit_vector()
            show_arrow = True

    # Key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 1
    if keys[pygame.K_RIGHT] and player_pos[0] < n - 1:
        player_pos[0] += 1
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= 1
    if keys[pygame.K_DOWN] and player_pos[1] < n - 1:
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

    # Weird vector
    if show_arrow and arrow_vector is not None:
        arrow_start = (n // 2) * cell_size + cell_size // 2, (n // 2) * cell_size + cell_size // 2  # Origin
        arrow_end = arrow_start[0] + arrow_vector[0] * cell_size, arrow_start[1] - arrow_vector[1] * cell_size
        pygame.draw.line(screen, arrow_color, arrow_start, arrow_end, 2)
        pygame.draw.polygon(screen, arrow_color, [(arrow_end[0] - 8, arrow_end[1] + 8), arrow_end, (arrow_end[0] + 8, arrow_end[1] + 8)])

    pygame.display.flip()

    clock.tick(movement_speed)  # Control frame rate

pygame.quit()
