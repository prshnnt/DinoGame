import pygame as pg
from settings import *
from entities.platform import Platform


class Bullet:
    """Basic bullet that travels horizontally."""

    def __init__(self, x, y, vx):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = 0

        self.width = 10
        self.height = 10
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.alive = True
        self.damage = 10

        # Create a simple bullet image
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, platforms: list[Platform]):
        """Update bullet position and check collisions."""
        if not self.alive:
            return

        # Move
        self.x += self.vx
        self.y += self.vy
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        # Check platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.alive = False
                return

        # Check screen boundaries
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.alive = False

    def draw(self, screen, camera):
        """Draw bullet with camera offset."""
        if self.alive:
            screen.blit(self.image, camera.apply(self.rect))
