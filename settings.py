# DEFAULT SETTINGS

FONT = {
    "courier": 'assets/Courier.ttf',
    "elfboy": 'assets/elf-boy.ttf'
}

AUDIO = {
    "bg": 'assets/bgfor2d.mp3',
    "collision": 'assets/collision.ogg',
    "pong": 'assets/pong.ogg',
    "score": 'assets/score.ogg'
}

IMG = {
    "ball": 'assets/Ball.png',
    "logo": 'assets/JAlogo.png',
    "paddle": 'assets/Paddle.jpg',
}

COLOR = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "blue": (2, 38, 41),
    "yellow": (255, 181, 0)
}

WIN = {
    "width": 800,
    "height": 500,
    "pong_bgcolor": COLOR['blue'],  # GAMEPLAY BGCOLOR
    "bgcolor": COLOR["yellow"],     # MENU
    "bgmusic": AUDIO["bg"],
    "title": "OOP PROJECT",
    "icon": IMG["logo"],
    "player_speed": 5,
    "ball_speed": 4,
    "score_limit": 5,
    "music": True,
    "player1_name": "Player one",
    "player2_name": "Player two"
}
