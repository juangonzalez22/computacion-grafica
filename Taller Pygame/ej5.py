import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(150, 100, 100, 60)

dragging = False
offset_x = 0
offset_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # izquierdo
                if rect.collidepoint(event.pos):
                    dragging = True
                    
                    offset_x = rect.x - event.pos[0]
                    offset_y = rect.y - event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                rect.x = event.pos[0] + offset_x
                rect.y = event.pos[1] + offset_y

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()