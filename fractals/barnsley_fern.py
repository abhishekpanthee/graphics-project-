import pygame
import random
from OpenGL.GL import *

class BarnsleyFern:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Initial viewport settings
        self.zoom = 1.0
        self.offset_x, self.offset_y = 0.0, 0.0
        self.max_iterations = 50000

        # 🌟 Modified for incremental generation
        self.points = []
        self.iter_count = 0
        self.x, self.y = 0.0, 0.0  # Start point
        self.points_per_frame = 500  # 🔥 Generate 500 points per frame

    def generate_points(self):
        """Incrementally generate 500 Barnsley Fern points per frame."""
        for _ in range(self.points_per_frame):
            if self.iter_count >= self.max_iterations:
                return  # Stop when max iterations are reached

            r = random.random()
            if r < 0.01:
                xn, yn = 0.0, 0.16 * self.y
            elif r < 0.86:
                xn, yn = 0.85 * self.x + 0.04 * self.y, -0.04 * self.x + 0.85 * self.y + 1.6
            elif r < 0.93:
                xn, yn = 0.2 * self.x - 0.26 * self.y, 0.23 * self.x + 0.22 * self.y + 1.6
            else:
                xn, yn = -0.15 * self.x + 0.28 * self.y, 0.26 * self.x + 0.24 * self.y + 0.44

            self.points.append((xn, yn))
            self.x, self.y = xn, yn
            self.iter_count += 1  # Keep track of generated points

    def render(self):
        """Render the Barnsley Fern."""
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Apply zoom and movement transformation
        glScalef(self.zoom, self.zoom, 1.0)
        glTranslatef(self.offset_x, self.offset_y, 0)

        glBegin(GL_POINTS)
        glColor3f(0.0, 1.0, 0.0)  # Green color

        for x, y in self.points:
            glVertex2f((x - 2.5) / 2.5, y / 5.0)  # Normalized coordinates

        glEnd()
        pygame.display.flip()

    def run(self):
        """Main loop to handle input and rendering."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.offset_y -= 0.1 / self.zoom
                    elif event.key == pygame.K_DOWN:
                        self.offset_y += 0.1 / self.zoom
                    elif event.key == pygame.K_LEFT:
                        self.offset_x += 0.1 / self.zoom
                    elif event.key == pygame.K_RIGHT:
                        self.offset_x -= 0.1 / self.zoom
                    elif event.key == pygame.K_w:
                        self.max_iterations += 5000
                    elif event.key == pygame.K_s:
                        self.max_iterations = max(10000, self.max_iterations - 5000)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up (Zoom in)
                        self.zoom *= 1.1
                    elif event.button == 5:  # Scroll down (Zoom out)
                        self.zoom *= 0.9

            self.generate_points()  # 🔥 Now generates 500 points per frame
            self.render()

        pygame.quit()

if __name__ == "__main__":
    BarnsleyFern().run()
