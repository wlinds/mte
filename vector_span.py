import pygame
import pygame.font

pygame.init()
screen_x, screen_y = 640, 640
screen = pygame.display.set_mode((screen_x, screen_y))
screen.fill((0, 22, 37)) # BG RGB

# Axes
center_x, center_y = screen_x/2, screen_y/2
pygame.draw.line(screen, (140, 140, 140), (center_x, 0), (center_x, screen_y), 1)
pygame.draw.line(screen, (140, 140, 140), (0, center_y), (screen_x, center_y), 1)

vectors = []

def add_vector(pos1, pos2):
    vector = [pos2[0] - pos1[0], pos2[1] - pos1[1]]
    vectors.append(vector)

def draw_vectors():
    for vector in vectors:
        x, y = center_x + vector[0], center_y + vector[1]
        text = f"({vector[0]}, {-vector[1]})"
        font = pygame.font.SysFont("Courier New", 14)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (x, y), 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos1 = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            pos2 = pygame.mouse.get_pos()
            add_vector(pos1, pos2)

    draw_vectors()
    pygame.display.update()