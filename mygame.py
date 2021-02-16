import pyxel
import random
from collections import deque


class Player:
    width = 40
    height = 24

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0

    @classmethod
    def update(cls):
        # Rainbow
        is_moving_right = False

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            Player.player.x = max(Player.player.x - 2, 0)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            Player.player.x = min(Player.player.x + 2,
                                  pyxel.width - Player.width)
            is_moving_right = True

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            Player.player.y = max(Player.player.y - 2, 0)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            Player.player.y = min(Player.player.y + 2,
                                  pyxel.height - Player.height)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet.append_bullet(Player.player.x + Player.width - 16,
                                 Player.player.y + Player.height//2 - 16//2)

        Rainbow.append_rainbow(is_moving_right=is_moving_right,
                               x=Player.player.x + 12, y=Player.player.y + (Player.player.animation_frame >= 3))
        Player.player.animation_frame = Player.player.frame // 3 % 6
        Player.player.frame += 1

    @classmethod
    def draw(cls):
        pyxel.blt(x=Player.player.x, y=Player.player.y, img=0, u=0, v=Player.height *
                  Player.player.animation_frame, w=Player.width, h=Player.height, colkey=5)

    @classmethod
    def setup(cls, x, y):
        Player.player = Player(x, y)


class Rainbow:
    width = 1
    height = 24

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0

    def __update(self):
        self.x -= 3
        self.frame += 1

    def __draw(self):
        for i in range(3):
            pyxel.blt(x=self.x + i, y=self.y, img=1,
                      u=0, v=0, w=Rainbow.width, h=Rainbow.height, colkey=1)

    @classmethod
    def setup(cls):
        Rainbow.rainbows = deque()

    @classmethod
    def append_rainbow(cls, is_moving_right, x, y):
        Rainbow.rainbows.append(Rainbow(x, y))
        if is_moving_right:
            Rainbow.rainbows.append(Rainbow(x-3, y))

    @classmethod
    def update_all(cls):
        for rainbow in Rainbow.rainbows.copy():
            rainbow.__update()
            if rainbow.x < -Rainbow.width:
                Rainbow.rainbows.popleft()

    @classmethod
    def draw_all(cls):
        for rainbow in Rainbow.rainbows:
            rainbow.__draw()


class Star:
    stars = deque()
    frame = 0
    count = 0
    width = 7
    height = 7

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = random.randint(0, 17)
        self.animation_frame = 0

    def __update(self):
        self.x -= 3
        self.animation_frame = self.frame // 3 % 6
        self.frame += 1

    def __draw(self):
        pyxel.blt(x=self.x, y=self.y, img=1,
                  u=16, v=Star.height*self.animation_frame, w=Star.width, h=Star.height, colkey=1)

    @classmethod
    def append_star(cls):
        if Star.count % 2 == 0:
            Star.stars.append(
                Star(x=pyxel.width, y=random.randint(0, (pyxel.height - Star.height) // 2)))
        else:
            Star.stars.append(
                Star(x=pyxel.width, y=random.randint((pyxel.height - Star.height) // 2, pyxel.height - Star.height)))
        Star.count += 1

    @classmethod
    def update_all(cls):
        if Star.frame % 3 == 0:
            Star.append_star()
        for star in Star.stars.copy():
            star.__update()
            if star.x < -Star.width:
                Star.stars.popleft()

        Star.frame += 1

    @classmethod
    def draw_all(cls):
        for star in Star.stars:
            star.__draw()


class Bullet:
    width = 16
    height = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0

    def __update(self):
        self.x += 4
        self.animation_frame = self.frame // 2 % 4
        self.frame += 1

    def __draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0,
                  u=40, v=Bullet.height*self.animation_frame, w=Bullet.width, h=Bullet.height, colkey=5)

    @classmethod
    def setup(cls):
        Bullet.bullets = deque()

    @classmethod
    def append_bullet(cls, x, y):
        if len(Bullet.bullets) < 3:
            Bullet.bullets.append(Bullet(x, y))

    @classmethod
    def update_all(cls):
        for bullet in Bullet.bullets.copy():
            bullet.__update()
            if bullet.x > pyxel.width:
                Bullet.bullets.popleft()

    @classmethod
    def draw_all(cls):
        for bullet in Bullet.bullets:
            bullet.__draw()


class Coin:
    width = 8
    height = 9

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 2.0 * random.random() + 0.8
        self.frame = 0
        self.animation_frame = 0

    def __update(self):
        self.x -= self.vx
        self.animation_frame = self.frame // 3 % 4
        self.frame += 1

    def __draw(self):
        pyxel.blt(x=int(self.x), y=self.y, img=1,
                  u=24, v=Coin.height*self.animation_frame, w=Coin.width, h=Coin.height, colkey=1)

    @classmethod
    def setup(cls):
        Coin.coins = deque()
        Coin.frame = 0

    @classmethod
    def append_coin(cls):
        Coin.coins.append(
            Coin(pyxel.width, random.randint(0, pyxel.height - Coin.height)))

    @classmethod
    def update_all(cls):
        if Coin.frame % 8 == 0:
            Coin.append_coin()
        for coin in Coin.coins.copy():
            coin.__update()
            if coin.x < -Coin.width:
                Coin.coins.remove(coin)
            if coin.x < Player.player.x + Player.width and Player.player.x < coin.x + Coin.width and coin.y < Player.player.y + Player.height and Player.player.y < coin.y + Coin.height:
                App.score += 1
                Coin.coins.remove(coin)

        Coin.frame += 1

    @classmethod
    def draw_all(cls):
        for coin in Coin.coins:
            coin.__draw()


class Bomb:
    width = 16
    height = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 1.5 * random.random() + 0.8
        self.frame = 0

    def __update(self):
        self.x -= self.vx
        self.frame += 1

    def __draw(self):
        pyxel.blt(x=int(self.x), y=self.y, img=2,
                  u=0, v=0, w=Bomb.width, h=Bomb.height, colkey=1)

    @classmethod
    def setup(cls):
        Bomb.bombs = deque()
        Bomb.frame = 0

    @classmethod
    def append_bomb(cls):
        Bomb.bombs.append(
            Bomb(pyxel.width, random.randint(0, pyxel.height - Bomb.height)))

    @classmethod
    def update_all(cls):
        if Bomb.frame % 30 == 0:
            Bomb.append_bomb()
        for bomb in Bomb.bombs.copy():
            bomb.__update()
            if bomb.x < -Bomb.width:
                Bomb.bombs.remove(bomb)
            if bomb.x < Player.player.x + Player.width and Player.player.x < bomb.x + Bomb.width and bomb.y < Player.player.y + Player.height and Player.player.y < bomb.y + Bomb.height:
                App.game_mode = 2

        Bomb.frame += 1

    @classmethod
    def draw_all(cls):
        for bomb in Bomb.bombs:
            bomb.__draw()


class App:
    def __init__(self):
        pyxel.init(width=160, height=90, caption="NyanCat")
        pyxel.load(filename="assets/cat.pyxres")

        self.setup()

        pyxel.run(self.update, self.draw)

    def setup(self):
        App.game_mode = 0
        App.score = 0

        # Player
        Player.setup(x=pyxel.width // 2 - 20, y=50)

        # Other
        Rainbow.setup()
        Coin.setup()
        Bomb.setup()
        Bullet.setup()

    def update(self):
        Star.update_all()
        Rainbow.update_all()
        if App.game_mode == 1:
            Coin.update_all()
            Bomb.update_all()
        Bullet.update_all()
        Player.update()

        # Reset
        if pyxel.btnp(pyxel.KEY_R):
            self.setup()

        # Start
        if pyxel.btnp(pyxel.KEY_S):
            App.game_mode = 1

        # End
        if pyxel.btnp(pyxel.KEY_E):
            App.game_mode = 2

        # Quit
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(1)

        Star.draw_all()
        Rainbow.draw_all()
        if App.game_mode == 1:
            Coin.draw_all()
            Bomb.draw_all()
        Bullet.draw_all()
        Player.draw()

        pyxel.text(0, 0, f"Game Mode:{App.game_mode}", 6)
        pyxel.text(0, 8, f"Score:{App.score}", 6)

App()
