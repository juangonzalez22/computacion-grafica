import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
running = True

initial_pos = [200, 150]
speed = 5
x_size = 100
y_size = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        initial_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        initial_pos[1] += speed
    if keys[pygame.K_LEFT]:
        initial_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        initial_pos[0] += speed
    
    if initial_pos[0] < x_size // 2:
        initial_pos[0] = x_size // 2
    if initial_pos[0] > 400 - x_size // 2:
        initial_pos[0] = 400 - x_size // 2

    if initial_pos[1] < y_size // 2:
        initial_pos[1] = y_size // 2
    if initial_pos[1] > 300 - y_size // 2:
        initial_pos[1] = 300 - y_size // 2
        
    screen.fill((255, 255, 255))
    pygame.draw.polygon (screen, (0, 0, 255), [
        (initial_pos[0]- x_size // 2, initial_pos[1] - y_size // 2),
        (initial_pos[0] + x_size // 2, initial_pos[1] - y_size // 2),
        (initial_pos[0] + x_size // 2, initial_pos[1] + y_size // 2),
        (initial_pos[0] - x_size // 2, initial_pos[1] + y_size // 2)
    ], width=0)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()