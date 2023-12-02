import socket
from InquirerPy import inquirer

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connexion au serveur...")
client.connect(("127.0.0.1", 62222))

print("Connexion au lobby...")
pseudo = inquirer.text("Quel est votre pseudo : ").execute()
client.send(f"/lobby {pseudo}".encode("utf-8"))
data = client.recv(4096).decode("utf-8")

print(data)
if data == f"{pseudo} is connected to the lobby":
    print("We are in !")

client.send(f"/lobbylist".encode("utf-8"))


client.send(f"/party".encode("utf-8"))
data = client.recv(4096).decode("utf-8")

print(data)

client.send(f"/wait".encode("utf-8"))
data = client.recv(4096).decode("utf-8")
print(data)


while data != "error":
    print("Sur quelle colonne voulez vous jouer ?")
    cmd = inquirer.number("Numéro colonne [0-6]").execute().encode("utf-8")
    client.send(cmd)
    data = client.recv(4096).decode("utf-8")
    print(data)