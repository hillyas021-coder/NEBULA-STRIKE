import pygame
import settings
from player import Player
print("screen Width:",settings.SCREEN_WIDTH)
import random
import math
import sys

pygame.init()

# WINDOW
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# COLORS
WHITE = (240, 245, 255)
CYAN = (0, 220, 255)
RED = (255, 65, 90)
GREEN = (60, 255, 160)
PURPLE = (150, 80, 255)
DARK = (5, 8, 25)
GREY = (45, 55, 80)

# FONTS
font = pygame.font.SysFont("arial", 24, bold=True)
small_font = pygame.font.SysFont("arial", 17)
big_font = pygame.font.SysFont("arial", 54, bold=True)

# GAME STATES
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"

state = MENU

# BACKGROUND STARS
stars = []

for i in range(120):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

# PLAYER
player = Player()

# GAME VARIABLES
health = 100
score = 0
level = 1

bullets = []
enemies = []
particles = []

last_shot = 0
last_spawn = 0
spawn_delay = 900


def draw_text(text, selected_font, color, x, y):
    image = selected_font.render(str(text), True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)


def draw_background():
    screen.fill(DARK)

    for star in stars:
        star[1] += star[2]

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen,
            (100, 140, 200),
            (star[0], star[1]),
            star[2]
        )


def draw_player():

   def draw_player():
    pygame.draw.rect(
        screen,
        CYAN,
        player.rect,
        border_radius=6
    )
     # Spaceship
    points = [
        (x, y - 25),
        (x - 22, y + 20),
        (x, y + 10),
        (x + 22, y + 20)
    ]

    pygame.draw.polygon(screen, CYAN, points)
    pygame.draw.polygon(screen, WHITE, points, 2)
    pygame.draw.circle(screen, PURPLE, (x, y), 6)


def create_enemy():
    x = random.randint(35, WIDTH - 35)

    enemies.append({
        "rect": pygame.Rect(x - 18, -45, 36, 40),
        "speed": random.uniform(2, 3.5) + level * 0.25,
        "phase": random.uniform(0, 6.28)
    })


def draw_enemy(enemy):
    rect = enemy["rect"]
    x, y = rect.center

    points = [
        (x, y + 22),
        (x - 23, y - 17),
        (x, y - 8),
        (x + 23, y - 17)
    ]

    pygame.draw.polygon(screen, RED, points)
    pygame.draw.polygon(screen, WHITE, points, 2)
    pygame.draw.circle(screen, PURPLE, (x, y), 5)


def create_explosion(x, y):
    for i in range(12):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 5)

        particles.append({
            "x": float(x),
            "y": float(y),
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "life": 30
        })


def update_particles():
    for particle in particles[:]:
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]
        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(
                screen,
                RED,
                (int(particle["x"]), int(particle["y"])),
                3
            )


def draw_hud():
    draw_text("SCORE: " + str(score), font, WHITE, 100, 30)
    draw_text("LEVEL: " + str(level), font, CYAN, 100, 65)

    # Health background
    pygame.draw.rect(
        screen, GREY,
        (WIDTH - 220, 25, 180, 20)
    )

    # Health foreground
    health_width = int(180 * health / 100)

    pygame.draw.rect(
        screen,
        GREEN if health > 30 else RED,
        (WIDTH - 220, 25, health_width, 20)
    )

    draw_text("HEALTH", small_font, WHITE, WIDTH - 130, 65)


