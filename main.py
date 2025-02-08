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
font = pygame.font.Font(None, 40)
menu_items = []

def draw_menu():
    screen.fill((0, 0, 30))
    menu_items.clear()
    
    for i, opt in enumerate(options):
        color = (255, 255, 255) if i == selected else (100, 100, 100)
        text = font.render(opt, True, color)
        text_rect = text.get_rect(center=(400, 200 + i * 50))
        screen.blit(text, text_rect)
        menu_items.append((opt, text_rect))  # Store option and rect for click detection
    
    pygame.display.flip()

def handle_click(pos):
    global selected
    for i, (_, rect) in enumerate(menu_items):
        if rect.collidepoint(pos):
            selected = i
            return True  # Indicate selection has changed
    return False

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if handle_click(event.pos):  # Check if mouse click selects an option
                if selected == 0:
                    Mandelbrot(screen).run()
                elif selected == 1:
                    Julia(screen).run()
                elif selected == 2:
                    Sierpinski(screen).run()
                elif selected == 3:
                    running = False

pygame.quit()
