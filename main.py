import pygame
import random
from entities.Space_Ship import Space_Ship  # Classe Space_Ship
from entities.Enemy_Ship import Enemy_Ship  # Classe Enemy_Ship
from entities.Missile import Missile  # Classe Missile

# Caminho para as imagens
path_images = './assets/images'
# Caminho para a música de fundo
path_music = './assets/sound_track'

# Caminho para o arquivo de recorde
record_file = 'record.txt'

# Variável para controlar o aumento da velocidade dos inimigos
enemy_speed_factor = 2.0

# Função para gerar a onda de inimigos
def generate_wave(enemy_images, number_of_enemies, min_spacing, width, height, speed_factor):
    enemies = []
    for _ in range(number_of_enemies):
        while True:
            x_position = random.randint(0, 960 - width)
            y_position = random.randint(-200, -50)  # Aparece fora da tela
            velocity = random.randint(2, 5) * speed_factor  # Aumentar velocidade com o fator

            # Escolhe uma imagem aleatória para o inimigo
            enemy_image = random.choice(enemy_images)

            # Verificar espaçamento mínimo com outras naves
            too_close = any(
                abs(x_position - enemy.x_position) < min_spacing
                and abs(y_position - enemy.y_position) < min_spacing
                for enemy in enemies
            )
            if not too_close:
                enemies.append(Enemy_Ship(enemy_image, x_position, y_position, velocity, width, height))
                break
    return enemies


# Função para carregar o recorde do arquivo
def load_record():
    try:
        with open(record_file, 'r') as file:
            lines = file.readlines()
            record = int(lines[0].strip())
            record_kills = int(lines[1].strip())
    except (FileNotFoundError, ValueError, IndexError):
        record, record_kills = 0, 0  # Se o arquivo não existir ou houver erro, define os valores como 0
    return record, record_kills

# Função para salvar o recorde no arquivo
def save_record(record, record_kills):
    with open(record_file, 'w') as file:
        file.write(f"{record}\n{record_kills}")

# Inicializa o pygame
pygame.init()
pygame.mixer.init()  # Inicializa o mixer para som

# Carregar e tocar a música de fundo
pygame.mixer.music.load(f'{path_music}/02 Las Vegas.mp3')  # Carrega o arquivo de música
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1, start=0.0)  # Toca a música em loop (-1 significa loop infinito)

# Configuração da janela
window = pygame.display.set_mode([960, 540])
pygame.display.set_caption('First Game')

# Carregar imagens
# Carregar o som de derrota
game_over_sound = pygame.mixer.Sound(f'{path_music}/fail.mp3')  # Caminho do arquivo de som
game_over_sound.set_volume(0.1)  # Diminui o volume do som de game over

background_image = pygame.image.load(f'{path_images}/space bg game.png')
player_ship_image = pygame.image.load(f'{path_images}/sprite_nave_pequena.png')
enemy_ship_image = pygame.image.load(f'{path_images}/naveROxa.webp')
enemy_ship_image2 = pygame.image.load(f'{path_images}/nave1.png')
enemy_ship_image3 = pygame.image.load(f'{path_images}/nave2.png')
enemy_ship_image4 = pygame.image.load(f'{path_images}/nave3.png')
enemy_ship_image5 = pygame.image.load(f'{path_images}/nave4.png')
enemy_ship_image6 = pygame.image.load(f'{path_images}/nave5.png')
enemy_ship_image7 = pygame.image.load(f'{path_images}/nave6.png')
enemy_ship_image8 = pygame.image.load(f'{path_images}/nave7.png')
enemy_ship_image9 = pygame.image.load(f'{path_images}/nave8.png')
enemy_ship_images = [enemy_ship_image, enemy_ship_image2, enemy_ship_image3, enemy_ship_image4, enemy_ship_image5, enemy_ship_image6, enemy_ship_image7, enemy_ship_image8, enemy_ship_image9]
missile_image = pygame.image.load(f'{path_images}/missile.png')

# Fonte para a mensagem de derrota e pontuação
font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 20)
record_font = pygame.font.Font(None, 20)

# Variáveis do fundo
background_y = 0
background_speed = 2

# Instância da nave do jogador
player_ship = Space_Ship(player_ship_image, 420, 400, 10)

# Listas para armazenar inimigos, mísseis da nave principal e mísseis inimigos
enemies = []
missiles = []
enemy_missiles = []

wave_number = 1
enemy_count = 5
enemies_destroyed = 0
kills = 0  # Contador de kills

# Cooldown de disparo
last_shot_time = 0
missile_cooldown = 500

# Variáveis para o loop
loop = True
clock = pygame.time.Clock()
game_over = False

# Inicializa a pontuação, tempo e recordes
start_time = pygame.time.get_ticks()
score = 0
record, record_kills = load_record()

# Funções para desenhar mensagens e pontuações
def draw_game_over():
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    window.blit(game_over_text, (300, 200))

def draw_score(score):
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

def draw_record(record):
    record_text = record_font.render(f"Record: {record}", True, (255, 255, 255))
    window.blit(record_text, (10, 50))

def draw_kills(kills):
    kills_text = score_font.render(f"Kills: {kills}", True, (255, 255, 255))
    window.blit(kills_text, (10, 90))

def draw_record_kills(record_kills):
    record_kills_text = record_font.render(f"Record Kills: {record_kills}", True, (255, 255, 255))
    window.blit(record_kills_text, (10, 130))

