import sys
import random
import pygame
import pygame_menu
from pygame.locals import *
from settings import *


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, x_pos, y_pos, pong):
        super().__init__(pong.imgpaddle, x_pos, y_pos)
        self.speed = pong.player_speed
        self.movement = 0
        self.screen_height = pong.height

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None, FONT_EXTERNAL=FONT['courier']):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                                            2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(FONT_EXTERNAL, 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Ball(Block):
    def __init__(self, x_pos, y_pos,  pong):
        super().__init__(pong.imgball, x_pos, y_pos)
        speed_x, speed_y = pong.ball_speed
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = pong.paddle_grp
        self.active = False
        self.score_time = 0
        self.font = pong.fnt1
        self.screen = pong.screen
        self.scr_width = pong.width
        self.scr_height = pong.height
        self.collision_sound = pong.snd_collision
        self.score_sound = pong.snd_score
        self.first_run = True
        self.music = pong.music

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.scr_height:
            if(self.music == True):
                pygame.mixer.Sound.play(self.collision_sound)

            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            if(self.music == True):
                pygame.mixer.Sound.play(self.collision_sound)

            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        if(self.first_run == True):
            self.direction = random.choice((-1, 1))
            self.first_run = False

        self.active = False
        self.speed_x *= self.direction
        self.speed_y *= self.direction
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (self.scr_width / 2, self.scr_height / 2)
        pygame.mixer.Sound.play(self.score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 800:
            countdown_number = 5
        if 800 < current_time - self.score_time <= 1600:
            countdown_number = 4
        if 1600 < current_time - self.score_time <= 2400:
            countdown_number = 3
        if 2400 < current_time - self.score_time <= 3200:
            countdown_number = 2
        if 3200 < current_time - self.score_time <= 4000:
            countdown_number = 1
        if current_time - self.score_time >= 4000:
            self.active = True

        time_counter = self.font.render(
            str(countdown_number), True, COLOR['black'])
        time_counter_rect = time_counter.get_rect(
            center=(self.scr_width / 2, self.scr_height / 2 + 50))
        pygame.draw.rect(self.screen, COLOR['blue'], time_counter_rect)
        self.screen.blit(time_counter, time_counter_rect)


class GameManager:
    def __init__(self, pong):
        self.screen = pong.screen
        self.p1_score = 0
        self.p2_score = 0
        self.ball_group = pong.ball_sprite
        self.paddle_group = pong.paddle_grp
        self.scr_width = pong.width
        self.scr_height = pong.height
        self.font = pong.fnt1
        self.player1_name = pong.player1_name
        self.player2_name = pong.player2_name

    def run_game(self):
        self.paddle_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= self.scr_width:
            self.direction = 1
            self.p1_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.direction = -1
            self.p2_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        p2_score = self.font.render(
            self.player2_name + " - " + str(self.p2_score), True, COLOR['white'])
        p1_score = self.font.render(
            self.player1_name + " - " + str(self.p1_score), True,  COLOR['white'])

        p2_score_rect = p2_score.get_rect(
            midleft=(self.scr_width / 2 + 40, self.scr_height / 2))
        p1_score_rect = p1_score.get_rect(
            midright=(self.scr_width / 2 - 40, self.scr_height / 2))

        self.screen.blit(p1_score, p1_score_rect)
        self.screen.blit(p2_score, p2_score_rect)


class Pong:
    def __init__(self):
        self.bgcolor = WIN['pong_bgcolor']
        self.size = self.width, self.height = WIN["width"], WIN["height"]
        self.title = WIN["title"]
        self.icon = WIN["icon"]
        self.sndpong = AUDIO['pong']
        self.sndscore = AUDIO['score']
        self.imgpaddle = IMG['paddle']
        self.imgball = IMG['ball']
        self.player_speed = WIN['player_speed']
        self.fntcourier = FONT['courier']
        self.fntelfboy = FONT['elfboy']
        self.ball_speed = WIN['ball_speed']
        self.score_limit = WIN['score_limit']
        self.music = WIN['music']
        self.player1_name = WIN['player1_name']
        self.player2_name = WIN['player2_name']
        self.difficulty = None

    def run(self, pg, screen):
        self.screen = screen
        if(self.difficulty != None and self.difficulty > 0):
            self.ball_speed = self.difficulty * 2

        self.ball_speed = self.ball_speed, self.ball_speed
        # pygame.init()

        self.fnt1 = pygame.font.Font(self.fntcourier, 30)
        self.fnt2 = pygame.font.Font(self.fntelfboy, 50)

        # self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.bgcolor)
        logo = pygame.image.load(self.icon)
        pygame.display.set_icon(logo)
        pygame.display.set_caption(self.title)

        pygame.mixer.pre_init(44100, -16, 2, 512)

        self.clock = pygame.time.Clock()

        self.snd_collision = pygame.mixer.Sound(self.sndpong)
        self.snd_score = pygame.mixer.Sound(self.sndscore)

        self.midline = pygame.Rect(self.width / 2 - 2, 0, 4, self.height)

        self.p1 = Player(self.width - 20, self.height / 2, self)
        self.p2 = Player(20, self.width / 2, self)

        self.paddle_grp = pygame.sprite.Group()
        self.paddle_grp.add(self.p2)
        self.paddle_grp.add(self.p1)

        self.ball = Ball(self.width / 2, self.height / 2, self)

        self.ball_sprite = pygame.sprite.GroupSingle()
        self.ball_sprite.add(self.ball)

        self.game_mgr = GameManager(self)
        self.playing = True

        btm = Button(COLOR['yellow'], 200, 200, 400, 80, "Back to Main Menu")

        self.running = True

        while self.running:
            self.screen.fill(self.bgcolor)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if self.playing and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.p1.movement -= self.p1.speed
                    if event.key == pygame.K_DOWN:
                        self.p1.movement += self.p1.speed
                    if event.key == pygame.K_w:
                        self.p2.movement -= self.p2.speed
                    if event.key == pygame.K_s:
                        self.p2.movement += self.p2.speed
                if self.playing and event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.p1.movement += self.p1.speed
                    if event.key == pygame.K_DOWN:
                        self.p1.movement -= self.p1.speed
                    if event.key == pygame.K_w:
                        self.p2.movement += self.p2.speed
                    if event.key == pygame.K_s:
                        self.p2.movement -= self.p2.speed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.playing and btm.isOver(mouse_pos):
                        self.running = False
                        break
                if event.type == pygame.MOUSEMOTION:
                    if btm.isOver(mouse_pos):
                        btm.color = COLOR['white']
                    else:
                        btm.color = COLOR['yellow']

            if self.playing:
                pygame.draw.rect(self.screen, COLOR['black'], self.midline)
                self.game_mgr.run_game()
                if self.game_mgr.p1_score >= self.score_limit or self.game_mgr.p2_score >= self.score_limit:
                    self.playing = False

            elif not self.playing and self.running:

                if self.game_mgr.p1_score >= self.score_limit:
                    winner_name = self.player1_name
                else:
                    winner_name = self.player2_name

                try:
                    self.winner = self.fnt2.render(
                        winner_name + " Wins", True, COLOR['white'], WIN['pong_bgcolor'])
                    self.winnerRect = self.winner.get_rect()
                    self.winnerRect.center = (400, 100)
                    self.screen.blit(self.winner, self.winnerRect)

                    btm.draw(self.screen, COLOR['black'])
                except:
                    break
            pygame.display.update()
            self.clock.tick(100)


settings = {
    "player1_name": WIN['player1_name'],
    "player2_name": WIN['player2_name'],
    "difficulty": 2,
    "music": WIN['music'],
    "score_limit": WIN['score_limit']
}

pygame.init()
surface = pygame.display.set_mode((WIN['width'], WIN['height']))

pygame.display.set_caption(WIN['title'])
pygame.mixer.music.load(WIN['bgmusic'])
if settings['music']:
    pygame.mixer.music.play()
JAicon = pygame.image.load(WIN['icon'])
pygame.display.set_icon(JAicon)

game = Pong()


def set_difficulty(value, difficulty):
    settings['difficulty'] = difficulty


def set_p1name(name):
    settings["player1_name"] = name


def set_music(name, switch):
    settings['music'] = switch
    if switch == False:
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play()


def set_max_score(name, limit):
    settings['score_limit'] = limit


def set_p2name(name):
    settings["player2_name"] = name


def start_the_game():
    game.player1_name = settings['player1_name']
    game.player2_name = settings['player2_name']
    game.difficulty = settings['difficulty']
    game.player1_name = settings['player1_name']
    game.music = settings['music']
    game.score_limit = settings['score_limit']
    game.run(pygame, surface)


def open_leaderboard():
    pass


menu = pygame_menu.Menu(WIN['height'], WIN['width'], 'MAIN MENU',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Player 1 name :',
                    default=settings['player1_name'], onchange=set_p1name)
menu.add_text_input('Player 2 name :',
                    default=settings['player2_name'], onchange=set_p2name)
menu.add_selector(
    'Difficulty: ', [('Normal', 2), ('Hard', 3), ('Easy', 1)], onchange=set_difficulty)
menu.add_selector(
    'Music: ', [('On', True), ('Off', False)], onchange=set_music)
menu.add_selector(
    'Max Score: ', [('5', 5), ('10', 10), ('20', 20), ('50', 50)], onchange=set_max_score)
menu.add_button('Play', start_the_game)
menu.add_button('Leaderboard', open_leaderboard)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
