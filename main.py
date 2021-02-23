import random
import pygame
import pygame_menu
from settings import *

print("************************************")
print("*        >> PONG GAME <<           *")
print("*              BY                  *")
print("*                                  *")
print("*         JAYVEE TORRES            *")
print("*          ADDY CASIL              *")
print("************************************")


# For creating game object that will
# be used for moving objects and collision
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):

        # Initialize Sprite
        super().__init__()

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


# Player object for creating paddle game object
class Player(Block):
    def __init__(self, x_pos, y_pos, pong):
        # Initialize Block Object as Parent Class
        super().__init__(pong.imgpaddle, x_pos, y_pos)
        self.speed = pong.player_speed
        self.movement = 0
        self.screen_height = pong.height

    # Maintain Player Position
    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    # Update Position
    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


# Used to make 'back to main menu' after a game session
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


# Used to create ball object
class Ball(Block):

    # Create Ball Object Instance
    def __init__(self, x_pos, y_pos,  pong):

        # Create Block Object Instance
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
        self.music = pong.music
        self.direction = random.choice((-1, 1))

    # Update Ball Position
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    # Detect Collisions
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.scr_height:

            # Play Collide Sound If music is On
            # and if the ball is collided to boundaries
            if(self.music == True):
                pygame.mixer.Sound.play(self.collision_sound)

            # Update Ball Y axis Position
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):

            # Play Collide Sound If music is On
            # and if the ball is collided to Player
            if(self.music == True):
                pygame.mixer.Sound.play(self.collision_sound)

            # Detect collision from Player and
            # change trajectory of the ball
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

    # Reset Ball Position From the start
    def reset_ball(self):
        self.active = False
        self.speed_x *= self.direction
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (self.scr_width / 2, self.scr_height / 2)

        if(self.music == True):
            pygame.mixer.Sound.play(self.score_sound)

    # Reset Ball Serving Time Countdown
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


# Object for managing Game Objects, Collisions and Score
class GameManager:

    # Initialize GameManager
    # Pass 'pong' variable as parameter
    # to pass data from Pong() Object
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
        self.score_limit = pong.score_limit
    # Method to start the game

    def run_game(self):
        self.paddle_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    # Reset Ball Position, Timer, and Update Player Score
    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= self.scr_width:
            self.p1_score += 1
            self.ball_group.sprite.reset_ball()

            if(self.p1_score >= self.score_limit):
                settings['score_player1'] += 1

        if self.ball_group.sprite.rect.left <= 0:
            self.p2_score += 1
            self.ball_group.sprite.reset_ball()

            if(self.p2_score >= self.score_limit):
                settings['score_player2'] += 1

        # Change to 1 to set the ball trajectory
        # to player who lose the ball
        # Change to -1 to set the ball trajectory to scorer
        self.ball_group.sprite.direction = 1

    # Update Score Board

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


