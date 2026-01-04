# utils/loader.py

import pygame as pg
import os
from utils.player_state import PlayerState


class SpriteSheet():
    def __init__(self,image):
        self.sheet:pg.Surface = image
    
    def get_image(self,frame:int,width:int,height:int,scale,color,top=0):
        image = pg.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0),((frame*width),top,width,height))
        image = pg.transform.scale(image,scale).convert_alpha()
        image.set_colorkey(color)
        return image
    

def load_image(path):
    image = pg.image.load(path).convert_alpha()
    return image

def load_player_sprites(path,size):
    sprites = {}
    sprite_sheet = SpriteSheet(load_image(path))

    frames_steps = [4,6,3,4,7]
    frames_steps_dict = {
        PlayerState.IDLE : 0,
        PlayerState.RUN : 1,
        PlayerState.DUCK : 4,
        PlayerState.KICK : 2,
        PlayerState.HURT : 3
    }
    counter =  0
    for key,value in frames_steps_dict.items():
        temp = []
        for i in range(frames_steps[value]):
            temp.append(sprite_sheet.get_image(counter , 24 , 21 , size , (0,0,0)))
            counter+=1
        sprites[key]=temp
    sprites[PlayerState.JUMP] = sprites[PlayerState.IDLE]
    return sprites