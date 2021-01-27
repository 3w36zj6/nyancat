import pyxel


class App:
    def __init__(self):
        pyxel.init(width=160, height=120, caption="NyanCat")
        pyxel.load(filename="assets/cat.pyxres")
        pyxel.image(1).load(x=0, y=0, filename="assets/cat_16x16.png")

        # Player
        self.player_x = 50
        self.player_y = 50

        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_player()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.player_x = max(self.player_x - 2, 0)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 40)

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.player_y = max(self.player_y - 2, 0)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.player_y = min(self.player_y + 2, pyxel.height - 24)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(x=75, y=45, img=1, u=0, v=0, w=16, h=16, colkey=13)
        pyxel.blt(x=self.player_x, y=self.player_y,
                  img=0, u=0, v=0, w=64, h=64, colkey=5)


App()