# Main Pong Game Object
class Pong:
    # Initialize Pong Instance Object
    def __init__(self):
        # Initialize Configuration and Resources
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

    # Run pong Game
    def run(self, pg, screen):

        # Set initialized screen object from
        # pygame to be used by pong window
        self.screen = screen

        # Set defficulty
        if(self.difficulty != None and self.difficulty > 0):
            # Dificulty value is multiplied by 2 as Ball speed
            self.ball_speed = self.difficulty * 2

        # Set Ball Speed
        self.ball_speed = self.ball_speed, self.ball_speed

        # Initialize Courier Font for Later use
        self.fnt1 = pygame.font.Font(self.fntcourier, 30)

        # Initialize Elf-Boy Font for Later use
        self.fnt2 = pygame.font.Font(self.fntelfboy, 50)

        # screen config
        self.screen.fill(self.bgcolor)          # Set Window Background Color
        logo = pygame.image.load(self.icon)
        pygame.display.set_icon(logo)           # Set Window Icon/Logo
        pygame.display.set_caption(self.title)  # Set Window Title

        pygame.mixer.pre_init(44100, -16, 2, 512)

        # get clock object from pygame
        self.clock = pygame.time.Clock()

        # Initialize Sounds to be used
        self.snd_collision = pygame.mixer.Sound(self.sndpong)
        self.snd_score = pygame.mixer.Sound(self.sndscore)

        # Center Line
        self.midline = pygame.Rect(self.width / 2 - 2, 0, 4, self.height)

        # Create Player
        self.p1 = Player(self.width - 20, self.height / 2, self)
        self.p2 = Player(20, self.width / 2, self)

        # Create Paddle Group
        # For player 1 and player 2
        self.paddle_grp = pygame.sprite.Group()
        self.paddle_grp.add(self.p2)
        self.paddle_grp.add(self.p1)

        # Create Ball Object
        self.ball = Ball(self.width / 2, self.height / 2, self)

        self.ball_sprite = pygame.sprite.GroupSingle()
        self.ball_sprite.add(self.ball)

        # Creat GameManager Object
        self.game_mgr = GameManager(self)
        self.playing = True
        self.running = True

        # Back to main Menu Button
        btm = Button(COLOR['yellow'], 200, 200, 400, 80, "Back to Main Menu")

        # Main Game Loop
        while self.running:

            # Set Game Window Background
            self.screen.fill(self.bgcolor)

            # Get Mouse Position
            mouse_pos = pygame.mouse.get_pos()

            # Event Listener
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

            # On finished game session
            # Show winner name
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
                    # Winner Announcement
                    self.winner = self.fnt2.render(
                        winner_name + " Wins", True, COLOR['white'], WIN['pong_bgcolor'])
                    self.winnerRect = self.winner.get_rect()
                    self.winnerRect.center = (400, 100)
                    self.screen.blit(self.winner, self.winnerRect)

                    btm.draw(self.screen, COLOR['black'])
                except:
                    break

            # Update Pygame
            pygame.display.update()

            # Game Clock Speed
            self.clock.tick(100)


# Configurable Settings by the user/player
settings = {
    "player1_name": WIN['player1_name'],
    "player2_name": WIN['player2_name'],
    "difficulty": 2,
    "music": WIN['music'],
    "score_limit": WIN['score_limit'],
    "score_player1": 0,
    "score_player2": 0,
    "theme": pygame_menu.themes.THEME_BLUE
}

# Initialuize PyGame
pygame.init()

# Initialize Screen
surface = pygame.display.set_mode((WIN['width'], WIN['height']))


# PyGame Window Configuration
pygame.display.set_caption(WIN['title'])
pygame.mixer.music.load(WIN['bgmusic'])
if settings['music']:
    pygame.mixer.music.play()
JAicon = pygame.image.load(WIN['icon'])
pygame.display.set_icon(JAicon)


# Create Pong Game Object
game = Pong()


# Set Difficulty of The Game
def set_difficulty(value, difficulty):
    settings['difficulty'] = difficulty


# Set Player 1 name
def set_p1name(name):
    settings["player1_name"] = name


# Set Music On/Off
def set_music(name, switch):
    settings['music'] = switch
    if switch == False:
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play()


# Set Max Score Limit
def set_max_score(name, limit):
    settings['score_limit'] = limit


# Set Player 2 name
def set_p2name(name):
    settings["player2_name"] = name


# Theme Switcher
def change_theme(name, theme):
    settings['theme'] = theme

# Start The Game method
# Apply user settings to Game


def start_the_game():
    game.player1_name = settings['player1_name']
    game.player2_name = settings['player2_name']
    game.difficulty = settings['difficulty']
    game.player1_name = settings['player1_name']
    game.music = settings['music']
    game.score_limit = settings['score_limit']
    game.run(pygame, surface)


