from enum import Enum
import pygame as pg
from settings import *

class MainState(Enum):
    MENU = 'menu'
    PLAY = 'play'
    PAUSED = 'paused'
    QUIT = 'quit'







class Button:
    def __init__(self, x, y, asset, scale):
        width = asset[0].get_width()
        height = asset[0].get_height()
        self.asset = asset
        self.image = pg.transform.scale(asset[0], (int(width * scale), int(height * scale))).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.hovered = False

    def update(self, events):
        action = False
        pos = pg.mouse.get_pos()
        
        # Check hover
        if self.rect.collidepoint(pos):
            self.hovered = True
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                self.image = self.asset[1].convert_alpha() # Clicked image
        else:
            self.hovered = False
        
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
            self.image = self.asset[0].convert_alpha() # Normal image
            
        return action

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class MainMenu:
    def __init__(self):
        # 1. LOAD THE IMAGES FIRST
        # Make sure these paths match your folder structure
        playbutton_imgs = [
            pg.image.load("assets/menu/playbutton_01.png").convert_alpha(), 
            pg.image.load("assets/menu/playbutton_02.png").convert_alpha()
        ]
        quitbutton_imgs = [
            pg.image.load("assets/menu/quit_01.png").convert_alpha(), 
            pg.image.load("assets/menu/quit_02.png").convert_alpha()
        ]
        
        # 2. CALCULATE POSITION (Optional centering logic)
        # Ensure SCREEN_WIDTH is imported from settings
        center_x = SCREEN_WIDTH // 2 - (playbutton_imgs[0].get_width() * 0.8) // 2
        
        # 3. CREATE BUTTONS USING THE LOADED IMAGES
        self.play_button = Button(center_x, 200, playbutton_imgs, 0.8)
        self.quit_button = Button(center_x, 300, quitbutton_imgs, 0.8)

    def handle_events(self, events):
        if self.play_button.update(events):
            return MainState.PLAY
        if self.quit_button.update(events):
            return MainState.QUIT
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        self.play_button.draw(screen)
        self.quit_button.draw(screen)

# Apply similar structure to PauseMenu and PlayMenu
class PauseMenu:
    def __init__(self):
        playbutton = [pg.image.load("assets/menu/playbutton_01.png").convert_alpha(), pg.image.load("assets/menu/playbutton_02.png").convert_alpha()]
        quitbutton = [pg.image.load("assets/menu/quit_01.png").convert_alpha(), pg.image.load("assets/menu/quit_02.png").convert_alpha()]
        savebutton = [pg.image.load("assets/menu/save_01.png").convert_alpha(), pg.image.load("assets/menu/save_02.png").convert_alpha()]
        optionsbutton = [pg.image.load("assets/menu/options_01.png").convert_alpha(), pg.image.load("assets/menu/options_02.png").convert_alpha()]
        self.resume_button = Button(300, 200, playbutton, 0.8) # Using playbutton for resume
        self.save_button = Button(300, 250, savebutton, 0.8)
        self.options_button = Button(300, 300, optionsbutton, 0.8)
        self.quit_button = Button(300, 350, quitbutton, 0.8)

    def draw(self, screen):
        if self.resume_button.draw(screen):
            return MainState.PLAY
        if self.save_button.draw(screen):
            # Implement save functionality here
            pass
        if self.options_button.draw(screen):
            # Implement options functionality here
            pass
        if self.quit_button.draw(screen):
            return MainState.QUIT
        return MainState.PAUSED
class PlayMenu:
    def __init__(self):
        crossbutton = [pg.image.load("assets/menu/cross_01.png").convert_alpha(), pg.image.load("assets/menu/cross_02.png").convert_alpha()]
        yesbutton = [pg.image.load("assets/menu/yes_01.png").convert_alpha(), pg.image.load("assets/menu/yes_02.png").convert_alpha()]
        self.cross_button = Button(300, 200, crossbutton, 0.8) # using cross button to pause
        pass # No buttons for now, just a placeholder
    def update(self, dt):
        pass
    def handle_events(self, events):
        # In PlayMenu.handle_events
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return MainState.PAUSED
    def draw(self, screen):
        # In a real game, this might draw HUD elements, score, etc.
        # For now, it just signifies that the game is actively playing.
        if self.cross_button.draw(screen):
            return MainState.PAUSED
        return MainState.PLAY