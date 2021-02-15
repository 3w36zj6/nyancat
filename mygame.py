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

    def update(self):
        self.x -= 3
        self.frame += 1

    def draw(self):
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
            rainbow.update()
            if rainbow.x < -16:
                Rainbow.rainbows.popleft()

    @classmethod
    def draw_all(self):
        for rainbow in Rainbow.rainbows:
            rainbow.draw()


class Star:
    stars = deque()
    frame = 0
    count = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = random.randint(0, 17)
        self.animation_frame = 0

    def update(self):
        self.x -= 3
        self.animation_frame = self.frame // 3 % 6
        self.frame += 1

    def draw(self):
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
            star.update()
            if star.x < -16:
                Star.stars.popleft()

        Star.frame += 1

    @classmethod
    def draw_all(self):
        for star in Star.stars:
            star.draw()


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
        self.player.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(1)

        Star.draw_all()
        Rainbow.draw_all()
        self.player.draw()


App()
