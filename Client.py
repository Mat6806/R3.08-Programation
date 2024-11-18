import socket, time

host = '127.0.0.1'
port = 10000

client_socket = socket.socket()
client_socket.connect((host, port))
print("Connecté au serveur.")
    
while True:
    message = input("Client: ")
    client_socket.send(message.encode())
    reply = client_socket.recv(1024).decode()
    print(f"Serveur: {reply}")
        
    if message.lower() in ["bye", "arret"]:
        print("Déconnexion...")
        client_socket.close()
        break