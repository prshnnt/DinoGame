import pygame as pg

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Game")
        self.clock = pg.time.Clock()
        self.running = True
    def update(self):
        pass
    def draw(self):
        pg.display.flip()
    def run(self):
        while self.running:
            dt = self.clock.tick(60)/1000
            self.update(dt)
            self.draw()
        pg.quit()
if __name__ == "__main__":
    game = Game()
    game.run()