import pyxel
from itertools import product

class App():
    def __init__(self):
        pyxel.init(int(1920/1.5), int(1080/1.5))
        pyxel.run(self.update, self.draw)

    def update(self):
        pass
    
    def draw(self):
        self.draw_text("create", [0, 0])

    def draw_text(self, text : str, coords : list):
        text = text.lower()
        letters_coords = {
            "exemple" : '',
            "a" : [10, 15, 0, 0, 80, 0, 1],
            "b" : [9, 15, 80, 0, 72, 0, 1],
            "c" : [10, 15, 152, 0, 80, 0, 1],
            "d" : [9, 15, 0, 120, 72, 0, 1],
            "e" : [10, 15, 88, 120, 88, 0, 1],
            "f" : [6, 15, 172, 120, 48, 0, 1],
            "g" : [9, 15, 0, 0, 72, 1, 1],
            "h" : [9, 15, 88, 0, 72, 1, 1],
            "i" : [2, 15, 184, 0, 16, 1, 1],
            "j" : [4, 15, 0, 120, 32, 1, 1],
            "k" : [10, 15, 48, 120, 80, 1, 1],
            "l" : [3, 15, 128, 120, 24, 1, 1],
            "m" : [14, 15, 0, 0, 112, 2, 1],
            "n" : [10, 15, 128, 0, 88, 2, 1],
            "o" : [10, 15, 0, 128, 88, 2, 1],
            "p" : [10, 15, 88, 128, 80, 2, 1],
            "q" : [9, 15, 176, 128, 72, 2, 1],
            "r" : [6, 15, 0, 0, 48, 0, 2],
            "s" : [9, 15, 48, 0, 72, 0, 2],
            "t" : [5, 15, 120, 0, 40, 0, 2]
        }
        for letter in text:
            pyxel.load(f"letter{letters_coords[letter][6]}.pyxres")
            try:
                for w, h in product(range(letters_coords[letter][0]), range(letters_coords[letter][1])):
                    pyxel.blt(coords[0]+w*8, coords[1]+h*8, letters_coords[letter][5], letters_coords[letter][2]+w*8, letters_coords[letter][3]+h*8, 8, 8)
                coords[0] += letters_coords[letter][4]+8
            except KeyError:
                pass

App()
