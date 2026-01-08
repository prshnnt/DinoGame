import pygame as pg
from settings import *

class BaseObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

        self.image:pg.Surface = None
        self.rect:pg.Rect = None
        self.mask:pg.Mask = None

    def set_image(self,image:pg.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pg.mask.from_surface(self.image)

    def move_x(self):
        self.x += self.vx
        self.rect.x = round(self.x)
        
    def move_y(self):
        self.y += self.vy
        self.rect.y = round(self.y)

    

        
class BaseEntity(BaseObject):
    def __init__(self):
        super().__init__()
        self.on_ground = False
        self.facing_right = True
        self.health = 100

        self.animations = {}
        self.frame_index = 0
        self.animation_duration = 100
        self.animation_last_update = pg.time.get_ticks()

    def set_image(self, image: pg.Surface):
        previous_rect = self.rect
        super().set_image(image)
        if previous_rect:
            self.rect.midbottom = previous_rect.midbottom
            self.x = self.rect.x
            self.y = self.rect.y

        
    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > MAX_VY:
            self.vy = MAX_VY

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

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
            if not self.facing_right:
                self.flip_image()


    def flip_image(self):
        self.image = pg.transform.flip(self.image, True, False).convert_alpha()
        self.mask = pg.mask.from_surface(self.image)

    def add_health(self,amount):
        self.health += amount
    def entity_hurt(self,amount):
        self.health -= amount
    
    