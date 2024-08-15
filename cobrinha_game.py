import pygame
import sys
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jogo da Cobrinha')

# Cores
BEIGE = (245, 222, 179)
DARK_GREEN = (34, 139, 34)
LINE_COLOR = (0, 100, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configurações do jogo
BLOCK_SIZE = 20
FPS = 10  # Velocidade reduzida

# Carregar imagens
apple_image = pygame.image.load('apple.png')  # Certifique-se de ter uma imagem de maçã redonda
apple_image = pygame.transform.scale(apple_image, (BLOCK_SIZE, BLOCK_SIZE))

# Carregar imagem da carinha
face_image = pygame.image.load('face.png')  # Adicione uma imagem de carinha
face_image = pygame.transform.scale(face_image, (BLOCK_SIZE, BLOCK_SIZE))


# Função para desenhar a cobrinha
def draw_snake(snake_list):
    for index, segment in enumerate(snake_list):
        if index == len(snake_list) - 1:
            # Desenhar a carinha na cabeça da cobrinha
            screen.blit(face_image, [segment[0], segment[1]])
        else:
            pygame.draw.rect(screen, BEIGE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])


# Função para desenhar as linhas do fundo
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, y), (SCREEN_WIDTH, y))


# Função para exibir o menu inicial
def show_menu():
    menu = True
    while menu:
        screen.fill(DARK_GREEN)
        draw_grid()
        font = pygame.font.SysFont(None, 75)
        title = font.render('Jogo da Cobrinha', True, WHITE)
        screen.blit(title, [(SCREEN_WIDTH - title.get_width()) // 2, SCREEN_HEIGHT // 4])

        font = pygame.font.SysFont(None, 35)
        start_button = font.render('Iniciar', True, WHITE)
        exit_button = font.render('Sair', True, WHITE)

        start_rect = start_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        exit_rect = exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(start_button, start_rect)
        screen.blit(exit_button, exit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    menu = False
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# Função para mostrar a pontuação
def show_score(score):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f'Pontuação: {score}', True, WHITE)
    screen.blit(score_text, [10, 10])


# Função para mostrar o tempo
def show_time(start_time):
    elapsed_time = round(time.time() - start_time)
    font = pygame.font.SysFont(None, 35)
    time_text = font.render(f'Tempo: {elapsed_time}s', True, WHITE)
    screen.blit(time_text, [SCREEN_WIDTH - 150, 10])


# Função para exibir a tela de fim de jogo
def show_game_over(score, elapsed_time):
    game_over = True
    while game_over:
        screen.fill(DARK_GREEN)
        draw_grid()

        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render(f'Perdeuu! Pts: {score} Temp: {elapsed_time}s', True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(game_over_text, game_over_rect)

        font = pygame.font.SysFont(None, 35)
        restart_button = font.render('Recomeçar', True, WHITE)
        exit_button = font.render('Sair', True, WHITE)

        restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        exit_rect = exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(restart_button, restart_rect)
        screen.blit(exit_button, exit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    game_over = False
                    game()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# Função principal do jogo
def game():
    snake_x = SCREEN_WIDTH / 2
    snake_y = SCREEN_HEIGHT / 2

    snake_x_change = 0
    snake_y_change = 0

    snake_list = []
    snake_length = 1
    score = 0

    start_time = time.time()

    food_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    game_close = False

    while not game_close:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -BLOCK_SIZE
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = BLOCK_SIZE
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -BLOCK_SIZE
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = BLOCK_SIZE
                    snake_x_change = 0

        snake_x += snake_x_change
        snake_y += snake_y_change

        if snake_x >= SCREEN_WIDTH or snake_x < 0 or snake_y >= SCREEN_HEIGHT or snake_y < 0:
            elapsed_time = round(time.time() - start_time)
            show_game_over(score, elapsed_time)

        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 1

        screen.fill(DARK_GREEN)
        draw_grid()
        screen.blit(apple_image, [food_x, food_y])

        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                elapsed_time = round(time.time() - start_time)
                show_game_over(score, elapsed_time)

        draw_snake(snake_list)
        show_score(score)
        show_time(start_time)

        pygame.display.update()

        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()


# Mostrar o menu antes de começar o jogo
show_menu()

# Iniciar o jogo
game()
