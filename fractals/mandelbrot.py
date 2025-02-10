

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Vertex Shader (Basic Full-Screen Quad)
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 pos;
out vec2 uv;
void main() {
    uv = pos * 0.5 + 0.5;  // Convert [-1,1] to [0,1]
    gl_Position = vec4(pos, 0.0, 1.0);
}
"""

# Fragment Shader (Mandelbrot Calculation)
FRAGMENT_SHADER = """
#version 330 core
in vec2 uv;
out vec4 fragColor;

uniform float zoom;
uniform vec2 offset;
uniform int maxIter;

void main() {
    vec2 c = (uv - vec2(0.5, 0.5)) * zoom + offset;
    vec2 z = vec2(0.0, 0.0);
    int i;
    for (i = 0; i < maxIter; i++) {
        if (dot(z, z) > 4.0) break;
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
    }
    
    float color = float(i) / float(maxIter);
    fragColor = vec4(color, color * 0.5, color * 0.2, 1.0);
}
"""

class Mandelbrot:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        glViewport(0, 0, self.width, self.height)

        # Compile shaders
        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
        )
        glUseProgram(self.shader)

        # Set up a full-screen quad
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        vertices = np.array([
            -1, -1,   1, -1,   -1,  1,
            -1,  1,   1, -1,    1,  1
        ], dtype=np.float32)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Mandelbrot Parameters
        self.zoom = 3.0
        self.offset = [-0.5, 0.0]
        self.max_iter = 256

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # Update uniforms
        glUseProgram(self.shader)
        glUniform1f(glGetUniformLocation(self.shader, "zoom"), self.zoom)
        glUniform2f(glGetUniformLocation(self.shader, "offset"), *self.offset)
        glUniform1i(glGetUniformLocation(self.shader, "maxIter"), self.max_iter)

        # Draw quad
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.offset[1] -= 0.1 * self.zoom
                    elif event.key == pygame.K_DOWN:
                        self.offset[1] += 0.1 * self.zoom
                    elif event.key == pygame.K_LEFT:
                        self.offset[0] -= 0.1 * self.zoom
                    elif event.key == pygame.K_RIGHT:
                        self.offset[0] += 0.1 * self.zoom
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.zoom *= 0.8
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                        self.zoom /= 0.8

            self.render()

        pygame.quit()

