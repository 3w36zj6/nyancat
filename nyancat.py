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

        if pyxel.btn(pyxel.KEY_LEFT):
            cls.player.x = max(cls.player.x - 2, 0)

        if pyxel.btn(pyxel.KEY_RIGHT):
            cls.player.x = min(cls.player.x + 2,
                               pyxel.width - cls.width)
            is_moving_right = True

        if pyxel.btn(pyxel.KEY_UP):
            cls.player.y = max(cls.player.y - 2, 0)

        if pyxel.btn(pyxel.KEY_DOWN):
            cls.player.y = min(cls.player.y + 2,
                               pyxel.height - cls.height)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet.append(cls.player.x + cls.width - 16,
                          cls.player.y + cls.height//2 - 16//2)

        Rainbow.append(is_moving_right=is_moving_right,
                       x=cls.player.x + 12, y=cls.player.y + (cls.player.animation_frame >= 3))
        cls.player.animation_frame = cls.player.frame // 3 % 6
        cls.player.frame += 1

    @classmethod
    def draw(cls):
        pyxel.blt(x=cls.player.x, y=cls.player.y, img=0, u=0, v=cls.height *
                  cls.player.animation_frame, w=cls.width, h=cls.height, colkey=5)

    @classmethod
    def setup(cls, x, y):
        cls.player = cls(x, y)


class Sprite:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    @classmethod
    def setup(cls):
        cls.sprites = deque()

    @classmethod
    def append(cls):
        pass

    @classmethod
    def update_all(cls):
        for sprite in cls.sprites:
            sprite.update()

    @classmethod
    def draw_all(cls):
        for sprite in cls.sprites:
            sprite.draw()


class Rainbow(Sprite):
    width = 1
    height = 24

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
                      u=0, v=0, w=Rainbow.width, h=Rainbow.height, colkey=1)

    @classmethod
    def append(cls, is_moving_right, x, y):
        cls.sprites.append(cls(x, y))
        if is_moving_right:
            cls.sprites.append(cls(x-3, y))

    @classmethod
    def update_all(cls):
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < - 10:
                cls.sprites.popleft()


