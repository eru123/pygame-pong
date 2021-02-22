import pygame
import sys
import random
from pygame.locals import *

pygame.init()


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player1(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(collision_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(collision_sound)
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
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

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

        time_counter = font.render(
            str(countdown_number), True, extra_color)
        time_counter_rect = time_counter.get_rect(
            center=(screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, blue, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class Player2(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player1_score = 0
        self.player2_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.player2_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player1_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player1_score = font.render(
            str(self.player1_score), True, extra_color)
        player2_score = font.render(
            str(self.player2_score), True, extra_color)

        player1_score_rect = player1_score.get_rect(
            midleft=(screen_width / 2 + 40, screen_height / 2))
        player2_score_rect = player2_score.get_rect(
            midright=(screen_width / 2 - 40, screen_height / 2))

        screen.blit(player1_score, player1_score_rect)
        screen.blit(player2_score, player2_score_rect)


class play():
    def run():
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        clock = pygame.time.Clock()

        screen_width = 800
        screen_height = 500
        screen = pygame.display.set_mode((screen_width, screen_height))
        collision_sound = pygame.mixer.Sound("pong.ogg")
        score_sound = pygame.mixer.Sound("score.ogg")
        midline = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

        player1 = Player1('Paddle.jpg', screen_width -
                          20, screen_height / 2, 5)

        player2 = Player2('Paddle.jpg', 20, screen_width / 2, 5)
        paddle_group = pygame.sprite.Group()
        paddle_group.add(player1)
        paddle_group.add(player2)

        ball = Ball('Ball.png', screen_width / 2,
                    screen_height / 2, 4, 4, paddle_group)
        ball_sprite = pygame.sprite.GroupSingle()
        ball_sprite.add(ball)

        game_manager = GameManager(ball_sprite, paddle_group)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player1.movement -= player1.speed
                    if event.key == pygame.K_DOWN:
                        player1.movement += player1.speed
                    if event.key == pygame.K_w:
                        player2.movement -= player2.speed
                    if event.key == pygame.K_s:
                        player2.movement += player2.speed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player1.movement += player1.speed
                    if event.key == pygame.K_DOWN:
                        player1.movement -= player1.speed
                    if event.key == pygame.K_w:
                        player2.movement += player2.speed
                    if event.key == pygame.K_s:
                        player2.movement -= player2.speed
            screen.fill(blue)
            pygame.draw.rect(screen, extra_color, midline)
            game_manager.run_game()
            pygame.display.flip()
            clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
