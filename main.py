import pygame
import OpenGL.GL as gl
from menu import main_menu
from config import WIDTH, HEIGHT, FPS
from mandelbrot import draw_mandelbrot_animation
from julia import draw_julia_animation
from sierpinski import draw_sierpinski_animation
from tesseract import tesseract_animation

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)


pygame.display.set_caption("Fractal Art Game")

def main():
    clock = pygame.time.Clock()
    current_fractal = main_menu(screen)
    
    zoom_factor = 1.0
    offset_x = offset_y = 0.0
    rotation_angle = 0.0
    zoom_increment = 0.05  # Speed of zooming
    
    while True:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        if current_fractal == 0:
            # Animated Mandelbrot
            draw_mandelbrot_animation(zoom_factor, offset_x, offset_y)
            zoom_factor += zoom_increment
            if zoom_factor > 2.5:
                zoom_factor = 1.0  # Reset zoom after reaching a limit

        elif current_fractal == 1:
            # Animated Julia set
            draw_julia_animation(zoom_factor, offset_x, offset_y)
            zoom_factor += zoom_increment
            if zoom_factor > 2.5:
                zoom_factor = 1.0

        elif current_fractal == 2:
            # Animated Sierpinski Triangle
            rotation_angle += 1  # Rotate triangle over time
            draw_sierpinski_animation(rotation_angle)

        elif current_fractal == 3:
            # Animated 4D Tesseract
            tesseract_animation()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
