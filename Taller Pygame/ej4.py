import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
running = True

circles = []
rectangles = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                circles.append(event.pos)
            if event.button == 3: 
                rectangles.append(event.pos)

    screen.fill((255, 255, 255))

    for pos in circles:
        pygame.draw.circle(screen, (255, 0, 0), pos, 20)

    # Dibujar rectángulos
    for pos in rectangles:
        rect = pygame.Rect(pos[0] - 20, pos[1] - 20, 40, 40)
        pygame.draw.rect(screen, (0, 0, 255), rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()