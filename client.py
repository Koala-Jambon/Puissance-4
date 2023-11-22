import socket
from InquirerPy import inquirer

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connexion au serveur...")
client.connect(("172.20.10.2", 62222))

print("Connexion au lobby...")
pseudo = inquirer.text("Quel est votre pseudo : ").execute()
client.send(f"/lobby {pseudo}".encode("utf-8"))
data = client.recv(1024).decode("utf-8")

print(data)
if data == f"{pseudo} is connected to the lobby":
    print("We are in !")

