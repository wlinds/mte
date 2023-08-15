import pygame, random
import numpy as np

# Constants & Screen setup
pygame.init()
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
    return chr(random.randint(97, 122)) # Randomizes random lowercase character

def display_text_with_border(text, font_size):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (255, 255, 255))

    # Create black-bordered surface
    border_size = 2
    bordered_surface = pygame.Surface((text_surface.get_width() + border_size * 2, text_surface.get_height() + border_size * 2))
    bordered_surface.fill((0, 0, 0))
    bordered_surface.blit(text_surface, (border_size, border_size))

    screen_center = (screen_size[0] // 2, screen_size[1] // 2)

    text_position = (screen_center[0] - bordered_surface.get_width() // 2, screen_center[1] - bordered_surface.get_height() // 2)

    screen.blit(bordered_surface, text_position)

command_list =[
    'ls', 'Lists the contents of the current directory.',
    'cd', 'Changes the current directory.',
    'pwd', 'Prints the current working directory.',
    'mkdir', 'Creates a new directory.',
    'touch', 'Creates a new empty file.',
    'rm', 'Removes a file or directory.',
    'cp', 'Copies a file or directory.',
    'mv', 'Moves or renames a file or directory.',
    'echo', 'Prints text to the terminal.',
    'man', 'Displays the manual page for a command.',
    'cat', 'Displays the contents of a file.',
    'grep', 'Searches for a pattern in a file.',
    'sort', 'Sorts the lines in a file.',
    'uniq', 'Removes duplicate lines from a file.',
    'wc', 'Counts the lines, words, and characters in a file.',
    'more', 'Allows you to scroll through the contents of a file.',
    'less', 'Allows you to scroll through the contents of a file, and search for text.',
    'history', 'Displays a list of previously entered commands.',
    'sudo', 'Allows you to run commands with root privileges.',
    ]

running = True
draw_area = False  # Toggle for drawing area
q_key_pressed = False  # Flag to track key press state

# Initial position for 3 random squares
random_squares = [[random.randint(0, n - 1), random.randint(0, n - 1)] for _ in range(3)]

# Initial selection of commands
def random_even(input_list, n):
  even_numbers = []
  for _ in range(n):
    random_number = random.randrange(0, len(input_list), 2)
    even_numbers.append(random_number)

  return even_numbers

selected_numbers = random_even(command_list, 3)

while running:
    screen.fill((0, 22, 37))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            # Create vector (Keybind 1)
            if event.key == pygame.K_1:
                do_items.append(DoItem(p1.pos.copy(), default_dot_color, 10, name_vector()))
                print(p1.pos)
                console_messages.insert(0, f"v{do_items[-1].name} created at {p1.pos}")

            # Remove closest vector (Keybind 2)
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

    # Update player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        p1.move(-1, 0)
    if keys[pygame.K_d]:
        p1.move(1, 0)
    if keys[pygame.K_w]:
        p1.move(0, -1)
    if keys[pygame.K_s]:
        p1.move(0, 1)

    # Toggle vector area (Keybind Q)
    if keys[pygame.K_q] and len(do_items) > 2:
        if not q_key_pressed:
            q_key_pressed = True
            draw_area = not draw_area
    else:
        q_key_pressed = False

    if draw_area and len(do_items) > 2:
        points = [p1.pos * cell_size + cell_size // 2] + [item.pos * cell_size + cell_size // 2 for item in do_items]
        pygame.draw.polygon(screen, (255, 255, 255, 100), points)

    # # Place random square
    # p4 = DoItem([random.randint(0,n-1), random.randint(0,n-1)], (0, 11, 37), n, "hej")
    # print(p4.pos)
    # pygame.draw.rect(screen, p4.color, (p4.pos[0] * cell_size, p4.pos[1] * cell_size, cell_size, cell_size))

    # Trail (visual only)
    trails.append(p1.pos.copy())
    trails = trails[-5:]
    for trail_pos in trails:
        pygame.draw.rect(screen, (160, 165, 150), (trail_pos[0] * cell_size, trail_pos[1] * cell_size, cell_size, cell_size))

    # Grid
    for row in range(n):
        for col in range(n):
            pygame.draw.rect(screen, (0, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

    # Draw vectors as points
    for i in do_items:
        pygame.draw.circle(screen, i.color, i.pos * cell_size + cell_size // 2, i.size)

        # Draw lines from player to each vector
        pygame.draw.line(screen, i.color, p1.pos * cell_size + cell_size // 2, i.pos * cell_size + cell_size // 2)

    # Update random square position after player selection
    for idx, square_pos in enumerate(random_squares):
        if p1.pos.tolist() == square_pos:
            random_squares = [[random.randint(0, n - 1), random.randint(0, n - 1)] for _ in range(3)]

            selected_numbers = random_even(command_list, 3)

            display_text_with_border(command_list[selected_numbers[0]+1],cell_size // 2)

            break

    

    # Draw the random squares with the selected questions
    for idx, square_pos in enumerate(random_squares):
        pygame.draw.rect(screen, (0, 11, 37), (square_pos[0] * cell_size, square_pos[1] * cell_size, cell_size, cell_size))
        font = pygame.font.Font(None, 36)
        text_surface = font.render((command_list[selected_numbers[idx]]), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(square_pos[0] * cell_size + cell_size // 2, square_pos[1] * cell_size + cell_size // 2))
        display_text_with_border(command_list[selected_numbers[0]+1], cell_size // 2)

        screen.blit(text_surface, text_rect)

    
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
