import pygame

def init_window(title, size):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    return screen
