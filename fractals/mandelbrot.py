import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Vertex Shader (Full-Screen Quad)
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 pos;
out vec2 uv;
void main() {
    uv = pos * 0.5 + 0.5;  // Convert [-1,1] to [0,1]
    gl_Position = vec4(pos, 0.0, 1.0);
}
"""

# Fragment Shader (Mandelbrot Calculation with HSL Color Mapping)
FRAGMENT_SHADER = """
#version 330 core
in vec2 uv;
out vec4 fragColor;

uniform float zoom;
uniform vec2 offset;
uniform int maxIter;

vec3 hsl_to_rgb(float h, float s, float l) {
    float c = (1.0 - abs(2.0 * l - 1.0)) * s;
    float x = c * (1.0 - abs(mod(h * 6.0, 2.0) - 1.0));
    float m = l - c / 2.0;
    vec3 rgb;
    if (h < 1.0/6.0) rgb = vec3(c, x, 0.0);
    else if (h < 2.0/6.0) rgb = vec3(x, c, 0.0);
    else if (h < 3.0/6.0) rgb = vec3(0.0, c, x);
    else if (h < 4.0/6.0) rgb = vec3(0.0, x, c);
    else if (h < 5.0/6.0) rgb = vec3(x, 0.0, c);
    else rgb = vec3(c, 0.0, x);
    return rgb + m;
}

void main() {
    vec2 c = (uv - vec2(0.5, 0.5)) * zoom + offset;
    vec2 z = vec2(0.0, 0.0);
    int i;
    for (i = 0; i < maxIter; i++) {
        if (dot(z, z) > 4.0) break;
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
    }
    
    float t = float(i) / float(maxIter);
    vec3 color = hsl_to_rgb(t, 1.0, 0.6);
    fragColor = vec4(color, 1.0);
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
        self.target_zoom = self.zoom
        self.target_offset = self.offset[:]
        self.pan_speed = 0.1

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # Smooth zooming animation
        self.zoom += (self.target_zoom - self.zoom) * 0.1
        self.offset[0] += (self.target_offset[0] - self.offset[0]) * 0.1
        self.offset[1] += (self.target_offset[1] - self.offset[1]) * 0.1

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
                    if event.key == pygame.K_SPACE:  # Zoom in at the hover location
                        self.target_zoom *= 0.5
                    elif event.key == pygame.K_z:  # Zoom out
                        self.target_zoom /= 0.5
                    elif event.key == pygame.K_LEFT:
                        self.target_offset[0] -= self.pan_speed * self.zoom
                    elif event.key == pygame.K_RIGHT:
                        self.target_offset[0] += self.pan_speed * self.zoom
                    elif event.key == pygame.K_UP:
                        self.target_offset[1] += self.pan_speed * self.zoom
                    elif event.key == pygame.K_DOWN:
                        self.target_offset[1] -= self.pan_speed * self.zoom
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Left Click Zoom In
                    if event.button == 1:
                        x, y = event.pos
                        self.target_offset = [
                            (x / self.width - 0.5) * self.zoom + self.offset[0],
                            ((self.height - y) / self.height - 0.5) * self.zoom + self.offset[1]
                        ]
                        self.target_zoom *= 0.5

            self.render()
        
        pygame.quit()

if __name__ == "__main__":
    Mandelbrot().run()