def draw_restart_button():
    # Definir o tamanho e posição do botão
    button_width, button_height = 200, 50
    button_x, button_y = (960 - button_width) // 2, 300

    # Desenhar o botão
    pygame.draw.rect(window, (0, 128, 255), (button_x, button_y, button_width, button_height))
    button_text = font.render("Restart", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    window.blit(button_text, text_rect)

    return pygame.Rect(button_x, button_y, button_width, button_height)

# Cooldown inicial de disparo
missile_cooldown = 500  # Tempo inicial em milissegundos

# Variável para controlar se o som de Game Over foi tocado
game_over_sound_played = False

# Função para desenhar o botão de restart
def draw_restart_button():
    button_text = font.render("RESTART", True, (255, 0, 0))
    text_width, text_height = button_text.get_size()
    button_x = (840 - text_width) // 2
    button_y = 300  # Posiciona abaixo da mensagem "GAME OVER"
    window.blit(button_text, (button_x, button_y))
    return pygame.Rect(button_x, button_y, text_width, text_height)

# Função para reiniciar o jogo
def restart_game():
    global player_ship, enemies, missiles, enemy_missiles
    global wave_number, enemy_count, enemies_destroyed, kills
    global last_shot_time, game_over, start_time, score, record, record_kills, enemy_speed_factor
    global game_over_sound_played

    # Reinicializar todas as variáveis do jogo
    player_ship = Space_Ship(player_ship_image, 420, 400, 10)
    enemies = []
    missiles = []
    enemy_missiles = []
    wave_number = 1
    enemy_count = 5
    enemies_destroyed = 0
    kills = 0
    last_shot_time = 0
    game_over = False
    start_time = pygame.time.get_ticks()
    score = 0
    enemy_speed_factor = 2.0

    # Reiniciar a música de fundo
    pygame.mixer.music.play(loops=-1, start=0.0)
    game_over_sound_played = False  # Resetar controle do som de Game Over

# Loop principal do jogo
while loop:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False
        if events.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_pos):
                restart_game()

    teclas = pygame.key.get_pressed()

    if game_over:
        # Desenhar a tela de Game Over
        draw_game_over()
        draw_score(score)
        draw_record(record)
        draw_kills(kills)
        draw_record_kills(record_kills)

        # Desenhar o botão de restart
        restart_button = draw_restart_button()

        # Tocar o som de Game Over apenas uma vez
        if not game_over_sound_played:
            pygame.mixer.music.stop()  # Parar música de fundo
            game_over_sound.play()
            game_over_sound_played = True  # Marcar que o som já foi tocado

        pygame.display.update()
        continue

    # Ajustar o cooldown de disparo baseado na onda
    missile_cooldown = max(100, 500 - (wave_number * 20))  # Reduz 20ms por onda, mínimo de 100ms

    player_ship.move(teclas)

    current_time = pygame.time.get_ticks()
    if teclas[pygame.K_SPACE] and current_time - last_shot_time >= missile_cooldown:
        missile = Missile(
            x=player_ship.x_position + player_ship.image.get_width() // 2 - 5,
            y=player_ship.y_position,
            width=10,
            height=20,
            image=missile_image,
            velocity=-5
        )
        missiles.append(missile)
        last_shot_time = current_time

    background_y += background_speed
    if background_y >= 540:
        background_y = 0

    for missile in missiles[:]:
        missile.move()
        if missile.is_off_screen(540):
            missiles.remove(missile)

        if not enemies:
            enemies = generate_wave(
                enemy_ship_images,  # Lista de imagens de naves inimigas
                enemy_count, 
                min_spacing=2, 
                width=50, 
                height=50, 
                speed_factor=enemy_speed_factor
            )
            wave_number += 1
            enemy_speed_factor += 0.1
            enemy_count += 2

    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemies.remove(enemy)

        enemy_missile = enemy.fire(current_time, missile_image)
        if enemy_missile:
            enemy_missiles.append(enemy_missile)

    for enemy_missile in enemy_missiles[:]:
        enemy_missile.move()
        if enemy_missile.is_off_screen(540):
            enemy_missiles.remove(enemy_missile)

    for missile in missiles[:]:
        missile_rect = missile.get_rect()
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x_position, enemy.y_position, enemy.width, enemy.height)
            if missile_rect.colliderect(enemy_rect):
                missiles.remove(missile)
                enemies.remove(enemy)
                enemies_destroyed += 1
                kills += 1
                if kills > record_kills:
                    record_kills = kills
                    save_record(record, record_kills)
                break

    player_rect = pygame.Rect(player_ship.x_position, player_ship.y_position, player_ship.image.get_width(), player_ship.image.get_height())
    for enemy_missile in enemy_missiles[:]:
        enemy_missile_rect = pygame.Rect(enemy_missile.x, enemy_missile.y, enemy_missile.width, enemy_missile.height)
        if player_rect.colliderect(enemy_missile_rect):
            game_over = True
            break

    if enemies_destroyed >= 20:
        enemy_count *= 2
        enemies_destroyed = 0

    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        score = elapsed_time

    if game_over and score > record:
        record = score
        save_record(record, record_kills)

    window.blit(background_image, (0, background_y))
    window.blit(background_image, (0, background_y - 540))
    player_ship.draw(window)
    for missile in missiles:
        missile.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    for enemy_missile in enemy_missiles:
        enemy_missile.draw(window)

    draw_score(score)
    draw_record(record)
    draw_kills(kills)
    draw_record_kills(record_kills)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
