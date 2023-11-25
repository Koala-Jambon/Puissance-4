import pyxel
import time
import itertools as tool
import api

class App:
    def __init__(self, player_list, player_number):
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.player_turn_number = 1
        self.player_list = player_list        
        self.player_number = self.nickname_to_number(player_number)
        self.choice_position = 0 
        self.pause = False
        pyxel.init(1920, 1080, title = "Online Power 4")
        pyxel.run(self.update, self.draw)

    #Peut importe si le joueur doit jouer ou non, il dessine le tableau de jeu et vérifie si il y a un gagnant
    def draw(self):
        pyxel.cls(0)
        for draw_x, draw_y in tool.product(range(7), range(6)):
            if self.board[draw_y][draw_x] == 0:
                pyxel.rect(150*draw_x+435, 930-150*draw_y, 150, 150, 1)
            if self.board[draw_y][draw_x] == 1:
                pyxel.rect(150*draw_x+435, 930-150*draw_y, 150, 150, 8)
            if self.board[draw_y][draw_x] == 2:
                pyxel.rect(150*draw_x+435, 930-150*draw_y, 150, 150, 10)
        pyxel.rect(150*(self.choice_position-1)+435, 0, 150, 150, 9)
        for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
            if getattr(api, func)() != 0:
                winner = number_to_nickname(getattr(api, func)())
                pyxel.text(0, 0, f"{winner} has won!", 7)
                time.sleep(1)
                pyxel.quit()
                exit()
        if api.check_tie() == True:
            pyxel.text(0, 0, "This game ended on a tie!", 7)
            time.sleep(1)
            pyxel.quit()
            exit()

#Ici tu te connecte au serveur(tu te demerde) et je veux juste que la liste des joueurs et le pseudo du joueur sur ce client ressortent.
App(["Freud", "Karl"], "Freud")#Ici la ligne représente la liste des joueurs, donnée par le serveur ; le "Freud" lui représente le pseudo du joueur sur lequel tourne ce code.
