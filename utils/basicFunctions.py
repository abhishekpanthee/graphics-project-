import pygame
def draw_text(screen, text, position, font_size=50, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size) 
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)  
    screen.blit(text_surface, text_rect)