import pygame
class Missile:
    def __init__(self, x, y, width, height, image, velocity):
        """
        Inicializa o míssil.

        :param x: Posição X inicial.
        :param y: Posição Y inicial.
        :param width: Largura do míssil.
        :param height: Altura do míssil.
        :param image: Imagem do míssil.
        :param velocity: Velocidade vertical do míssil (negativa para subir).
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))  # Redimensionar imagem
        self.velocity = velocity

    def move(self):
        """
        Move o míssil verticalmente para cima.
        """
        self.y += self.velocity

    def is_off_screen(self, screen_height):
        """
        Verifica se o míssil saiu da tela.

        :param screen_height: Altura da tela.
        :return: True se o míssil saiu da tela; False caso contrário.
        """
        return self.y + self.height < 0

    def draw(self, surface):
        """
        Desenha o míssil na tela.

        :param surface: Superfície onde o míssil será desenhado.
        """
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """
        Retorna o retângulo de colisão do míssil.

        :return: pygame.Rect representando o míssil.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
