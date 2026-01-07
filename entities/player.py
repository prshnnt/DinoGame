import pygame as pg
from entities.platform import Platform
from settings import *
from utils.boundingbox import load_animation
from utils.player_state import PlayerState
from enum import Enum

from core.Base import BaseEntity


PLAYER_COLOR = (200,50,50)



class PlayerSprite(Enum):
    DOUX = "assets/player/DinoSprites-doux.png"
    MORT = "assets/player/DinoSprites-mort.png"
    TARD = "assets/player/DinoSprites-tard.png"
    VITA = "assets/player/DinoSprites-vita.png"

class Player(BaseEntity):
    def __init__(self,pos,sprite:PlayerSprite = PlayerSprite.DOUX):
        super().__init__()
        self.state = PlayerState.IDLE
        # animation 
        self.animations = {}
        self.frame_index = 0
        self.animation_duration= 100
        self.load_animations(sprite,(3,3))
        self.image = self.animations[self.state][0]

        self.rect = self.image.get_rect()
        self.rect.center = (pos[0],pos[1])
        self.x = self.rect.x
        self.y = self.rect.y

        self.kick_timer = 0
        self.kick_duration = 200

        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1200  # ms

        self.hurt_timer = 0
        self.hurt_duration = 400
    
    def handle_input(self):
        keys = pg.key.get_pressed()
        self.vx = 0
        if self.state!= PlayerState.HURT:
            if keys[pg.K_LEFT]:
                self.vx = -PLAYER_SPEED
                self.facing_right = False
            if keys[pg.K_RIGHT]:
                self.vx = PLAYER_SPEED
                self.facing_right = True
            if keys[pg.K_UP]:
                self.jump()
                self.state = PlayerState.JUMP
            if keys[pg.K_DOWN] and self.on_ground:
                self.state = PlayerState.DUCK
            if keys[pg.K_a]:
                self.state = PlayerState.KICK
                
    def load_animations(self,sprite:PlayerSprite,scale):
        animations = load_animation(sprite.value,"assets/player/player_bb.json",scale)
        temp = {}
        for i in animations.keys():
            temp[PlayerState(i)] = animations[i]
        self.animations = temp
        print(temp)

    def hurt(self, direction):
        if self.invincible:
            return
        self.state = PlayerState.HURT
        self.invincible = True
        self.invincible_timer = pg.time.get_ticks()
        self.hurt_timer = pg.time.get_ticks()

        self.vx = 8 * direction
        self.vy = -6

    
        
    def update_state(self):
        now = pg.time.get_ticks()

        if self.state == PlayerState.HURT:
            if now - self.hurt_timer > self.hurt_duration:
                self.state = PlayerState.IDLE
            return
        if self.invincible:
            if now - self.invincible_timer > self.invincible_duration:
                self.invincible = False
        if not self.on_ground:
            self.state = PlayerState.JUMP
        elif self.vx != 0:
            self.state = PlayerState.RUN
        else:
            self.state = PlayerState.IDLE



    def collide_wall(self,platforms:list[Platform]):
        # --- X AXIS MOVEMENT ---
        self.move_x()
        # X Collision Check
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                elif self.vx < 0:
                    self.rect.left = platform.rect.right
                
                # CRITICAL FIX: Sync self.x with the new rect position
                self.x = self.rect.x 

        # --- Y AXIS MOVEMENT ---
        self.on_ground = False
        self.move_y()
        # Y Collision Check
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0
                
                # CRITICAL FIX: Sync self.y with the new rect position
                self.y = self.rect.y
        

    def update(self, dt, platforms):
        self.handle_input()
        self.apply_gravity()
        self.collide_wall(platforms)
        self.update_state()
        self.animate(self.state)


    def draw(self, screen, camera):
        if self.invincible:
            if (pg.time.get_ticks() // 100) % 2 == 0:
                return
        screen.blit(self.image, camera.apply(self.rect))

    