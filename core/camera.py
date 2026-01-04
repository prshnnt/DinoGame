import pygame as pg
from settings import *


class Camera:
    def __init__(self,width,height):
        self.camera_rect = pg.Rect(0,0,width,height)

    def update(self, target):
        # Center camera on player X
        self.camera_rect.x = target.centerx - SCREEN_WIDTH // 2

        # Clamp camera to level bounds
        self.camera_rect.x = max(0, self.camera_rect.x)
        self.camera_rect.x = min(self.camera_rect.x, self.camera_rect.width - SCREEN_WIDTH)

    def apply(self, rect):
        return rect.move(-self.camera_rect.x, 0)
