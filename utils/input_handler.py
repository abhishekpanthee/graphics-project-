import pygame

def handle_menu_input(selected, options_count):
    action = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return selected, "exit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % options_count
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % options_count
            elif event.key == pygame.K_RETURN:
                action = "select"
    return selected, action
