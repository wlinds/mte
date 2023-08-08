import pygame
import numpy as np
import math

pygame.init()
n = 17
cell_size = 30
movement_speed = 20

screen_size = (n * cell_size, n * cell_size)
console_height = 80
console_color = (0, 22, 37)
console_font = pygame.font.Font(None, 16)
console_text_color = (255, 255, 255)

screen = pygame.display.set_mode((screen_size[0], screen_size[1] + console_height))
font = pygame.font.Font(None, 16)
text_color = (140, 140, 250)

player_pos = np.array([n // 2, n // 2])
player_color = (145, 120, 40)

v1 = np.array([n - 1, n // 2])  # Initial position for the random player (right side)
v1_speed = 1  # Speed of v1 movement
random_player_color = (255, 0, 0)  # Color for the random player
smooth_wave = [9.9781585, 0.6605701]

arrow_color = (0, 255, 0)
def generate_random_unit_vector():
    angle = np.random.uniform(0, 2 * np.pi)  # Random angle in radians
    unit_vector = np.array([math.cos(angle), math.sin(angle)])
    return unit_vector

arrow_vector = None
show_arrow = False

# Transformation matrix
transformation_matrix = np.eye(2)  # Identity matrix as initial transformation

console_messages = []  # List to store console messages

clock = pygame.time.Clock()

def add_console_message(message):
    console_messages.append(message)
    if len(console_messages) > 10:
        console_messages.pop(0)  # Remove oldest message if there are more than 10 messages

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button clicked
            arrow_vector = generate_random_unit_vector()
            arrow_vector = smooth_wave
            show_arrow = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                transformation_matrix = np.array([[1, 0], [0, 1]])  # Identity matrix
            elif event.key == pygame.K_2:
                # Define the transformation matrix based on the selected vector pairs
                v1_basis = np.array([v1, np.array([v1[0], 0])])  # First vector pair
                v2_basis = np.array([np.array([0, v1[1]]), np.array([0, 1])])  # Second vector pair
                transformation_matrix = np.linalg.inv(v1_basis).dot(v2_basis)  # Calculate the transformation matrix

    v1[0] -= v1_speed
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

    if show_arrow and arrow_vector is not None:
        # Alter the direction of v1 based on arrow_vector
        v1_angle = np.arctan2(v1[1] - n // 2, v1[0] - n // 2)  # Calculate angle of v1
        arrow_angle = np.arctan2(arrow_vector[1], arrow_vector[0])  # Calculate angle of arrow_vector
        new_v1_angle = v1_angle + arrow_angle  # Update angle of v1
        v1_magnitude = np.linalg.norm(v1 - (n // 2, n // 2))  # Calculate magnitude of v1
        add_console_message(f"v1 magnitude: {v1_magnitude:.2f}")
        v1 = np.array([n // 2 + v1_magnitude * np.cos(new_v1_angle), n // 2 + v1_magnitude * np.sin(new_v1_angle)])

    screen.fill((0, 22, 37))

    # Apply the transformation to the grid
    for row in range(n):
        for col in range(n):
            transformed_pos = np.dot(transformation_matrix, np.array([col, row]))  # Apply the transformation
            pygame.draw.rect(screen, (0, 0, 0), (transformed_pos[0] * cell_size, transformed_pos[1] * cell_size, cell_size, cell_size), 1)

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
    player_vector_text = font.render(f"({v1[0] - n // 2}, {n // 2 - v1[1]})", True, text_color)
    text_x = v1[0] * cell_size
    text_y = (v1[1] - 1/2) * cell_size
    screen.blit(player_vector_text, (text_x, text_y))

    # Weird vector
    if show_arrow and arrow_vector is not None:
        
        #arrow_start = (n // 2) * cell_size + cell_size // 2, (n // 2) * cell_size + cell_size // 2  # Origin
        arrow_start = player_pos[0] * cell_size, player_pos[1] * cell_size

        arrow_end = arrow_start[0] + arrow_vector[0] * cell_size, arrow_start[1] - arrow_vector[1] * cell_size
        pygame.draw.line(screen, arrow_color, arrow_start, arrow_end, 2)
        pygame.draw.polygon(screen, arrow_color, [(arrow_end[0] - 8, arrow_end[1] + 8), arrow_end, (arrow_end[0] + 8, arrow_end[1] + 8)])

    # Draw console window
    pygame.draw.rect(screen, console_color, (0, screen_size[1], screen_size[0], console_height))
    for i, message in enumerate(console_messages):
        console_text = console_font.render(message, True, console_text_color)
        screen.blit(console_text, (10, screen_size[1] + 10 + i * 20))

    pygame.display.flip()

    clock.tick(movement_speed)  # Control frame rate

pygame.quit()
