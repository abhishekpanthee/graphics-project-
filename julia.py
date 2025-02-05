import OpenGL.GL as gl
import numpy as np
from config import WIDTH, HEIGHT

def julia(x, y, c=complex(-0.7, 0.27015), max_iter=100):
    z = complex(x, y)
    for i in range(max_iter):
        if abs(z) > 2:
            return i / max_iter
        z = z * z + c
    return 1

def draw_julia_animation(zoom_factor, offset_x, offset_y, max_iter=100):
    for x in range(-WIDTH // 2, WIDTH // 2, 2):
        for y in range(-HEIGHT // 2, HEIGHT // 2, 2):
            mx = (x / (WIDTH / 4)) * zoom_factor + offset_x
            my = (y / (HEIGHT / 4)) * zoom_factor + offset_y
            color = julia(mx, my)
            gl.glColor3f(color, 0.5, 1 - color)
            gl.glBegin(gl.GL_POINTS)
            gl.glVertex2f(x / WIDTH * 2, y / HEIGHT * 2)
            gl.glEnd()
