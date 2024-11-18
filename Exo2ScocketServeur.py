import socket, time
host = '127.0.0.1'
reply = "hello"
port = 10000
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Serveur en écoute sur le port {port}...")
while True:
        conn, address = server_socket.accept()
        print(f"Connexion acceptée de {address}")
        
        while True:
            message = conn.recv(1024).decode()
            print(f"Message reçu: {message}")
            
            if message.lower() == "arret":
                conn.send("Serveur arrêté.".encode())
                conn.close()
                server_socket.close()
                print("Fermeture du serveur...") 
            elif message.lower() == "bye":
                conn.send("Client déconnecté.".encode())
                conn.close()
                print(f"Client {address} déconnecté.")
                break
            else:
                reply = f"Serveur: Bien reçu votre message '{message}'."
                conn.send(reply.encode())
