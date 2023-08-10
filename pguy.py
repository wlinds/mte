import pygame, random
import numpy as np

pygame.init()

# Constants & Screen setup
n = 10 # grid size
cell_size = 50
movement_speed = 60 # FPS

screen_size = (n * cell_size, n * cell_size)
console_height = 80
screen = pygame.display.set_mode((screen_size[0], screen_size[1] + console_height))

p1_color = (145, 120, 40)
default_dot_color = (220, 210, 0)

i = [1,0]
j = [0,1]

class DoItem:
    def __init__(self, pos, color, size, name):
        self.pos = pos
        self.color = color
        self.size = size
        self.name = name

class Player:
    def __init__(self, x, y):
        self.pos = np.array([x, y])

    def move(self, dx, dy):
        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy
        if 0 <= new_x < n and 0 <= new_y < n:
            self.pos[0] = new_x
            self.pos[1] = new_y

p1 = Player(n // 2, n // 2)
do_items = []  # Store DoItem instances (points)
trails = [] # Store position for trail behind player
console_messages = []

def name_vector():
    return chr(random.randint(97, 122))

running = True
while running:
    screen.fill((0, 22, 37))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                do_items.append(DoItem(p1.pos.copy(), default_dot_color, 10, name_vector()))
                print(p1.pos)
                console_messages.insert(0, f"v{do_items[-1].name} created at {p1.pos}")

            elif event.key == pygame.K_2 and do_items:
                closest_index = None
                closest_distance = float('inf')
                for idx, i in enumerate(do_items):
                    distance = np.linalg.norm(i.pos - p1.pos)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_index = idx

                if closest_index is not None:
                    console_messages.insert(0, f"v{do_items[closest_index].name} removed. Distance from player: {closest_distance}")
                    do_items.pop(closest_index)

    # Update
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        p1.move(-1, 0)
    if keys[pygame.K_d]:
        p1.move(1, 0)
    if keys[pygame.K_w]:
        p1.move(0, -1)
    if keys[pygame.K_s]:
        p1.move(0, 1)
    
    trails.append(p1.pos.copy())
    trails = trails[-5:]

    # Draw vectors as points
    for i in do_items:
        pygame.draw.circle(screen, i.color, i.pos * cell_size + cell_size // 2, i.size)

        # Draw lines from player to each vector
        pygame.draw.line(screen, i.color, p1.pos * cell_size + cell_size // 2, i.pos * cell_size + cell_size // 2)

    # Draw plane between the points and the player
    if len(do_items) > 2:
        points = [p1.pos * cell_size + cell_size // 2] + [item.pos * cell_size + cell_size // 2 for item in do_items]
        pygame.draw.polygon(screen, (255, 255, 255, 100), points)

    # Trail (visual only)
    for trail_pos in trails:
        pygame.draw.rect(screen, (160, 165, 150), (trail_pos[0] * cell_size, trail_pos[1] * cell_size, cell_size, cell_size))

    # Grid
    for row in range(n):
        for col in range(n):
            pygame.draw.rect(screen, (0, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

    pygame.draw.rect(screen, p1_color, (p1.pos[0] * cell_size, p1.pos[1] * cell_size, cell_size, cell_size))
    
    # Draw console window
    pygame.draw.rect(screen, (0, 22, 37), (0, screen_size[1], screen_size[0], console_height))
    console_font = pygame.font.Font(None, 16)
    console_text_color = (255, 255, 255)

    if console_height != 0:
        num_lines = min(len(console_messages), console_height // 20 - 1)
    else:
        num_lines = 0

    for i, message in enumerate(console_messages[:num_lines]):
        console_text = console_font.render(message, True, console_text_color)
        screen.blit(console_text, (10, screen_size[1] + console_height - 10 - (i + 1) * 20))
    
    pygame.display.flip()

    game = pygame.time.Clock()
    game.tick(60)

pygame.quit()
