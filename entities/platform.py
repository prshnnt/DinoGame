import pygame as pg


class Platform:
    def __init__(self,x,y,w,h,image:pg.Surface):
        self.image = pg.transform.scale(image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self,screen:pg.Surface,rect):
        screen.blit(self.image,rect)

