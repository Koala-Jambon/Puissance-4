import pyxel
import time
import itertools as tool
import api

class App:
    
    def __init__(self, player_ip_list, player_ip, board, player_turn_ip):
        self.game = api.Game(player_ip_list, board, player_turn_ip)
        self.end = False
        self.player_number = self.game.ip_to_number(player_ip)
        self.choice_position = 0
        pyxel.init(1920, 1080, title="Online Power 4")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.player_turn_number == self.player_number and self.end == False:
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0, 1, 2, 3, 4, 5, 6]:
                self.choice_position += 1
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                self.choice_position += -1
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.game.check_column(self.choice_position - 1) == True:
                self.game.drop_piece(self.choice_position - 1)
                self.player_turn_number = self.game.change_player_turn()
                #Envoie self.choice_position au serveur et récupère toute les infos du serv                                                                                  
                self.choice_position = 0
        elif self.end == False:
            # Waiting for the other player to send a message then self.draw()
            pass
        else:
            time.sleep(3)
            pyxel.quit()
            exit()

    # Peu importe si le joueur doit jouer ou non, il dessine le tableau de jeu et vérifie si il y a un gagnant
    def draw(self):
        pyxel.cls(0)
        for draw_x, draw_y in tool.product(range(7), range(6)):
            pyxel.rect(150 * draw_x + 435, 930 - 150 * draw_y, 150, 150, 1)
            if self.board[draw_y][draw_x] == 0:
                pyxel.circ(150 * draw_x + 510, 1005 - 150 * draw_y, 70, 0)
            if self.board[draw_y][draw_x] == 1:
                pyxel.circ(150 * draw_x + 510, 1005 - 150 * draw_y, 70, 8)
            if self.board[draw_y][draw_x] == 2:
                pyxel.circ(150 * draw_x + 510, 1005 - 150 * draw_y, 70, 10)
            if self.player_turn_number == 1:
                pyxel.circ(150 * (self.choice_position - 1) + 510, 75, 70, 8)
            else:
                pyxel.circ(150 * (self.choice_position - 1) + 510, 75, 70, 10)
        if self.end == True:
            pyxel.text(960, 540, f"La partie est terminée", 7)

# Ici tu te connecte au serveur(tu te demerde) et je veux juste que la liste des joueurs et le pseudo du joueur sur ce client ressortent.
App(["Freud", "Karl"], #Liste des IPs
    "IP DU JOUEUR ICI", #IP DU joueur qui fait tourner ce code
    api.board(), #Création du tableau, ici il est vierge
    "Karl") #Ip du joueur qui doit jouer
