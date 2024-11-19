import pygame
from time import time as timer

def handle_missiles(missiles, player_ship, missile_image, missile_cooldown, last_shot_time):
    current_time = pygame.time.get_ticks()
    if pygame.key.get_pressed()[pygame.K_SPACE] and current_time - last_shot_time >= missile_cooldown:
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

    for missile in missiles[:]:
        missile.move()
        if missile.is_off_screen(540):
            missiles.remove(missile)

    return missiles, last_shot_time


def update_background(background_y, background_speed):
    background_y += background_speed
    if background_y >= 540:
        background_y = 0
    return background_y


def check_collisions(missiles, enemies):
    for missile in missiles[:]:
        missile_rect = missile.get_rect()
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x_position, enemy.y_position, enemy.width, enemy.height)
            if missile_rect.colliderect(enemy_rect):
                missiles.remove(missile)  
                enemies.remove(enemy)
                break  # Evita erros de iteração
    return enemies
