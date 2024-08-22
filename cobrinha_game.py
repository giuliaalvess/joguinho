import pygame
import sys
import random
import time
import json

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
GREEN = (0, 255, 0)  # Cor nova para "Perdeu!"
PINK = (255, 192, 203)

# Configurações do jogo
BLOCK_SIZE = 20
APPLE_POINTS = 10
difficulty = 'fácil'
FPS = {'fácil': 5, 'médio': 10, 'difícil': 15}  # Velocidade para cada nível

# Carregar imagens
apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (BLOCK_SIZE, BLOCK_SIZE))

face_image = pygame.image.load('face.png')
face_image = pygame.transform.scale(face_image, (BLOCK_SIZE, BLOCK_SIZE))

# Função para desenhar a cobrinha
def draw_snake(snake_list):
    for index, segment in enumerate(snake_list):
        if index == len(snake_list) - 1:
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
    global difficulty
    menu = True
    while menu:
        screen.fill(PINK)
        font = pygame.font.SysFont(None, 75)
        title = font.render('Jogo da Cobrinha', True, WHITE)
        screen.blit(title, [(SCREEN_WIDTH - title.get_width()) // 2, SCREEN_HEIGHT // 6])

        font = pygame.font.SysFont(None, 35)
        start_button = font.render('Iniciar', True, WHITE)
        rank_button = font.render('Rank', True, WHITE)
        exit_button = font.render('Sair', True, WHITE)

        start_rect = start_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        rank_rect = rank_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        exit_rect = exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        screen.blit(start_button, start_rect)
        screen.blit(rank_button, rank_rect)
        screen.blit(exit_button, exit_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    difficulty = select_difficulty()  # Seleciona a dificuldade
                    player_name = ask_name()  # Pergunta o nome
                    menu = False
                    game(player_name)  # Inicia o jogo com o nome do jogador
                if rank_rect.collidepoint(event.pos):
                    show_rank()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Função para escolher a dificuldade
def select_difficulty():
    selecting = True
    selected_difficulty = None
    while selecting:
        screen.fill(PINK)
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

# Função para solicitar o nome do jogador
def ask_name():
    font = pygame.font.SysFont(None, 35)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(PINK)
        font = pygame.font.SysFont(None, 35)
        prompt = font.render('Escreva seu nome abaixo', True, WHITE)
        screen.blit(prompt, [(SCREEN_WIDTH - prompt.get_width()) // 2, SCREEN_HEIGHT // 2 - 50])

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

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
def show_game_over(score, elapsed_time, player_name):
    save_score(score, elapsed_time, player_name)
    game_over = True
    while game_over:
        screen.fill(DARK_GREEN)
        draw_grid()

        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render(f'Perdeu! Pts: {score} Temp: {elapsed_time}s', True, GREEN)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(game_over_text, game_over_rect)

        font = pygame.font.SysFont(None, 35)
        restart_button = font.render('Recomeçar', True, WHITE)
        rank_button = font.render('Rank', True, WHITE)
        exit_button = font.render('Sair', True, WHITE)
        home_button = font.render('Tela Inicial', True, WHITE)

        restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        rank_rect = rank_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        exit_rect = exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        home_rect = home_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        screen.blit(restart_button, restart_rect)
        screen.blit(rank_button, rank_rect)
        screen.blit(exit_button, exit_rect)
        screen.blit(home_button, home_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    game_over = False
                if rank_rect.collidepoint(event.pos):
                    show_rank()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if home_rect.collidepoint(event.pos):
                    show_menu()

# Função para salvar a pontuação
def save_score(score, elapsed_time, player_name):
    try:
        with open('highscores.json', 'r') as file:
            high_scores = json.load(file)
            if not isinstance(high_scores, list):
                high_scores = []
    except FileNotFoundError:
        high_scores = []

    high_scores.append({'name': player_name, 'score': score, 'time': elapsed_time})
    high_scores = sorted(high_scores, key=lambda x: (-x['score'], x['time']))[:10]  # Top 10

    with open('highscores.json', 'w') as file:
        json.dump(high_scores, file, indent=4)

# Função para exibir o ranking
def show_rank():
    screen.fill(PINK)
    try:
        with open('highscores.json', 'r') as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        high_scores = []

    font = pygame.font.SysFont(None, 35)
    title = font.render('Ranking', True, WHITE)
    screen.blit(title, [(SCREEN_WIDTH - title.get_width()) // 2, 20])

    # Desenhar a lista de pontuações
    font = pygame.font.SysFont(None, 30)
    y_offset = 60
    for entry in high_scores:
        score_text = font.render(f"{entry['name']} - {entry['score']} - {entry['time']}s", True, WHITE)
        screen.blit(score_text, [20, y_offset])
        y_offset += 30

    # Adicionar a barra de rolagem
    scrollbar_height = 20
    scrollbar_width = 15
    scrollbar_x = SCREEN_WIDTH - scrollbar_width - 10
    scrollbar_y = 60
    scrollbar_length = min(len(high_scores) * 30, SCREEN_HEIGHT - scrollbar_y - scrollbar_height - 10)

    scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_length)
    pygame.draw.rect(screen, WHITE, scrollbar_rect)

    scroll_value = 0
    if len(high_scores) * 30 > SCREEN_HEIGHT - 60 - scrollbar_height:
        scroll_value = max(0, min(scrollbar_length - scrollbar_height, pygame.mouse.get_pos()[1] - scrollbar_y - scrollbar_height / 2))
        pygame.draw.rect(screen, WHITE, (scrollbar_x, scrollbar_y + scroll_value, scrollbar_width, scrollbar_height))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if scrollbar_rect.collidepoint(event.pos):
                        scroll_value = max(0, min(scrollbar_length - scrollbar_height, event.pos[1] - scrollbar_y - scrollbar_height / 2))
                        pygame.display.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# Função principal do jogo
def game(player_name):
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2
    x_change = BLOCK_SIZE
    y_change = 0
    snake_list = []
    snake_length = 1
    apple_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    apple_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    clock = pygame.time.Clock()
    start_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_change == 0:
                    x_change = 0
                    y_change = -BLOCK_SIZE
                if event.key == pygame.K_DOWN and y_change == 0:
                    x_change = 0
                    y_change = BLOCK_SIZE
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                if event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0

        x += x_change
        y += y_change

        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            break

        for segment in snake_list[:-1]:
            if segment == [x, y]:
                break

        snake_list.append([x, y])
        if len(snake_list) > snake_length:
            del snake_list[0]

        screen.fill(DARK_GREEN)
        draw_grid()
        draw_snake(snake_list)

        pygame.draw.rect(screen, GREEN, [apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE])

        show_score(snake_length * APPLE_POINTS)
        show_time(start_time)

        pygame.display.update()

        if x == apple_x and y == apple_y:
            apple_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            apple_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        clock.tick(FPS[difficulty])

    show_game_over(snake_length * APPLE_POINTS, round(time.time() - start_time), player_name)

# Inicializa o menu
show_menu()
