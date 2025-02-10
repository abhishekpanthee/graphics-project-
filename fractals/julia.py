import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 pos;
out vec2 uv;
void main() {
    uv = pos * 0.5 + 0.5;
    gl_Position = vec4(pos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 uv;
out vec4 fragColor;

uniform float zoom;
uniform vec2 offset;
uniform int maxIter;
uniform vec2 c;

void main() {
    vec2 z = (uv - vec2(0.5, 0.5)) * zoom + offset;
    int i;
    for (i = 0; i < maxIter; i++) {
        if (dot(z, z) > 4.0) break;
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
    }
    float t = float(i) / float(maxIter);
    fragColor = vec4(t, t * 0.5, 1.0 - t, 1.0);
}
"""

class Julia:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        glViewport(0, 0, self.width, self.height)

        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
        )
        glUseProgram(self.shader)

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

        self.zoom = 3.0
        self.offset = [-0.5, 0.0]
        self.max_iter = 256
        self.c = [-0.7, 0.27015]

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.shader)
        glUniform1f(glGetUniformLocation(self.shader, "zoom"), self.zoom)
        glUniform2f(glGetUniformLocation(self.shader, "offset"), *self.offset)
        glUniform1i(glGetUniformLocation(self.shader, "maxIter"), self.max_iter)
        glUniform2f(glGetUniformLocation(self.shader, "c"), *self.c)

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
                        self.offset[1] += 0.1 * self.zoom
                    elif event.key == pygame.K_DOWN:
                        self.offset[1] -= 0.1 * self.zoom
                    elif event.key == pygame.K_LEFT:
                        self.offset[0] -= 0.1 * self.zoom
                    elif event.key == pygame.K_RIGHT:
                        self.offset[0] += 0.1 * self.zoom
                    elif event.key == pygame.K_w:
                        self.max_iter += 10
                    elif event.key == pygame.K_s:
                        self.max_iter -= 10
                    elif event.key == pygame.K_a:
                        self.c[0] -= 0.01
                    elif event.key == pygame.K_d:
                        self.c[0] += 0.01
                    elif event.key == pygame.K_q:
                        self.c[1] -= 0.01
                    elif event.key == pygame.K_e:
                        self.c[1] += 0.01
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.zoom *= 0.9
                    elif event.button == 5:  # Scroll down
                        self.zoom *= 1.1
            self.render()
        pygame.quit()

if __name__ == "__main__":
    Julia().run()
