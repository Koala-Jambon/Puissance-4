import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 62222))
sock.listen()

client, client_address = sock.accept()
print(f"Un nouveau gars est arrivé : {client_address}")
data = client.recv(1024)
print(data)
client.close()
sock.close()