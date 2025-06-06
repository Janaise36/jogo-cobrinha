import pygame
from pygame.locals import *
import random
import time

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
POS_INICIAL_X = WINDOWS_HEIGHT / 2
POS_INICIAL_Y = WINDOWS_WIDTH / 2
BLOCK = 10

pygame.font.init()
fonte = pygame.font.SysFont('arial', 35, True, True)

def colision(pos1, pos2):
    return pos1 == pos2

def off_limits(pos):
    return not (0 <= pos[0] < WINDOWS_WIDTH and 0 <= pos[1] < WINDOWS_HEIGHT)

def random_on_grid(obstaculo_pos):
    x = random.randint(0, WINDOWS_WIDTH // BLOCK) * BLOCK
    y = random.randint(0, WINDOWS_HEIGHT // BLOCK) * BLOCK
    while (x, y) in obstaculo_pos:
        x = random.randint(0, WINDOWS_WIDTH // BLOCK) * BLOCK
        y = random.randint(0, WINDOWS_HEIGHT // BLOCK) * BLOCK
    return x, y

pontos = 0
velocidade = 10
pygame.init()
window = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption('Jogo da Cobrinha')

snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((BLOCK, BLOCK))
snake_surface.fill((53, 59, 72))
snake_direction = K_LEFT

obstaculo_pos = []
obstaculo_surface = pygame.Surface((BLOCK, BLOCK))
obstaculo_surface.fill((0, 0, 0))

apple_surface = pygame.Surface((BLOCK, BLOCK))
apple_surface.fill((255, 0, 0))
apple_pos = random_on_grid(obstaculo_pos)

def game_over():
    window.fill((68, 189, 50))
    fonte = pygame.font.SysFont('arial', 60, True, True)
    gameOver = 'GAME OVER'
    text_over = fonte.render(gameOver, True, (255, 255, 255))
    window.blit(text_over, (110, 300))
    pygame.display.update()
    time.sleep(5)
    pygame.quit()

while True:
    pygame.time.Clock().tick(velocidade)
    window.fill((68, 189, 50))

    mensagem = f'Pontos: {pontos}'
    texto = fonte.render(mensagem, True, (255, 255, 255))
    window.blit(texto, (420, 30))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if (event.key == K_UP and snake_direction == K_DOWN) or \
                   (event.key == K_DOWN and snake_direction == K_UP) or \
                   (event.key == K_RIGHT and snake_direction == K_LEFT) or \
                   (event.key == K_LEFT and snake_direction == K_RIGHT):
                    continue
                else:
                    snake_direction = event.key

    window.blit(apple_surface, apple_pos)

    if colision(apple_pos, snake_pos[0]):
        snake_pos.append((-10, -10))
        apple_pos = random_on_grid(obstaculo_pos)
        obstaculo_pos.append(random_on_grid(obstaculo_pos))
        pontos += 1
        if pontos % 5 == 0:
            velocidade += 2

    for pos_obstaculo in obstaculo_pos:
        if colision(pos_obstaculo, snake_pos[0]):
            game_over()

    for pos_snake in snake_pos:
        window.blit(snake_surface, pos_snake)

    for pos_obstaculo in obstaculo_pos:
        window.blit(obstaculo_surface, pos_obstaculo)

    for i in range(len(snake_pos) - 1, 0, -1):
        if colision(snake_pos[0], snake_pos[i]):
            game_over()
        snake_pos[i] = snake_pos[i-1]

    if off_limits(snake_pos[0]):
        game_over()

    if snake_direction == K_UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - BLOCK)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + BLOCK)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (snake_pos[0][0] - BLOCK, snake_pos[0][1])
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (snake_pos[0][0] + BLOCK, snake_pos[0][1])

    pygame.display.update()