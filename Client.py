import socket, time

class Client : 
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()

    def connexionserv(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connecté au serveur {self.host}:{self.port}")
        except ConnectionRefusedError as erorr:
            print(f"Connexion refusée : {erorr}")
        except TimeoutError as erorr:
            print(f"Délai dépassé : {erorr}")
    
    def envoimessage(self, message : str):
        try:
            self.client_socket.send(message.encode())
            reply = self.client_socket.recv(1024).decode()
            return reply
        except Exception as erorr:
            print(f"impossible d'envoyer le msg : {erorr}")
    
    '''test'''
    
    
    
    def close_connection(self):
        """
        Ferme la connexion au serveur.
        """
        if self.client_socket:
            self.client_socket.close()
            print("Connexion fermée.")

    def start_interaction(self):
        """
        Démarre l'interaction entre le client et le serveur.
        """
        self.connect()

        try:
            while True:
                message = input("Client: ")
                if message.lower() in ["bye", "arret"]:
                    print("Déconnexion demandée...")
                    self.send_message(message)
                    break
                reply = self.send_message(message)
                print(f"Serveur: {reply}")
        finally:
            self.close_connection()


if __name__ == "__main__":
    # Création et démarrage du client
    clien1 = Client('127.0.0.1', 5000)
    clien1.connexionserv()
    clien1.start_interaction
            
