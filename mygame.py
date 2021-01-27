import pyxel


class App:
    def __init__(self):
        pyxel.init(width=160, height=120, caption="NyanCat")
        pyxel.load(filename="assets/cat.pyxres")
        pyxel.image(1).load(x=0, y=0, filename="assets/cat_16x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(x=75, y=45, img=1, u=0, v=0, w=16, h=16, colkey=13)
        pyxel.blt(x=10, y=10, img=0, u=0, v=0, w=64, h=64, colkey=5)


App()
