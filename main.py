import pygame as pg
from enum import Enum
import sys
from settings import *
from entities.player import Player , PlayerState
from entities.enemy import Enemy
from entities.platform import Platform
from core.camera import Camera
from core.screen_shake import ScreenShake
from core.parallax import ParallaxBackground
from core.level import Level as Stage
from core.Base import Button,MainState , State , BaseObject
from utils.loader import load_image

class Play(BaseObject):
    def __init__(self,game):
        pg.init()
        self.screen = game.screen
        self.game = game
        self.pause_button = Button(
                (5,5,50,50),
                pg.image.load("assets/menu/pause_01.png").convert_alpha(),
                pg.image.load("assets/menu/pause_02.png").convert_alpha(),
                lambda: self.game.set_state(MainState.PAUSED)
            )
        
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.level_index = 1
        self.player = Player((100,SCREEN_HEIGHT-150))
        
        self.world_width = 3000
        self.world_height = SCREEN_HEIGHT
        self.load_level(self.level_index)
        self.camera = Camera(self.world_width,self.world_height)
        self.screen_shake = ScreenShake()
        self.parallax = ParallaxBackground()
        for i in range(1,6):
            self.parallax.add_layer(
                load_image(f"assets/background/plx-{i}.png"),i*0.2
            )


    def load_level(self, index):
        default = pg.image.load("assets/background/ground.png").convert_alpha()
        self.level = Stage(f"levels/level{index}.json",default)
        self.player.rect.topleft = self.level.player_start

        self.world_width = self.level.end_x
        
        self.platforms = self.level.platforms
        self.enemies = self.level.enemies
        platforms = []
        count = self.world_width//default.get_width() + 1
        for i in range(int(-count/2),count):
            platforms.append(Platform(i*default.get_width(),SCREEN_HEIGHT-default.get_height(),default.get_width(),default.get_height(),default))
        for i in platforms:
            self.platforms.append(i)

            
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
  


    def update(self,dt,events,mouse_pos):
        self.pause_button.update(dt,self.game.events,self.game.mouse_pos)

        self.player.update(dt,self.platforms)

        for enemy in self.enemies:
            enemy.update(self.platforms,self.camera,self.player)

        self.handle_enemy_collision()
        self.camera.update(self.player.rect)

    def draw(self,screen:pg.Surface):
        offset_x, offset_y = self.screen_shake.update()

        self.screen.fill(SKY_BLUE)
        # draw parallax FIRST
        self.parallax.draw(self.screen, self.camera.rect.x + offset_x)

        for platform in self.platforms:
            platform.draw(self.screen,self.camera.apply(platform.rect).move(offset_x,offset_y))
        self.player.draw(self.screen,self.camera)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(self.screen,self.camera)
        
        self.pause_button.draw(self.screen)
        pg.display.flip()

class PlayState(State):
    def __init__(self,game):
        super().__init__(game.screen,[])
        self.play = Play(game)
        self.add_object(self.play)


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
        self.load_main_menu()
        self.load_play_frame()
        self.load_pause_frame()

    def set_state(self,state):
        self.current_state = state

    def load_main_menu(self):
        self.states[MainState.MENU] = State(self.screen,[])
        cx,cy = self.screen.get_rect().center

        box_width = 200
        box_height = 80

        self.states[MainState.MENU].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*1,box_width,box_height),
                pg.image.load("assets/menu/playbutton_01.png").convert_alpha(),
                pg.image.load("assets/menu/playbutton_02.png").convert_alpha(),
                lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.MENU].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*3.3,box_width,box_height),
                pg.image.load("assets/menu/level_01.png").convert_alpha(),
                pg.image.load("assets/menu/level_02.png").convert_alpha(),
                # lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.MENU].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*5.6,box_width,box_height),
                pg.image.load("assets/menu/options_01.png").convert_alpha(),
                pg.image.load("assets/menu/options_02.png").convert_alpha(),
                # lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.MENU].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*8,box_width,box_height),
                pg.image.load("assets/menu/quit_01.png").convert_alpha(),
                pg.image.load("assets/menu/quit_02.png").convert_alpha(),
                lambda: self.set_state(MainState.QUIT)
            )   
        )
    def load_play_frame(self):
        self.states[MainState.PLAY] = PlayState(self)

    def load_pause_frame(self):
        self.states[MainState.PAUSED] = State(self.screen,[])
        cx,cy = self.screen.get_rect().center

        box_width = 250
        box_height = 100

        self.states[MainState.PAUSED].add_object(
            Button(
                (cx*2 - 100,20,50,50),
                pg.image.load("assets/menu/cross_01.png").convert_alpha(),
                pg.image.load("assets/menu/cross_02.png").convert_alpha(),
                lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.PAUSED].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*1,box_width,box_height),
                pg.image.load("assets/menu/playbutton_01.png").convert_alpha(),
                pg.image.load("assets/menu/playbutton_02.png").convert_alpha(),
                lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.PAUSED].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*4,box_width,box_height),
                pg.image.load("assets/menu/options_01.png").convert_alpha(),
                pg.image.load("assets/menu/options_02.png").convert_alpha(),
                # lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.PAUSED].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*7,box_width,box_height),
                pg.image.load("assets/menu/quit_01.png").convert_alpha(),
                pg.image.load("assets/menu/quit_02.png").convert_alpha(),
                lambda: self.set_state(MainState.MENU)
            )   
        )
    def handle_events(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_p:
                    self.set_state(MainState.PAUSED if self.current_state == MainState.PLAY else MainState.PLAY)



    def update(self,dt):
        self.states[self.current_state].update(dt,self.events,self.mouse_pos)


    def draw(self):
        if self.current_state == MainState.QUIT:
            self.running = False
            return
        self.screen.fill(self.bg_color)
        self.states[self.current_state].draw()
        pg.draw.circle(self.screen,WHITE,self.mouse_pos,5)
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