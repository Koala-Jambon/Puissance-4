import time
from colorama import Style, Fore
from yaspin import yaspin
from yaspin.spinners import Spinners
import json
import socket
from InquirerPy import inquirer


def info_log(message, timer: int):
    message = Fore.BLUE + message
    with yaspin(Spinners.earth, text=message) as sp:
        time.sleep(timer)


def successful_log(message):
    print(Fore.GREEN + f"#>{message}")


def error_log(message):
    print(Fore.RED + f"!>{message}")


def welcome():
    print(Fore.LIGHTGREEN_EX + """
 ____  __.           .__                      _____  
|    |/ _|_________  |  | _____              /  |  | 
|      < /  _ \__  \ |  | \__  \    ______  /   |  |_
|    |  (  <_> ) __ \|  |__/ __ \_ /_____/ /    ^   /
|____|__ \____(____  /____(____  /         \____   | 
        \/         \/          \/               |__|
""")
    print(Style.RESET_ALL, end="")


def server_connect(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        info_log("Connexion au serveur de la NASA...", 2)
        time.sleep(1)
        client.connect((ip, port))
        successful_log("Vous êtes connecté")
    except OSError:
        error_log("Le serveur a empêché notre ATTAQUE")
        exit_game()
    time.sleep(1)
    return client


def lobby_connection(client):
    info_log("Préparation du PAYLOAD", 1)
    pseudo = inquirer.text("Identifiant de connexion : ", qmark="?>", amark="?>", default="Frank").execute()
    client.send(f"/lobby {pseudo}".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    if data["message"] == "connected":
        successful_log("Vous avez réussi à vous introduire sans être repéré")
        time.sleep(0.7)
    else:
        exit_game()


def get_player(client):
    info_log("Récupérations des données utilisateurs...", 1)
    client.send("/lobbylist".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    print(Fore.RESET + "<------JOUEURS------>")
    for ip in data:
        print(Fore.BLUE + data[ip]['pseudo'] + Fore.BLACK + " | ", end="")
        if data[ip]["status"] == "ingame":
            print(Fore.RED + data[ip]["status"] + " n°" + data[ip]["partie_id"])
        else:
            print(Fore.GREEN + data[ip]["status"])

    print(Fore.RESET + "<------------------->", end="\n\n")


def get_party(client):
    info_log("Récupérations des parties", 1)
    client.send("/partylist".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    print(Fore.RESET + "<------PARTIES------>")
    for p_id in data:
        print(Fore.BLUE + "| Partie n°" + p_id)
        print(Fore.BLUE + "| Joueurs : " + Fore.BLACK + str(data[p_id]["joueurs"]))
    print(Fore.RESET + "<------------------->")


def question(client):
    action = inquirer.select("Que voulez-vous faire ?", [{"name": "Créer une partie", "value": "/create"},
                                                         {"name": "Rejoindre une partie", "value": "/join"}]).execute()
    if action == "/join":
        party_id = inquirer.number("Quelle partie voulez-vous rejoindre ?").execute()
        action = f"{action} {party_id}"

    client.send(f"{action}".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    print(data)

    if data["message"] == "error":
        error_log(data["details"])
        question(client)
    if "partie_id" in data:
        successful_log(f"Vous êtes dans la partie n°{data['partie_id']}")


def wait_people(client):
    print("Debug: WAITING PEOPLE")
    data = {"message": "/waitpeople"}
    with yaspin(Spinners.arc, text="Attente d'un autre joueur") as sp:
        while data["message"] == "/waitpeople":
            send_json("/waitpeople".encode("utf-8"))
            data = recv_json(client)
    return data


def exit_game():
    error_log("VOUS ALLEZ QUITTER")
    # os.system("shutdown -h now")
    exit()


def send_json(client, data_dict):
    try:
        print(f"on envoie {data_dict}")
        client.send(json.dumps(data_dict).encode("utf-8"))
        return True
    except OSError:
        raise OSError("Erreur dans l'envoie d'un message")


def recv_json(client: socket.socket):
    try:
        data = client.recv(1024).decode("utf-8")
        return json.loads(data)
    except json.JSONDecodeError:
        print(f"ERREUR DE DECODAGE")
    except OSError:
        raise OSError("Problème réception du JSON")


def recv_simple(client: socket.socket):
    try:
        data = client.recv(1024).decode("utf-8")
        return data
    except OSError:
        raise OSError("Problème réception du message simple")