import socket, threading, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,  QLabel, QLineEdit, QPushButton,  QVBoxLayout, QTextEdit, QFileDialog

class MainWindow(QMainWindow):
    """
    Interface graphique pour interagir avec un serveur via des sockets.
    Permet la connexion au serveur, l'upload de fichiers, et l'affichage des réponses.
    """
    def __init__(self):
        super().__init__()

        # Initialise le socket pour la connexion client
        self.client_socket = socket.socket()
        self.connected = False  # État de la connexion au serveur

        # Configuration de l'interface utilisateur
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QVBoxLayout()
        widget.setLayout(grid)
        
        # Entrée pour l'adresse IP du serveur
        grid.addWidget(QLabel("Adresse IP :"))
        self.ip = QLineEdit("127.0.0.1")  # IP par défaut
        grid.addWidget(self.ip)
 
        # Entrée pour le port du serveur
        grid.addWidget(QLabel("Port :"))
        self.port = QLineEdit("4200")  # Port par défaut
        grid.addWidget(self.port)

        # Bouton pour se connecter/déconnecter du serveur
        self.Servconnect = QPushButton('connexion au serveur')
        self.Servconnect.clicked.connect(self.connexionserv)
        grid.addWidget(self.Servconnect)
        
        # Bouton pour uploader un fichier (désactivé par défaut)
        self.upload_button = QPushButton('Upload de Programme')
        self.upload_button.clicked.connect(self.upload)
        self.upload_button.setEnabled(False)
        grid.addWidget(self.upload_button)

        # Zone d'affichage des résultats reçus du serveur
        grid.addWidget(QLabel("Résultat du serveur :"))
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)  # Empêche la modification directe
        grid.addWidget(self.result_display)

    def connexionserv(self):
        """
        Gère la connexion et la déconnexion du serveur.
        Active le bouton d'upload après connexion réussie.
        """
        if not self.connected:
            try:
                ip = self.ip.text()  # Récupère l'adresse IP saisie
                port = int(self.port.text())  # Récupère le port saisi
                self.client_socket.connect((ip, port))  # Établit la connexion au serveur
                self.connected = True
                self.upload_button.setEnabled(True)  # Active l'upload
                self.result_display.append("Connecté au serveur.")
                self.Servconnect.setText("arret")  # Change le texte du bouton
            except ConnectionRefusedError as error:
                self.result_display.append(f"Erreur connexion refusée : {error}")
            except TimeoutError as error:
                self.result_display.append(f"Erreur délai dépassé : {error}")
            except Exception as error:
                self.result_display.append(f"Erreur inattendue : {error}")
        else:
            self.close_connection()  # Ferme la connexion si déjà connectée
            self.Servconnect.setText("Connexion au serveur")  # Reset du bouton
            self.upload_button.setEnabled(False)
            self.result_display.append("Déconnecté du serveur.")

    def upload(self):
        """
        Permet à l'utilisateur de sélectionner un fichier et de l'envoyer au serveur.
        Affiche les erreurs en cas de problème.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier à uploader", "", "All Files (*)")
        
        if path:  # Vérifie si un fichier a été sélectionné
            try:
                # Lit le contenu du fichier sélectionné
                with open(path, 'r') as file:
                    program_data = file.read()
                
                # Envoie le contenu au serveur via le socket
                self.client_socket.sendall(program_data.encode('utf-8'))
                self.result_display.append(f"Programme '{path}' envoyé. En attente de réponse...")

                # Lance un thread pour recevoir la réponse du serveur
                threading.Thread(target=self.receive_server_response, daemon=True).start()
            except Exception as error:
                self.result_display.append(f"Erreur lors de l'envoi du programme : {error}")

    def receive_server_response(self):
        """
        Attend et affiche la réponse envoyée par le serveur.
        Capture les erreurs de réception.
        """
        try:
            response = self.client_socket.recv(4096).decode('utf-8')  # Lit la réponse du serveur
            self.result_display.append(f"Réponse du serveur :\n{response}")
        except Exception as error:
            self.result_display.append(f"Erreur lors de la réception de la réponse : {error}")

    def close_connection(self):
        """
        Ferme la connexion au serveur et réinitialise l'interface.
        Capture les erreurs liées à la fermeture.
        """
        if self.client_socket:
            try:
                self.client_socket.close()  # Ferme le socket
                self.connected = False
                self.result_display.append("Connexion fermée.")
            except Exception as e:
                self.result_display.append(f"Erreur lors de la fermeture de la connexion : {e}")


if __name__ == "__main__":
    # Initialise l'application PyQt et démarre l'interface utilisateur
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

