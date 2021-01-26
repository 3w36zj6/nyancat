import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="NyanCat")
        pyxel.image(0).load(0, 0, "assets/cat_16x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(x=75, y=45, img=0, u=0, v=0, w=16, h=16, colkey=13)


App()
