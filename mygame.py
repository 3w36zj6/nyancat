import pyxel


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.x = max(self.x - 2, 0)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.x = min(self.x + 2, pyxel.width - 40)

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.y = max(self.y - 2, 0)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.y = min(self.y + 2, pyxel.height - 24)

        self.frame += 1

    def draw(self):
        pyxel.blt(x=self.x, y=self.y, img=0, u=0, v=24 *
                  (self.frame // 3 % 6), w=40, h=24, colkey=5)


class App:
    def __init__(self):
        pyxel.init(width=160, height=90, caption="NyanCat")
        pyxel.load(filename="assets/cat.pyxres")

        # Player
        self.player = Player(x=50, y=50)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(x=75, y=45, img=1, u=0, v=0, w=40, h=24, colkey=5)

        self.player.draw()


App()
