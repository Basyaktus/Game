import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Троникс")

ball_radius = 20
ball_color = (255, 0, 0)
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
ball_speed = [2, 8]

rect_width, rect_height = 100, 20
rect_color = (0, 255, 0)
rect = pygame.Rect(WIDTH // 1.5, HEIGHT - rect_height - 10, rect_width, rect_height)
rect_speed = [0, 0]
rect_move_speed = 5

life = 3
font = pygame.font.SysFont(None, 36)

bonus_radius = 10
bonus_color = (0, 255, 255)
lucky_num = [1, 4, 7]

block_width, block_height = 50, 20
block_color = (0, 0, 255)
block_border_color = (0, 0, 0)
blocks = [pygame.Rect(x, y + block_height, block_width, block_height) for x in range(0, WIDTH, block_width) for y in range(0, 100, block_height)]

bonuses = []
expand_active = False
clock_active = False
bonus_start_time = 0
bonus_duration = 10  

banana_image = pygame.image.load('banana.png')
banana_image = pygame.transform.scale(banana_image, (bonus_radius * 2, bonus_radius * 2))

background_image = pygame.image.load('застака.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

heart_image = pygame.image.load('heart.png')
heart_image = pygame.transform.scale(heart_image, (bonus_radius * 2, bonus_radius * 2))

clock_image = pygame.image.load('clock.png')
clock_image = pygame.transform.scale(clock_image, (bonus_radius * 2, bonus_radius * 2))

bad_image=pygame.image.load('bad.png')
bad_image=pygame.transform.scale(bad_image, (bonus_radius * 2, bonus_radius * 2))

clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        rect.x -= rect_move_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        rect.x += rect_move_speed

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0:
        ball.left = 0
        ball_speed[0] = -ball_speed[0]
    if ball.right >= WIDTH:
        ball.right = WIDTH
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 36: 
        ball.top = 36
        ball_speed[1] = -ball_speed[1]
    if ball.colliderect(rect):
        ball.bottom = rect.top
        ball_speed[1] = -ball_speed[1]

    if ball.bottom >= HEIGHT:
        ball.x = WIDTH // 2 - ball_radius
        ball.y = HEIGHT // 2 - ball_radius
        ball_speed[0] *= 1.2
        ball_speed[1] *= 1.2
        life -= 1
        if life <= 0:
            screen.fill((0, 0, 0))
            draw_text('Вы проиграли', font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            time.sleep(3)
            pygame.quit()
            sys.exit()

    if rect.left < 0:
        rect.left = 0
    if rect.right > WIDTH:
        rect.right = WIDTH

    for block in blocks[:]:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_speed[1] = -ball_speed[1]
            z = random.randint(0, 10)
            if z in lucky_num:
                bonus_type = random.choice(['expand', 'life', 'clock', 'bad'])
                bonus = pygame.Rect(block.x + block_width // 2 - bonus_radius, block.y + block_height // 2 - bonus_radius, bonus_radius * 2, bonus_radius * 2)
                bonuses.append((bonus, bonus_type))
            break

    for bonus, bonus_type in bonuses[:]:
        bonus.y += 5
        if bonus.colliderect(rect):
            bonuses.remove((bonus, bonus_type))
            if bonus_type == 'expand' and not expand_active:
                rect.width = rect.width * 2 
                expand_active = True
                bonus_start_time = time.time()
            elif bonus_type == 'life':
                life += 1
            elif bonus_type == 'bad':
                life -= 1
            elif bonus_type == 'clock' and not clock_active:
                ball_speed[0] *= 0.5
                ball_speed[1] *= 0.5
                clock_active = True
                bonus_start_time = time.time()
        elif bonus.top > HEIGHT:
            bonuses.remove((bonus, bonus_type))

    if expand_active and time.time() - bonus_start_time > bonus_duration:
        rect.width = rect_width 
        expand_active = False

    if clock_active and time.time() - bonus_start_time > bonus_duration:
        ball_speed[0] *= 2
        ball_speed[1] *= 2
        clock_active = False

    screen.blit(background_image, (0, 0)) 
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.rect(screen, rect_color, rect)
    for block in blocks:
        pygame.draw.rect(screen, block_color, block)
        pygame.draw.rect(screen, block_border_color, block, 1)
    for bonus, bonus_type in bonuses:
        if bonus_type == 'expand':
            screen.blit(banana_image, bonus.topleft) 
        elif bonus_type == 'life':
            screen.blit(heart_image, bonus.topleft)
        elif bonus_type == 'clock':
            screen.blit(clock_image, bonus.topleft)
        elif bonus_type == 'bad':
            screen.blit(bad_image, bonus.topleft)

    life_text = font.render(f'Lives: {life}', True, (0, 0, 0))
    screen.blit(life_text, (10, 0))

    if not blocks:
        screen.fill((0, 0, 0))
        draw_text('Вы выиграли', font, (0, 255, 0), screen, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)