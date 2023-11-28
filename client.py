import pyxel
import time
import itertools as tool
import api


class App:
    
    def __init__(self, player_ip_list, player_number, board, player_turn_nickname):
        self.end = False
        self.board = board
        self.player_ip_list = player_ip_list
        self.player_turn_number = api.nickname_to_number(player_turn_nickname, self.player_ip_list)
        self.player_number = api.ip_to_number(player_ip, self.player_ip_list)
        self.choice_position = 0
        self.pause = False
        pyxel.init(1920, 1080, title="Online Power 4")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.player_turn_number == self.player_number and self.end == False:
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0, 1, 2, 3, 4, 5, 6]:
                self.choice_position += 1
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                self.choice_position += -1
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and api.check_column(self.choice_position - 1,self.board) == True:
                api.drop_piece(self.choice_position - 1, self.board, self.player_turn_number)
                #self.player_turn_number = api.change_player_turn(self.player_turn_number)
                #Envoie self.choice_position au serveur et récupère toute les infos du serv                                                                                  
                self.choice_position = 0
        elif self.end == False:
            # Waiting for the other player to send a message then self.draw()
            pass
        else:
            time.sleep(3)
            pyxel.quit()
            exit()

    # Peut importe si le joueur doit jouer ou non, il dessine le tableau de jeu et vérifie si il y a un gagnant
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
        for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
            if getattr(api, func)(self.board) != 0:
                winner = api.number_to_nickname(getattr(api, func)(self.board), self.player_list)
                pyxel.text(960, 540, f"{winner} has won!", 7)
                self.end = True
        if api.check_tie(self.board) == True:
            pyxel.text(960, 540, "This game ended on a tie!", 7)
            self.end = True
            

# Ici tu te connecte au serveur(tu te demerde) et je veux juste que la liste des joueurs et le pseudo du joueur sur ce client ressortent.
App(["Freud", "Karl"],
    "IP DU JOUEUR ICI", api.board(), "Karl")  # Ici la ligne représente la liste des joueurs, donnée par le serveur ; le "Freud" lui représente le pseudo du joueur sur lequel tourne ce code.
