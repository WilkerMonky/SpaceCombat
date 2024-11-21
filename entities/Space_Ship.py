import pygame

class Space_Ship:
    def __init__(self, image, x_position, y_position, velocity):
        self.image = image
        self.x_position = x_position
        self.y_position = y_position
        self.velocity = velocity

    def move(self, keys):
        # Movimentação vertical
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_position -= self.velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_position += self.velocity

        # Movimentação horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_position += self.velocity
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_position -= self.velocity

        # Limitar movimento na janela
        self.y_position = max(-10, min(self.y_position, 440))
        self.x_position = max(-10, min(self.x_position, 860))

    def draw(self, surface):
        surface.blit(self.image, (self.x_position, self.y_position))