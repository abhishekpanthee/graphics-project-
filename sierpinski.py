import OpenGL.GL as gl
import numpy as np
from config import WIDTH, HEIGHT

def sierpinski(t, depth=5):
    # Use recursive method to generate Sierpinski triangle points
    if depth == 0:
        gl.glVertex2f(t[0], t[1])
        gl.glVertex2f(t[2], t[3])
        gl.glVertex2f(t[4], t[5])
    else:
        mid1 = [(t[0] + t[2]) / 2, (t[1] + t[3]) / 2]
        mid2 = [(t[2] + t[4]) / 2, (t[3] + t[5]) / 2]
        mid3 = [(t[4] + t[0]) / 2, (t[5] + t[1]) / 2]
        sierpinski([t[0], t[1], mid1[0], mid1[1], mid3[0], mid3[1]], depth-1)
        sierpinski([t[2], t[3], mid1[0], mid1[1], mid2[0], mid2[1]], depth-1)
        sierpinski([t[4], t[5], mid2[0], mid2[1], mid3[0], mid3[1]], depth-1)

def draw_sierpinski_animation(rotation_angle):
    t = [-0.5, -0.5, 0.5, -0.5, 0, 0.5]
    gl.glPushMatrix()
    gl.glRotatef(rotation_angle, 0, 0, 1)
    gl.glBegin(gl.GL_TRIANGLES)
    sierpinski(t)
    gl.glEnd()
    gl.glPopMatrix()
