import sys
import random
import pygame as pg
from pygame.locals import *
from settings import *


clicked = False

pg.init()

# Window Size
screen = pg.display.set_mode(WIN_SIZE)

# Window Icon
APP_ICON = pg.image.load(IMG_ICO)
pg.display.set_icon(APP_ICON)

# Window Title
pg.display.set_caption(WIN_TITLE)

# Background Music
pg.mixer.music.load(AUD_BGM)
pg.mixer.music.play()

# FONT
FONT = pg.font.Font(FNT_COURIER, 20)
FONT2 = pg.font.Font(FNT_ELFBOY, 50)


while 1:
    screen.fill(CLR_BG)
    title = FONT2.render('Pong Game', True, CLR_BLACK, CLR_BG)
    textRect = title.get_rect()
    textRect.center = (400, 30)
    screen.blit(title, textRect)
    pg.display.update()
