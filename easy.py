import pygame, sys, random
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 500
extra_color = (0, 0, 0)
bg = (255, 181, 0)
blue = (2, 38, 41)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('OOP PROJECT')
pygame.mixer.music.load("bgfor2d.mp3")
pygame.mixer.music.play()
font = pygame.font.SysFont('Courier', 20)
JAicon = pygame.image.load('JAlogo.png')
pygame.display.set_icon(JAicon)

clicked = False


class button():
    button_col = red
    hover_col = blue
    click_col = black
    text_col = white
    width = 180
    height = 60

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):
        pygame.init()
        global clicked
        action = False

        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        pygame.draw.line(screen, black, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, black, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action


play = button(300, 80, 'Play now')
settings = button(300, 170, 'Settings')
about = button(300, 250, 'About')
quit = button(300, 330, 'Quit')

run = True
while run:

    screen.fill(bg)

    if play.draw_button():

        clicked = False

        class button1():
            button_color1 = red
            hover_color1 = blue
            click_color1 = black
            text_color1 = white
            x = 180
            y = 60

            def __init__(self, x, y, text):
                self.abscissa = x
                self.vertical = y
                self.text = text

            def draw_button1(self):

                global clicked
                action = False

                pos = pygame.mouse.get_pos()

                button1_rect = Rect(self.abscissa, self.vertical, self.x, self.y)

                if button1_rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1:
                        clicked = True
                        pygame.draw.rect(screen, self.click_color1, button1_rect)
                    elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                        clicked = False
                        action = True
                    else:
                        pygame.draw.rect(screen, self.hover_color1, button1_rect)
                else:
                    pygame.draw.rect(screen, self.button_color1, button1_rect)

                pygame.draw.line(screen, black, (self.abscissa, self.vertical),
                                 (self.abscissa + self.x, self.vertical), 2)
                pygame.draw.line(screen, black, (self.abscissa, self.vertical),
                                 (self.abscissa, self.vertical + self.y), 2)
                pygame.draw.line(screen, black, (self.abscissa, self.vertical + self.y),
                                 (self.abscissa + self.x, self.vertical + self.y), 2)
                pygame.draw.line(screen, black, (self.abscissa + self.x, self.vertical),
                                 (self.abscissa + self.x, self.vertical + self.y), 2)

                text_img1 = font.render(self.text, True, self.text_color1)
                text_len1 = text_img1.get_width()
                screen.blit(text_img1, (self.abscissa + int(self.x / 2) - int(text_len1 / 2), self.vertical + 25))
                return action

        easy = button1(300, 80, 'Easy')
        medium = button1(300, 160, 'Medium')
        hard = button1(300, 240, 'Hard')

        run = True
        while run:
            screen.fill(bg)

            if easy.draw_button1():

                class Block(pygame.sprite.Sprite):
                    def __init__(self, path, x_pos, y_pos):
                        super().__init__()
                        self.image = pygame.image.load(path)
                        self.rect = self.image.get_rect(center=(x_pos, y_pos))


                class Player1(Block):
                    def __init__(self, path, x_pos, y_pos, speed):
                        super().__init__(path, x_pos, y_pos)
                        self.speed = speed * 0.5
                        self.movement = 0

                    def screen_constrain(self):
                        if self.rect.top <= 0:
                            self.rect.top = 0
                        if self.rect.bottom >= screen_height:
                            self.rect.bottom = screen_height

                    def update(self, ball_group):
                        self.rect.y += self.movement
                        self.screen_constrain()


                class Player2(Block):
                    def __init__(self, path, x_pos, y_pos, speed):
                        super().__init__(path, x_pos, y_pos)
                        self.speed = speed * 0.5
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
                        self.speed_x = speed_x * 0.5
                        self.speed_y = speed_y * 0.5
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
                            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
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
                        self.speed_x *= 0.5
                        self.speed_y *= 0.5
                        self.score_time = pygame.time.get_ticks()
                        self.rect.center = (screen_width / 2, screen_height / 2)
                        pygame.mixer.Sound.play(score_sound)

                    def restart_counter(self):
                        current_time = pygame.time.get_ticks()
                        countdown_number = 5

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
                        time_counter = font.render(str(countdown_number), True, extra_color)
                        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
                        pygame.draw.rect(screen, blue, time_counter_rect)
                        screen.blit(time_counter, time_counter_rect)


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
                        player1_score = font.render(str(self.player1_score), True, extra_color)
                        player2_score = font.render(str(self.player2_score), True, extra_color)

                        player1_score_rect = player1_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
                        player2_score_rect = player2_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

                        screen.blit(player1_score, player1_score_rect)
                        screen.blit(player2_score, player2_score_rect)

                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.init()
                clock = pygame.time.Clock()

                screen_width = 800
                screen_height = 500
                screen = pygame.display.set_mode((screen_width, screen_height))
                collision_sound = pygame.mixer.Sound("pong.ogg")
                score_sound = pygame.mixer.Sound("score.ogg")
                midline = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)


                player1 = Player1('Paddle.jpg', 20, screen_height / 2, 5)
                player2 = Player2('Paddle.jpg', screen_width - 20, screen_height / 2, 5)
                paddle_group = pygame.sprite.Group()
                paddle_group.add(player1)
                paddle_group.add(player2)

                ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
                ball_sprite = pygame.sprite.GroupSingle()
                ball_sprite.add(ball)

                game_manager = GameManager(ball_sprite, paddle_group)

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_w:
                                player1.movement -= player1.speed
                            if event.key == pygame.K_s:
                                player1.movement += player1.speed
                            if event.key == pygame.K_UP:
                                player2.movement -= player2.speed
                            if event.key == pygame.K_DOWN:
                                player2.movement += player2.speed
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_w:
                                player1.movement += player1.speed
                            if event.key == pygame.K_s:
                                player1.movement -= player1.speed
                            if event.key == pygame.K_UP:
                                player2.movement += player2.speed
                            if event.key == pygame.K_DOWN:
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
            if medium.draw_button1():
                class Block(pygame.sprite.Sprite):
                    def __init__(self, path, x_pos, y_pos):
                        super().__init__()
                        self.image = pygame.image.load(path)
                        self.rect = self.image.get_rect(center=(x_pos, y_pos))


                class Player1(Block):
                    def __init__(self, path, x_pos, y_pos, speed):
                        super().__init__(path, x_pos, y_pos)
                        self.speed = speed * 1
                        self.movement = 0

                    def screen_constrain(self):
                        if self.rect.top <= 0:
                            self.rect.top = 0
                        if self.rect.bottom >= screen_height:
                            self.rect.bottom = screen_height

                    def update(self, ball_group):
                        self.rect.y += self.movement
                        self.screen_constrain()


                class Player2(Block):
                    def __init__(self, path, x_pos, y_pos, speed):
                        super().__init__(path, x_pos, y_pos)
                        self.speed = speed * 1
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
                        self.speed_x = speed_x * 0.75
                        self.speed_y = speed_y * 0.75
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
                            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
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
                        self.speed_x *= 0.75
                        self.speed_y *= 0.75
                        self.score_time = pygame.time.get_ticks()
                        self.rect.center = (screen_width / 2, screen_height / 2)
                        pygame.mixer.Sound.play(score_sound)

                    def restart_counter(self):
                        current_time = pygame.time.get_ticks()
                        countdown_number = 5

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
                        time_counter = font.render(str(countdown_number), True, extra_color)
                        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
                        pygame.draw.rect(screen, blue, time_counter_rect)
                        screen.blit(time_counter, time_counter_rect)


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
                        player1_score = font.render(str(self.player1_score), True, extra_color)
                        player2_score = font.render(str(self.player2_score), True, extra_color)

                        player1_score_rect = player1_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
                        player2_score_rect = player2_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

                        screen.blit(player1_score, player1_score_rect)
                        screen.blit(player2_score, player2_score_rect)


                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.init()
                clock = pygame.time.Clock()

                screen_width = 800
                screen_height = 500
                screen = pygame.display.set_mode((screen_width, screen_height))
                collision_sound = pygame.mixer.Sound("pong.ogg")
                score_sound = pygame.mixer.Sound("score.ogg")
                midline = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

                player1 = Player1('Paddle.jpg', 20, screen_height / 2, 5)
                player2 = Player2('Paddle.jpg', screen_width - 20, screen_height / 2, 5)
                paddle_group = pygame.sprite.Group()
                paddle_group.add(player1)
                paddle_group.add(player2)

                ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
                ball_sprite = pygame.sprite.GroupSingle()
                ball_sprite.add(ball)

                game_manager = GameManager(ball_sprite, paddle_group)

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_w:
                                player1.movement -= player1.speed
                            if event.key == pygame.K_s:
                                player1.movement += player1.speed
                            if event.key == pygame.K_UP:
                                player2.movement -= player2.speed
                            if event.key == pygame.K_DOWN:
                                player2.movement += player2.speed
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_w:
                                player1.movement += player1.speed
                            if event.key == pygame.K_s:
                                player1.movement -= player1.speed
                            if event.key == pygame.K_UP:
                                player2.movement += player2.speed
                            if event.key == pygame.K_DOWN:
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
            if hard.draw_button1():
                class Block(pygame.sprite.Sprite):
                    def __init__(self, path, x_pos, y_pos):
                        super().__init__()
                        self.image = pygame.image.load(path)
                        self.rect = self.image.get_rect(center=(x_pos, y_pos))


                class Player1(Block):
                    def __init__(self, path, x_pos, y_pos, speed):
                        super().__init__(path, x_pos, y_pos)
                        self.speed = speed * 1.5
                        self.movement = 0

                    def screen_constrain(self):
                        if self.rect.top <= 0:
                            self.rect.top = 0
                        if self.rect.bottom >= screen_height:
                            self.rect.bottom = screen_height

                    def update(self, ball_group):
                        self.rect.y += self.movement
                        self.screen_constrain()


                class Player2(Block):
                    def __init__(self, path, x_pos, y_pos, speed):
                        super().__init__(path, x_pos, y_pos)
                        self.speed = speed * 1.5
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
                        self.speed_x = speed_x * 1.5
                        self.speed_y = speed_y * 1.5
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
                            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
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
                        self.speed_x *= 1.5
                        self.speed_y *= 1.5
                        self.score_time = pygame.time.get_ticks()
                        self.rect.center = (screen_width / 2, screen_height / 2)
                        pygame.mixer.Sound.play(score_sound)

                    def restart_counter(self):
                        current_time = pygame.time.get_ticks()
                        countdown_number = 5

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
                        time_counter = font.render(str(countdown_number), True, extra_color)
                        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
                        pygame.draw.rect(screen, blue, time_counter_rect)
                        screen.blit(time_counter, time_counter_rect)


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
                        player1_score = font.render(str(self.player1_score), True, extra_color)
                        player2_score = font.render(str(self.player2_score), True, extra_color)

                        player1_score_rect = player1_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
                        player2_score_rect = player2_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

                        screen.blit(player1_score, player1_score_rect)
                        screen.blit(player2_score, player2_score_rect)


                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.init()
                clock = pygame.time.Clock()

                screen_width = 800
                screen_height = 500
                screen = pygame.display.set_mode((screen_width, screen_height))
                collision_sound = pygame.mixer.Sound("pong.ogg")
                score_sound = pygame.mixer.Sound("score.ogg")
                midline = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

                player1 = Player1('Paddle.jpg', 20, screen_height / 2, 5)
                player2 = Player2('Paddle.jpg', screen_width - 20, screen_height / 2,5)
                paddle_group = pygame.sprite.Group()
                paddle_group.add(player1)
                paddle_group.add(player2)

                ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
                ball_sprite = pygame.sprite.GroupSingle()
                ball_sprite.add(ball)

                game_manager = GameManager(ball_sprite, paddle_group)

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_w:
                                player1.movement -= player1.speed
                            if event.key == pygame.K_s:
                                player1.movement += player1.speed
                            if event.key == pygame.K_UP:
                                player2.movement -= player2.speed
                            if event.key == pygame.K_DOWN:
                                player2.movement += player2.speed
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_w:
                                player1.movement += player1.speed
                            if event.key == pygame.K_s:
                                player1.movement -= player1.speed
                            if event.key == pygame.K_UP:
                                player2.movement += player2.speed
                            if event.key == pygame.K_DOWN:
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            font2 = pygame.font.Font('elf boy.ttf', 60)
            title = font2.render('PONG GAME', True, white, black)
            textRect = title.get_rect()
            textRect.center = (389, 30)
            screen.blit(title, textRect)
            pygame.display.update()

        pygame.quit()

    if settings.draw_button():
        pygame.init()

        white = (255, 255, 255)
        blue = (2, 38, 41)
        font = pygame.font.Font("Courier.ttf", 20)
        text = font.render('This part is still under development.', False, white)
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
    if quit.draw_button():
        pygame.quit()
        sys.exit()

    if about.draw_button():
        pygame.init()

        screen = pygame.display.set_mode((screen_width, screen_height))
        FPS = 30
        clock = pygame.time.Clock()

        blue = ("#022629")
        white = (255, 255, 255)


        def blit_text(surface, text, pos, font, color=pygame.Color('white')):
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
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
            run = False
    font2 = pygame.font.Font('elf boy.ttf', 60)
    title = font2.render('PONG GAME', True, white, black)
    textRect = title.get_rect()
    textRect.center = (389, 30)
    screen.blit(title, textRect)
    pygame.display.update()

pygame.quit()

