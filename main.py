import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

from fractals.mandelbrot import Mandelbrot
from fractals.julia import Julia  # Import Julia class

class MenuOption:
    def __init__(self, text, action, position):
        self.text = text
        self.action = action
        self.position = position

def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(*color)
    glWindowPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

class Game:
    def __init__(self):
        pygame.init()
        glutInit()

        self.screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Fractal Explorer")

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.menu_options = [
            MenuOption("Mandelbrot", self.run_mandelbrot, (300, 450)),
            MenuOption("Julia Set", self.run_julia, (300, 400)),
            MenuOption("Exit", self.quit_game, (300, 350))
        ]
        
        self.running = True
        self.current_screen = "menu"
        self.selected_option = 0

    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        render_text(250, 500, "Fractal Explorer", GLUT_BITMAP_TIMES_ROMAN_24, (1, 1, 0))

        for i, option in enumerate(self.menu_options):
            color = (1, 0, 0) if i == self.selected_option else (1, 1, 1)
            render_text(*option.position, option.text, GLUT_BITMAP_HELVETICA_18, color)

        pygame.display.flip()

    def run_mandelbrot(self):
        self.current_screen = "mandelbrot"
        fractal = Mandelbrot()
        fractal.run()

    def run_julia(self):
        self.current_screen = "julia"
        fractal = Julia()
        fractal.run()

    def quit_game(self):
        self.running = False

    def handle_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.menu_options[self.selected_option].action()

    def run(self):
        while self.running:
            if self.current_screen == "menu":
                self.handle_menu_input()
                self.render_menu()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
