import pygame as pg
import sys
from settings import *
from entities.player import Player
from entities.platform import Platform
from core.camera import Camera


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True

        self.world_width = 3000
        self.world_height = SCREEN_HEIGHT
        self.camera = Camera(self.world_width,self.world_height)

        self.player = Player((100,SCREEN_HEIGHT-150))
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT),   # ground
            Platform(300, 400, 200, 30),
            Platform(600, 300, 200, 30),
            Platform(200, 250, 150, 30)
        ]


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
    
    def update(self,dt):
        self.player.update(dt,self.platforms)
        self.camera.update(self.player.rect)

    def draw(self):
        self.screen.fill(SKY_BLUE)
        for platform in self.platforms:
            pg.draw.rect(
                self.screen,
                (100, 100, 100),
                self.camera.apply(platform.rect)
            )
        self.player.draw(self.screen,self.camera)
        pg.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)/1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()