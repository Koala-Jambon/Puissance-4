import socket
import threading
import time

import api
import json
import random

# Initialisation du serveur sur le port `62222`
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 62222))
sock.listen()

# Création du lobby et du tableau des parties
lobby = {}
party = {}


def handle_client(client: socket.socket, client_address):
    print(f"Un nouveau gars est arrivé : {client_address}")
    message = None
    while message != "/quit":
        data = client.recv(1024).decode("utf-8")
        print(f"DATA : {data} //")
        print(type(data))

        if data == "":
            print("Message vide")
            client.close()
            message = "/quit"
            continue

        data = data.split()

        if data[0] == "/lobby":
            try:
                print(f"{lobby[client_address]} est déjà dans le lobby")
            except KeyError:
                print(f"Ajout de {data[1]} au lobby")
                lobby[client_address] = {"pseudo": data[1], "status": "disponible", "partie_id": None, "client": client}
            client.send(f"{data[1]} is connected to the lobby".encode("utf-8"))

        # Si le client ne s'enregistre pas on vérifie qu'il l'est pour pouvoir faire les autres commandes
        if client_address not in lobby:
            client.send(f"Veuillez d'abord rejoindre le lobby".encode("utf-8"))
            continue

        if data[0] == "/party":
            p_id = str(len(party) + 1)
            lobby[client_address]["status"] = "En jeu"
            lobby[client_address]["partie_id"] = p_id

            party[p_id] = {"joueurs": [client_address], "jeu": None}
            client.send(f"Partie {p_id}".encode("utf-8"))
            print("OOOK")

        elif data[0] == "/join":
            # Ici le try except essaye de lire les arguments de /join, si il n'y arrive pas il renvoie une erreur
            try:
                # Vérifions si le joueur n'est pas déjà dans une partie ET qu'il y a moins de 2 joueurs
                if client_address not in party[data[1]]["joueurs"] and len(party[data[1]]["joueurs"]) < 2:

                    party[data[1]]["joueurs"].append(client_address)
                    lobby[client_address]["partie_id"] = data[1]
                else:
                    client.send(f"Vous êtes déjà dans la partie {data[1]}. /leave pour la quitter".encode("utf-8"))

                if len(party[data[1]]["joueurs"]) == 2:
                    # On fait les requetes API pour générer le tableau et on détermine le tour
                    tour = list(random.choice(party[data[1]]["joueurs"]))
                    tour.append(lobby[tuple(tour)]["pseudo"])
                    """
                    {"joueurs": [["127.0.0.1", 45512], ["127.0.0.1", 45522]], "jeu": {"board": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], "tour": ["127.0.0.1", 45512, "ddd"]}}
                    """
                    party[data[1]]["jeu"] = {"board": api.board(), "tour": tour}
                client.send("Vous avez rejoins la partie".encode("utf-8"))

            except KeyError:
                client.send("Veuillez renseigner un identifiant de partie valide.".encode("utf-8"))

        # Et là c'est quand le client est prêt à jouer et qu'il attend
        elif data[0] == "/wait":
            p_id = lobby[client_address]["partie_id"]
            while len(party[p_id]["joueurs"]) != 2:
                # On attend qu'un joueur rejoigne la partie
                print("---ON ATTEND---")
                print(party)
                time.sleep(1)
            jouer(p_id, client, client_address)
    print("Fermeture d'un client")


def jouer(partie_id, client: socket.socket, client_address):
    print(party)
    client.send(json.dumps(party[partie_id]).encode("utf-8"))
    while True:
        data = client.recv(4096).decode("utf-8")
        print(data)
        client.send(f"J'ai reçu {data}".encode())

error = False
while not error:
    print("Waiting for a Client...")
    client, client_address = sock.accept()
    threading.Thread(target=handle_client, args=(client, client_address)).start()
    print("Le thread a été lancé")

