from OpenGL.GL import glEnable, GL_DEPTH_TEST, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, gluNewQuadric
from OpenGL.GL import glGenFramebuffers, glBindFramebuffer, glGenTextures, glBindTexture, GL_FRAMEBUFFER
from OpenGL.GL import glTexImage2D, GL_TEXTURE_2D, glTexParameteri, GL_NEAREST, GL_CLAMP_TO_BORDER, GL_DEPTH_COMPONENT
from OpenGL.GLU import gluLookAt
from OpenGL.GL import *
import numpy as np
import pygame
from pygame.locals import *

# Shadow map resolution
SHADOW_WIDTH = 1024
SHADOW_HEIGHT = 1024

# Light properties
light_pos = [2.0, 4.0, -2.0]

# Initialize OpenGL for shadow mapping using FBO
def init_opengl_for_shadows():
    glEnable(GL_DEPTH_TEST)

    # Create and configure a depth texture
    depth_map = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0,
                 GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    border_color = [1.0, 1.0, 1.0, 1.0]
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)

    # Create a framebuffer for rendering the depth map
    depth_fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, depth_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)
    glDrawBuffer(GL_NONE)  # No color buffer is drawn to
    glReadBuffer(GL_NONE)

    # Ensure framebuffer is complete
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        raise Exception("Framebuffer not complete")

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    return depth_map, depth_fbo

# Function to render the scene from the light's point of view
def render_scene_from_light(light_pos, sphere_radius, slices, stacks, rotation_angle):
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(light_pos[0], light_pos[1], light_pos[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    create_sphere(sphere_radius, slices, stacks, rotation_angle)

# Function to render the scene from the camera's point of view
def render_scene_from_camera(sphere_radius, slices, stacks, rotation_angle, depth_map):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear both color and depth buffers
    glEnable(GL_DEPTH_TEST)

    # Enable shadow comparison
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, depth_map)

    # Set up the camera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 1.5, -5, 0, 0, 0, 0, 1, 0)

    create_sphere(sphere_radius, slices, stacks, rotation_angle)

    glDisable(GL_TEXTURE_2D)

# Function to create a 3D sphere
def create_sphere(radius, slices, stacks, rotation_angle):
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glRotatef(rotation_angle, 0, 1, 0)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)
    glPopMatrix()
    for i in range(slices):
        lat0 = np.pi * (-0.5 + float(i) / slices)
        z0 = radius * np.sin(lat0)
        zr0 = radius * np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(i + 1) / slices)
        z1 = radius * np.sin(lat1)
        zr1 = radius * np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(stacks + 1):
            lng = 2 * np.pi * float(j) / stacks
            x = np.cos(lng)
            y = np.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()
    glPopMatrix()

def check_opengl_state():
    status = glGetError()
    if status != GL_NO_ERROR:
        print(f"OpenGL Error: {status}")

# Call this function after key OpenGL calls to check for errors


# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('FBO Shadow Mapping')

    sphere_radius = 1
    slices = 20
    stacks = 20

    depth_map, depth_fbo = init_opengl_for_shadows()

    rotation_angle = 0
    clock = pygame.time.Clock()
    light_pos = [2.0, 4.0, -2.0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        rotation_angle += 1

        # First pass: render the scene from the light's perspective
        glBindFramebuffer(GL_FRAMEBUFFER, depth_fbo)
        glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        glClear(GL_DEPTH_BUFFER_BIT)
        render_scene_from_light(light_pos, sphere_radius, slices, stacks, rotation_angle)

        # Second pass: render the scene from the camera's perspective
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, 800, 600)
        render_scene_from_camera(sphere_radius, slices, stacks, rotation_angle, depth_map)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
