import pygame
import random
from entities.Space_Ship import Space_Ship
from entities.Missile import Missile
class Enemy_Ship(Space_Ship):
    def __init__(self, image, x_position, y_position, velocity, width, height, fire_rate=1000):
        """
        Inicializa a nave inimiga.
        
        :param image: Imagem da nave inimiga.
        :param x_position: Posição X inicial.
        :param y_position: Posição Y inicial.
        :param velocity: Velocidade de movimento.
        :param width: Largura da nave inimiga.
        :param height: Altura da nave inimiga.
        :param fire_rate: Tempo em milissegundos para o disparo dos mísseis (default 1000ms).
        """
        self.original_image = pygame.transform.rotate(
            pygame.transform.scale(image, (width, height)), 180
        )
        self.image = self.original_image
        super().__init__(self.image, x_position, y_position, velocity)
        self.direction = random.choice([-1, 1])  # Direção inicial (esquerda ou direita)
        self.width = width
        self.height = height
        self.last_shot_time = 0  # Controle de tempo para disparar
        self.fire_rate = fire_rate  # A cada quanto tempo a nave dispara um míssil
    
    def move(self):
        # Movimentação horizontal (zigue-zague)
        self.x_position += self.velocity * self.direction

        # Alterar direção ao bater na borda
        if self.x_position <= 0 or self.x_position >= 960 - self.width:
            self.direction *= -1
            self.y_position += 20  # Desce ao atingir a borda

    def fire(self, current_time, missile_image):
        """
        Dispara um míssil da nave inimiga.

        :param current_time: Tempo atual para verificar o intervalo de disparo.
        :param missile_image: Imagem do míssil.
        :return: Míssil disparado ou None.
        """
        if current_time - self.last_shot_time >= self.fire_rate:
            self.last_shot_time = current_time
            return Missile(
                x=self.x_position + self.width // 2 - 5,
                y=self.y_position + self.height,  # Dispara da parte inferior da nave
                width=10,
                height=20,
                image=missile_image,
                velocity=5  # Míssil vai para baixo
            )
        return None
    
    def is_off_screen(self):
        # Verificar se a nave inimiga está abaixo da tela
        return self.y_position > 540
