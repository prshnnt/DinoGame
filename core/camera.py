import pygame as pg
from settings import *


class Camera:
    def __init__(self,width,height):
        self.rect = pg.Rect(0,0,width,height)

    def update(self, target):
        # Center camera on player X
        self.rect.x = target.centerx - SCREEN_WIDTH // 2
        self.rect.y = target.centery - SCREEN_HEIGHT // 2


        # Clamp camera to level bounds
        self.rect.x = max(0, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.x = min(self.rect.x, self.rect.width - SCREEN_WIDTH*2)
        self.rect.y = min(self.rect.y, self.rect.height - SCREEN_HEIGHT)


    def apply(self, rect):
        return rect.move(-self.rect.x, -self.rect.y)
