import pygame
import vispy.scene
from vispy.scene import visuals

class Sierpinski:
    def __init__(self, screen):
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.bgcolor = 'black'
        self.view.camera = 'arcball'
        self.create_sierpinski()

    def create_sierpinski(self):
        vertices = [[0, 0, 1], [1, 0, 0], [-1, 0, 0], [0, 1, 0]]
        faces = [[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 2, 3]]
        mesh = visuals.Mesh(vertices=vertices, faces=faces, color='blue', shading='smooth')
        self.view.add(mesh)

    def run(self):
        vispy.app.run()
