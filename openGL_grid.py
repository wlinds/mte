import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Main:
    def __init__(self):
        pygame.init()
        self.display = (800, 600) # TODO: adjust text render position for different display sizes
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)

        # !! FOV also affects text position on screen.
        gluPerspective(50, (self.display[0] / self.display[1]), 0.1, 50.0) # FOV, Aspect Ratio, zNear & zFar (both clipping distace)
        glTranslatef(0.0, 0.0, -5)

        self.grid_size = 16 # Set plane size (extrudes along x and y axis) (size 16 will create a 32x32 grid)
        self.grid_spacing = 0.5
        self.grid_position_z = 0.0
        self.camera_speed_z = 0.0 # Camera z level movement speed

        self.rotation_speed = 1.0
        self.rotation_angle_x = 0.0
        self.rotation_angle_z = 0.0
        self.rotation_angle_y = 0.0

        self.dragging = False # Detecting mouse click (click and hold to change camera_speed_z) #TODO: Change keybind?
        self.drag_start_y = 0

        self.cube_loc = (0.25, 0.25, 0.25)

        # Dict mapping used only for displaying player input
        self.key_names = {
            pygame.K_q: "Q",
            pygame.K_e: "E",
            pygame.K_d: "D",
            pygame.K_a: "A",
            pygame.K_s: "S",
            pygame.K_w: "W",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
        }

    # Semi-static text (GUI)
    def draw_text(self, position, text):
        glPushMatrix()
        glTranslatef(*position)
        glRasterPos3f(0, 0, 0)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
        glPopMatrix()

    # Follow rotation and position (for cube and other objects, GUI)
    def follow_text(self, position, text, color=(1.0, 1.0, 1.0)):
        glPushMatrix()
        glTranslatef(*position)
        glRotatef(self.rotation_angle_x, 1, 0, 0)
        glRotatef(self.rotation_angle_y, 0, 1, 0)
        glRotatef(self.rotation_angle_z, 0, 0, 1)
        glColor3f(*color)
        glRasterPos3f(0, 0, 0)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
        glPopMatrix()

    def draw_stupid_cube(self, position, size):
        # Stupid cube vertices
        u = size * 0.5
        vertices = [
            [u, u, u], [-u, u, u], [-u, -u, u], [u, -u, u],
            [u, u, -u], [-u, u, -u], [-u, -u, -u], [u, -u, -u]
        ]
        # Stupid cube corner connections
        faces = [
            [0, 1, 2, 3], [3, 2, 6, 7], [7, 6, 5, 4],
            [4, 5, 1, 0], [0, 3, 7, 4], [1, 5, 6, 2]
        ]
        glBegin(GL_QUADS)
        for stupid_face in faces:
            for vertex_index in stupid_face:
                vertex = vertices[vertex_index]
                glVertex3fv([vertex[0] + position[0], vertex[1] + position[1], vertex[2] + position[2]])
        glEnd()

    def move_on_grid(self, direction):
        step = self.grid_spacing
        if direction == "left":
            self.cube_loc = (self.cube_loc[0] - step, self.cube_loc[1], self.cube_loc[2])
        elif direction == "right":
            self.cube_loc = (self.cube_loc[0] + step, self.cube_loc[1], self.cube_loc[2])
        elif direction == "up":
            self.cube_loc = (self.cube_loc[0], self.cube_loc[1] + step, self.cube_loc[2])
        elif direction == "down":
            self.cube_loc = (self.cube_loc[0], self.cube_loc[1] - step, self.cube_loc[2])

    def display_rotation_combination(self):
        #TODO: Simplified as rotation matrix, maybe?
        coefficients = {
            "x": self.rotation_angle_x,
            "y": self.rotation_angle_y,
            "z": self.rotation_angle_z,
        }

        rotations = {symbol: angle % 360 for symbol, angle in coefficients.items()}
        non_zero = {symbol: angle for symbol, angle in rotations.items() if angle != 0}

        if non_zero:
            rotation_combination = " + ".join([f"({symbol}: {angle:.2f}°)" for symbol, angle in non_zero.items()])
        else:
            rotation_combination = "No Rotation"

        return rotation_combination

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.dragging = True
                    self.drag_start_y = event.pos[1]
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False

            # Display all keys currently pressed
            keys = pygame.key.get_pressed()
            pressed_keys_text = "+".join([self.key_names[key] for key in self.key_names if keys[key]])

            self.rotation_speed = 1.0
            self.rotation_angle_x += self.rotation_speed * (keys[pygame.K_q] - keys[pygame.K_e])
            self.rotation_angle_z += self.rotation_speed * (keys[pygame.K_d] - keys[pygame.K_a])
            self.rotation_angle_y += self.rotation_speed * (keys[pygame.K_s] - keys[pygame.K_w])

            if keys[pygame.K_LEFT]:
                self.move_on_grid("left")
            if keys[pygame.K_RIGHT]:
                self.move_on_grid("right")
            if keys[pygame.K_UP]:
                self.move_on_grid("up")
            if keys[pygame.K_DOWN]:
                self.move_on_grid("down")

            if self.dragging:
                mouse_y = pygame.mouse.get_pos()[1]
                scroll = self.drag_start_y - mouse_y
                self.camera_speed_z += scroll * 0.00001

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPushMatrix()
            glRotatef(self.rotation_angle_x, 0.0, 0.0, 1.0)
            glRotatef(self.rotation_angle_z, 0.0, 1.0, 0.0)
            glRotatef(self.rotation_angle_y, 1.0, 0.0, 0.0)
            glTranslatef(0, 0, self.camera_speed_z)
            self.grid_position_z += self.camera_speed_z

            # Define wireframe grid
            glBegin(GL_LINES)
            glColor3f(0.0, 0.5, 0.5)
            spacing = self.grid_spacing
            size = self.grid_size
            for i in range(-size, size + 1):
                glVertex3f(i * spacing, size * spacing, self.grid_position_z)
                glVertex3f(i * spacing, -size * spacing, self.grid_position_z)
                glVertex3f(size * spacing, i * spacing, self.grid_position_z)
                glVertex3f(-size * spacing, i * spacing, self.grid_position_z)
            glEnd()

            # Draw the line from origin to cube
            distance_to_cube = ((self.cube_loc[0] ** 2) + (self.cube_loc[1] ** 2) + (self.cube_loc[2] ** 2)) ** 0.5
            distance_text = f"Distance: {distance_to_cube:.2f}"
            self.draw_text((self.cube_loc[0] * 0.5, self.cube_loc[1] * 0.5, self.cube_loc[2] * 0.5), distance_text)

            cube_size = self.grid_spacing
            self.draw_stupid_cube(self.cube_loc, cube_size)

            self.follow_text((self.cube_loc[0] - 0.3, self.cube_loc[1], self.cube_loc[2]), "Stupid cube #1")

            glPopMatrix() # Pop (glPushMatrix) before rotating (otherwise crashes with error 1283, b'stack overflow' (?))


            # Render text (zoom level and rotation)
            # TODO: Text position should not be hardcoded like this to account for different screen size preferences,
            # rn it's hardcoded to a classic VGA 800x600 window. This is an UI issue and will not be prioritized.
            rotation_text = self.display_rotation_combination()
            text_position = (-6, -4.5, -5)
            bottom_text = f"Zoom Level (Mouse): {self.grid_position_z:.2f} | Rotation (WASD+QE): {rotation_text}"
            glColor3f(1.0, 1.0, 1.0)
            self.draw_text(text_position, bottom_text)

            self.draw_text((-2, 1.5, 1.5), pressed_keys_text)

            pygame.display.flip()
            pygame.time.wait(10)

if __name__ == "__main__":
    app = Main()
    app.run()
