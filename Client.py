import socket, threading, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,  QLabel, QLineEdit, QPushButton,  QVBoxLayout, QFileDialog, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.client_socket = socket.socket()
        self.connected = False

      
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QVBoxLayout()
        widget.setLayout(grid)
        
        grid.addWidget(QLabel("Adresse IP :"))
        self.ip = QLineEdit("127.0.0.1")
        grid.addWidget(self.ip)
 
        grid.addWidget(QLabel("Port :"))
        self.port = QLineEdit("4200")
        grid.addWidget(self.port)

        self.Servconnect = QPushButton('connexion au serveur')
        self.Servconnect.clicked.connect(self.connexionserv)
        grid.addWidget(self.Servconnect)
        
        
        self.upload_button = QPushButton('Upload de Programme')
        self.upload_button.clicked.connect(self.upload)
        self.upload_button.setEnabled(False)
        grid.addWidget(self.upload_button)

        grid.addWidget(QLabel("Résultat du serveur :"))
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        grid.addWidget(self.result_display)


    def connexionserv(self):
        if not self.connected:
            try:
                ip = self.ip.text()
                port = int(self.port.text())
                self.client_socket.connect((ip,port))
                self.connected = True
                self.upload_button.setEnabled(True)
                self.result_display.append("Connecté au serveur.")
                self.Servconnect.setText("arret")
            except ConnectionRefusedError as error:
                self.result_display.append(f"erreur connexion refusée {error}")
            except TimeoutError as error:
                self.result_display.append(f"erreur délai depassé {error}")
            except Exception as error:
                self.result_display.append(f"erreur inatendu {error}")
        
        else: 
            self.close_connection()
            self.connect_button.setText("Connexion au serveur")
            self.upload_button.setEnabled(False)
            self.result_display.append("Déconnecté du serveur.")




    def upload(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier à uploader", "", "Python Files (*.py);;All Files (*)")
        
        if path:
            try:
                with open(path, 'r') as file:
                    program_data = file.read()
                
                self.client_socket.sendall(program_data.encode('utf-8'))
                self.result_display.append(f"Programme '{path}' envoyé. En attente de réponse...")

                threading.Thread(target=self.receive_server_response, daemon=True).start()
            
            except Exception as error:
                self.result_display.append(f"Erreur lors de l'envoi du programme : {error}")
    
       
    def receive_server_response(self):
        try:
            response = self.client_socket.recv(4096).decode('utf-8')
            self.result_display.append(f"Réponse du serveur :\n{response}")
        except Exception as error:
            self.result_display.append(f"Erreur lors de la réception de la réponse : {error}")


    def close_connection(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                self.connected = False
                self.result_display.append("Connexion fermée.")
            except Exception as e:
                self.result_display.append(f"Erreur lors de la fermeture de la connexion : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


