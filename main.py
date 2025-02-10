import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

from fractals.mandelbrot import Mandelbrot  # Mandelbrot class
import numpy as np

class MenuOption:
    def __init__(self, text, action, position):
        self.text = text
        self.action = action
        self.position = position
        self.hover = False

    def is_mouse_over(self, mouse_pos):
        x, y = mouse_pos
        text_width = len(self.text) * 15
        text_height = 30
        return (self.position[0] <= x <= self.position[0] + text_width and
                self.position[1] - text_height <= y <= self.position[1])

def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    """Render text using OpenGL GLUT bitmap fonts."""
    glColor3f(*color)  # Set text color
    glWindowPos2f(x, y)  # ✅ Use `glWindowPos2f` instead of `glRasterPos2f`
    
    for char in text:
        glutBitmapCharacter(font, ord(char))  # Render each character

class Game:
    def __init__(self):
        pygame.init()
        glutInit()

        self.screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Fractal Explorer")

        # OpenGL Setup for 2D Text Rendering
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)  # Make sure (0,0) is bottom-left
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.menu_options = [
            MenuOption("Mandelbrot", self.run_mandelbrot, (300, 450)),
            MenuOption("Exit", self.quit_game, (300, 380))
        ]
        
        self.running = True
        self.current_screen = "menu"
        self.selected_option = 0  # Default selected menu option

    def render_menu(self):
        """Render the menu screen using OpenGL."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Render title
        render_text(250, 500, "Fractal Explorer", GLUT_BITMAP_TIMES_ROMAN_24, (1, 1, 0))

        # Render menu options
        for i, option in enumerate(self.menu_options):
            color = (1, 0, 0) if i == self.selected_option else (1, 1, 1)  # Highlight selected option
            render_text(*option.position, option.text, GLUT_BITMAP_HELVETICA_18, color)

        pygame.display.flip()

    def run_mandelbrot(self):
        """Switch to Mandelbrot fractal rendering"""
        self.current_screen = "mandelbrot"
        self.mandelbrot = Mandelbrot()
        self.mandelbrot.run()

    def quit_game(self):
        """Exit game"""
        self.running = False

    def restore_menu_state(self):
        """Reset OpenGL state for menu rendering"""
        glViewport(0, 0, 800, 600)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def handle_menu_input(self):
        """Handle keyboard input for menu navigation"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.menu_options[self.selected_option].action()
                elif event.key == pygame.K_ESCAPE:
                    if self.current_screen != "menu":
                        self.current_screen = "menu"

    def run(self):
        """Main game loop"""
        while self.running:
            if self.current_screen == "menu":
                self.handle_menu_input()
                self.render_menu()
            elif self.current_screen == "mandelbrot":
                self.run_mandelbrot()  # Only runs once, not in a loop
                # self.current_screen = "menu"  # Return to menu after fractal display

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
