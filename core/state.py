from enum import Enum
import pygame as pg

class MainState(Enum):
    MENU = 'menu'
    PLAY = 'play'
    PAUSED = 'paused'
    QUIT = 'quit'


playbutton = [pg.image.load("assets/menu/playbutton_01.png").convert_alpha(), pg.image.load("assets/menu/playbutton_02.png").convert_alpha()]
quitbutton = [pg.image.load("assets/menu/quit_01.png").convert_alpha(), pg.image.load("assets/menu/quit_02.png").convert_alpha()]
savebutton = [pg.image.load("assets/menu/save_01.png").convert_alpha(), pg.image.load("assets/menu/save_02.png").convert_alpha()]
optionsbutton = [pg.image.load("assets/menu/options_01.png").convert_alpha(), pg.image.load("assets/menu/options_02.png").convert_alpha()]
crossbutton = [pg.image.load("assets/menu/cross_01.png").convert_alpha(), pg.image.load("assets/menu/cross_02.png").convert_alpha()]
yesbutton = [pg.image.load("assets/menu/yes_01.png").convert_alpha(), pg.image.load("assets/menu/yes_02.png").convert_alpha()]


class Button:
    def __init__(self, x:float, y:float, image:pg.Surface, scale:float):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect:pg.Rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self,screen):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action # if clicked then return true

class MainMenu:
    def __init__(self):
        self.play_button = Button(300, 200, playbutton[0], 0.8)
        self.quit_button = Button(300, 300, quitbutton[0], 0.8)
    def draw(self,screen):
        if self.play_button.draw(screen):
            return MainState.PLAY
        if self.quit_button.draw(screen):
            return MainState.QUIT # Will be handled in main loop to quit
        return MainState.MENU
class PauseMenu:
    def __init__(self):
        self.resume_button = Button(300, 200, playbutton[0], 0.8) # Using playbutton for resume
        self.save_button = Button(300, 250, savebutton[0], 0.8)
        self.options_button = Button(300, 300, optionsbutton[0], 0.8)
        self.quit_button = Button(300, 350, quitbutton[0], 0.8)

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
        self.cross_button = Button(300, 200, crossbutton[0], 0.8) # using cross button to pause
        pass # No buttons for now, just a placeholder
    def draw(self, screen):
        # In a real game, this might draw HUD elements, score, etc.
        # For now, it just signifies that the game is actively playing.
        if self.cross_button.draw(screen):
            return MainState.PAUSED
        return MainState.PLAY