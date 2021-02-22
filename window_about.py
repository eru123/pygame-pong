import pygame
import sys
import random
from pygame.locals import *
from settings import *
from button import button

clicked = False

pygame.init()

# Window Size
screen = pygame.display.set_mode(WIN_SIZE)

# Window Icon
APP_ICON = pygame.image.load(PATH_ICO)
pygame.display.set_icon(APP_ICON)

# Window Title
pygame.display.set_caption(WIN_TITLE)

# Background Music
pygame.mixer.music.load(PATH_BGM)
pygame.mixer.music.play()

# FONT
FONT = pygame.font.SysFont('Courier', 20)

# button(xPosition,yPosition,width,height,text,PyGameScreen)
BTN_PLAY = button(300, 80, 180, 60, 'Start Game', screen)
BTN_QUIT = button(300, 170, 180, 60, 'Quit', screen)
BTN_SETTINGS = button(300, 250, 180, 60, 'Settings', screen)
BTN_ABOUT = button(300, 330, 180, 60, 'About', screen)


while 1:
    screen.fill(CLR_BG)
    if BTN_PLAY.draw_button(FONT, clicked):
        WINDOW_PLAY.run()

    if BTN_QUIT.draw_button(FONT, clicked):
        pygame.quit()
        sys.exit()

    if BTN_SETTINGS.draw_button(FONT, clicked):
        pygame.init()

        white = (255, 255, 255)
        blue = (2, 38, 41)
        font = pygame.font.Font("Courier.ttf", 20)
        text = font.render(
            'This part is still under development.', False, white)
        done = False
        while not done:
            screen.fill(blue)
            screen.blit(text, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    if BTN_ABOUT.draw_button(FONT, clicked):

        pygame.init()

        screen = pygame.display.set_mode((screen_width, screen_height))
        FPS = 30
        clock = pygame.time.Clock()

        blue = ("#022629")
        white = (255, 255, 255)

        def blit_text(surface, text, pos, font, color=pygame.Color('white')):
            # 2D array where each row is a list of words.
            words = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]  # The width of a space.
            max_width, max_height = surface.get_size()
            x, y = pos
            for line in words:
                for word in line:
                    word_surface = font.render(word, 0, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    surface.blit(word_surface, (x, y))
                    x += word_width + space
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.

        text = "This Pong Game is made by Jayvee Torres and Addy Casil.\n" \
               "TUTORIAL:\n" \
               "To control the player 1's paddle press \"W\" and \"S\".\n" \
               "To control the player 2's paddle press key \"UP\" and key \"DOWN\".\n" \
               "MECHANICS:\n" \
               "This game has two players. It consist of two paddle and a ball.The two players should back bounce the ball to their opponent using their paddle to score.\n"
        font = pygame.font.SysFont('Courier', 20)
        done = False
        while not done:

            dt = clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(pygame.Color('#022629'))
            blit_text(screen, text, (20, 20), font)
            pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    FONT2 = pygame.font.Font(PATH_FNT2, 50)
    title = FONT2.render('Pong Game', True, CLR_BLACK, CLR_BG)
    textRect = title.get_rect()
    textRect.center = (400, 30)
    screen.blit(title, textRect)
    pygame.display.update()


pygame.quit()
