import pygame
import numpy as np
from utils.basicFunctions import draw_text

class Mandelbrot:
   

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.zoom = 1
        self.offset_x, self.offset_y = -0.5, 0
        self.max_iter = 256

    def compute_mandelbrot(self, x, y):
        c = complex(x, y)
        z = 0
        for i in range(self.max_iter):
            if abs(z) > 2:
                return i
            z = z * z + c
        return self.max_iter

    def render(self):
        # draw_text(self.screen, "hello", (400, 300))
        for x in range(self.width):
            for y in range(self.height):
                real = (x - self.width / 2) / (self.zoom * self.width) + self.offset_x
                imag = (y - self.height / 2) / (self.zoom * self.height) + self.offset_y
                color = self.compute_mandelbrot(real, imag)
                self.screen.set_at((x, y), (color % 8 * 32, color % 16 * 16, color % 32 * 8))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.render()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
