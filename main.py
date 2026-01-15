from enum import Enum
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

class MainState(Enum):
    MENU = 'menu'
    PLAY = 'play'
    PAUSED = 'paused'
    QUIT = 'quit'

class Button:
    def __init__(self, rect:pg.Rect|tuple,image1:pg.Surface,image2:pg.Surface,callback=None):
        self.rect = pg.Rect(rect)
        self.image1 = pg.transform.scale(image1,(self.rect.width,self.rect.height)).convert_alpha()
        self.image2 = pg.transform.scale(image2,(self.rect.width,self.rect.height)).convert_alpha()
        self.callback = callback

        self.image = self.image1
        self.hovered = False
        self.clicked = False
    def update(self,events,mouse_pos):
        # call callback function if button state is clicked , bas itna samjho jyada dhyan nhi do code pe
        if self.callback and self.clicked and pg.mouse.get_pressed()[0] == 0:
            self.callback()
            self.clicked = False
            return
        # set click state of button to true if clicked and hovered
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            self.image = self.image2
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                print("Button clicked!"+str(self.callback))
                
        else:
            # set state to false if not clicked
            self.clicked = False
            self.hovered = False
            self.image = self.image1


    def draw(self,screen:pg.Surface):
        screen.blit(self.image,(self.rect.x,self.rect.y))

class State:
    def __init__(self,screen:pg.Surface,objects):
        self.screen = screen
        self.objects = objects
    def add_object(self,obj):
        self.objects.append(obj)
    def remove_object(self,obj):
        self.objects.remove(obj)
    def update(self,events,mouse_pos):
        for obj in self.objects:
            obj.update(events,mouse_pos)
    def draw(self):
        for obj in self.objects:
            obj.draw(self.screen)


class Play:
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
  


    def update(self,dt,x):
        self.pause_button.update(self.game.events,self.game.mouse_pos)
        if self.player.rect.x >= self.level.end_x:
            self.level_index += 1
            self.player.rect.x = self.level.player_start[0]
            self.load_level(self.level_index)
            pg.display.set_caption(f"{TITLE} - Level {self.level_index}")
            self.screen_shake.start(10)

        self.player.update(dt,self.platforms)

        for enemy in self.enemies:
            enemy.update(self.platforms,self.camera,self.player)

        self.handle_enemy_collision()
        self.camera.update(self.player.rect)

    def draw(self,x):
        offset_x, offset_y = self.screen_shake.update()

        self.screen.fill(SKY_BLUE)
        # draw parallax FIRST
        self.parallax.draw(self.screen, self.camera.rect.x + offset_x)

        for platform in self.platforms:
            platform.draw(self.screen,self.camera.apply(platform.rect).move(offset_x,offset_y))
        self.player.draw(self.screen,self.camera)
        for enemy in self.enemies:
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
                (cx - (box_width//2),(box_height//2)*3.5,box_width,box_height),
                pg.image.load("assets/menu/level_01.png").convert_alpha(),
                pg.image.load("assets/menu/level_02.png").convert_alpha(),
                # lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.MENU].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*5.8,box_width,box_height),
                pg.image.load("assets/menu/options_01.png").convert_alpha(),
                pg.image.load("assets/menu/options_02.png").convert_alpha(),
                # lambda: self.set_state(MainState.PLAY)
            )   
        )
        self.states[MainState.MENU].add_object(
            Button(
                (cx - (box_width//2),(box_height//2)*12,box_width,box_height),
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
        self.states[self.current_state].update(self.events,self.mouse_pos)


    def draw(self):
        if self.current_state == MainState.QUIT:
            self.running = False
            return
        self.screen.fill(self.bg_color)
        self.states[self.current_state].draw()
        pg.draw.circle(self.screen,WHITE,self.mouse_pos,5)
        pg.display.flip()
        pass

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