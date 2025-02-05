import OpenGL.GL as gl
import numpy as np

rotation_angle = 0

def tesseract_animation():
    global rotation_angle
    rotation_angle += 0.01
    vertices = np.array([
        [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
        [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1],
    ])

    gl.glPushMatrix()
    gl.glRotatef(rotation_angle * 20, 1, 1, 0)  # Rotate in 3D space
    gl.glBegin(gl.GL_LINES)
    gl.glColor3f(0, 1, 1)
    for i, v in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            gl.glVertex3fv(v[:3])
            gl.glVertex3fv(vertices[j][:3])
    gl.glEnd()
    gl.glPopMatrix()
