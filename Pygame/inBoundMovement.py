import pygame

pygame.init()
ancho, alto = 500, 500
screen = pygame.display.set_mode((ancho, alto))
clock = pygame.time.Clock()

pos = [250, 250]  # posición inicial
vel = 5           # velocidad de movimiento
radio = 15
limiteSup = 500 - radio
limiteInf = 0 + radio

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pos[1] -= vel
    if keys[pygame.K_DOWN]:
        pos[1] += vel
    if keys[pygame.K_LEFT]:
        pos[0] -= vel
    if keys[pygame.K_RIGHT]:
        pos[0] += vel
        
    if pos[0] > limiteSup:
        pos[0] = limiteSup
    if pos[0] < limiteInf:
        pos[0] = limiteInf
    if pos[1] > limiteSup:
        pos[1] = limiteSup
    if pos[1] < limiteInf:
        pos[1] = limiteInf
        
    

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), pos, radio)
    pygame.display.flip()
    clock.tick(120)

pygame.quit()