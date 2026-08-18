import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini RPG Adventure")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player
player = pygame.Rect(50, 50, 40, 40)
player_speed = 5
lives = 3
score = 0
has_key = False

# Sword
attack_timer = 0

# Treasure
key_rect = pygame.Rect(700, 100, 20, 20)
door_rect = pygame.Rect(740, 500, 40, 60)

# Health Pack
health_pack = pygame.Rect(
    random.randint(50, 750),
    random.randint(50, 550),
    20,
    20
)

# Enemies
enemies = []

for i in range(5):
    enemies.append(
        pygame.Rect(
            random.randint(100, 700),
            random.randint(100, 500),
            35,
            35
        )
    )

running = True
game_state = "playing"

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                attack_timer = 15

    keys = pygame.key.get_pressed()

    if game_state == "playing":

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_UP]:
            player.y -= player_speed
        if keys[pygame.K_DOWN]:
            player.y += player_speed

        player.x = max(0, min(WIDTH - player.width, player.x))
        player.y = max(0, min(HEIGHT - player.height, player.y))

        # Enemy movement
        for enemy in enemies[:]:

            if enemy.x < player.x:
                enemy.x += 2
            elif enemy.x > player.x:
                enemy.x -= 2

            if enemy.y < player.y:
                enemy.y += 2
            elif enemy.y > player.y:
                enemy.y -= 2

            # Attack
            if attack_timer > 0:
                attack_box = pygame.Rect(
                    player.x - 20,
                    player.y - 20,
                    80,
                    80
                )

                if attack_box.colliderect(enemy):
                    enemies.remove(enemy)
                    score += 10

            # Damage
            if player.colliderect(enemy):
                lives -= 1
                player.x = 50
                player.y = 50

                if lives <= 0:
                    game_state = "lose"

        if attack_timer > 0:
            attack_timer -= 1

        # Collect key
        if player.colliderect(key_rect):
            has_key = True

        # Health pack
        if player.colliderect(health_pack):
            if lives < 3:
                lives += 1

            health_pack.x = -100

        # Win
        if has_key and player.colliderect(door_rect):
            game_state = "win"

    # Drawing
    screen.fill((20,20,30))

    # Door
    pygame.draw.rect(screen,(139,69,19),door_rect)

    # Key
    if not has_key:
        pygame.draw.rect(screen,(255,255,0),key_rect)

    # Health
    if health_pack.x > 0:
        pygame.draw.rect(screen,(0,255,0),health_pack)

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen,(255,0,0),enemy)

    # Player
    pygame.draw.rect(screen,(0,100,255),player)

    # Sword effect
    if attack_timer > 0:
        pygame.draw.circle(
            screen,
            (255,255,255),
            player.center,
            50,
            3
        )

    # HUD
    text = font.render(
        f"Lives: {lives}  Score: {score}",
        True,
        (255,255,255)
    )

    screen.blit(text,(10,10))

    if has_key:
        key_text = font.render(
            "Key Collected!",
            True,
            (255,255,0)
        )
        screen.blit(key_text,(10,50))

    if game_state == "win":
        win_text = font.render(
            "YOU ESCAPED THE DUNGEON!",
            True,
            (255,255,255)
        )
        screen.blit(win_text,(220,280))

    if game_state == "lose":
        lose_text = font.render(
            "GAME OVER",
            True,
            (255,255,255)
        )
        screen.blit(lose_text,(320,280))

    pygame.display.update()

pygame.quit()