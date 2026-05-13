import pygame as pg
from settings import *
from entities.platform import Platform
from utils.player_state import PlayerState
from core.Base import BaseEntity


class EnemyBase(BaseEntity):
    """Base class for all enemy types."""

    def __init__(self, pos):
        super().__init__()
        self.state = PlayerState.IDLE
        self.animations = {}
        self.frame_index = 0
        self.animation_duration = 100

        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.x = self.rect.x
        self.y = self.rect.y

        self.vx = 0
        self.vy = 0

        self.on_ground = False
        self.alive = True
        self.active = False
        self.speed = 2
        self.facing_right = True

    def change_direction(self):
        """Change facing direction based on velocity."""
        self.facing_right = self.vx > 0

    def update_state(self):
        """Update enemy state based on current status."""
        if not self.on_ground:
            self.state = PlayerState.JUMP
        elif self.vx != 0:
            self.state = PlayerState.RUN
        else:
            self.state = PlayerState.IDLE

    def update(self, platforms: list[Platform], camera, player):
        """Override in subclasses for specific behavior."""
        if not self.alive:
            return
        self.update_state()
        self.animate(self.state)

    def draw(self, screen, camera):
        """Draw enemy with camera offset."""
        screen.blit(self.image, camera.apply(self.rect))
