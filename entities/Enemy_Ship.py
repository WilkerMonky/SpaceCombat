import pygame
import random
from entities.Space_Ship import Space_Ship


class Enemy_Ship(Space_Ship):
    def __init__(self, image, x_position, y_position, velocity, width, height):
        """
        Inicializa a nave inimiga.
        
        :param image: Imagem da nave inimiga.
        :param x_position: Posição X inicial.
        :param y_position: Posição Y inicial.
        :param velocity: Velocidade de movimento.
        :param width: Largura da nave inimiga.
        :param height: Altura da nave inimiga.
        """
        # Redimensionar e girar a imagem para corrigir a orientação
        self.original_image = pygame.transform.rotate(
            pygame.transform.scale(image, (width, height)), 180
        )
        self.image = self.original_image
        super().__init__(self.image, x_position, y_position, velocity)
        self.direction = random.choice([-1, 1])  # Direção inicial (esquerda ou direita)
        self.width = width
        self.height = height

    def move(self):
        # Movimentação horizontal (zigue-zague)
        self.x_position += self.velocity * self.direction

        # Alterar direção ao bater na borda
        if self.x_position <= 0 or self.x_position >= 960 - self.width:
            self.direction *= -1
            self.y_position += 20  # Desce ao atingir a borda

    def is_off_screen(self):
        # Verifica se o inimigo saiu da tela (parte inferior)
        return self.y_position > 540