# Leader board
def open_leaderboard():

    # Leader Board Dictionary Schema
    lb = {"1": {"name": "",  "wins": 0},  "2": {"name": "", "wins": 0}}

    # Create Leader Board Data
    if settings['score_player1'] >= settings['score_player1']:
        lb["1"]["name"] = settings['player1_name']
        lb["1"]["wins"] = settings['score_player1']
        lb["2"]["name"] = settings['player2_name']
        lb["2"]["wins"] = settings['score_player2']
    else:
        lb["2"]["name"] = settings['player1_name']
        lb["2"]["wins"] = settings['score_player1']
        lb["1"]["name"] = settings['player2_name']
        lb["1"]["wins"] = settings['score_player2']

    # Create Leader board window
    lb_window = pygame_menu.Menu(
        WIN['height'], WIN['width'], 'LEADERBOARD', theme=settings['theme'])
    lb_window.add_label("1. " + lb['1']['name'] +
                        " - " + str(lb['1']['wins']) + " Wins")
    lb_window.add_label("2. " + lb['2']['name'] +
                        " - " + str(lb['2']['wins']) + " Wins")

    # Back to main menu
    lb_window.add_button('BACK', create_main_menu)

    lb_window.mainloop(surface)


# Settings Menu Window
def create_settings_window():
    cog = pygame_menu.Menu(WIN['height'], WIN['width'],
                           'SETTINGS', theme=settings['theme'])

    cog.add_text_input('Player 1 name :',
                       default=settings['player1_name'], onchange=set_p1name)
    cog.add_text_input('Player 2 name :',
                       default=settings['player2_name'], onchange=set_p2name)
    cog.add_selector(
        'Difficulty: ', [('Normal', 2), ('Hard', 3), ('Easy', 1)], onchange=set_difficulty)
    cog.add_selector(
        'Music: ', [('On', True), ('Off', False)], onchange=set_music)
    cog.add_selector(
        'Max Score: ', [('5', 5), ('10', 10), ('20', 20), ('50', 50)], onchange=set_max_score)
    cog.add_selector('Theme: ', [
        ('BLUE', pygame_menu.themes.THEME_BLUE),
        ('DARK', pygame_menu.themes.THEME_DARK),
        ('GREEN', pygame_menu.themes.THEME_GREEN),
        ('ORANGE', pygame_menu.themes.THEME_ORANGE),
        ('SOLARIZED', pygame_menu.themes.THEME_SOLARIZED),
    ], onchange=change_theme)

    # Back to main menu
    # Apply theme if changed
    cog.add_button('BACK', create_main_menu)

    cog.mainloop(surface)

# About Menu


def create_about_window():
    about_text = "PONG GAME\nVersion 1.0\n\n"\
        "DEVELOPERS:\n"\
        "Jayvee Torres\n"\
        "Addy Casil\n"

    about = pygame_menu.Menu(
        WIN['height'], WIN['width'], 'ABOUT', theme=settings['theme'])
    about.add_label(about_text)
    about.add_button('BACK', create_main_menu)
    about.mainloop(surface)


def create_help_window():
    help_text = "TUTORIAL\n" \
        "\nPLAYER 1 CONTROL:\npress W key to move up\npress S key to move up\n" \
        "\nPLAYER 2 CONTROL:\npress UP key to move up\npress DOWN key to move up\n"\
        "\nMECHANICS:\n"\
        "This game has two players.\n" \
        "It consist of two paddle \n" \
        "and a ball.The two players\n" \
        "should back bounce the ball\n" \
        "to their opponent using\n" \
        "their paddle to score\n"

    instruction = pygame_menu.Menu(
        WIN['height'], WIN['width'], 'HELP', theme=settings['theme'])
    instruction.add_label(help_text)
    instruction.add_button('BACK', create_main_menu)
    instruction.mainloop(surface)

# Main menu window


def create_main_menu():
    menu = pygame_menu.Menu(
        WIN['height'], WIN['width'], 'MAIN MENU', theme=settings['theme'])
    menu.add_button('PLAY', start_the_game)
    menu.add_button('LEADERBOARD', open_leaderboard)
    menu.add_button('SETTINGS', create_settings_window)
    menu.add_button('HELP', create_help_window)
    menu.add_button('ABOUT', create_about_window)
    menu.add_button('EXIT', pygame_menu.events.EXIT)
    menu.mainloop(surface)


# Start Main Menu WIndow
create_main_menu()
