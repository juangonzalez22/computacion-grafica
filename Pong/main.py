import pygame
import math
import random

pygame.init()

font = pygame.font.Font("font.ttf", 200)

screen_size = [800, 600]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

collision_sound = pygame.mixer.Sound("collision.wav")
score_sound = pygame.mixer.Sound("score.wav")

# Fondos
bg = pygame.image.load("bg.jpg").convert()
bg = pygame.transform.scale(bg, screen_size)

menu_bg = pygame.image.load("menubg.jpg").convert()
menu_bg = pygame.transform.scale(menu_bg, screen_size)

help_bg = pygame.image.load("helpbg.jpg").convert()
help_bg = pygame.transform.scale(help_bg, screen_size)

player_size = [5, screen_size[1] // 5]
player_1_pos = [20, screen_size[1] // 2 - player_size[1] // 2]
player_2_pos = [screen_size[0] - 20 - player_size[0], screen_size[1] // 2 - player_size[1] // 2]

ball_size = [10, 10]
ball_pos = [screen_size[0] // 2 - ball_size[0] // 2,
            screen_size[1] // 2 - ball_size[1] // 2]

players_speed = screen_size[1] // 60
original_ball_speed_unit = 5
ball_speed_unit = 5
ball_speed = [ball_speed_unit, ball_speed_unit]

player_1_points = 0
player_2_points = 0

font_alpha = 50

last_point = 0

paused = True
pause_start = 0
pause_duration = 1000

def random_direction():
    directions = [
        [ball_speed_unit, ball_speed_unit],
        [ball_speed_unit, -ball_speed_unit],
        [-ball_speed_unit, ball_speed_unit],
        [-ball_speed_unit, -ball_speed_unit]
    ]
    return random.choice(directions)

def direction_last_point():
    if last_point == 1:
        return [-ball_speed_unit, random.choice([-ball_speed_unit, ball_speed_unit])]
    else:
        return [ball_speed_unit, random.choice([-ball_speed_unit, ball_speed_unit])]


running = True
state = 0 

while running:

    mouse_click = False 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
                if state == 0:
                    state = 1
                    ball_speed_unit = 0
                else:
                    state = 0
                    ball_speed_unit = original_ball_speed_unit
                    ball_speed = random_direction()
                    paused = True
                    pause_start = pygame.time.get_ticks()
                    ball_pos = [screen_size[0] // 2 - ball_size[0] // 2,
                                screen_size[1] // 2 - ball_size[1] // 2]
                    player_1_points = 0
                    player_2_points = 0
                    player_1_pos = [20, screen_size[1] // 2 - player_size[1] // 2]
                    player_2_pos = [screen_size[0] - 20 - player_size[0], screen_size[1] // 2 - player_size[1] // 2]

    if state == 0:
        screen.blit(bg, (0, 0))

        player_1_score_text = font.render(str(player_1_points), True, (255, 255, 255))
        player_1_score_text.set_alpha(font_alpha)

        player_2_score_text = font.render(str(player_2_points), True, (255, 255, 255))
        player_2_score_text.set_alpha(font_alpha)

        screen.blit(player_1_score_text,
                    (screen_size[0]//4 - player_1_score_text.get_width()//2,
                     screen_size[1]//2 - player_1_score_text.get_height()//2))

        screen.blit(player_2_score_text,
                    (3 * screen_size[0]//4 - player_2_score_text.get_width()//2,
                     screen_size[1]//2 - player_2_score_text.get_height()//2))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player_1_pos[1] -= players_speed
        if keys[pygame.K_s]:
            player_1_pos[1] += players_speed

        if keys[pygame.K_UP]:
            player_2_pos[1] -= players_speed
        if keys[pygame.K_DOWN]:
            player_2_pos[1] += players_speed

        player_1_pos[1] = max(0, min(screen_size[1] - player_size[1], player_1_pos[1]))
        player_2_pos[1] = max(0, min(screen_size[1] - player_size[1], player_2_pos[1]))

        if not paused:
            ball_pos[0] += ball_speed[0]
            ball_pos[1] += ball_speed[1]
        else:
            if pygame.time.get_ticks() - pause_start > pause_duration:
                paused = False
                ball_speed = direction_last_point()

        if ball_pos[0] < 0:
            player_2_points += 1
            score_sound.play()
            player_1_pos = [20, screen_size[1] // 2 - player_size[1] // 2]
            player_2_pos = [screen_size[0] - 20 - player_size[0], screen_size[1] // 2 - player_size[1] // 2]
            ball_pos = [screen_size[0] // 2 - ball_size[0] // 2,
                        screen_size[1] // 2 - ball_size[1] // 2]
            paused = True
            last_point = 2
            pause_start = pygame.time.get_ticks()

        if ball_pos[0] > screen_size[0] - ball_size[0]:
            player_1_points += 1
            score_sound.play()
            player_1_pos = [20, screen_size[1] // 2 - player_size[1] // 2]
            player_2_pos = [screen_size[0] - 20 - player_size[0], screen_size[1] // 2 - player_size[1] // 2]
            ball_pos = [screen_size[0] // 2 - ball_size[0] // 2,
                        screen_size[1] // 2 - ball_size[1] // 2]
            paused = True
            last_point = 1
            pause_start = pygame.time.get_ticks()

        if ball_pos[1] < 0 or ball_pos[1] > screen_size[1] - ball_size[1]:
            ball_speed[1] = -ball_speed[1]
            ball_speed[0] *= 1.05
            ball_speed[1] *= 1.05
            collision_sound.play()

        if player_1_points == 10 or player_2_points == 10:
            state = 1
            ball_speed_unit = 0

        rect1 = (*player_1_pos, *player_size)
        pygame.draw.rect(screen, (0, 0, 0), rect1)
        pygame.draw.rect(screen, (255, 255, 255), rect1, 1)

        rect2 = (*player_2_pos, *player_size)
        pygame.draw.rect(screen, (0, 0, 0), rect2)
        pygame.draw.rect(screen, (255, 255, 255), rect2, 1)

        pygame.draw.circle(screen, (255, 255, 255),
                           (ball_pos[0] + ball_size[0] // 2,
                            ball_pos[1] + ball_size[1] // 2),
                           ball_size[0] // 2)

        if (ball_pos[0] <= player_1_pos[0] + player_size[0] and
            ball_pos[1] + ball_size[1] >= player_1_pos[1] and
            ball_pos[1] <= player_1_pos[1] + player_size[1]):
            ball_speed[0] = abs(ball_speed[0])
            ball_speed[0] *= 1.01
            ball_speed[1] *= 1.01
            collision_sound.play()

        if (ball_pos[0] + ball_size[0] >= player_2_pos[0] and
            ball_pos[1] + ball_size[1] >= player_2_pos[1] and
            ball_pos[1] <= player_2_pos[1] + player_size[1]):
            ball_speed[0] = -abs(ball_speed[0])
            ball_speed[0] *= 1.01
            ball_speed[1] *= 1.01
            collision_sound.play()

    elif state == 1:
        screen.blit(menu_bg, (0, 0))

        title_text = font.render("PONG", True, (255, 255, 255))
        screen.blit(title_text,
                    (screen_size[0]//2 - title_text.get_width()//2,
                     screen_size[1]//2 - title_text.get_height()//2))

        play_button = pygame.Rect(screen_size[0]//2 - 100, screen_size[1]//2 + 100, 200, 50)
        help_button = pygame.Rect(screen_size[0]//2 - 100, screen_size[1]//2 + 170, 200, 50)

        mouse_pos = pygame.mouse.get_pos()

        if play_button.collidepoint(mouse_pos):
            color = (200, 200, 200)
            if mouse_click:
                state = 0
                state = 0
                ball_speed_unit = original_ball_speed_unit
                ball_speed = direction_last_point()
                paused = True
                pause_start = pygame.time.get_ticks()
                ball_pos = [screen_size[0] // 2 - ball_size[0] // 2,
                            screen_size[1] // 2 - ball_size[1] // 2]
                player_1_points = 0
                player_2_points = 0
                player_1_pos = [20, screen_size[1] // 2 - player_size[1] // 2]
                player_2_pos = [screen_size[0] - 20 - player_size[0], screen_size[1] // 2 - player_size[1] // 2]
        else:
            color = (255, 255, 255)

        if help_button.collidepoint(mouse_pos):
            help_color = (200, 200, 200)
            if mouse_click:
                state = 2
        else:
            help_color = (255, 255, 255)

        pygame.draw.rect(screen, color, play_button)
        pygame.draw.rect(screen, help_color, help_button)

        play_font = pygame.font.Font("font.ttf", 50)
        play_text = play_font.render("PLAY", True, (0, 0, 0))
        help_text = play_font.render("HELP", True, (0, 0, 0))

        screen.blit(play_text,
                    (screen_size[0]//2 - play_text.get_width()//2,
                     screen_size[1]//2 + 100 + 25 - play_text.get_height()//2))

        screen.blit(help_text,
                    (screen_size[0]//2 - help_text.get_width()//2,
                     screen_size[1]//2 + 170 + 25 - help_text.get_height()//2))

    elif state == 2:
        screen.blit(help_bg, (0, 0))

        help_title = font.render("HELP", True, (255, 255, 255))
        screen.blit(help_title,
                    (screen_size[0]//2 - help_title.get_width()//2,
                     screen_size[1]//4 - help_title.get_height()//2))

        instructions_font = pygame.font.Font("font.ttf", 30)
        instructions = [
            "Player 1: W / S",
            "Player 2: UP / DOWN",
            "First to 10 points wins"
        ]

        for i, instruction in enumerate(instructions):
            instruction_text = instructions_font.render(instruction, True, (255, 255, 255))
            screen.blit(instruction_text,
                        (screen_size[0]//2 - instruction_text.get_width()//2,
                         screen_size[1]//2 + i * 50))

        back_button = pygame.Rect(screen_size[0]//2 - 100, screen_size[1] - 120, 200, 50)

        mouse_pos = pygame.mouse.get_pos()

        if back_button.collidepoint(mouse_pos):
            color = (200, 200, 200)
            if mouse_click:
                state = 1
                ball_speed_unit = 0
        else:
            color = (255, 255, 255)

        pygame.draw.rect(screen, color, back_button)

        back_font = pygame.font.Font("font.ttf", 40)
        back_text = back_font.render("BACK", True, (0, 0, 0))

        screen.blit(back_text,
                    (screen_size[0]//2 - back_text.get_width()//2,
                     screen_size[1] - 120 + 25 - back_text.get_height()//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()