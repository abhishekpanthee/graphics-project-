import pygame
import random
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *

class BarnsleyFern:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        self.zoom = 0.5  
        self.offset_x, self.offset_y = 1, -1  
        self.max_iterations = 50000
        
        self.points = []
        self.iter_count = 0
        self.x, self.y = 0.0, 0.0  
        self.points_per_frame = 90
        self.color_phase = 0  
        
        self.rotation_angle = 0
        self.glow_intensity = 0.5
        self.glow_direction = 1

    
        self.zoom_direction = 1  
        self.last_zoom_time = time.time()  

    def generate_points(self):
        for _ in range(self.points_per_frame):
            if self.iter_count >= self.max_iterations:
                return  

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
            self.iter_count += 1

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        if time.time() - self.last_zoom_time >= 4.5:  
            self.zoom_direction *= -1  
            self.last_zoom_time = time.time()

        self.zoom += 0.0015 * self.zoom_direction  
        self.zoom = max(0.4, min(1.0, self.zoom))  

        glScalef(self.zoom, self.zoom, 1.0)
        glTranslatef(self.offset_x, self.offset_y, 0)

        self.rotation_angle += 0.03  
        glRotatef(math.sin(self.rotation_angle) * 3, 0, 0, 1)


        self.color_phase += 0.02
        r = (math.sin(self.color_phase) + 1) / 2
        g = (math.sin(self.color_phase + 2) + 1) / 2
        b = (math.sin(self.color_phase + 4) + 1) / 2

        self.glow_intensity += 0.02 * self.glow_direction
        if self.glow_intensity >= 1 or self.glow_intensity <= 0.5:
            self.glow_direction *= -1  


        glBegin(GL_POINTS)
        for i, (x, y) in enumerate(self.points):
            alpha = max(0.3, (i / len(self.points))) * self.glow_intensity  
            glColor4f(r, g, b, alpha)
            
            x_wave = x + 0.005 * math.sin(y * 10 + self.color_phase)
            y_wave = y + 0.005 * math.cos(x * 10 + self.color_phase)

            glVertex2f((x_wave - 2.5) / 2.5, y_wave / 5.0)
        glEnd()
        
        pygame.display.flip()

    def run(self):
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
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  
                        self.zoom *= 1.1
                    elif event.button == 5:  
                        self.zoom *= 0.9

            self.generate_points()
            self.render()

        pygame.quit()

if __name__ == "__main__":
    BarnsleyFern().run()
