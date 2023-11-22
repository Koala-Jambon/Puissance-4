import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 62222))
sock.listen()

clients = []

def handle_client(client, client_address):
    print(f"Un nouveau gars est ar  rivé : {client_address}")
    data = client.recv(1024).decode("utf-8")
    data = data.split()
    if data[0] == "/lobby":
        print(f"Ajout de {data[1]} au lobby")
        client.send(f"{data[1]} is connected to the lobby".encode("utf-8"))
    else:
        client.close()


error = False
while not error:
    client, client_address = sock.accept()
    print("GUY")
    clients.append(threading.Thread(target=handle_client, args=(client, client_address)).run())


