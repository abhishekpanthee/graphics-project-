import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from utils.textRenderer import TextRenderer
from fractals.mandelbrot import Mandelbrot
# from fractals.julia import JuliaSet
# from fractals.sierpinski3d import Sierpinski3D

class MenuOption:
    def __init__(self, text, action, position):
        self.text = text
        self.action = action
        self.position = position
        self.hover = False
    
    def is_mouse_over(self, mouse_pos):
        x, y = mouse_pos
        text_width = len(self.text) * 15  # Approximate width
        text_height = 30  # Approximate height
        return (self.position[0] <= x <= self.position[0] + text_width and
                self.position[1] - text_height <= y <= self.position[1])

class Game:
    def __init__(self):
        pygame.init()
        # Create both OpenGL and regular surface
        self.screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Fractal Explorer")
        
        # Initialize OpenGL for menu
        glViewport(0, 0, 800, 600)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Initialize text renderer
        self.text_renderer = TextRenderer("./Lato/Lato-Black.ttf", 24)
        
        # Calculate vertical spacing
        start_y = 450
        spacing = 70
        
        # Create menu options with evenly spaced positions
        self.menu_options = [
            MenuOption("Mandelbrot", self.run_mandelbrot, (300, start_y)),
            MenuOption("Julia", self.run_julia, (300, start_y - spacing)),
            MenuOption("Sierpinski 3D", self.run_sierpinski, (300, start_y - 2 * spacing)),
            MenuOption("Exit", self.quit_game, (300, start_y - 3 * spacing))
        ]
        
        self.running = True
        self.current_screen = "menu"
        
    def run_mandelbrot(self):
        self.current_screen = "mandelbrot"
        # Create a new Pygame window without OpenGL for Mandelbrot
        pygame.display.quit()
        pygame.display.init()
        screen = pygame.display.set_mode((800, 600))
        
        try:
            mandelbrot = Mandelbrot(screen)
            mandelbrot.run()
        except Exception as e:
            print(f"Error running Mandelbrot: {e}")
        finally:
            # Restore OpenGL window
            pygame.display.quit()
            pygame.display.init()
            self.screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
            self.current_screen = "menu"
            self.restore_menu_state()
    
    def run_julia(self):
        self.current_screen = "julia"
        try:
            pass  # Implement Julia set here
        except Exception as e:
            print(f"Error running Julia: {e}")
        finally:
            self.current_screen = "menu"
            self.restore_menu_state()
    
    def run_sierpinski(self):
        self.current_screen = "sierpinski"
        try:
            pass  # Implement Sierpinski here
        except Exception as e:
            print(f"Error running Sierpinski: {e}")
        finally:
            self.current_screen = "menu"
            self.restore_menu_state()
    
    def restore_menu_state(self):
        glViewport(0, 0, 800, 600)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def quit_game(self):
        self.running = False
    
    def handle_menu_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_y = 600 - mouse_pos[1]  # Flip Y coordinate for OpenGL
        
        for option in self.menu_options:
            option.hover = option.is_mouse_over((mouse_pos[0], mouse_y))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for option in self.menu_options:
                        if option.hover:
                            option.action()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen != "menu":
                        self.current_screen = "menu"
    
    def render_menu(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Render title
        self.text_renderer.render_text(250, 500, "Fractal Explorer")
        
        # Render menu options
        for option in self.menu_options:
            color = (1, 1, 0) if option.hover else (1, 1, 1)
            glColor3f(*color)
            self.text_renderer.render_text(*option.position, option.text)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            if self.current_screen == "menu":
                self.handle_menu_input()
                self.render_menu()
            else:
                # Handle escape key to return to menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current_screen = "menu"
        
        self.cleanup()
    
    def cleanup(self):
        self.text_renderer.cleanup()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()