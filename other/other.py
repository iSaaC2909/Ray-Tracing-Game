import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.GL.framebufferobjects import glGenFramebuffers, glBindFramebuffer, glFramebufferTexture2D
from OpenGL.GL import glGenTextures, glBindTexture, glTexImage2D, glTexParameteri, GL_NEAREST, GL_DEPTH_COMPONENT
from OpenGL.GL import glTexParameterfv, GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, GL_CLAMP_TO_BORDER

# Shadow map resolution
SHADOW_WIDTH = 1024
SHADOW_HEIGHT = 1024

# Light properties
light_pos = [2.0, 4.0, -2.0]

# Initialize OpenGL settings
def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Clear color is black
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Create and draw a sphere
def create_sphere(radius, slices, stacks):
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glPushMatrix()
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)
    glPopMatrix()

# Function to check for OpenGL errors
def check_opengl_error():
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL Error: {gluErrorString(error).decode('utf-8')}")

# Initialize shadow mapping
def init_shadow_mapping():
    # Create and configure depth texture
    depth_map = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    border_color = [1.0, 1.0, 1.0, 1.0]
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)

    # Create framebuffer and attach depth texture
    depth_fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, depth_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    return depth_map, depth_fbo

# Render the scene from the light's perspective
def render_from_light(light_pos, sphere_radius, slices, stacks, depth_fbo):
    glBindFramebuffer(GL_FRAMEBUFFER, depth_fbo)
    glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1.0, 1.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(light_pos[0], light_pos[1], light_pos[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    create_sphere(sphere_radius, slices, stacks)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

# Render the scene from the camera's perspective with shadows
def render_from_camera(light_pos, sphere_radius, slices, stacks, depth_map):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 1.5, -5, 0, 0, 0, 0, 1, 0)

    # Bind shadow map
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, depth_map)
    
    # Render scene with shadows
    create_sphere(sphere_radius, slices, stacks)

    # Clean up
    glBindTexture(GL_TEXTURE_2D, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('PyOpenGL Sphere with Shadows')

    init_opengl()
    depth_map, depth_fbo = init_shadow_mapping()

    sphere_radius = 1
    slices = 20
    stacks = 20

    rotation_angle = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Render from light's perspective to create shadow map
        render_from_light(light_pos, sphere_radius, slices, stacks, depth_fbo)

        # Render from camera's perspective with shadows
        render_from_camera(light_pos, sphere_radius, slices, stacks, depth_map)

        pygame.display.flip()
        clock.tick(60)

        # Check for OpenGL errors
        check_opengl_error()

    pygame.quit()

if __name__ == "__main__":
    main()
