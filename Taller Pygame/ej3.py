import pygame
import math

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
running = True

color = (255, 0, 0)

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
    
    # Se genera el polígono con los puntos calculados, de color 1
    pygame.draw.polygon(screen, color, points, width=0)
    
    # Si se presiona R, se pone de ese color. Si se presiona G, se pone de ese color. Si se presiona B, se pone de ese color.
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_r]:
        color = (255, 0, 0)
    if keys[pygame.K_g]:
        color = (0, 255, 0)
    if keys[pygame.K_b]:
        color = (0, 0, 255)
        
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()