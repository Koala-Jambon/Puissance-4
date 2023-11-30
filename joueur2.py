import socket
from InquirerPy import inquirer
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connexion au serveur...")
client.connect(("127.0.0.1", 62222))

print("Connexion au lobby...")
pseudo = inquirer.text("Quel est votre pseudo : ").execute()
client.send(f"/lobby {pseudo}".encode("utf-8"))
data = client.recv(1024).decode("utf-8")

print(data)
if data == f"{pseudo} is connected to the lobby":
    print("We are in !")

client.send(f"/join 1".encode("utf-8"))
data = client.recv(1024).decode("utf-8")


# Et maintenant on joue
client.send(f"/wait".encode("utf-8"))
data = client.recv(1024).decode("utf-8")
print(data)
data = json.loads(data)
if data["you"] == data["tour"]:
    while data != "error":
        print("Sur quelle colonne voulez vous jouer ?")
        cmd = inquirer.number("Numéro colonne [0-6]").execute()
        client.send(f"/play {cmd}".encode("utf-8"))
        data = client.recv(4096).decode("utf-8")
        print(data)
else:
    while True:
        client.send(f"/wait {json.dumps({'board': data['board']})}".encode("utf-8"))
        print("J'attends")
        data = client.recv(1024).decode("utf-8")
        print(data)
        print("Sur quelle colonne voulez vous jouer ?")
        cmd = inquirer.number("Numéro colonne [0-6]").execute()
        client.send(f"/play {cmd}".encode("utf-8"))
        data = client.recv(4096).decode("utf-8")
        print(data)
