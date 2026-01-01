import pygame as pg
from settings import *

class Camera:
    def __init__(self,width,height):
        self.camera_rect = pg.Rect(0,0,width,height)

    def apply(self,rect:pg.Rect) -> pg.Rect:
        """ yeh world rect(world map) hai usse screen rect mai lata hai
            basically yeh pure map ke elements ko camera ke opposite move karta hai 
            mtlb player static lagna chahiye isiliye 
            camera player ke sath move karega na isiliye
        """
        return rect.move(-self.camera_rect.x,-self.camera_rect.y)
    
    def update(self,target:pg.Rect):
        """
        Docstring for update

        :param target: pg.Rect (player.rect)
        """
        x = (target.centerx - SCREEN_WIDTH) // 2
        # y = (target.centery - SCREEN_HEIGHT) // 2

        y = 0

        self.camera_rect.x = x
        self.camera_rect.y = y
    