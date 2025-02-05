import pygame
from config import WIDTH, HEIGHT, FONT_PATH, WHITE, BLACK

def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main_menu(screen):
    pygame.display.set_caption("Fractal Art Game - Main Menu")
    menu_options = ["1. Mandelbrot Set", "2. Julia Set", "3. Sierpiński Triangle", "4. 4D Tesseract", "5. Credits", "Press [ESC] to Quit"]
    running = True

    while running:
        screen.fill(BLACK)
        draw_text(screen, "Fractal Art Game", 40, WIDTH // 2, 100)
        
        for i, option in enumerate(menu_options):
            draw_text(screen, option, 30, WIDTH // 2, 200 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 2
                elif event.key == pygame.K_4:
                    return 3
                elif event.key == pygame.K_5:
                    credits_screen(screen)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def credits_screen(screen):
    pygame.display.set_caption("Credits")
    running = True
    while running:
        screen.fill(BLACK)
        draw_text(screen, "Fractal Art Game", 40, WIDTH // 2, 100)
        draw_text(screen, "Developed by: You!", 30, WIDTH // 2, 200)
        draw_text(screen, "Press [ESC] to Return", 25, WIDTH // 2, 600)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
