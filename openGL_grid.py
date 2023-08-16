import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def draw_text(position, text):
    glPushMatrix()
    glTranslatef(*position)
    glRasterPos3f(0, 0, 0)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    glPopMatrix()

pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


gluPerspective(50, (display[0] / display[1]), 0.1, 50.0) # Field of View, Aspect Ratio, zNear & zFar (both clipping distace)
glTranslatef(0.0, 0.0, -5) # Move grid on negative z axis

grid_position_z = 0.0
grid_speed = 0.001

rotation_angle = 0.0
rotation_speed = 1.0

dragging = False # Used for detecting mouse click (click and hold to change grid_speed variable)
drag_start_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            drag_start_y = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        rotation_angle += rotation_speed  # Counter-clockwise rotation
    if keys[pygame.K_e]:
        rotation_angle -= rotation_speed  # Clockwise rotation
    
    if dragging:
        mouse_y = pygame.mouse.get_pos()[1]
        scroll = drag_start_y - mouse_y
        grid_speed += scroll * 0.00001  # Mouse movement sensitivity setting

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear buffers at beginning of each frame
    glPushMatrix()
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    glTranslatef(0, 0, grid_speed)
    grid_position_z += grid_speed

    # Define wireframe grid
    glBegin(GL_LINES)
    glColor3f(0.0, 0.5, 0.5)
    spacing = 0.5
    
    # Creates lines along the x and y axis (size 4 will create an 8x8 grid)
    size = 4
    
    for i in range(-size, size + 1):
        glVertex3f(i * spacing, size * spacing, grid_position_z)
        glVertex3f(i * spacing, -size * spacing, grid_position_z)
        glVertex3f(size * spacing, i * spacing, grid_position_z)
        glVertex3f(-size * spacing, i * spacing, grid_position_z)

    glEnd()

    glPopMatrix() # Pop (glPushMatrix) before rotating (otherwise crashes with error 1283, b'stack overflow' (?))

    # Render text (zoom level and rotation)
    text_position = (-4.5, -4.5, -5)
    zoom_text = f"Zoom Level: {grid_position_z:.2f} | Rotation Level: {rotation_angle:.2f} | Rotation Speed: {rotation_speed:.2f}"
    glColor3f(1.0, 1.0, 1.0)
    draw_text(text_position, zoom_text)

    pygame.display.flip()
    pygame.time.wait(10)
