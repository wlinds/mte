import pygame, pygame.font
import random
import numpy as np

pygame.init()
screen_x, screen_y = 640, 640
screen = pygame.display.set_mode((screen_x, screen_y))
center_x, center_y = screen_x/2, screen_y/2


def draw_ax():
    screen.fill((0, 22, 37)) # BG RGB
    pygame.draw.line(screen, (140, 140, 140), (center_x, 0), (center_x, screen_y), 1)
    pygame.draw.line(screen, (140, 140, 140), (0, center_y), (screen_x, center_y), 1)

vectors = []
vector_name= []

def add_vector(pos1, pos2):
    vector = [pos2[0] - center_x, pos2[1] - center_y] # Always relative to origo

    var_name = chr(random.randint(65, 90)).lower()
    while var_name in vector_name:
        var_name = chr(random.randint(65, 90)).lower()  # reroll if exist

    vector_name.append(var_name)
    vectors.append(vector)
    print(var_name, vector)

def draw_vectors():
    for vector in vectors:
        x, y = center_x + vector[0], center_y + vector[1]
        text = f"({vector[0]}, {-vector[1]})"
        font = pygame.font.SysFont("Courier New", 14)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))
        pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (x, y), 1)

def draw_v_list():
    x, y = screen_x -220, 10
    width, height = 100, 25
    y_offset = 20
    for index, vector in enumerate(vectors):
        text = f"({vector_name[index]}: {vector[0]}, {-vector[1]})"
        font = pygame.font.SysFont("Courier New", 15)
        text_surface = font.render(text, True, (140, 140, 250))
        screen.blit(text_surface, (x + 10, y + 10 + y_offset))
        y_offset += 25


class Text:
    def __init__(self, text):
        self.text = text
        self.font = pygame.font.SysFont("Courier New", 20)
        self.base_color = (255, 255, 255)
        self.glow_color = (90, 90, 240)
        self.text_surface = self.font.render(self.text, True, self.base_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (center_x, center_y + center_y*-0.1)

    def render(self):
        glow_offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]

        for offset in glow_offsets:
            glow_surface = self.font.render(self.text, True, self.glow_color)
            glow_rect = glow_surface.get_rect(center=(self.text_rect.centerx + offset[0],
                                                      self.text_rect.centery + offset[1]))
            screen.blit(glow_surface, glow_rect)

        screen.blit(self.text_surface, self.text_rect)

    def delete(self):
        self.text = ""  # Set the text to an empty string
        self.update_surface()

    def update_surface(self):
        self.text_surface = self.font.render(self.text, True, self.base_color)

class MenuBar:
    def __init__(self):
        self.menu_height = 30
        self.menu_items = ["File...", "Operations..."]
        self.item_width = screen_x // len(self.menu_items)
        self.show_dropdown = False

    def draw(self):
        menu_rect = pygame.Rect(0, 0, screen_x, self.menu_height)
        pygame.draw.rect(screen, (40, 40, 40), menu_rect)

        font = pygame.font.SysFont("Courier New", 20)

        for i, item in enumerate(self.menu_items):
            item_rect = pygame.Rect(i * self.item_width, 0, self.item_width, self.menu_height)
            text_surface = font.render(item, True, (255, 255, 255))
            screen.blit(text_surface, (item_rect.x + 10, item_rect.y + 5))

            if item_rect.collidepoint(pygame.mouse.get_pos()):
                highlight = (190, 190, 190)
                selected_text = font.render(item, True, highlight)
                screen.blit(selected_text, (item_rect.x + 10, item_rect.y + 5))

        if self.show_dropdown:
            dropdown_rect = pygame.Rect(0, self.menu_height, self.item_width, self.menu_height * (len(self.menu_items) + len(vectors) + 1))
            pygame.draw.rect(screen, (40, 40, 40), dropdown_rect)

            dropdown_options = ["Remove all"]
            dropdown_options.extend([f"Remove vector {vector_name[i]}" for i in range(0, len(vectors))])

            for i, option in enumerate(dropdown_options):
                option_rect = pygame.Rect(0, (i + 1) * self.menu_height, self.item_width, self.menu_height)
                option_surface = font.render(option, True, (255, 255, 255))
                screen.blit(option_surface, (option_rect.x + 10, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                # Check if the click occurred within the menu bar area
                if pos[0] < screen_x // 3 and pos[1] < self.menu_height:
                    self.show_dropdown = not self.show_dropdown
                    # Prevent drawing vectors when clicking on the menu bar TODO: fix dropdown
                    return
                elif self.show_dropdown and pos[0] < screen_x // 3 and self.menu_height <= pos[1] < (len(self.menu_items) + len(vectors) + 1) * self.menu_height:
                    selected_option = (pos[1] - self.menu_height) // self.menu_height
                    if selected_option == 0:
                        erase_all_vectors()
                    elif 1 <= selected_option <= len(vectors):
                        delete_vector(selected_option)

def erase_all_vectors():
    vectors.clear()

def delete_vector(selected_option):
    del vectors[selected_option-1]
    del vector_name[selected_option-1]

def linear_combination():
    result_vector = [0, 0]
    for vector in vectors:
        result_vector[0] += vector[0]
        result_vector[1] += vector[1]
    return result_vector

def draw_linear_combination(result_vector):
    x, y = center_x + result_vector[0], center_y + result_vector[1]
    text = f"Linear Combination of {', '.join(vector_name)}: ({result_vector[0]}, {-result_vector[1]})"
    font = pygame.font.SysFont("Courier New", 14)
    text_surface = font.render(text, True, (40, 255, 80))
    text_rect = text_surface.get_rect(midbottom=(center_x, screen_y - 20))
    screen.blit(text_surface, text_rect)
    pygame.draw.line(screen, (40, 255, 80), (center_x, center_y), (x, y), 2)

def main():
    is_drawing = False
    menu_bar = MenuBar()

    while True:
        draw_ax()
        menu_bar.draw()

        if len(vectors) > 1:
                # Draw the linear combination box
                result_vector = linear_combination()
                draw_linear_combination(result_vector)

        elif len(vectors) == 0:
            text_object = Text("Use your mouse to draw a vector!")
            
        elif len(vectors) > 0:
            text_object.delete()
            if text_object != None: # make sure its None lol
                text_object == None

        if text_object:
            text_object.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu_bar.handle_event(event)
                pos1 = pygame.mouse.get_pos()
                if pos1[0] >= screen_x // 3 or pos1[1] >= menu_bar.menu_height + len(menu_bar.menu_items) * menu_bar.menu_height:
                    is_drawing = True

            elif event.type == pygame.MOUSEBUTTONUP:
                menu_bar.handle_event(event)
                pos2 = pygame.mouse.get_pos()
                if is_drawing:
                    add_vector(pos1, pos2)
                    is_drawing = False

        # Continuously draw the line from the origin to the current mouse position
        if is_drawing:
            menu_bar.handle_event(event)
            current_mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), current_mouse_pos, 1)

            # Store preview coordinates
            preview_coords = (current_mouse_pos[0] - center_x, center_y - current_mouse_pos[1])
            vector_lenth = np.sqrt(preview_coords[0]**2 + preview_coords[1]**2)

            # Display the current coordinates relative to the origin
            x, y = preview_coords
            text = f"({x}, {y} len={int(vector_lenth)})"
            font = pygame.font.SysFont("Courier New", 14)
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (current_mouse_pos[0] + 5, current_mouse_pos[1] - 15))

        draw_vectors()
        draw_v_list()

        pygame.display.update()

if __name__ == "__main__":
    main()