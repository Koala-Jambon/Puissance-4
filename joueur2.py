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
while data != "quit":
    client.send(f"/wait".encode("utf-8"))
    data = client.recv(1024).decode("utf-8")
    data.split()
    if data[0] == "/jeu":
        coup = inquirer.number("Sur quelle colonne voulez vous jouer ?").execute()
