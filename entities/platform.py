import pygame as pg

class Platform:
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)
    def draw(self,screen):
        pg.draw.rect(screen,(100,100,100),self.rect)

