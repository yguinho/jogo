import pygame
import random
import time
import os

print("Inicializando o Pygame...")
# Inicialização do pygame
pygame.init()

# Configuração da tela
screen_width = 900
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))

# Título e Ícone
pygame.display.set_caption("Space Shooter")
try:
    icon = pygame.image.load('img/spaceship.png')
    pygame.display.set_icon(icon)
except pygame.error as e:
    print(f"Erro ao carregar a imagem do ícone: {e}")

# Redimensionar imagens
def scale_image(image_path, scale_factor):
    image = pygame.image.load(image_path)
    scaled_width = int(image.get_width() * scale_factor)
    scaled_height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (scaled_width, scaled_height))

# Imagem de fundo
background_img = pygame.image.load('img/bg.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Jogador
player_img = scale_image('img/spaceship.png', 0.107)  # Diminuição para 0.85x do tamanho original
player_width, player_height = player_img.get_size()
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 20
player_x_change = 0
player_y_change = 0
player_shot_cooldown = 0.15
last_player_shot_time = 0

def player(x, y):
    screen.blit(player_img, (x, y))

# Inimigos
enemy_img = scale_image('img/enemy.png', 0.09)  # Aumento para 1.5x do tamanho reduzido
enemy_width, enemy_height = enemy_img.get_size()
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 3  # Diminuído o número de inimigos

def create_enemies():
    for i in range(num_of_enemies):
        enemy_x.append(random.randint(0, screen_width - enemy_width))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(0.2)  # Velocidade dos inimigos
        enemy_y_change.append(0.2)  # Velocidade dos inimigos

def reset_game():
    global player_x, player_y, player_x_change, player_y_change, bullet_x, bullet_y, bullet_state, score_value, game_over
    global enemy_x, enemy_y, enemy_x_change, enemy_y_change, last_player_shot_time
    player_x = (screen_width - player_width) // 2
    player_y = screen_height - player_height - 20
    player_x_change = 0
    player_y_change = 0
    bullet_x = 0
    bullet_y = player_y
    bullet_state = "ready"
    score_value = 0
    game_over = False
    enemy_x.clear()
    enemy_y.clear()
    enemy_x_change.clear()
    enemy_y_change.clear()
    create_enemies()
    last_player_shot_time = 0

create_enemies()

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Bala
bullet_img = scale_image('img/bullet.png', 0.1)
bullet_width, bullet_height = bullet_img.get_size()
bullet_x = 0
bullet_y = player_y
bullet_x_change = 0
bullet_y_change = 4
bullet_dx = 0
bullet_dy = -bullet_y_change
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state, bullet_x, bullet_y, last_player_shot_time
    current_time = time.time()
    if current_time - last_player_shot_time >= player_shot_cooldown:
        bullet_state = "fire"
        bullet_x = x + (player_width // 2) - (bullet_width // 2)
        bullet_y = y
        screen.blit(bullet_img, (bullet_x, bullet_y))
        last_player_shot_time = current_time

def is_collision(x1, y1, x2, y2, distance_threshold):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance < distance_threshold

# Pontuação
score_value = 0
high_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_high_score(x, y):
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(high_score_text, (x, y + 40))  # Ajustado para ficar abaixo do Score

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 32)

def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (
        screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))

# Pausa
pause_font = pygame.font.Font('freesansbold.ttf', 64)

def show_pause():
    pause_text = pause_font.render("PAUSE", True, (255, 255, 255))
    screen.blit(pause_text, (
        screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - pause_text.get_height() // 2))

# Funções para salvar e carregar o high score
def load_high_score():
    global high_score
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            try:
                high_score = int(file.read())
            except ValueError:
                high_score = 0
    else:
        high_score = 0

def save_high_score():
    global high_score
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

print("Iniciando o loop principal...")
# Carregar o high score ao iniciar o jogo
load_high_score()

# Loop principal do jogo
running = True
game_over = False
paused = False

while running:
    screen.blit(background_img, (0, 0))  # Desenhar fundo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movimento do jogador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x_change = -0.5
            if event.key == pygame.K_d:
                player_x_change = 0.5
            if event.key == pygame.K_w:
                player_y_change = -0.5
            if event.key == pygame.K_s:
                player_y_change = 0.5
            if event.key == pygame.K_r and game_over:
                reset_game()
                load_high_score()  # Recarregar o high score ao reiniciar
            if event.key == pygame.K_p:
                paused = not paused  # Alterna o estado de pausa

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_x_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player_y_change = 0

        # Disparo da bala ao clicar com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                fire_bullet(player_x, player_y)

    if not paused:
        if not game_over:
            # Atualizar posição do jogador
            player_x += player_x_change
            player_y += player_y_change
            if player_x <= 0:
                player_x = 0
            elif player_x >= screen_width - player_width:
                player_x = screen_width - player_width
            if player_y <= 0:
                player_y = 0
            elif player_y >= screen_height - player_height:
                player_y = screen_height - player_height

            # Atualizar posição dos inimigos
            for i in range(num_of_enemies):
                enemy_x[i] += enemy_x_change[i]
                enemy_y[i] += enemy_y_change[i]  # Inimigos descendo a tela
                if enemy_x[i] <= 0:
                    enemy_x_change[i] = 0.2
                elif enemy_x[i] >= screen_width - enemy_width:
                    enemy_x_change[i] = -0.2

                # Colisão com o jogador
                if is_collision(enemy_x[i], enemy_y[i], player_x, player_y, 27):
                    game_over = True
                    if score_value > high_score:
                        high_score = score_value
                        save_high_score()  # Salva o novo high score
                    break

                # Colisão com a bala
                collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y, 27)
                if collision:
                    bullet_y = player_y
                    bullet_state = "ready"
                    score_value += 1
                    enemy_x[i] = random.randint(0, screen_width - enemy_width)
                    enemy_y[i] = random.randint(50, 150)

                # Reiniciar inimigos que passam do final da tela
                if enemy_y[i] > screen_height:
                    enemy_x[i] = random.randint(0, screen_width - enemy_width)
                    enemy_y[i] = random.randint(50, 150)

                enemy(enemy_x[i], enemy_y[i])

            # Movimento da bala
            if bullet_state == "fire":
                bullet_x += bullet_dx
                bullet_y += bullet_dy
                screen.blit(bullet_img, (bullet_x, bullet_y))
            if bullet_y <= 0:
                bullet_y = player_y
                bullet_state = "ready"

            player(player_x, player_y)
            show_score(text_x, text_y)
            show_high_score(text_x, text_y)
        else:
            show_game_over()
    else:
        show_pause()

    pygame.display.update()

print("Saindo do jogo...")
pygame.quit()
