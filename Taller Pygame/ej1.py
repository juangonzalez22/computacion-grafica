import pygame
import math

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
running = True

center = (200, 150)
radius = 50
num_sides = 12

points = []
for i in range(num_sides):
    angle = 2 * math.pi * i / num_sides
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    points.append((x, y))

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    
    # Círculo
    pygame.draw.circle(screen, (255, 0, 0), (75, 150), 50, width=5)
    
    # Línea
    pygame.draw.line(screen, (0, 255, 0), (350, 50), (350, 250), width=5)
    
    # Dodecágono correcto
    pygame.draw.polygon(screen, (0, 0, 255), points, width=5)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()