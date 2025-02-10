import pygame
import numpy as np
from OpenGL.GL import *
from utils.shader_loader import create_shader_program


class FractalRenderer:
    def __init__(self):
        self.width, self.height = 800, 600
        self.shader_program = None
        self.vao = None
        self.offset = np.array([0.0, 0.0], dtype=np.float32)
        self.zoom = 1.0

    def init_gl(self):
        """Initialize OpenGL context and shaders"""
        glClearColor(0, 0, 0, 1)

        # Load and compile shaders
        self.shader_program = create_shader_program(
            "shaders/vertex_shader.glsl",
            "shaders/mandelbrot_shader.glsl"
        )
        glUseProgram(self.shader_program)

        # Set up full-screen quad
        vertices = np.array([
            -1, -1, 0,  1, -1, 0,  -1, 1, 0,
            -1, 1, 0,   1, -1, 0,   1, 1, 0
        ], dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        loc = glGetAttribLocation(self.shader_program, "aPos")
        if loc == -1:
            raise RuntimeError("Error: Attribute 'aPos' not found in shader!")

        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 0, None)

    def render(self):
        """Render the fractal using shaders"""
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.shader_program)
        glUniform2f(glGetUniformLocation(self.shader_program, "resolution"), self.width, self.height)
        glUniform2f(glGetUniformLocation(self.shader_program, "offset"), *self.offset)
        glUniform1f(glGetUniformLocation(self.shader_program, "zoom"), self.zoom)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        pygame.display.flip()

    def handle_input(self, event):
        """Handle zoom and movement"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.offset[1] += 0.1 / self.zoom
            elif event.key == pygame.K_DOWN:
                self.offset[1] -= 0.1 / self.zoom
            elif event.key == pygame.K_LEFT:
                self.offset[0] -= 0.1 / self.zoom
            elif event.key == pygame.K_RIGHT:
                self.offset[0] += 0.1 / self.zoom
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.zoom *= 1.1
            elif event.key == pygame.K_MINUS:
                self.zoom /= 1.1
