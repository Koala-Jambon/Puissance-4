import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 62222))
sock.listen()

lobby = {}
party = {}


def handle_client(client, client_address):
    print(f"Un nouveau gars est arrivé : {client_address}")
    message = None
    while message != "/quit":
        data = client.recv(1024).decode("utf-8")
        print(data)
        print(type(data))

        if data == "":
            client.close()
            message = "/quit"
            continue

        data = data.split()

        if data[0] == "/lobby":
            try:
                print(f"{lobby[client_address]} est déjà dans le lobby")
            except KeyError:
                print(f"Ajout de {data[1]} au lobby")
                lobby[client_address] = {"pseudo": data[1], "status": "disponible", "partie_id": None}
            client.send(f"{data[1]} is connected to the lobby".encode("utf-8"))
        elif data[0] == "/party":
            if client_address not in lobby:
                client.send(f"Veuillez d'abord rejoindre le lobby".encode("utf-8"))
                continue

            p_id = str(len(party) + 1)
            lobby[client_address]["status"] = "En jeu"
            lobby[client_address]["partie_id"] = p_id

            party[p_id] = {"joueurs": [client_address], "jeu": None}
            client.send(f"Partie {p_id}".encode("utf-8"))
            print("OOOK")

        elif data[0] == "/join":
            try:
                if client_address not in party[data[1]]["joueurs"]:
                    party[data[1]]["joueurs"].append(client_address)
                # quand il y a 2 joueurs, la partie peut commencer
                party[data[1]]["jeu"] = None # On fait les requetes API pour générer le tableau.
                client.send("Joueur ajouté dans la partie".encode("utf-8"))
            except KeyError:
                client.send("Veuillez renseigner un identifiant de partie valide.".encode("utf-8"))
        else:
            print("Aucune commande recevable")
            client.close()




error = False
while not error:
    client, client_address = sock.accept()
    print("GUY")
    thread = threading.Thread(target=handle_client, args=(client, client_address)).run()


