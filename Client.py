import socket, time

class Client : 
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()

    def connexionserv(self):
        
        try:
            self.client_socket.connect((self.host,self.port))
            print("Connecté au serveur.")
            while True:
                message = input("Client: ")
                self.client_socket.send(message.encode())   
                reply = self.client_socket.recv(1024).decode()
                print(f"Serveur: {reply}")
                if message.lower() in ["bye", "arret"]:
                    print("Déconnexion demandée...")
                    break
        except ConnectionRefusedError as error:
            print(f"Connexion refusée : {error}")
        except TimeoutError as error:
            print(f"Délai dépassé : {error}")

        print("Connecté au serveur.")


if __name__ == "__main__":
    # Création et démarrage du client
    Connect = Client('127.0.0.1', 10000)
    Connect.connexionserv()
            
