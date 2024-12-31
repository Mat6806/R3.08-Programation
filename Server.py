import socket, threading, os , subprocess,re

class Serveur:
    """
    Classe Serveur :
    - Permet de gérer un serveur TCP capable d'exécuter des programmes reçus des clients.
    - Supporte les langages : Python, C, C++, Java.
    """

    def __init__(self, host="127.0.0.0", port=4200):
        """
        Initialise le serveur avec l'adresse et le port donnés.
        Configure le socket et la liste des clients connectés.
        """
        self.host = host  # Adresse IP du serveur
        self.port = port  # Port du serveur
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []  # Liste des sockets clients connectés
    
    def srv_start(self):
        """
        Démarre le serveur et accepte les connexions des clients.
        Chaque connexion est gérée dans un thread séparé.
        """
        try:
            self.server_socket.bind((self.host, self.port))  # Associe l'IP et le port au socket
            self.server_socket.listen(1)  # Écoute les connexions entrantes
            print(f"Le serveur lance une connexion sur {self.host}:{self.port}")

            while True:
                # Accepte une connexion client
                client_socket, client_address = self.server_socket.accept()
                print(f"Connexion acceptée de {client_address}")
                # Lance un thread pour gérer le client
                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, client_address), daemon=True
                )
                client_thread.start()
        except Exception as error:
            print(f"Erreur du serveur : {error}")
        finally:
            self.srv_stop()

    def srv_stop(self):
        """
        Arrête le serveur en fermant toutes les connexions actives.
        """
        for client_socket in self.clients:
            client_socket.close()
        self.server_socket.close()
        print("Serveur arrêté.")

    def handle_client(self, client_socket, client_address):
        """
        Gère les interactions avec un client spécifique :
        - Reçoit le code envoyé.
        - Identifie le langage et exécute le programme.
        - Retourne le résultat ou les erreurs au client.
        """
        self.clients.append(client_socket)
        try:
            while True:
                data = client_socket.recv(4096).decode('utf-8')  # Reçoit le code du client
                if not data:
                    print(f"Déconnexion de {client_address}")
                    break

                print(f"Programme reçu de {client_address}. Exécution en cours...")
                result = self.execute_program(data)  # Exécute le code reçu

                # Envoie le résultat au client
                client_socket.sendall(result.encode('utf-8'))
                print(f"Résultat envoyé à {client_address}")
        except Exception as e:
            print(f"Erreur avec le client {client_address}: {e}")
        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"Connexion fermée avec {client_address}")

    def execute_program(self, code):
        """
        Détecte le langage du code reçu et appelle la méthode d'exécution appropriée.
        """
        lines = code.splitlines()
        for line in lines:
            try:
                if line.startswith("#include") and "<stdio.h>" in line:
                    return self.execute_c_program(code)
                elif line.startswith("#include") and "<iostream>" in line:
                    return self.execute_cpp_program(code)
                elif "public class" in line:
                    return self.execute_java_program(code)
                else:
                    return self.execute_python_program(code)
            except Exception as error:
                return f"Erreur inattendue lors de l'exécution : {error}"

    def execute_python_program(self, code):
        """
        Exécute un programme Python reçu.
        """
        try:
            with open("temp_program.py", "wb") as temp_file:
                temp_file.write(code.encode('utf-8'))
            result = subprocess.check_output(["python", "temp_program.py"], universal_newlines=True)
            os.remove("temp_program.py")  # Supprime le fichier temporaire
            return result
        except Exception as error:
            return f"Erreur inattendue lors de l'execution : {error}"

    def execute_c_program(self, code):
        """
        Compile et exécute un programme C reçu.
        """
        try:
            with open("temp_program.c", "wb") as temp_file:
                temp_file.write(code.encode('utf-8'))

            subprocess.run(["gcc", "temp_program.c", "-o", "temp_program"], check=True)
            compile_result = subprocess.check_output(["temp_program.exe"], universal_newlines=True)

            os.remove("temp_program.c")
            os.remove("temp_program.exe")
            return compile_result
        except Exception as error:
            return f"Erreur inattendue lors de l'exécution : {error}"
            
    def execute_cpp_program(self, code):
        """
        Compile et exécute un programme C++ reçu.
        """
        try:
            with open("temp_program.cpp", "wb") as temp_file:
                temp_file.write(code.encode('utf-8'))

            subprocess.run(["g++", "temp_program.cpp", "-o", "temp_program"], check=True)
            compile_result = subprocess.check_output(["temp_program.exe"], universal_newlines=True)

            os.remove("temp_program.cpp")
            os.remove("temp_program.exe")
            return compile_result
        except Exception as error:
            return f"Erreur inattendue lors de l'exécution : {error}"
        
    def execute_java_program(self, code):
        """
        Compile et exécute un programme Java reçu.
        """
        try:
            class_name_match = re.search(r'public\s+class\s+(\w+)', code)
            class_name = class_name_match.group(1)
            file_name = f"{class_name}.java"
            
            with open(file_name, "wb") as temp_file:
                temp_file.write(code.encode('utf-8'))

            subprocess.run(["javac", file_name], check=True)
            run_result = subprocess.check_output(["java", class_name], universal_newlines=True)

            os.remove(file_name)
            os.remove(f"{class_name}.class")
            return run_result
        except Exception as error:
            return f"Erreur inattendue lors de l'exécution : {error}"


if __name__ == "__main__":
    """
    Point d'entrée principal du script.
    Démarre le serveur et gère l'arrêt via Ctrl+C.
    """
    server = Serveur(host="127.0.0.1", port=4200)
    try:
        server.srv_start()
    except KeyboardInterrupt:
        server.srv_stop()
