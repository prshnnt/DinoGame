import pygame as pg
from settings import *

class ParallaxLayer:
    def __init__(self,image:pg.Surface,speed):
        self.image = image
        self.speed = speed
        self.width = image.get_width()
    def draw(self,screen:pg.Surface,camera_x):
        offsetx = camera_x * self.speed
        x = -offsetx % self.width
        screen.blit(self.image, (x,0))
        screen.blit(self.image, (x-self.width,0))
        screen.blit(self.image, (x+self.width,0))

class ParallaxBackground:
    def __init__(self):
        self.layers = []

    def add_layer(self,image:pg.Surface,speed):
        self.layers.append(ParallaxLayer(image,speed))

    def draw(self,screen:pg.Surface,camera_x):
        for layer in self.layers:
            layer.draw(screen,camera_x)