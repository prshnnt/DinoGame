import pygame as pg
import sys
from settings import *
from entities.player import Player , PlayerState
from entities.enemy import Enemy
from entities.platform import Platform
from core.camera import Camera
from core.screen_shake import ScreenShake


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
        self.screen_shake = ScreenShake()
        self.player = Player((100,SCREEN_HEIGHT-150))
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT),   # ground
            Platform(-SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT),   # ground
            Platform(SCREEN_WIDTH*2, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT),   # ground
            Platform(300, 400, 200, 30),
            Platform(600, 300, 200, 30),
            Platform(200, 250, 150, 30)
        ]
        self.enemies = [
            Enemy((500, SCREEN_HEIGHT-100)),
            Enemy((800, SCREEN_HEIGHT-100))
        ]


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
            
    def handle_enemy_collision(self):
        for enemy in self.enemies:
            if not enemy.alive:
                continue

            if self.player.rect.colliderect(enemy.rect):
                #player killing enemy by jumping over him
                if self.player.vy > 0 and self.player.rect.bottom <= enemy.rect.centery:
                    enemy.alive = False
                    self.player.vy = JUMP_FORCE/2
                # player kicking enemy
                elif self.player.state == PlayerState.KICK:
                    print(True)
                    enemy.alive = False
                else:
                    direction = -1 if enemy.rect.centerx > self.player.rect.centerx else 1
                    self.player.hurt(direction)
                self.screen_shake.start(6)
  


    def update(self,dt):
        self.player.update(dt,self.platforms)

        for enemy in self.enemies:
            enemy.update(self.platforms,self.camera,self.player)

        self.handle_enemy_collision()
        self.camera.update(self.player.rect)

    def draw(self):
        offset_x, offset_y = self.screen_shake.update()

        self.screen.fill(SKY_BLUE)
        for platform in self.platforms:
            pg.draw.rect(
                self.screen,
                (100, 100, 100),
                self.camera.apply(platform.rect).move(offset_x,offset_y)
            )
        self.player.draw(self.screen,self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen,self.camera)
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