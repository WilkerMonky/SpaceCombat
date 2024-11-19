import pygame
import random


class Missile:
    def __init__(self, x, y, width, height, image, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))  
        self.velocity = velocity

    def move(self):
        self.y += self.velocity

    def is_off_screen(self, screen_height):
        return self.y + self.height < 0

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Space_Ship:
    def __init__(self, image, x, y, velocity):
        self.image = pygame.transform.scale(image, (50, 50))
        self.x_position = x
        self.y_position = y
        self.velocity = velocity

    def move(self, teclas):
        if teclas[pygame.K_LEFT] and self.x_position > 0:
            self.x_position -= self.velocity
        if teclas[pygame.K_RIGHT] and self.x_position < 960 - self.image.get_width():
            self.x_position += self.velocity
        if teclas[pygame.K_UP] and self.y_position > 0:
            self.y_position -= self.velocity
        if teclas[pygame.K_DOWN] and self.y_position < 540 - self.image.get_height():
            self.y_position += self.velocity

    def draw(self, surface):
        surface.blit(self.image, (self.x_position, self.y_position))


class Enemy_Ship:
    def __init__(self, image, x_position, y_position, velocity, width, height):
        self.image = pygame.transform.scale(image, (width, height))
        self.x_position = x_position
        self.y_position = y_position
        self.velocity = velocity
        self.width = width
        self.height = height

    def move(self):
        self.y_position += self.velocity

    def is_off_screen(self):
        return self.y_position > 540

    def draw(self, surface):
        surface.blit(self.image, (self.x_position, self.y_position))


def generate_wave(enemy_image, number_of_enemies, min_spacing, width, height):
    enemies = []

    for _ in range(number_of_enemies):
        while True:
            x_position = random.randint(0, 960 - width)
            y_position = random.randint(-200, -50)  
            velocity = random.randint(2, 5)

            too_close = any(
                abs(x_position - enemy.x_position) < min_spacing
                and abs(y_position - enemy.y_position) < min_spacing
                for enemy in enemies
            )
            
            if not too_close:
                enemies.append(Enemy_Ship(enemy_image, x_position, y_position, velocity, width, height))
                break

    return enemies
