import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# !! FOV also affects text position on screen.
gluPerspective(50, (display[0] / display[1]), 0.1, 50.0) # Field of View, Aspect Ratio, zNear & zFar (both clipping distace)
glTranslatef(0.0, 0.0, -5) # Move grid on negative z axis

grid_spacing = 0.5
grid_position_z = 0.0
grid_speed = 0.0

base_rotation_speed = 1.0
slow_rotation_factor = 0.5 # Currently not implemented, but could be used to lower rotation speed

rotation_angle_x = 0.0
rotation_speed = 1.0

rotation_angle_z = 0.0
rotation_speed_z = 1.0

rotation_angle_y = 0.0
rotation_speed_y = 1.0

dragging = False # Used for detecting mouse click (click and hold to change grid_speed variable) #TODO: Change keybind?
drag_start_y = 0

# Draw semi-static text
def draw_text(position, text):
    glPushMatrix()
    glTranslatef(*position)
    glRasterPos3f(0, 0, 0)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    glPopMatrix()

# Follow rotation (for cube and other objects)
def follow_text(position, text, color=(1.0, 1.0, 1.0)):
    glPushMatrix()
    glTranslatef(*position)
    glRotatef(rotation_angle_x, 1, 0, 0)
    glRotatef(rotation_angle_y, 0, 1, 0)
    glRotatef(rotation_angle_z, 0, 0, 1)
    glColor3f(*color)  # Set text color
    glRasterPos3f(0, 0, 0)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    glPopMatrix()


def draw_stupid_cube(position, size):

    # Stupid cube vertices
    u = size * 0.5
    vertices = [
        [ u,  u,  u],
        [-u,  u,  u],
        [-u, -u,  u],
        [ u, -u,  u],
        [ u,  u, -u],
        [-u,  u, -u],
        [-u, -u, -u],
        [ u, -u, -u]
    ]
    
    # Stupid cube corner connections
    faces = [
        [0, 1, 2, 3],
        [3, 2, 6, 7],
        [7, 6, 5, 4],
        [4, 5, 1, 0],
        [0, 3, 7, 4],
        [1, 5, 6, 2]
    ]

    glBegin(GL_QUADS)
    for stupid_face in faces:
        for vertex_index in stupid_face:
            vertex = vertices[vertex_index]
            glVertex3fv([vertex[0] + position[0], vertex[1] + position[1], vertex[2] + position[2]])
    glEnd()

def display_rotation_combination():
    #TODO: Simplified as rotation matrix, maybe?
    coefficients = {
        "x": rotation_angle_x,
        "y": rotation_angle_y,
        "z": rotation_angle_z,
    }

    rotations = {symbol: angle % 360 for symbol, angle in coefficients.items()}    
    non_zero = {symbol: angle for symbol, angle in rotations.items() if angle != 0}
    
    if non_zero:
        rotation_combination = " + ".join([f"({symbol}: {angle:.2f}°)" for symbol, angle in non_zero.items()])
    else:
        rotation_combination = "No Rotation"
    
    return rotation_combination

# Function to map key_names to pressed key (only used for UI)
def get_pressed_keys():
    pressed_keys = [key_names[key] for key in key_names if keys[key]]
    return "+".join(pressed_keys)

key_names = {
    pygame.K_q: "Q",
    pygame.K_e: "E",
    pygame.K_d: "D",
    pygame.K_a: "A",
    pygame.K_s: "S",
    pygame.K_w: "W",
}

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

    # Only used for displaying a combinations of keys currently pressed
    pressed_keys_text = get_pressed_keys()

    if keys[pygame.K_q]:
        rotation_angle_x += rotation_speed  # Counter-clockwise rotation
    if keys[pygame.K_e]:
        rotation_angle_x -= rotation_speed  # Clockwise rotation

    if keys[pygame.K_d]:
        rotation_angle_z += rotation_speed  # Counter-clockwise rotation
    if keys[pygame.K_a]:
        rotation_angle_z -= rotation_speed  # Clockwise rotation

    if keys[pygame.K_s]:
        rotation_angle_y += rotation_speed  # Counter-clockwise rotation
    if keys[pygame.K_w]:
        rotation_angle_y -= rotation_speed  # Clockwise rotation
    
    if dragging:
        mouse_y = pygame.mouse.get_pos()[1]
        scroll = drag_start_y - mouse_y
        grid_speed += scroll * 0.00001  # Mouse movement sensitivity setting


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear buffers at beginning of each frame
    glPushMatrix()
    glRotatef(rotation_angle_x, 0.0, 0.0, 1.0)
    glRotatef(rotation_angle_z, 0.0, 1.0, 0.0)
    glRotatef(rotation_angle_y, 1.0, 0.0, 0.0)
    glTranslatef(0, 0, grid_speed)
    grid_position_z += grid_speed

    # Define wireframe grid
    glBegin(GL_LINES)
    glColor3f(0.0, 0.5, 0.5)
    spacing = grid_spacing
    
    # Creates lines along the x and y axis (size 4 will create an 8x8 grid)
    size = 16
    
    for i in range(-size, size + 1):
        glVertex3f(i * spacing, size * spacing, grid_position_z)
        glVertex3f(i * spacing, -size * spacing, grid_position_z)
        glVertex3f(size * spacing, i * spacing, grid_position_z)
        glVertex3f(-size * spacing, i * spacing, grid_position_z)

    glEnd()


    cube_size = grid_spacing
    cube_loc = (0.25, 0.25, 0.25)
    draw_stupid_cube(cube_loc, cube_size)

    follow_text((cube_loc[0] - 0.3, cube_loc[1], cube_loc[2]), "Stupid cube #1")

    glPopMatrix() # Pop (glPushMatrix) before rotating (otherwise crashes with error 1283, b'stack overflow' (?))

    # Render text (zoom level and rotation)
    # TODO: Text position should not be hardcoded like this to account for different screen size preferences,
    # rn it's hardcoded to a classic VGA 800x600 window. This is an UI issue and will not be prioritized.

    rotation_text = display_rotation_combination()
    text_position = (-6, -4.5, -5)
    bottom_text = f"Zoom Level (Mouse): {grid_position_z:.2f} | Rotation (WASD+QE): {rotation_text}"
    glColor3f(1.0, 1.0, 1.0)
    draw_text(text_position, bottom_text)

    # Key currently pressed
    draw_text((-2,1.5,1.5), f"{pressed_keys_text}")

    pygame.display.flip()
    pygame.time.wait(10)
