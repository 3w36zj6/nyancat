import pyxel
import random
from collections import deque


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        # Rainbow
        is_moving_right = False

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.x = max(self.x - 2, 0)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.x = min(self.x + 2, pyxel.width - 40)
            is_moving_right = True

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.y = max(self.y - 2, 0)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.y = min(self.y + 2, pyxel.height - 24)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet.append_bullet(self.x + 40 - 16, self.y + 24//2 - 16//2)

        Rainbow.append_rainbow(is_moving_right=is_moving_right,
                               x=self.x + 12, y=self.y + (self.animation_frame >= 3))
        self.animation_frame = self.frame // 3 % 6
        self.frame += 1

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0, u=0, v=24 *
                  self.animation_frame, w=40, h=24, colkey=5)


class Rainbow:
    rainbows = deque()

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
                      u=0, v=0, w=16, h=24, colkey=1)

    @classmethod
    def append_rainbow(cls, is_moving_right, x, y):
        Rainbow.rainbows.append(Rainbow(x, y))
        if is_moving_right:
            Rainbow.rainbows.append(Rainbow(x-3, y))

    @classmethod
    def update_all(self):
        for rainbow in Rainbow.rainbows.copy():
            rainbow.__update()
            if rainbow.x < -16:
                Rainbow.rainbows.popleft()

    @classmethod
    def draw_all(self):
        for rainbow in Rainbow.rainbows:
            rainbow.__draw()


class Star:
    stars = deque()
    frame = 0
    count = 0

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
                  u=16, v=7*self.animation_frame, w=7, h=7, colkey=1)

    @classmethod
    def append_star(cls):
        if Star.count % 2 == 0:
            Star.stars.append(
                Star(x=pyxel.width, y=random.randint(0, (pyxel.height - 7) // 2)))
        else:
            Star.stars.append(
                Star(x=pyxel.width, y=random.randint((pyxel.height - 7) // 2, pyxel.height - 7)))
        Star.count += 1

    @classmethod
    def update_all(self):
        if Star.frame % 3 == 0:
            Star.append_star()
        for star in Star.stars.copy():
            star.__update()
            if star.x < -16:
                Star.stars.popleft()

        Star.frame += 1

    @classmethod
    def draw_all(self):
        for star in Star.stars:
            star.__draw()


class Bullet:
    bullets = deque()

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
                  u=40, v=16*self.animation_frame, w=16, h=16, colkey=5)

    @classmethod
    def append_bullet(cls, x, y):
        if len(Bullet.bullets) < 3:
            Bullet.bullets.append(Bullet(x, y))

    @classmethod
    def update_all(self):
        for bullet in Bullet.bullets.copy():
            bullet.__update()
            if bullet.x > pyxel.width:
                Bullet.bullets.popleft()

    @classmethod
    def draw_all(self):
        for bullet in Bullet.bullets:
            bullet.__draw()

class Coin:
    coins = deque()
    frame = 0

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
                  u=24, v=9*self.animation_frame, w=8, h=9, colkey=1)

    @classmethod
    def append_coin(cls):
        Coin.coins.append(Coin(pyxel.width, random.randint(0, pyxel.height - 9)))

    @classmethod
    def update_all(self):
        if Coin.frame % 8 == 0:
            Coin.append_coin()
        for coin in Coin.coins.copy():
            coin.__update()
            if coin.x < -8:
                Coin.coins.remove(coin)

        Coin.frame += 1

    @classmethod
    def draw_all(self):
        for coin in Coin.coins:
            coin.__draw()

class Bomb:
    bombs = deque()
    frame = 0

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
                  u=0, v=0, w=16, h=16, colkey=11)

    @classmethod
    def append_bomb(cls):
        Bomb.bombs.append(Bomb(pyxel.width, random.randint(0, pyxel.height - 16)))

    @classmethod
    def update_all(self):
        if Bomb.frame % 30 == 0:
            Bomb.append_bomb()
        for bomb in Bomb.bombs.copy():
            bomb.__update()
            if bomb.x < -16:
                Bomb.bombs.remove(bomb)

        Bomb.frame += 1

    @classmethod
    def draw_all(self):
        for bomb in Bomb.bombs:
            bomb.__draw()


class App:
    def __init__(self):
        pyxel.init(width=160, height=90, caption="NyanCat")
        pyxel.load(filename="assets/cat.pyxres")

        # Player
        self.player = Player(x=pyxel.width // 2 - 20, y=50)

        pyxel.run(self.update, self.draw)

    def update(self):
        Star.update_all()
        Rainbow.update_all()
        Coin.update_all()
        Bomb.update_all()
        Bullet.update_all()
        self.player.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(1)

        Star.draw_all()
        Rainbow.draw_all()
        Coin.draw_all()
        Bomb.draw_all()
        Bullet.draw_all()
        self.player.draw()


App()
