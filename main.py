import pygame
import random
from entities.Space_Ship import Space_Ship  # Classe Space_Ship
from entities.Enemy_Ship import Enemy_Ship  # Classe Enemy_Ship
from entities.Missile import Missile  # Classe Missile

# Caminho para as imagens
path_images = './assets/images'
# Variável para controlar o aumento da velocidade dos inimigos
enemy_speed_factor = 3.0

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

# Configuração da janela
window = pygame.display.set_mode([960, 540])
pygame.display.set_caption('First Game')

# Carregar imagens
background_image = pygame.image.load(f'{path_images}/space bg game.png')
player_ship_image = pygame.image.load(f'{path_images}/sprite_nave_pequena.png')
enemy_ship_image = pygame.image.load(f'{path_images}/naveROxa.webp')
missile_image = pygame.image.load(f'{path_images}/missile.png')  # Caminho correto da imagem do míssil

# Fonte para a mensagem de derrota
font = pygame.font.Font(None, 74)

# Variáveis do fundo
background_y = 0
background_speed = 2  # Velocidade de movimento do fundo

# Instância da nave do jogador
player_ship = Space_Ship(player_ship_image, 420, 400, 10)

# Lista para armazenar inimigos e mísseis
enemies = []
missiles = []
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

# Função para desenhar a mensagem de derrota
def draw_game_over():
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    window.blit(game_over_text, (300, 200))

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

    # Movimentação e atualização dos mísseis
    for missile in missiles[:]:
        missile.move()
        if missile.is_off_screen(540):
            missiles.remove(missile)  # Remove mísseis que saíram da tela

    # Gerar nova onda de inimigos se a lista estiver vazia
    if not enemies:
        enemies = generate_wave(enemy_ship_image, enemy_count, min_spacing=2, width=50, height=50, speed_factor=enemy_speed_factor)
        wave_number += 1
        enemy_speed_factor +=1
        enemy_count += 2  # Aumenta o número de inimigos por onda




    # Movimentação e atualização dos inimigos
    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemies.remove(enemy)  # Remove inimigos que saíram da tela

    # Verificar colisões entre mísseis e inimigos
    for missile in missiles[:]:
        missile_rect = missile.get_rect()
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x_position, enemy.y_position, enemy.width, enemy.height)
            if missile_rect.colliderect(enemy_rect):  # Colisão detectada
                missiles.remove(missile)  # Remove o míssil
                enemies.remove(enemy)  # Remove o inimigo
                enemies_destroyed += 1  # Incrementa o contador de inimigos destruídos
                break  # Interrompe o loop para evitar erros de iteração

    # Verificar colisão entre a nave do jogador e os inimigos
    player_rect = pygame.Rect(player_ship.x_position, player_ship.y_position, player_ship.image.get_width(), player_ship.image.get_height())
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy.x_position, enemy.y_position, enemy.width, enemy.height)
        if player_rect.colliderect(enemy_rect):  # Colisão detectada
            game_over = True
            break


    # A cada 10 inimigos destruídos, duplica a quantidade de inimigos na próxima onda
    if enemies_destroyed >= 10:
        enemy_count *= 2  # Duplica o número de inimigos
        enemies_destroyed = 0  # Reseta o contador

    # Desenho dos elementos na tela
    window.blit(background_image, (0, background_y))            # Fundo principal
    window.blit(background_image, (0, background_y - 540))      # Fundo secundário para loop
    player_ship.draw(window)                                    # Nave do jogador
    for missile in missiles:                                    # Desenhar os mísseis
        missile.draw(window)
    for enemy in enemies:                                       # Desenhar os inimigos
        enemy.draw(window)

    # Atualizar a tela
    pygame.display.update()
    clock.tick(165)  # Limitar a 60 FPS

pygame.quit()
