import pygame
import settings


class Player:

    def __init__(self):
        # Player position and size
        self.rect = pygame.Rect(
            settings.SCREEN_WIDTH // 2 - 20,
            settings.SCREEN_HEIGHT - 90,
            40,
            45
        )

        # Player properties
        self.speed = 6
        self.health = 100

    # Player movement
    def move(self, keys, screen):

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep player inside the screen
        self.rect.clamp_ip(screen.get_rect())

    # Player shooting
    def shoot(self):

        bullet = pygame.Rect(
            self.rect.centerx - 3,
            self.rect.top - 12,
            6,
            18
        )

        return bullet