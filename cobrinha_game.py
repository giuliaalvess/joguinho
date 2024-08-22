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
LIGHT_PINK = (255, 182, 193)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Configurações do jogo
BLOCK_SIZE = 20
APPLE_POINTS = 10
difficulty = 'fácil'
FPS = {'fácil': 5, 'médio': 10, 'difícil': 15}

# Carregar imagens
apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (BLOCK_SIZE, BLOCK_SIZE))

head_image = pygame.image.load('head.png')
head_image = pygame.transform.scale(head_image, (BLOCK_SIZE, BLOCK_SIZE))

body_image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
body_image.fill(GREEN)  # Corpo verde

# Função para desenhar a cobrinha
def draw_snake(snake_list):
    for index, segment in enumerate(snake_list):
        if index == 0:
            screen.blit(head_image, [segment[0], segment[1]])
        else:
            screen.blit(body_image, [segment[0], segment[1]])

# Função para desenhar as linhas do fundo
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE * 2):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE * 2):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

# Função para exibir o menu inicial
def show_menu():
    global difficulty
    menu = True
    while menu:
        screen.fill(LIGHT_PINK)
        font = pygame.font.SysFont(None, 75)
        title = font.render('Jogo da Cobrinha', True, WHITE)
        screen.blit(title, [(SCREEN_WIDTH - title.get_width()) // 2, SCREEN_HEIGHT // 6])

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
                    difficulty = select_difficulty()  # Seleciona a dificuldade
                    if difficulty:  # Verifica se a dificuldade foi selecionada
                        game()  # Inicia o jogo
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Função para escolher a dificuldade
def select_difficulty():
    selecting = True
    selected_difficulty = None
    while selecting:
        screen.fill(LIGHT_PINK)
        font = pygame.font.SysFont(None, 75)
        title = font.render('Escolha a Dificuldade', True, WHITE)
        screen.blit(title, [(SCREEN_WIDTH - title.get_width()) // 2, SCREEN_HEIGHT // 6])

        font = pygame.font.SysFont(None, 35)
        easy_button = font.render('Fácil', True, WHITE)
        medium_button = font.render('Médio', True, WHITE)
        hard_button = font.render('Difícil', True, WHITE)

        easy_rect = easy_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        medium_rect = medium_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        hard_rect = hard_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        screen.blit(easy_button, easy_rect)
        screen.blit(medium_button, medium_rect)
        screen.blit(hard_button, hard_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    selected_difficulty = 'fácil'
                    selecting = False
                elif medium_rect.collidepoint(event.pos):
                    selected_difficulty = 'médio'
                    selecting = False
                elif hard_rect.collidepoint(event.pos):
                    selected_difficulty = 'difícil'
                    selecting = False

    return selected_difficulty

# Função principal do jogo
def game():
    global difficulty
    snake_list = [[100, 100], [80, 100], [60, 100]]
    snake_speed = FPS[difficulty]
    apple_position = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                      random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    score = 0
    start_time = time.time()
    clock = pygame.time.Clock()
    direction = 'RIGHT'
    change_to = direction

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        if direction == 'UP':
            new_head = [snake_list[0][0], snake_list[0][1] - BLOCK_SIZE]
        elif direction == 'DOWN':
            new_head = [snake_list[0][0], snake_list[0][1] + BLOCK_SIZE]
        elif direction == 'LEFT':
            new_head = [snake_list[0][0] - BLOCK_SIZE, snake_list[0][1]]
        elif direction == 'RIGHT':
            new_head = [snake_list[0][0] + BLOCK_SIZE, snake_list[0][1]]

        snake_list.insert(0, new_head)

        if new_head[0] == apple_position[0] and new_head[1] == apple_position[1]:
            apple_position = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                              random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
            score += APPLE_POINTS
        else:
            snake_list.pop()

        # Verifica colisões com as bordas ou com o próprio corpo
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
                new_head in snake_list[1:]):
            show_game_over(score, round(time.time() - start_time))
            return

        screen.fill(LIGHT_PINK)
        draw_grid()
        draw_snake(snake_list)
        screen.blit(apple_image, apple_position)
        show_score(score)
        show_time(start_time)

        pygame.display.update()
        clock.tick(snake_speed)

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
        game_over_text = font.render(f'Perdeu! Pontos: {score} Tempo: {elapsed_time}s', True, GREEN)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(game_over_text, game_over_rect)

        font = pygame.font.SysFont(None, 35)
        restart_button = font.render('Recomeçar', True, WHITE)
        exit_button = font.render('Sair', True, WHITE)
        home_button = font.render('Tela Inicial', True, WHITE)

        restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        exit_rect = exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        home_rect = home_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.blit(restart_button, restart_rect)
        screen.blit(exit_button, exit_rect)
        screen.blit(home_button, home_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    game()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if home_rect.collidepoint(event.pos):
                    show_menu()

# Inicia o jogo
show_menu()
