import re
import pygame as pg
from enum import Enum
from settings import *
from entities.platform import Platform
from entities.player import  Player
from core.camera import Camera
from core.Base import BaseEntity
from utils.player_state import PlayerState
from utils.boundingbox import load_animation



class PlayerSprite(Enum):
    DOUX = "assets/player/DinoSprites-doux.png"
    MORT = "assets/player/DinoSprites-mort.png"
    TARD = "assets/player/DinoSprites-tard.png"
    VITA = "assets/player/DinoSprites-vita.png"

class Enemy(BaseEntity):
    def __init__(self,pos,sprite:PlayerSprite = PlayerSprite.TARD):
        super().__init__()
        self.state = PlayerState.IDLE
        # animation 
        self.animations = {}
        self.frame_index = 0
        self.animation_duration= 100
        self.load_animations(sprite,(3,3),reverse = False)
        self.image = self.animations[self.state][0]

        self.rect = self.image.get_rect()
        self.rect.center = (pos[0],pos[1])
        self.x = self.rect.x
        self.y = self.rect.y
        # -----------------------

        self.vx = -2

        self.on_ground = False
        self.alive = True
        self.active = False # only move when active

        self.pause_time = 0
        self.pause_duration = 500
        self.speed = 2
    def animate(self,state):
        current_time = pg.time.get_ticks()

        if current_time - self.animation_last_update > self.animation_duration:
            #update frame index
            self.frame_index += 1
            if self.frame_index >= len(self.animations[state]):
                self.frame_index = 0
            # update image 
            self.set_image(self.animations[state][self.frame_index])
            self.animation_last_update = current_time
            if self.facing_right:
                self.flip_image()
    def load_animations(self,sprite:PlayerSprite,scale,reverse = False):
        animations = load_animation(sprite.value,"assets/player/player_bb.json",scale,reverse)
        temp = {}
        for i in animations.keys():
            temp[PlayerState(i)] = animations[i]
        self.animations = temp
    def update_state(self):
        if not self.on_ground:
            self.state = PlayerState.JUMP
        elif self.vx != 0:
            self.state = PlayerState.RUN
        else:
            self.state = PlayerState.IDLE

    def change_direction(self):
        self.facing_right = self.vx < 0

    def update(self,platforms:list[Platform],camera:Camera,player:Player):
        if not self.alive:
            return
        if not camera.apply(self.rect).colliderect(
            pg.Rect(0,0,SCREEN_WIDTH,SCREEN_WIDTH)
        ):
            self.active = False
            return
        else:
            self.active = True
            if player.rect.x - self.rect.x>0:
                self.vx = abs(self.vx)
            else:
                self.vx = -abs(self.vx)
                
        self.apply_gravity()
        self.change_direction()
        self.update_state()
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
        
        self.animate(self.state)


    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
