import pygame
import random
from entities.Space_Ship import Space_Ship  # Classe Space_Ship
from entities.Enemy_Ship import Enemy_Ship  # Classe Enemy_Ship
from entities.Missile import Missile  # Classe Missile

# Caminho para as imagens
path_images = './assets/images'
# Caminho para a música de fundo
path_music = './assets/sound_track'

# Variável para controlar o aumento da velocidade dos inimigos
enemy_speed_factor = 2.0

# Função para gerar a onda de inimigos
def generate_wave(enemy_image, number_of_enemies, min_spacing, width, height, speed_factor):
    """
    Gera uma onda de inimigos com espaçamento mínimo entre as naves.
    """
    enemies = []

    for _ in range(number_of_enemies):
        while True:
            x_position = random.randint(0, 960 - width)
            y_position = random.randint(-200, -50)  # Aparece fora da tela
            velocity = random.randint(2, 5) * speed_factor  # Aumentar velocidade com o fator

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
background_image = pygame.image.load(f'{path_images}/space bg game.png')
player_ship_image = pygame.image.load(f'{path_images}/sprite_nave_pequena.png')
enemy_ship_image = pygame.image.load(f'{path_images}/naveROxa.webp')
missile_image = pygame.image.load(f'{path_images}/missile.png')  # Caminho correto da imagem do míssil

# Fonte para a mensagem de derrota e pontuação
font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)  # Fonte para a pontuação

# Variáveis do fundo
background_y = 0
background_speed = 2  # Velocidade de movimento do fundo

# Instância da nave do jogador
player_ship = Space_Ship(player_ship_image, 420, 400, 10)

# Lista para armazenar inimigos, mísseis da nave principal e mísseis inimigos
enemies = []
missiles = []
enemy_missiles = []

wave_number = 1
enemy_count = 5
enemies_destroyed = 0  # Contador de inimigos destruídos

# Cooldown de disparo
last_shot_time = 0  # Tempo do último disparo (em milissegundos)
missile_cooldown = 500  # Cooldown em milissegundos (1 segundo)

# Variáveis para o loop
loop = True
clock = pygame.time.Clock()  # Para limitar os FPS
game_over = False

# Inicializa a pontuação
start_time = pygame.time.get_ticks()  # Marca o tempo de início do jogo
score = 0  # Pontuação inicial

# Função para desenhar a mensagem de derrota
def draw_game_over():
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    window.blit(game_over_text, (300, 200))

# Função para desenhar a pontuação
def draw_score(score):
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))  # Desenha no canto superior esquerdo

while loop:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False

    teclas = pygame.key.get_pressed()

    if game_over:
        draw_game_over()
        pygame.display.update()
        continue  # Não continua o loop de jogo após a derrota

    # Movimentação da nave do jogador
    player_ship.move(teclas)

    # Disparar um míssil ao pressionar espaço, respeitando o cooldown
    current_time = pygame.time.get_ticks()
    if teclas[pygame.K_SPACE] and current_time - last_shot_time >= missile_cooldown:
        missile = Missile(
            x=player_ship.x_position + player_ship.image.get_width() // 2 - 5,
            y=player_ship.y_position,
            width=10,
            height=20,
            image=missile_image,
            velocity=-5  # Velocidade para cima
        )
        missiles.append(missile)
        last_shot_time = current_time  # Atualiza o tempo do último disparo

    # Atualizar a posição do fundo
    background_y += background_speed
    if background_y >= 540:  # Reiniciar o fundo quando ele sair da tela
        background_y = 0

    # Movimentação e atualização dos mísseis da nave principal
    for missile in missiles[:]:
        missile.move()
        if missile.is_off_screen(540):
            missiles.remove(missile)  # Remove mísseis que saíram da tela

    # Gerar nova onda de inimigos se a lista estiver vazia
    if not enemies:
        enemies = generate_wave(enemy_ship_image, enemy_count, min_spacing=2, width=50, height=50, speed_factor=enemy_speed_factor)
        wave_number += 1
        enemy_speed_factor += 0.2   
        enemy_count += 2  # Aumenta o número de inimigos por onda

    # Movimentação e atualização dos inimigos
    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemies.remove(enemy)  # Remove inimigos que saíram da tela

        # Disparar mísseis dos inimigos
        enemy_missile = enemy.fire(current_time, missile_image)
        if enemy_missile:
            enemy_missiles.append(enemy_missile)

    # Movimentação e atualização dos mísseis dos inimigos
    for enemy_missile in enemy_missiles[:]:
        enemy_missile.move()
        if enemy_missile.is_off_screen(540):
            enemy_missiles.remove(enemy_missile)  # Remove mísseis que saíram da tela

    # Verificar colisões entre mísseis da nave principal e os inimigos
    for missile in missiles[:]:
        missile_rect = missile.get_rect()
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x_position, enemy.y_position, enemy.width, enemy.height)
            if missile_rect.colliderect(enemy_rect):  # Colisão detectada
                missiles.remove(missile)  # Remove o míssil
                enemies.remove(enemy)  # Remove o inimigo
                enemies_destroyed += 1  # Incrementa o contador de inimigos destruídos
                break  # Interrompe o loop para evitar erros de iteração

    # Verificar colisões entre mísseis dos inimigos e a nave do jogador
    player_rect = pygame.Rect(player_ship.x_position, player_ship.y_position, player_ship.image.get_width(), player_ship.image.get_height())
    for enemy_missile in enemy_missiles[:]:
        enemy_missile_rect = pygame.Rect(enemy_missile.x, enemy_missile.y, enemy_missile.width, enemy_missile.height)
        if player_rect.colliderect(enemy_missile_rect):  # Colisão detectada
            game_over = True
            pygame.mixer.music.set_volume(0.0) 
            game_over_sound.play()  # Toca o som de derrota
            break

    # Atualizar a pontuação (baseada no tempo de jogo)
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Tempo em segundos
        score = elapsed_time  # A pontuação é igual ao tempo de vida em segundos

    # A cada 10 inimigos destruídos, duplica a quantidade de inimigos na próxima onda
    if enemies_destroyed >= 10:
        enemy_count *= 2  # Duplica o número de inimigos
        enemies_destroyed = 0  # Reseta o contador

    # Desenho dos elementos na tela
    window.blit(background_image, (0, background_y))            # Fundo principal
    window.blit(background_image, (0, background_y - 540))      # Fundo secundário para loop
    player_ship.draw(window)                                    # Nave do jogador
    for missile in missiles:                                    # Desenhar os mísseis da nave principal
        missile.draw(window)
    for enemy in enemies:                                       # Desenhar os inimigos
        enemy.draw(window)
    for enemy_missile in enemy_missiles:                        # Desenhar os mísseis inimigos
        enemy_missile.draw(window)

    # Desenhar a pontuação na tela
    draw_score(score)

    # Atualizar a tela
    pygame.display.update()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
