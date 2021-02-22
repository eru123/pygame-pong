import sys
import random
import pygame as pg
from settings import FONT, COLOR, AUDIO, WIN, IMG


class Block(pg.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pg.image.load(path)
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

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.scr_height:
            pg.mixer.Sound.play(self.collision_sound)
            self.speed_y *= -1

        if pg.sprite.spritecollide(self, self.paddles, False):
            pg.mixer.Sound.play(self.collision_sound)
            collision_paddle = pg.sprite.spritecollide(
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
        self.score_time = pg.time.get_ticks()
        self.rect.center = (self.scr_width / 2, self.scr_height / 2)
        pg.mixer.Sound.play(self.score_sound)

    def restart_counter(self):
        current_time = pg.time.get_ticks()
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
        pg.draw.rect(self.screen, COLOR['blue'], time_counter_rect)
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

    def run_game(self):
        self.paddle_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= self.scr_width:
            self.p2_score += 1
            self.direction = 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.direction = -1
            self.p1_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        p1_score = self.font.render(
            str(self.p1_score), True, COLOR['black'])
        p2_score = self.font.render(
            str(self.p2_score), True,  COLOR['black'])

        p1_score_rect = p1_score.get_rect(
            midleft=(self.scr_width / 2 + 40, self.scr_height / 2))
        p2_score_rect = p2_score.get_rect(
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
        self.ball_speed = WIN['ball_speed']

    def run(self):
        self.ball_speed = self.ball_speed, self.ball_speed

        pg.init()

        self.fnt1 = pg.font.Font(self.fntcourier, 50)
        self.screen = pg.display.set_mode(self.size)
        self.screen.fill(self.bgcolor)
        logo = pg.image.load(self.icon)
        pg.display.set_icon(logo)
        pg.display.set_caption(self.title)
        pg.display.flip()

        pg.mixer.pre_init(44100, -16, 2, 512)

        self.clock = pg.time.Clock()

        self.snd_collision = pg.mixer.Sound(self.sndpong)
        self.snd_score = pg.mixer.Sound(self.sndscore)

        self.midline = pg.Rect(self.width / 2 - 2, 0, 4, self.height)

        self.p1 = Player(self.width - 20, self.height / 2, self)
        self.p2 = Player(20, self.width / 2, self)

        self.paddle_grp = pg.sprite.Group()
        self.paddle_grp.add(self.p2)
        self.paddle_grp.add(self.p1)

        self.ball = Ball(self.width / 2, self.height / 2, self)

        self.ball_sprite = pg.sprite.GroupSingle()
        self.ball_sprite.add(self.ball)

        self.game_mgr = GameManager(self)

        while True:
            self.screen.fill(self.bgcolor)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.p1.movement -= self.p1.speed
                    if event.key == pg.K_DOWN:
                        self.p1.movement += self.p1.speed
                    if event.key == pg.K_w:
                        self.p2.movement -= self.p2.speed
                    if event.key == pg.K_s:
                        self.p2.movement += self.p2.speed
                if event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        self.p1.movement += self.p1.speed
                    if event.key == pg.K_DOWN:
                        self.p1.movement -= self.p1.speed
                    if event.key == pg.K_w:
                        self.p2.movement += self.p2.speed
                    if event.key == pg.K_s:
                        self.p2.movement -= self.p2.speed

            pg.draw.rect(self.screen, COLOR['black'], self.midline)
            self.game_mgr.run_game()
            pg.display.flip()
            self.clock.tick(120)


game = Pong()
game.run()
