import random
import pygame as pg
from enum import Enum
from settings import *
from entities.platform import Platform
from entities.player import Player
from entities.enemy_base import EnemyBase
from core.camera import Camera
from utils.player_state import PlayerState
from utils.boundingbox import load_animation


class EnemySprite(Enum):
    DOUX = "assets/player/DinoSprites-doux.png"
    MORT = "assets/player/DinoSprites-mort.png"
    TARD = "assets/player/DinoSprites-tard.png"
    VITA = "assets/player/DinoSprites-vita.png"


class GroundEnemy(EnemyBase):
    """Enemy that walks on the ground."""

    def __init__(self, pos):
        super().__init__(pos)
        self.load_animations(EnemySprite.TARD, (3, 3))
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = 2
        self.vx = -self.speed
        self.facing_right = False

    def load_animations(self, sprite: EnemySprite, scale):
        animations = load_animation(sprite.value, "assets/player/player_bb.json", scale, reverse=False)
        temp = {}
        for i in animations.keys():
            temp[PlayerState(i)] = animations[i]
        self.animations = temp

    def update(self, platforms: list[Platform], camera, player):
        if not self.alive:
            return

        # Check if player is in view
        if not camera.apply(self.rect).colliderect(pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
            self.active = False
            return
        else:
            self.active = True
            # Move towards player
            if player.rect.x > self.rect.x:
                self.vx = self.speed
                self.facing_right = True
            else:
                self.vx = -self.speed
                self.facing_right = False

        self.apply_gravity()
        self.update_state()

        # X movement and collision
        self.move_x()
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.left = platform.rect.right
                    self.vx = 0
                self.x = self.rect.x

        # Y movement and collision
        self.on_ground = False
        self.move_y()
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0
                self.y = self.rect.y

        self.animate(self.state)


class FlyEnemy(EnemyBase):
    """Enemy that flies in the air."""

    def __init__(self, pos):
        super().__init__(pos)
        self.load_animations(EnemySprite.VITA, (3, 3))
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = 3
        self.vx = -self.speed
        self.facing_right = False
        self.flying = True

    def load_animations(self, sprite: EnemySprite, scale):
        animations = load_animation(sprite.value, "assets/player/player_bb.json", scale, reverse=False)
        temp = {}
        for i in animations.keys():
            temp[PlayerState(i)] = animations[i]
        self.animations = temp

    def update(self, platforms: list[Platform], camera, player):
        if not self.alive:
            return

        # Check if player is in view
        if not camera.apply(self.rect).colliderect(pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
            self.active = False
            return
        else:
            self.active = True
            # Move towards player
            if player.rect.x > self.rect.x:
                self.vx = self.speed
                self.facing_right = True
            else:
                self.vx = -self.speed
                self.facing_right = False

        self.update_state()

        # X movement and collision (no gravity for flying enemies)
        self.move_x()
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.left = platform.rect.right
                    self.vx = 0
                self.x = self.rect.x

        # Y movement (can move up/down, e.g., bobbing or tracking player height)
        self.y += self.vy
        self.rect.y = round(self.y)

        self.animate(self.state)

    def apply_gravity(self):
        """Override - flying enemies don't fall."""
        pass


class ShooterEnemy(EnemyBase):
    """Enemy that shoots bullets at the player."""

    def __init__(self, pos):
        super().__init__(pos)
        self.load_animations(EnemySprite.MORT, (3, 3))
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = 1.5
        self.vx = -self.speed
        self.facing_right = False

        # Shooting mechanics
        self.shoot_timer = 0
        self.shoot_cooldown = 1500  # ms between shots
        self.bullets = []

    def load_animations(self, sprite: EnemySprite, scale):
        animations = load_animation(sprite.value, "assets/player/player_bb.json", scale, reverse=False)
        temp = {}
        for i in animations.keys():
            temp[PlayerState(i)] = animations[i]
        self.animations = temp

    def shoot(self, player: Player):
        """Create a bullet towards the player."""
        # Determine direction
        if player.rect.x > self.rect.x:
            bullet_vx = 8
        else:
            bullet_vx = -8

        # Create bullet at enemy position
        from entities.bullet import Bullet
        bullet = Bullet(self.rect.centerx, self.rect.centery, bullet_vx)
        self.bullets.append(bullet)

    def update(self, platforms: list[Platform], camera, player):
        if not self.alive:
            return

        # Check if player is in view
        if not camera.apply(self.rect).colliderect(pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
            self.active = False
            return
        else:
            self.active = True
            # Move towards player
            if player.rect.x > self.rect.x:
                self.vx = self.speed
                self.facing_right = True
            else:
                self.vx = -self.speed
                self.facing_right = False

        self.apply_gravity()
        self.update_state()

        # X movement and collision
        self.move_x()
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.left = platform.rect.right
                    self.vx = 0
                self.x = self.rect.x

        # Y movement and collision
        self.on_ground = False
        self.move_y()
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0
                self.y = self.rect.y

        # Shooting logic
        now = pg.time.get_ticks()
        self.shoot_timer += 16  # Approximate frame time
        if self.shoot_timer >= self.shoot_cooldown and self.active:
            self.shoot(player)
            self.shoot_timer = 0

        self.animate(self.state)

    def update_bullets(self, platforms: list[Platform]):
        """Update all bullets and remove ones that hit something."""
        for bullet in self.bullets[:]:
            bullet.update(platforms)
            if not bullet.alive:
                self.bullets.remove(bullet)

    def draw_bullets(self, screen, camera):
        """Draw all bullets."""
        for bullet in self.bullets:
            bullet.draw(screen, camera)


def create_enemy(enemy_type: str, pos):
    """Factory function to create different enemy types."""
    if enemy_type == "ground":
        return GroundEnemy(pos)
    elif enemy_type == "fly":
        return FlyEnemy(pos)
    elif enemy_type == "shooter":
        return ShooterEnemy(pos)
    else:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