class Star(Sprite):
    frame = 0
    count = 0
    width = 7
    height = 7

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
                  u=16, v=Star.height*self.animation_frame, w=Star.width, h=Star.height, colkey=1)

    @classmethod
    def append(cls):
        if cls.count % 2 == 0:
            cls.sprites.append(
                cls(x=pyxel.width, y=random.randint(0, (pyxel.height - cls.height) // 2)))
        else:
            cls.sprites.append(
                cls(x=pyxel.width, y=random.randint((pyxel.height - cls.height) // 2, pyxel.height - cls.height)))
        cls.count += 1

    @classmethod
    def update_all(cls):
        if cls.frame % 3 == 0:
            cls.append()
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < -cls.width:
                cls.sprites.popleft()

        cls.frame += 1


class Bullet(Sprite):
    width = 16
    height = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        self.x += 4
        self.animation_frame = self.frame // 2 % 4
        self.frame += 1

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0,
                  u=40, v=Bullet.height*self.animation_frame, w=Bullet.width, h=Bullet.height, colkey=5)

    @classmethod
    def append(cls, x, y):
        if len(cls.sprites) < 3:
            cls.sprites.append(cls(x, y))

    @classmethod
    def update_all(cls):
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x > pyxel.width:
                cls.sprites.popleft()


class Coin(Sprite):
    width = 8
    height = 9
    frame = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 2.0 * random.random() + 0.8
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        self.x -= self.vx
        self.animation_frame = self.frame // 3 % 4
        self.frame += 1

    def draw(self):
        pyxel.blt(x=int(self.x), y=self.y, img=1,
                  u=24, v=Coin.height*self.animation_frame, w=Coin.width, h=Coin.height, colkey=1)

    @classmethod
    def append(cls):
        cls.sprites.append(
            cls(pyxel.width, random.randint(0, pyxel.height - cls.height)))

    @classmethod
    def update_all(cls):
        if cls.frame % 8 == 0:
            cls.append()
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < -cls.width:
                cls.sprites.remove(sprite)
                continue

            if sprite.x < Player.player.x + Player.width and Player.player.x < sprite.x + cls.width and sprite.y < Player.player.y + Player.height and Player.player.y < sprite.y + cls.height:
                if App.game_mode == 1:
                    App.score += 1
                cls.sprites.remove(sprite)
                continue

            for bullet in Bullet.sprites:
                if sprite.x < bullet.x + Bullet.width and bullet.x < sprite.x + cls.width and sprite.y < bullet.y + Bullet.height and bullet.y < sprite.y + cls.height:
                    cls.sprites.remove(sprite)
                    break

        cls.frame += 1


class Bomb(Sprite):
    width = 16
    height = 16
    frame = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = (1.5 * random.random() + 0.8) * \
            (1 + (pyxel.frame_count - App.start_frame_count) / 600)
        self.frame = 0

    def update(self):
        self.x -= self.vx
        self.frame += 1

    def draw(self):
        pyxel.blt(x=int(self.x), y=self.y, img=2,
                  u=0, v=0, w=Bomb.width, h=Bomb.height, colkey=1)

    @classmethod
    def append(cls):
        if App.game_mode == 1:
            cls.sprites.append(
                cls(pyxel.width, random.randint(0, pyxel.height - cls.height)))

    @classmethod
    def update_all(cls):
        if cls.frame % max(30 - (pyxel.frame_count - App.start_frame_count) // 600, 5) == 0:
            cls.append()
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.x < -cls.width:
                cls.sprites.remove(sprite)
                continue

            for bullet in Bullet.sprites.copy():
                if sprite.x < bullet.x + Bullet.width and bullet.x < sprite.x + cls.width and sprite.y < bullet.y + Bullet.height and bullet.y < sprite.y + cls.height:
                    cls.sprites.remove(sprite)
                    Bullet.sprites.remove(bullet)
                    Explosion.append(sprite.x, sprite.y)
                    break

            player_center_x = Player.player.x + Player.width // 2
            player_center_y = Player.player.y + Player.height // 2
            sprite_center_x = sprite.x + cls.width // 2
            sprite_center_y = sprite.y + cls.height // 2
            # if sprite.x < Player.player.x + Player.width and Player.player.x < sprite.x + cls.width and sprite.y < Player.player.y + Player.height and Player.player.y < sprite.y + cls.height:
            if (player_center_x - sprite_center_x)**2 + (player_center_y - sprite_center_y)**2 < 10**2:
                App.game_mode = 2
                if sprite in cls.sprites:
                    cls.sprites.remove(sprite)
                Explosion.append(sprite.x, sprite.y)

        cls.frame += 1


class Explosion(Sprite):
    count = 0
    width = 16
    height = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.animation_frame = 0

    def update(self):
        self.animation_frame = self.frame // 3
        self.frame += 1

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0,
                  u=56, v=Explosion.height*self.animation_frame, w=Explosion.width, h=Explosion.height, colkey=5)

    @classmethod
    def append(cls, x, y):
        cls.sprites.append(cls(x=x, y=y))

    @ classmethod
    def update_all(cls):
        for sprite in cls.sprites.copy():
            sprite.update()
            if sprite.animation_frame > 3:
                cls.sprites.popleft()


class App:
    score = 0
    high_score = 0

    def __init__(self):
        pyxel.init(width=160, height=90, caption="NyanCat")
        pyxel.load(filename="assets/cat.pyxres")

        self.setup()

        pyxel.run(self.update, self.draw)

    def setup(self):
        App.game_mode = 0
        App.high_score = max(App.score, App.high_score)
        App.score = 0

        # Player
        Player.setup(x=pyxel.width // 2 - 20, y=50)

        # Other
        Rainbow.setup()
        Star.setup()
        Coin.setup()
        Bomb.setup()
        Bullet.setup()
        Explosion.setup()

    def update(self):
        Star.update_all()
        Rainbow.update_all()
        if App.game_mode != 0:
            Coin.update_all()
            Bomb.update_all()
        Bullet.update_all()
        Explosion.update_all()
        Player.update()

        # Reset
        if pyxel.btnp(pyxel.KEY_R):
            self.setup()

        # Start
        if pyxel.btnp(pyxel.KEY_S) and App.game_mode == 0:
            App.game_mode = 1
            App.start_frame_count = pyxel.frame_count

        # End
        """
        if pyxel.btnp(pyxel.KEY_E):
           App.game_mode = 2
        """

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
        Explosion.draw_all()
        Player.draw()

        pyxel.text(0, 0, f"High Score:{App.high_score}", [
                   9, 10, 7][pyxel.frame_count // 2 % 3])
        pyxel.text(0, 7, f"Score:{App.score}", 13)

        if App.game_mode == 0:
            pyxel.text(0, pyxel.height - 6, "Press [S] key to start.", 13)
        elif App.game_mode == 1:
            pass
        elif App.game_mode == 2:
            pyxel.text(0, pyxel.height - 6, "Press [R] key to retry.", 13)


App()
