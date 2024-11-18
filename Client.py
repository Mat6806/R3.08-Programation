import socket, time

class Client : 
    def __init__(self, host: str = '127.0.0.1', port: int = 10000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()

    def connexionserv(host,port):
        print("Connecté au serveur."  )



    while True:
        message = input("Client: ")
        client_socket.send(message.encode())
        reply = client_socket.recv(1024).decode()
        print(f"Serveur: {reply}")
            
        if message.lower() in ["bye", "arret"]:
            print("Déconnexion...")
            client_socket.close()
            break