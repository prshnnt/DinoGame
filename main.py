import pygame as pg
import sys
from settings import *
from entities.player import Player , PlayerState
from entities.enemy import Enemy
from entities.platform import Platform
from core.camera import Camera
from core.screen_shake import ScreenShake
from core.parallax import ParallaxBackground
from utils.loader import load_image
from core.level import Level
from core.state import MainState


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.running = True
        self.bg_color = SKY_BLUE
        
        # Initialize states
        self.states = {}
        self.current_state = MainState.MENU

    def hamdle_events(self):
        events = pg.event.get() # Get events once per frame
        # 1. Global Event Handling (Quit)
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

    def update(self,dt):
        pass
    def draw(self):
        self.screen.fill(self.bg_color)
        pg.display.flip()
        pass
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.hamdle_events()
            self.update(dt)
            self.draw()


        pg.quit()
        sys.exit()



class Play:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.level_index = 1
        self.player = Player((100,SCREEN_HEIGHT-150))

        self.world_width = 3000
        self.world_height = SCREEN_HEIGHT
        self.camera = Camera(self.world_width,self.world_height)
        self.screen_shake = ScreenShake()
        self.parallax = ParallaxBackground()
        for i in range(1,6):
            self.parallax.add_layer(
                load_image(f"assets/background/plx-{i}.png"),i*0.2
            )

        self.load_level(self.level_index)

    def load_level(self, index):
        default = pg.image.load("assets/background/ground.png").convert_alpha()
        self.level = Level(f"levels/level{index}.json",default)
        self.player.rect.topleft = self.level.player_start
        
        self.platforms = self.level.platforms
        self.enemies = self.level.enemies
        platforms = []
        count = self.world_width//default.get_width() + 1
        for i in range(int(-count/2),count):
            platforms.append(Platform(i*default.get_width(),SCREEN_HEIGHT-default.get_height(),default.get_width(),default.get_height(),default))
        for i in platforms:
            self.platforms.append(i)
        self.camera.rect.x = 0

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
                    enemy.alive = False
                else:
                    direction = -1 if enemy.rect.centerx > self.player.rect.centerx else 1
                    self.player.hurt(direction)
                self.screen_shake.start(6)
  


    def update(self,dt):
        if self.player.rect.x >= self.level.end_x:
            self.level_index += 1
            self.load_level(self.level_index)
            pg.display.set_caption(f"{TITLE} - Level {self.level_index}")
            self.screen_shake.start(6)

        self.player.update(dt,self.platforms)

        for enemy in self.enemies:
            enemy.update(self.platforms,self.camera,self.player)

        self.handle_enemy_collision()
        self.camera.update(self.player.rect)

    def draw(self):
        offset_x, offset_y = self.screen_shake.update()

        self.screen.fill(SKY_BLUE)
        # draw parallax FIRST
        self.parallax.draw(self.screen, self.camera.rect.x + offset_x)

        for platform in self.platforms:
            platform.draw(self.screen,self.camera.apply(platform.rect).move(offset_x,offset_y))
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