def reset_game():
    global health, score, level
    global last_shot, last_spawn, spawn_delay, state

    player.center = (WIDTH // 2, HEIGHT - 90)

    health = 100
    score = 0
    level = 1

    bullets.clear()
    enemies.clear()
    particles.clear()

    last_shot = 0
    last_spawn = 0
    spawn_delay = 900

    state = PLAYING


def game_loop():
    global state, score, health, level
    global last_shot, last_spawn, spawn_delay

    running = True

    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        draw_background()

        # EVENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif state == MENU and event.key == pygame.K_RETURN:
                    reset_game()

                elif state == PLAYING and event.key == pygame.K_p:
                    state = PAUSED

                elif state == PAUSED and event.key == pygame.K_p:
                    state = PLAYING

                elif state == GAME_OVER and event.key == pygame.K_r:
                    reset_game()

        keys = pygame.key.get_pressed()

        # PLAYING
        if state == PLAYING:

            # PLAYER MOVEMENT
            
            player.move(keys,screen)          
             # SHOOTING
            if keys[pygame.K_SPACE]:
                if current_time - last_shot > 250:

                    bullets.append(player.shoot())
                    last_shot = current_time

            # ENEMY SPAWNING
            if current_time - last_spawn > spawn_delay:
                create_enemy()
                last_spawn = current_time

            # BULLET MOVEMENT
            for bullet in bullets[:]:
                bullet.y -= 10

                if bullet.bottom < 0:
                    bullets.remove(bullet)

            # ENEMY MOVEMENT
            for enemy in enemies[:]:
                enemy["rect"].y += enemy["speed"]
                enemy["phase"] += 0.04

                enemy["rect"].x += int(
                    math.sin(enemy["phase"]) * 2
                )

                if enemy["rect"].top > HEIGHT:
                    enemies.remove(enemy)
                    health -= 10

                elif enemy["rect"].colliderect(player.rect):
                    create_explosion(*enemy["rect"].center)
                    enemies.remove(enemy)
                    health -= 20

            # COLLISION DETECTION
            for bullet in bullets[:]:

                for enemy in enemies[:]:

                    if bullet.colliderect(enemy["rect"]):

                        if bullet in bullets:
                            bullets.remove(bullet)

                        if enemy in enemies:
                            enemies.remove(enemy)

                        create_explosion(*enemy["rect"].center)
                        score += 10
                        break

            # LEVEL PROGRESSION
            level = 1 + score // 100
            spawn_delay = max(250, 900 - level * 60)

            if health <= 0:
                health = 0
                state = GAME_OVER

            # DRAW OBJECTS
            draw_player()
            draw_hud()

            for bullet in bullets:
                pygame.draw.rect(
                    screen, CYAN, bullet,
                    border_radius=3
                )

            for enemy in enemies:
                draw_enemy(enemy)

        # PARTICLES
        update_particles()

        # MAIN MENU
        if state == MENU:
            draw_text(
                "NEBULA STRIKE",
                big_font, CYAN,
                WIDTH // 2, 190
            )

            draw_text(
                "SPACE SHOOTER",
                font, WHITE,
                WIDTH // 2, 250
            )

            draw_text(
                "PRESS ENTER TO START",
                font, GREEN,
                WIDTH // 2, 340
            )

            draw_text(
                "WASD / ARROWS = MOVE",
                small_font, WHITE,
                WIDTH // 2, 405
            )

            draw_text(
                "SPACE = SHOOT | P = PAUSE",
                small_font, WHITE,
                WIDTH // 2, 435
            )

        # PAUSE SCREEN
        elif state == PAUSED:
            draw_text(
                "GAME PAUSED",
                big_font, CYAN,
                WIDTH // 2, 250
            )

            draw_text(
                "PRESS P TO RESUME",
                font, WHITE,
                WIDTH // 2, 330
            )

        # GAME OVER
        elif state == GAME_OVER:
            draw_text(
                "GAME OVER",
                big_font, RED,
                WIDTH // 2, 220
            )

            draw_text(
                "FINAL SCORE: " + str(score),
                font, WHITE,
                WIDTH // 2, 300
            )

            draw_text(
                "PRESS R TO RESTART",
                font, GREEN,
                WIDTH // 2, 365
            )

            draw_text(
                "PRESS ESC TO EXIT",
                small_font, WHITE,
                WIDTH // 2, 410
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()