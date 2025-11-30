import pygame
import sys
import random
import time

pygame.init()

WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitarian")

player_image = pygame.image.load("Game/Moon.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (35, 35))
player_rect = player_image.get_rect()
player_rect.topleft = (320, 200)

def create_enemy():
    """Returns a dictionary with an image, rect, and alpha for fade-in."""
    img = pygame.image.load("Game/Death.png").convert_alpha()
    img = pygame.transform.scale(img, (50, 50))
    rect = img.get_rect()
    rect.topleft = (random.randint(0, WIDTH - 50),
                    random.randint(0, HEIGHT - 50))
    return {"image": img, "rect": rect, "alpha": 0}

enemies = [create_enemy() for _ in range(5)]

fade_speed = 3

direction = "D"
vel_x = 0
vel_y = 0
gravity_speed = 10

angle = 0
target_angle = 0
rotation_step = 9

last_change_time = time.time()

def reset_enemies():
    """Teleport all enemies, reset alpha, reduce player speed."""
    global gravity_speed
    for e in enemies:
        e["rect"].topleft = (random.randint(0, WIDTH - 50),
                             random.randint(0, HEIGHT - 50))
        e["alpha"] = 0
        e["image"].set_alpha(0)

    # Reduce speed gradually
    gravity_speed = max(2, gravity_speed - 1)

clock = pygame.time.Clock()


while True:
    now = time.time()


    if now - last_change_time >= 5:
        reset_enemies()
        last_change_time = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Change direction clockwise
                if direction == "D":
                    direction = "L"
                elif direction == "L":
                    direction = "U"
                elif direction == "U":
                    direction = "R"
                elif direction == "R":
                    direction = "D"
                target_angle += 90

    if angle < target_angle:
        angle += rotation_step
        if angle > target_angle:
            angle = target_angle
    elif angle > target_angle:
        angle -= rotation_step
        if angle < target_angle:
            angle = target_angle

    for e in enemies:
        if e["alpha"] < 255:
            e["alpha"] += fade_speed
            e["image"].set_alpha(min(e["alpha"], 255))

    vel_x = vel_y = 0
    if direction == "D" and player_rect.bottom < HEIGHT:
        vel_y = gravity_speed
    elif direction == "U" and player_rect.top > 0:
        vel_y = -gravity_speed
    elif direction == "L" and player_rect.left > 0:
        vel_x = -gravity_speed
    elif direction == "R" and player_rect.right < WIDTH:
        vel_x = gravity_speed

    player_rect.x += vel_x
    player_rect.y += vel_y

    for e in enemies:
        if e["alpha"] == 255 and player_rect.colliderect(e["rect"]):
            pygame.quit()
            exit()

    rotated_image = pygame.transform.rotate(player_image, angle)
    rotated_rect = rotated_image.get_rect(center=player_rect.center)

    screen.fill((0, 0, 17))

    for e in enemies:
        screen.blit(e["image"], e["rect"])

    screen.blit(rotated_image, rotated_rect)

    pygame.display.update()
    clock.tick(60)
