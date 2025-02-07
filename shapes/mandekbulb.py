import numpy as np
import vispy.scene
from vispy.scene import visuals
from config import MANDELBULB_RES, LIGHT_ROTATION_SPEED

class Mandelbulb:
    def __init__(self):
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.bgcolor = 'black'
        self.view.camera = 'arcball'
        self.mesh = self.create_mandelbulb()
        self.view.add(self.mesh)

    def mandelbulb_formula(self, x, y, z, power=8):
        z_complex = complex(x, y)
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r)
        phi = np.arctan2(y, x)
        r_power = r ** power
        new_x = r_power * np.sin(theta * power) * np.cos(phi * power)
        new_y = r_power * np.sin(theta * power) * np.sin(phi * power)
        new_z = r_power * np.cos(theta * power)
        return new_x, new_y, new_z

    def create_mandelbulb(self):
        points = []
        for i in range(MANDELBULB_RES):
            for j in range(MANDELBULB_RES):
                x, y, z = np.random.uniform(-1, 1, 3)
                new_x, new_y, new_z = self.mandelbulb_formula(x, y, z)
                points.append([new_x, new_y, new_z])

        points = np.array(points)
        mesh = visuals.Markers()
        mesh.set_data(points, edge_color=None, face_color=(1, 1, 1, 0.8), size=2)
        return mesh

    def run(self):
        vispy.app.run()
