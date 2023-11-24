import pyxel
import time

class App:
    def __init__(self):
        pyxel.init(1920, 1080, title = "Puissance 4 en ligne")
        self.x = 0
        self.y = 0
        self.pause = False
        self.position = 0
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.pause == False:
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.position in [0,1,2,3,4,5,6]:
                self.position += 1
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.position in [2,3,4,5,6,7]:
                self.position += -1
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.position != 0:
                self.drop_piece()
            self.x = 150*(self.position-1)+435
        
    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, self.y, 150, 150, 9)
    
    def drop_piece(self):
        self.pause = True
        for loop in range(930):
            self.y += 1
            self.draw()
            self.update()
            time.sleep(0.001)
        self.pause = False
App()
