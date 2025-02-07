import pygame
from fractals.mandelbrot import Mandelbrot
from fractals.julia import Julia
from shapes.sierpinski import Sierpinski
from utils.graphics import init_window

# Initialize pygame
pygame.init()
screen = init_window("Interactive Fractal Art", (800, 600))

# Menu options
options = ["Mandelbrot", "Julia", "Sierpinski 3D", "Exit"]
selected = 0

def draw_menu():
    screen.fill((0, 0, 30))
    font = pygame.font.Font(None, 40)
    for i, opt in enumerate(options):
        color = (255, 255, 255) if i == selected else (100, 100, 100)
        text = font.render(opt, True, color)
        screen.blit(text, (350, 200 + i * 50))
    pygame.display.flip()

running = True
while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(options)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if selected == 0:
                    Mandelbrot(screen).run()
                elif selected == 1:
                    Julia(screen).run()
                elif selected == 2:
                    Sierpinski(screen).run()
                elif selected == 3:
                    running = False

pygame.quit()
