import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 62222))
sock.listen()

lobby = {}
party = []

def handle_client(client, client_address):
    print(f"Un nouveau gars est arrivé : {client_address}")
    data = client.recv(1024).decode("utf-8")
    data = data.split()
    if data[0] == "/lobby":
        try:
            print(f"{lobby[client_address]} est déjà dans le lobby")
        except KeyError:
            print(f"Ajout de {data[1]} au lobby")
            lobby[client_address] = {"pseudo": data[1], "status": "disponible"}
        client.send(f"{data[1]} is connected to the lobby".encode("utf-8"))

    if data[0] == "/party":
        print(f"{data[1]} crée une partie.")
        if client_address not in lobby:
            client.send(f"Veuillez d'abord rejoindre le lobby".encode("utf-8"))
        print("OKKKK")
    else:
        client.close()



error = False
while not error:
    client, client_address = sock.accept()
    print("GUY")
    threading.Thread(target=handle_client, args=(client, client_address)).run()


