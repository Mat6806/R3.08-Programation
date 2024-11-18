import socket, threading
host = '127.0.0.1'
reply = "hello"
port = 10000
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Connexion acceptée de {host}")
while True:
    try:
        conn, address = server_socket.accept()

        message = conn.recv(1024).decode()
        print(f"{address}: {message}")
            
        if message.lower() == "arret":
                conn.send("Serveur arrêté.".encode())
                conn.close()
                break
        elif message.lower() == "bye":
                conn.send("Client déconnecté.".encode())
                conn.close()
                break
        else:
                reply = f"Serveur: Bien reçu '{message}'"
                conn.send(reply.encode())
    except:
        print(f"Connexion avec {address} terminée.")
        conn.close()
        break

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
server_socket.listen(5)
print(f"Serveur asynchrone en écoute sur le port {port}...")
    
while True:
    conn, address = server_socket.accept()
    thread = threading.Thread(target=conn, args=(conn, address))
    thread.start()