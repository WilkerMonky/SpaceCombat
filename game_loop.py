import pygame
from game_objects import Space_Ship, Enemy_Ship, Missile, generate_wave
from game_utils import handle_missiles, update_background, check_collisions

def game_loop():
    pygame.init()

    path_images = './assets/images'

    # Configuração da janela
    window = pygame.display.set_mode([960, 540])
    pygame.display.set_caption('First Game')

    # Carregar imagens
    background_image = pygame.image.load(f'{path_images}/space bg game.png')
    player_ship_image = pygame.image.load(f'{path_images}/sprite_nave_pequena.png')
    enemy_ship_image = pygame.image.load(f'{path_images}/naveROxa.webp')
    missile_image = pygame.image.load(f'{path_images}/missile.png')

    # Variáveis do fundo
    background_y = 0
    background_speed = 2

    # Instância da nave do jogador
    player_ship = Space_Ship(player_ship_image, 420, 400, 10)

    # Lista para armazenar inimigos e mísseis
    enemies = []
    missiles = []
    wave_number = 1
    enemy_count = 5

    # Cooldown de disparo
    last_shot_time = 0
    missile_cooldown = 500  

    # Variáveis para o loop
    loop = True
    clock = pygame.time.Clock()

    while loop:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                loop = False

        teclas = pygame.key.get_pressed()

        # Movimentação da nave do jogador
        player_ship.move(teclas)

        # Disparar um míssil
        missiles, last_shot_time = handle_missiles(missiles, player_ship, missile_image, missile_cooldown, last_shot_time)

        # Atualizar a posição do fundo
        background_y = update_background(background_y, background_speed)

        # Gerar nova onda de inimigos
        if not enemies:
            enemies = generate_wave(enemy_ship_image, enemy_count, min_spacing=2, width=50, height=50)
            wave_number += 1
            enemy_count += 2

        # Movimentação e atualização dos inimigos
        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen():
                enemies.remove(enemy)

        # Verificar colisões
        enemies = check_collisions(missiles, enemies)

        # Desenho dos elementos na tela
        window.blit(background_image, (0, background_y))
        window.blit(background_image, (0, background_y - 540))
        player_ship.draw(window)
        for missile in missiles:
            missile.draw(window)
        for enemy in enemies:
            enemy.draw(window)

        # Atualizar a tela
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
