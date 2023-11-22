import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 62222))
sock.listen()

client, client_address = sock.accept()
print(f"Un nouveau gars est arrivé : {client_address}")
data = client.recv(1024).decode("utf-8")
data = data.split()
if data[0] == "/lobby":
    print(f"Ajout de {data[1]} au lobby")
    client.send(f"{data[1]} is connected to the lobby".encode("utf-8"))
    client.close()
    sock.close()