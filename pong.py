import pygame as pg
from settings import FONT, COLOR, AUDIO, WIN


class Pong:
    def __init__(self):
        self.bgcolor = WIN["bgcolor"]
        self.size = self.width, self.height = WIN["width"], WIN["height"]
        self.title = WIN["title"]
        self.icon = WIN["icon"]

    def run(self):
        self.screen = pg.display.set_mode(self.size)
        self.screen.fill(self.bgcolor)
        logo = pg.image.load(self.icon)
        pg.display.set_icon(logo)
        pg.display.set_caption(self.title)
        pg.display.flip()
        self.running = True

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False


game = Pong()
game.run()
