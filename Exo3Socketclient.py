import socket
import threading

def listen_server(client_socket):
    while True:
        try:
            reply = client_socket.recv(1024).decode()
            print(f"Serveur: {reply}")
        except:
            print("Connexion au serveur interrompue.")
            break

def client_asynchrone(host="127.0.0.1", port=10000):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("Connecté au serveur.")
    
    thread = threading.Thread(target=listen_server, args=(client_socket,))
    thread.start()
    
    while True:
        message = input("Vous: ")
        client_socket.send(message.encode())
        
        if message.lower() in ["bye", "arret"]:
            print("Déconnexion...")
            client_socket.close()
            break

client_asynchrone()