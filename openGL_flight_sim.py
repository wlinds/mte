import math, time, random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sounddevice as sd
import numpy as np


# Player placeholder TODO: Import obj model
class Player:
    def __init__(self):
        self.position = [0.0, 2.0, 0.0]
        self.radius = 0.1
        self.player_color = np.array([0.4, 0.3, 0.6])

    def adjust_color(self, new_color):
        self.player_color = np.clip(new_color, 0.0, 1.0)

    def draw(self):
        x, y, z = self.position
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3fv(self.player_color)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radius, 20, 20)
        gluDeleteQuadric(quadric)
        glPopMatrix()

screen_res = (800, 600)

normal_movement_mode = True # Turning this off is quite interesting

# Turning rotation off (False) makes controling the player easier but less fun
# I guess it should be fine-tuned

allow_player_rotation = True    # Rotation is weird af but kinda funny
limit_player_rotation = False   # Currently only affects left/right
max_rotation_angle = 25.0
max_rotation_speed = 2.0

now_playing = "None" # Unused, TODO: display song on screen

class Main:
    def __init__(self):
        self.screen_resolution = screen_res
        self.grid_spacing = 1.0
        self.grid_size = 128
        self.grid_position_x = 0.0
        self.grid_position_y = 0.0
        self.grid_position_z = 0.0

        self.rotation_angle_x = 0.0
        self.rotation_angle_y = 0.0

        self.max_rotation_angle = max_rotation_angle
        self.rotation_speed = max_rotation_speed
        self.reset_rotation = False

        self.player = Player()

    def draw_grid(self):
        glBegin(GL_LINES)
        glColor3f(0.0, 0.5, 0.5)
        spacing = self.grid_spacing
        size = self.grid_size

        for i in range(-size, size + 1):
            # Vertical lines
            glVertex3f(i * spacing + self.grid_position_x, size * spacing + self.grid_position_y, self.grid_position_z)
            glVertex3f(i * spacing + self.grid_position_x, -size * spacing + self.grid_position_y, self.grid_position_z)
            
            # Horizontal lines
            glVertex3f(size * spacing + self.grid_position_x, i * spacing + self.grid_position_y, self.grid_position_z)
            glVertex3f(-size * spacing + self.grid_position_x, i * spacing + self.grid_position_y, self.grid_position_z)
        glEnd()

    def follow_text(self, position, text, color=(1.0, 1.0, 1.0)):
        glPushMatrix()
        glTranslatef(*position)
        glRotatef(self.rotation_angle_x, 1, 0, 0)
        glRotatef(self.rotation_angle_y, 0, 1, 0)
        glColor3f(*color)
        glRasterPos3f(0, 0, 0)
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
        glPopMatrix()

    def run(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.screen_resolution[0] / self.screen_resolution[1]), 0.1, 200.0)
        glTranslatef(0, 0, -5)
        
        glRotatef(-66, 1.0, 0.0, 0.0)  # Initial fixed perspective (grid rotation)
        
        clock = pygame.time.Clock()
        start_time = time.time()

        # Music loop -- check out https://soundcloud.com/lindstedt for more music ;)
        bg_music = pygame.mixer.Sound("assets/audio/music/bitsocker_Vår_Hjälte_-Lindstedt_Music.wav")
        self.channel0 = pygame.mixer.Channel(0)
        self.channel0.play(bg_music, loops=-1)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Movement keybinds TODO: Ease out/ease in animation instead of instant rotation snap back
            keys = pygame.key.get_pressed()
            if keys[K_s]:
                self.grid_position_z += 0.08
                if allow_player_rotation:
                    self.rotation_angle_y += self.rotation_speed
            if keys[K_w]:
                self.grid_position_z -= 0.08
                if allow_player_rotation:
                    self.rotation_angle_y -= self.rotation_speed
            if keys[K_a]:
                self.grid_position_x += 0.08
                if allow_player_rotation:
                    self.rotation_angle_x += self.rotation_speed
                    self.reset_rotation = False
            if keys[K_d]:
                self.grid_position_x -= 0.08
                if allow_player_rotation:
                    self.rotation_angle_x -= self.rotation_speed
                    self.reset_rotation = False
            if not (keys[K_a] or keys[K_d]) and allow_player_rotation:
                self.reset_rotation = True


            # Testing color adjustment
            if keys[K_1]:
                self.player.adjust_color(np.array([0.8, 0.2, 0.4]))
            if keys[K_2]:
                self.player.adjust_color(np.array([0.4, 0.3, 0.6]))

            # Player rotation limit
            if self.rotation_angle_x > self.max_rotation_angle and limit_player_rotation:
                self.rotation_angle_x = self.max_rotation_angle
            elif self.rotation_angle_x < -self.max_rotation_angle and limit_player_rotation:
                self.rotation_angle_x = -self.max_rotation_angle

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()

            glRotatef(self.rotation_angle_x, 0.0, 1.0, 0.0) # TODO: Should probably swap x & y for better readability??
            glRotatef(self.rotation_angle_y, 1.0, 0.0, 0.0)

            if self.reset_rotation:
                self.rotation_angle_x = 0.0

            # Constant grid movement
            if normal_movement_mode:
                self.grid_position_y -= 0.05  # -y to move the grid forward
                #self.grid_position_z += 0.01  # +z to move the grid downward

            # Experimental weird movement
            else:
                forward_vector = [
                    -math.sin(math.radians(self.rotation_angle_y)),
                    0,
                    -math.cos(math.radians(self.rotation_angle_y)),
                ]

                # Update grid position based on forward vector
                movement_speed = 0.05
                self.grid_position_y += forward_vector[0] * movement_speed
                self.grid_position_x += forward_vector[1] * movement_speed
                self.grid_position_z += forward_vector[2] * movement_speed

            # Draw grid
            self.draw_grid()

            self.player.draw()

            #glTranslatef(self.player_position[0], self.player_position[1], self.player_position[2])

            # Intro text
            #self.fade_text.display(self.screen_resolution) #TODO Try to implement this again

            # Player position text
            self.follow_text(
                self.player.position,
                f"Rot: ({self.rotation_angle_x:.2f}, {self.rotation_angle_y:.2f})",
            )

            glPopMatrix()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Main()
    game.run()
