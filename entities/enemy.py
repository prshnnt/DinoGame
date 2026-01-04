import pygame as pg
from settings import *
from entities.platform import Platform
from entities.player import  Player
from core.camera import Camera

class Enemy:
    def __init__(self,pos,ground_height):
        self.rect:pg.Rect = pg.Rect(pos[0],pos[1]-ground_height,40,50)
        self.vx = -2
        self.vy = 0

        self.on_ground = False
        self.alive = True
        self.active = False # only move when active

        self.image = pg.Surface((40,50))
        self.image.fill((50,50,200))

        self.pause_time = 0
        self.pause_duration = 500
        self.speed = 2
        self.facing_right = True

    def apply_gravity(self):
        self.vy +=GRAVITY
        if self.vy > MAX_VY:
            self.vy = MAX_VY
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
                
        self.change_direction()
        # X movement
        self.rect.x += self.vx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                else:
                    self.rect.left = platform.rect.right
                self.vx *= -1  # turn around

        # Gravity
        self.apply_gravity()

        # Y movement
        self.rect.y += self.vy
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0
        if self.vx == 0:
            if pg.time.get_ticks() - self.pause_time > self.pause_duration:
                self.vx = self.speed if self.vx <= 0 else -self.speed


    def draw(self,screen:pg.Surface,camera:Camera):
        if self.alive:
            if self.facing_right:
                self.image.fill((0,0,0))
            else:
                self.image.fill((255,255,255))
            screen.blit(self.image , camera.apply(self.rect))
