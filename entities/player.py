import pygame as pg
from settings import *
from core.camera import Camera
PLAYER_COLOR = (200,50,50)

# entities/player_states.py

from enum import Enum

class PlayerState(Enum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    DUCK = "duck"
    KICK = "kick"
    HURT = "hurt"


class Player:
    def __init__(self,pos):
        self.state = PlayerState.IDLE
        self.facing_right = True

        # animation 
        self.animations = {}
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = pg.Surface((40,60))
        self.image.fill((200,50,50))
        self.load_animations()

        self.rect = self.image.get_rect()
        self.rect.center = (pos[0],pos[1])

        self.vx = 0
        self.vy = 0
        self.on_ground = False
    
    def load_animations(self):
        self.animations = {
            PlayerState.IDLE : [self.image],
            PlayerState.RUN : [self.image],
            PlayerState.JUMP : [self.image],
            PlayerState.DUCK : [self.image],
            PlayerState.KICK : [self.image],
            PlayerState.HURT : [self.image]
        }
    def update_state(self):
        if self.state == PlayerState.HURT:
            return
        if not self.on_ground:
            self.state = PlayerState.JUMP
        elif self.vx !=0:
            self.state = PlayerState.RUN
        else:
            self.state = PlayerState.IDLE
    
    def animate(self):
        frames = self.animations[self.state]
        
        self.frame_index += self.animation_speed
        if self.frame_index>=len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]
        # self.image.fill((200,50,50))

        if not self.facing_right:
            self.image= pg.transform.flip(self.image,True,False)
            # self.image.fill((255,0,0))

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
            if keys[pg.K_UP] and self.on_ground:
                self.vy = JUMP_FORCE
                self.on_ground = False
                self.state = PlayerState.JUMP

            if keys[pg.K_DOWN] and self.on_ground:
                self.state = PlayerState.DUCK

            elif keys[pg.K_LCTRL]:
                self.state = PlayerState.KICK

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy >MAX_VY:
            self.vy = MAX_VY
    
    def update(self,dt,platforms):
        self.handle_input()

        self.rect.x += self.vx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx>0:
                    self.rect.right = platform.rect.left
                elif self.vx<0:
                    self.rect.left = platform.rect.right

        self.apply_gravity()

        self.rect.y += self.vy
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy>0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground =True
                elif self.vy<0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0
        
        self.update_state()
        self.animate()


    def draw(self,screen,camera:Camera):
        screen.blit(self.image,camera.apply(self.rect))
    