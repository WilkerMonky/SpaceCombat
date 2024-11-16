import pygame
import random
from entities.Space_Ship import Space_Ship  # Classe Space_Ship
from entities.Enemy_Ship import Enemy_Ship  # Classe Enemy_Ship


class Missile:
    def __init__(self, x, y, width, height, image, velocity):
        """
        Inicializa o míssil.

        :param x: Posição X inicial.
        :param y: Posição Y inicial.
        :param width: Largura do míssil.
        :param height: Altura do míssil.
        :param image: Imagem do míssil.
        :param velocity: Velocidade vertical do míssil.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))  # Redimensionar imagem
        self.velocity = velocity

    def move(self):
        """Move o míssil verticalmente para cima."""
        self.y += self.velocity

    def is_off_screen(self, screen_height):
        """Verifica se o míssil saiu da tela."""
        return self.y + self.height < 0

    def draw(self, surface):
        """Desenha o míssil na tela."""
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Retorna o retângulo de colisão do míssil."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


# Caminho para as imagens
path_images = './assets/images'

def generate_wave(enemy_image, number_of_enemies, min_spacing, width, height):
    """
    Gera uma onda de inimigos com espaçamento mínimo entre as naves.
    """
    enemies = []

    for _ in range(number_of_enemies):
        while True:
            x_position = random.randint(0, 960 - width)
            y_position = random.randint(-200, -50)  # Aparece fora da tela
            velocity = random.randint(2, 5)

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

# Cooldown de disparo
last_shot_time = 0  # Tempo do último disparo (em milissegundos)
missile_cooldown = 500  # Cooldown em milissegundos (1 segundo)

# Variáveis para o loop
loop = True
clock = pygame.time.Clock()  # Para limitar os FPS

while loop:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False

    teclas = pygame.key.get_pressed()

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
        enemies = generate_wave(enemy_ship_image, enemy_count, min_spacing=2, width=50, height=50)
        wave_number += 1
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
                break  # Interrompe o loop para evitar erros de iteração

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
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
